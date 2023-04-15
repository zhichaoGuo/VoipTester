from SipTool.SdpBody import SdpBody

from SipTool.SipHeader import SipHeader
from SipTool.SipMethodLine import MethodLine


class SipMessage:
    """
    sip message
    分为三个部分：method_line，headers，body
    """

    def __init__(self, buf: bytes):
        self.buf = buf
        buf_str = buf.decode('utf-8')
        if buf.find(b'\r\n\r\n') != len(buf) - 4:
            self.method_line = MethodLine(buf_str.split('\r\n\r\n')[0].split('\r\n')[0])
            self.headers = SipHeader(buf_str.split('\r\n\r\n')[0].split('\r\n')[1:])
            if self.method_line.method == 'INFO':  # Todo xml类型的body的处理
                pass
            else:
                self.body = SdpBody(buf_str.split('\r\n\r\n')[1])
        else:
            self.method_line = MethodLine(buf_str.split('\r\n')[0])
            self.headers = SipHeader(buf_str.split('\r\n')[1:])
        # Todo 增加判断来电去电类型


class SipRequest(SipMessage):
    def __init__(self, buf: bytes):
        super().__init__(buf)

    def is_hold(self):
        """
        判断buf是否为INVITE中带有sendonly
        """
        if self.method_line.method != 'INVITE':
            return False
        if self.buf.find(b'\r\n\r\n') != -1:
            # 如果带有body
            # 去除b'转为str型
            buf_str = str(self.buf)[2:-1]
            header_list = buf_str.split('\\r\\n\\r\\n')[0].split('\\r\\n')[1:]
            body = buf_str.split('\\r\\n\\r\\n')[1]
            if body.find('a=sendonly') != -1:
                return True
            else:
                return False
        else:
            # 未带body
            print('message do not have body!')
            return False

    def is_resume(self):
        if self.method_line.method != 'INVITE':
            return False
        if self.is_hold():
            return False
        if str(self.buf)[2:-1].find('Subject: SIP Call') != -1:
            return False
        else:
            return True

    def is_authorization(self):
        return hasattr(self.headers, 'ProxyAuthorization')


class SipResponse(SipMessage):
    def __init__(self, buf: bytes):
        super().__init__(buf)
