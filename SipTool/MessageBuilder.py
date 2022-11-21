from SipTool.Herder import Via, From, To

responses_line = {'100': 'Trying',
                  '180': 'Ringing',
                  '200': 'OK',
                  '202': 'Accepted',
                  '401': 'Unauthorized',
                  '403': 'Forbidden',
                  '407': 'Proxy Authentication Required',
                  '486': 'Busy Here',
                  '487': 'Request Cancelled'}


class SipMessageBuilder:
    def __init__(self):
        self.body = None
        self.buf = ''

    def add_state_line_request(self, method, cur_message=None):
        self.buf += f'{method} sip:{1501}@10.20.0.122:5060;transport=UDP SIP/2.0'

    def add_state_line_responses(self, method, cur_message=None):
        self.buf += f'SIP/2.0 {method} {responses_line[method]}' + '\r\n'

    def add_Via(self, _via: Via):
        self.buf += 'Via: SIP/2.0/UDP '
        self.buf += f'{_via.ip}' if _via.ip else ''
        self.buf += f':{_via.port}' if _via.port else ''
        self.buf += f';branch={_via.branch}' if _via.branch else ''
        self.buf += f';rport={_via.rport}' if _via.rport else ''
        self.buf += '\r\n'

    def add_From(self, _from: From):
        self.buf += 'From: <sip:'
        self.buf += f'{_from.account}' if _from.account else ''
        self.buf += f'@{_from.ip}' if _from.ip else ''
        self.buf += f':{_from.port}' if _from.port else ''
        self.buf += f';transport={_from.transport}' if _from.transport else '>'
        self.buf += f';tag={_from.tag}' if _from.tag else ''
        self.buf += f';epid={_from.epid}' if _from.epid else ''
        self.buf += '\r\n'

    def add_To(self, _to: To, tag=''):  # Todo 完善tag机制
        self.buf += 'To: <sip:'
        self.buf += f'{_to.account}' if _to.account else ''
        self.buf += f'@{_to.ip}' if _to.ip else ''
        self.buf += f':{_to.port}>' if _to.port else '>'
        self.buf += f';tag={_to.tag}' if _to.tag else f';tag={tag}' if tag else ''
        self.buf += f';epid={_to.epid}' if _to.epid else ''
        self.buf += '\r\n'

    def add_CallId(self, buf):
        self.buf += f'Call-ID: {buf}'
        self.buf += '\r\n'

    def add_CSeq(self, buf):
        self.buf += f'CSeq: {buf}'
        self.buf += '\r\n'

    def add_Contact(self, buf):
        self.buf += f'Contact: {buf}'
        self.buf += '\r\n'

    def add_ProxyAuthorization(self,buf):
        self.buf += f'Proxy-Authenticate: {buf}'
        self.buf += '\r\n'

    def add_MaxForwards(self):
        self.buf += ''
        self.buf += '\r\n'

    def add_UserAgent(self, buf):
        self.buf += f'User-Agent: {buf}'
        self.buf += '\r\n'

    def add_ContentDisposition(self):
        self.buf += ''
        self.buf += '\r\n'

    def add_Diversion(self):
        self.buf += ''
        self.buf += '\r\n'

    def add_ReferTo(self):
        self.buf += ''
        self.buf += '\r\n'

    def add_ReferredBy(self):
        self.buf += ''
        self.buf += '\r\n'

    def add_Replaces(self):
        self.buf += ''
        self.buf += '\r\n'

    def add_Supported(self, _supported):
        self.buf += f'Supported: {_supported}'
        self.buf += '\r\n'

    def add_Subject(self):
        self.buf += ''

    def add_Expires(self):
        self.buf += ''

    def add_AllowEvents(self):
        self.buf += ''

    def add_Allow(self, _allow):
        self.buf += f'Allow: {_allow}'
        self.buf += '\r\n'

    def add_Event(self):
        self.buf += ''

    def add_Warning(self):
        self.buf += ''

    def add_ContentType(self, _content_type):
        self.buf += f'Content-Type: {_content_type}'
        self.buf += '\r\n'

    def _add_ContentLength(self):
        self.buf += f'Content-Length: {len(self.body)}'
        self.buf += '\r\n\r\n'

    def add_body(self, _body=''):
        self.body = f'{_body}\r\n' if _body else ''

    def build_message(self):
        self._add_ContentLength()
        self.buf += self.body
        return self.buf


class SipBodyBuilder:
    def __init__(self):
        self.buf = ''

    def add_line(self, buf):
        self.buf += buf
        self.buf += '\r\n'

    def add_v(self, _v):
        self.buf += f'v={_v}\r\n'

    def add_o(self, _o):
        self.buf += f'o={_o}\r\n'

    def add_i(self, _i):
        self.buf += f'i={_i}\r\n'

    def add_u(self, _u):
        self.buf += f'u={_u}\r\n'

    def add_e(self, _e):
        self.buf += f'e={_e}\r\n'

    def add_p(self, _p):
        self.buf += f'p={_p}\r\n'

    def add_b(self, _b):
        self.buf += f'b={_b}\r\n'

    def add_z(self, _z):
        self.buf += f'z={_z}\r\n'

    def add_k(self, _k):
        self.buf += f'k={_k}\r\n'

    def add_s(self, _s):
        self.buf += f's={_s}\r\n'

    def add_c(self, _c):
        self.buf += f'c={_c}\r\n'

    def add_t(self, _t):
        self.buf += f't={_t}\r\n'

    def add_m(self, _m):
        self.buf += f'v={_m}\r\n'

    def add_a(self, _a):
        self.buf += f'a={_a}\r\n'
