from SipTool.Body import Body
from SipTool.Herder import Header
from SipTool.MethodLine import MethodLine


class SipMessage:
    def __init__(self, message: bytes):
        self.buf = message
        buf_str = message.decode('utf-8')
        if message.find(b'\r\n\r\n') != len(message) - 4:
            self.method_line = MethodLine(buf_str.split('\r\n\r\n')[0].split('\r\n')[0])
            self.headers = Header(buf_str.split('\r\n\r\n')[0].split('\r\n')[1:])
            self.body = Body(buf_str.split('\r\n\r\n')[1])
        else:
            self.method_line = MethodLine(buf_str.split('\r\n')[0])
            self.headers = Header(buf_str.split('\r\n')[1:])
        # Todo 增加判断来电去电类型
