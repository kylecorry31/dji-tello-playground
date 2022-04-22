from cffi import FFI


class H264Decoder:
    def __init__(self):
        self.ffi = FFI()
        self.ffi.cdef("size_t decode(char* in_buffer, size_t in_length, char* out_buffer, size_t out_length);")
        self.C = self.ffi.dlopen("./video/h264-decode/target/debug/h264_decode_ffi.dll")

    def decode(self, frame: bytes, output_width: int, output_height: int) -> bytes:
        size = output_width * output_height * 3
        input_buf = self.ffi.new("char[{}]".format(len(frame)), frame)
        input_length = len(frame)
        output_buf = self.ffi.new("char[{}]".format(size))
        output_length = size
        try:
            written_size = self.C.decode(input_buf, input_length, output_buf, output_length)
            print(written_size)
            if written_size == 0:
                return None
            return bytes(self.ffi.string(output_buf))[:written_size]
        except Exception as e:
            print(e)
            return None
        finally:
            self.ffi.release(input_buf)
            self.ffi.release(output_buf)
