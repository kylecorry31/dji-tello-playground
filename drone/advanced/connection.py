import socket
import threading
import time


class Connection:
    def __init__(self, request_ip: str, request_port: int, response_port: int, response_buffer_size: int = 1024,
                 print_responses: bool = False):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', response_port))
        self.request_address = (request_ip, request_port)

        # Receiver thread
        self.response = None
        self.response_listener = None
        self.response_buffer_size = response_buffer_size
        self.print_responses = print_responses

        self.receive_thread = threading.Thread(target=self.__receiver)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def __receiver(self):
        while True:
            try:
                data, address = self.socket.recvfrom(1024)
                if self.print_responses:
                    print(data)
                if address != self.request_address:
                    continue
                self.response = data
                listener = self.response_listener
                if listener is not None:
                    listener(data)
            except Exception as e:
                print(e)

    def listen(self, listener):
        self.response_listener = listener

    def send(self, data: bytes, wait: bool = False, timeout: float = 5) -> bytes:
        start_time = time.time()

        if wait:
            # Clear the previous response
            self.response = None

        self.socket.sendto(data, self.request_address)

        if not wait:
            return None

        # Wait for a response
        while self.response is None:
            if time.time() - start_time > timeout:
                return None
            time.sleep(0.1)

        return self.response
