import re


class MethodLine:
    def __init__(self, buf: str):
        # INVITE sip:1502@192.168.0.68:5060 SIP/2.0
        # ACK sip:1502@192.168.0.68:5060 SIP/2.0
        # CANCEL sip:1501@10.20.0.122:5060;transport=UDP SIP/2.0
        # BYE sip:1501@10.20.0.122:5060;transport=UDP SIP/2.0
        # SIP/2.0 100 Trying
        # SIP/2.0 487 Request Cancelled
        # REGISTER sip:10.3.3.49:8060 SIP/2.0
        if buf[:7] == 'SIP/2.0':  # is responses
            self.is_responses = True
            re_responses = r'SIP/2.0 (?P<method>\d{3}) (?P<state>.+)'
            self.method = re.search(re_responses, buf.strip(), re.U).groupdict()['method']
            self.state = re.search(re_responses, buf.strip(), re.U).groupdict()['state']
        else:  # is requests
            self.is_responses = False
            try:
                re_requests = r'(?P<method>\w+) sip:(?P<account>.+)@(?P<ip>.+):(?P<port>\d+)(;transport=UDP)? SIP/2.0'
                self.method = re.search(re_requests, buf.strip(), re.U).groupdict()['method']
                self.account = re.search(re_requests, buf.strip(), re.U).groupdict()['account']
                self.ip = re.search(re_requests, buf.strip(), re.U).groupdict()['ip']
                self.port = re.search(re_requests, buf.strip(), re.U).groupdict()['port']
            except AttributeError:
                re_requests = r'(?P<method>\w+) sip:(?P<ip>.+):(?P<port>\d+)(;transport=UDP)? SIP/2.0'
                self.method = re.search(re_requests, buf.strip(), re.U).groupdict()['method']
                self.account = None
                self.ip = re.search(re_requests, buf.strip(), re.U).groupdict()['ip']
                self.port = re.search(re_requests, buf.strip(), re.U).groupdict()['port']
