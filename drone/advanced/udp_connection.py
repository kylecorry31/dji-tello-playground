import socket
import threading
import time


class UdpConnection:
    def __init__(self, request_ip: str, request_port: int, response_port: int, response_buffer_size: int = 1024,
                 print_responses: bool = False):
        """
        A two-way UDP connection
        :param request_ip: The IP address to send data to. If only receiving, this can be None.
        :param request_port: The UDP port to send data to. If only receiving, this can be None.
        :param response_port: The UDP port to receive data from. If only sending, this can be None.
        :param response_buffer_size: The buffer size to receive responses. Defaults to 1024 bytes.
        :param print_responses: Set to True to print responses (data and addresses). Defaults to False.
        """
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if response_port is not None:
            self.__socket.bind(('', response_port))
        self.__request_address = (request_ip, request_port)

        # Receiver thread
        self.__response = None
        self.__response_listeners = []
        self.__response_buffer_size = response_buffer_size
        self.__print_responses = print_responses

        self.__receive_thread = threading.Thread(target=self.__receiver)
        self.__receive_thread.daemon = True
        if response_port is not None:
            self.__receive_thread.start()

        self.__running = True

    def __receiver(self):
        while self.__running:
            try:
                data, address = self.__socket.recvfrom(self.__response_buffer_size)
                if self.__print_responses:
                    print(data, address)
                self.__response = data
                listeners_to_remove = []
                for listener in self.__response_listeners:
                    if not listener(data, address):
                        listeners_to_remove.append(listener)
                for listener in listeners_to_remove:
                    self.remove_listener(listener)
            except Exception as e:
                print(e)

    def cancel(self):
        """
        Close the socket and stop the receiver thread
        """
        self.__running = False
        self.__socket.close()

    def listen(self, listener):
        """
        Listen for a response. The listener will be called with the bytes received from the socket.
        :param listener: The listener which takes two parameters (bytes and (ip, port)) and optionally returns False to stop listening.
        """
        self.__response_listeners.append(listener)

    def remove_listener(self, listener):
        """
        Remove a listener.
        :param listener: The listener to remove.
        """
        if listener in self.__response_listeners:
            self.__response_listeners.remove(listener)

    def send(self, data: bytes, wait: bool = False, timeout: float = 5, response_listener=None) -> bytes:
        """
        Send data over the UDP connection.
        :param data: The data to send (bytes)
        :param wait: True if it should wait for a response.
        :param timeout: The timeout in seconds to wait for a response.
        :param response_listener: The listener to set to receive a response (does not require wait to be True)
        :return: If waiting, it will return the latest bytes received or None if it times out. Returns None if not waiting.
        """
        start_time = time.time()

        if wait:
            # Clear the previous response
            self.__response = None

        if response_listener is not None:
            self.listen(response_listener)
        self.__socket.sendto(data, self.__request_address)

        if not wait:
            return None

        # Wait for a response
        while self.__response is None:
            if time.time() - start_time > timeout:
                return None
            time.sleep(0.1)

        return self.__response
