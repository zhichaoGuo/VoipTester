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
            if self.method_line.method == 'INFO':  # Todo xml类型的body的处理
                pass
            else:
                self.body = Body(buf_str.split('\r\n\r\n')[1])
        else:
            self.method_line = MethodLine(buf_str.split('\r\n')[0])
            self.headers = Header(buf_str.split('\r\n')[1:])
        # Todo 增加判断来电去电类型

    def is_hold(self):
        """
        判断buf是否为INVITE中带有sendonly
        """
        if self.method_line.method != 'INVITE':
            print('message is not a INVITE message')
            return False
        if self.buf.find(b'\r\n\r\n') != -1:
            # 如果带有body
            # 去除b'转为str型
            buf_str = str(self.buf)[2:-1]
            header_list = buf_str.split('\\r\\n\\r\\n')[0].split('\\r\\n')[1:]
            body = buf_str.split('\\r\\n\\r\\n')[1]
            if body.find('a=sendonly') != -1:
                print('123123123123')
                return True
            else:
                print('message do not have send only')
                return False
        else:
            # 未带body
            print('message do not have body!')
            return False

    def is_resume(self):
        if self.method_line.method != 'INVITE':
            print('message is not a resume message')
            return False
        if self.is_hold():
            print('message is a hold message')
            return False
        if str(self.buf)[2:-1].find('Subject: SIP Call') != -1:
            return False
        else:
            return True
