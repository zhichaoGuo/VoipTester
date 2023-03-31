from SipTool.SipMethodLine import MethodLine
from SipTool.SipMessage import SipRequest, SipResponse


def parser_buf(buf: bytes):
    buf_str = buf.decode('utf-8')
    if buf.find(b'\r\n\r\n') != len(buf) - 4:
        method_line = MethodLine(buf_str.split('\r\n\r\n')[0].split('\r\n')[0])
    else:
        method_line = MethodLine(buf_str.split('\r\n')[0])
    # 判断是request
    if method_line.is_responses:
        return SipResponse(buf)
    else:
        return SipRequest(buf)

