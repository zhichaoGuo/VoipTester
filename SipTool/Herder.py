import re

from SipTool.common.Utils import cut_in


class Header:
    def __init__(self, header_list: list):
        for header in header_list:
            # 跳过分割产生的空行
            if header == '':
                continue
            line_method, line_body = cut_in(header, ':')
            if line_method == 'Via':
                self.Via = Via(line_body)
            elif line_method == 'From':
                self.From = From(line_body)
            elif line_method == 'To':
                self.To = To(line_body)
            elif line_method == 'Call-ID':
                self.CallID = CallID(line_body)
            elif line_method == 'CSeq':
                self.CSeq = CSeq(line_body)
            elif line_method == 'Contact':
                self.Contact = Contact(line_body)
            elif line_method == 'Proxy-Authorization':
                self.ProxyAuthorization = ProxyAuthorization(line_body)
            elif line_method == 'Max-Forwards':
                self.MaxForwards = MaxForwards(line_body)
            elif line_method == 'User-Agent':
                self.UserAgent = UserAgent(line_body)
            elif line_method == 'Content-Disposition':
                self.ContentDisposition = ContentDisposition(line_body)
            elif line_method == 'Diversion':
                self.Diversion = Diversion(line_body)
            elif line_method == 'Refer-To':
                self.ReferTo = ReferTo(line_body)
            elif line_method == 'Referred-By':
                self.ReferredBy = ReferredBy(line_body)
            elif line_method == 'Replaces':
                self.Replaces = Replaces(line_body)
            elif line_method == 'Supported':
                self.Supported = Supported(line_body)
            elif line_method == 'Subject':
                self.Subject = Subject(line_body)
            elif line_method == 'Expires':
                self.Expires = Expires(line_body)
            elif line_method == 'Allow-Events':
                self.AllowEvents = AllowEvents(line_body)
            elif line_method == 'Allow':
                self.Allow = Allow(line_body)
            elif line_method == 'Event':
                self.Event = Event(line_body)
            elif line_method == 'Warning':
                self.Warning_ = Warning_(line_body)
            elif line_method == 'Content-Type':
                self.ContentType = ContentType(line_body)
            elif line_method == 'Content-Length':
                pass
            else:
                print('can not match %s in header' % line_method)


class HeaderLine:
    def __init__(self, buf):
        self.buf = buf

    def __str__(self):
        return self.buf


class Via(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        # print(buf)
        try:  # Via: SIP/2.0/UDP 192.168.0.68:5060;branch=z9hG4bK-524287-1---405e1b7d2300f323;rport=5060
            re_tpl = r'SIP/2.0/UDP (?P<ip>.+):(?P<port>[0-9]{1,6});branch=(?P<branch>.+);rport=(?P<rport>.+)'
            self.port = re.search(re_tpl, buf.strip(), re.U).groupdict()['port']
            self.ip = re.search(re_tpl, buf.strip(), re.U).groupdict()['ip']
            self.branch = re.search(re_tpl, buf.strip(), re.U).groupdict()['branch']
            self.rport = re.search(re_tpl, buf.strip(), re.U).groupdict()['rport']
        except Exception:
            try:  # Via: SIP/2.0/UDP 192.168.0.68:5060;branch=z9hG4bK-524287-1---405e1b7d2300f323;rport
                re_tpl = r'SIP/2.0/UDP (?P<ip>.+):(?P<port>[0-9]{1,6});branch=(?P<branch>.+);rport'
                self.port = re.search(re_tpl, buf.strip(), re.U).groupdict()['port']
                self.ip = re.search(re_tpl, buf.strip(), re.U).groupdict()['ip']
                self.branch = re.search(re_tpl, buf.strip(), re.U).groupdict()['branch']
                self.rport = None
            except Exception:
                try:  # 'Via: SIP/2.0/UDP 10.20.0.16:5060;branch=z9hG4bK1938747582'
                    re_tpl = r'SIP/2.0/UDP (?P<ip>.+):(?P<port>[0-9]{1,6});branch=(?P<branch>.+)'
                    self.port = re.search(re_tpl, buf.strip(), re.U).groupdict()['port']
                    self.ip = re.search(re_tpl, buf.strip(), re.U).groupdict()['ip']
                    self.branch = re.search(re_tpl, buf.strip(), re.U).groupdict()['branch']
                    self.rport = None
                except AttributeError:
                    print('parse Via header err!!')
                    self.port = None
                    self.ip = None
                    self.branch = None
                    self.rport = None


class From(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        # print('From:%s'%buf)
        try:  # From: <sip:1501@10.20.0.14:5060;transport=UDP>;tag=bc697b1b6499ea1;epid=DP1e6e6d
            re_tpl = r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>[0-9]{1,6});transport=(?P<transport>.+)>;tag=(?P<tag>.+);epid=(?P<epid>.+)'
            self.account = re.search(re_tpl, buf.strip(), re.U).groupdict()['account']
            self.ip = re.search(re_tpl, buf.strip(), re.U).groupdict()['ip']
            self.port = re.search(re_tpl, buf.strip(), re.U).groupdict()['port']
            self.transport = re.search(re_tpl, buf.strip(), re.U).groupdict()['transport']
            self.tag = re.search(re_tpl, buf.strip(), re.U).groupdict()['tag']
            self.epid = re.search(re_tpl, buf.strip(), re.U).groupdict()['epid']
        except Exception:
            try:  # From: <sip:1502@192.168.0.68:5060>;tag=443f54eb7dcb273;epid=DP200b41
                re_tpl = r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>[0-9]{1,6})>;tag=(?P<tag>.+);epid=(?P<epid>.+)'
                self.account = re.search(re_tpl, buf.strip(), re.U).groupdict()['account']
                self.ip = re.search(re_tpl, buf.strip(), re.U).groupdict()['ip']
                self.port = re.search(re_tpl, buf.strip(), re.U).groupdict()['port']
                self.transport = None
                self.tag = re.search(re_tpl, buf.strip(), re.U).groupdict()['tag']
                self.epid = re.search(re_tpl, buf.strip(), re.U).groupdict()['epid']
            except Exception:
                try:  # From: <sip:1502@192.168.0.68:5060>;tag=443f54eb7dcb273
                    re_tpl = r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>[0-9]{1,6})>;tag=(?P<tag>.+)'
                    self.account = re.search(re_tpl, buf.strip(), re.U).groupdict()['account']
                    self.ip = re.search(re_tpl, buf.strip(), re.U).groupdict()['ip']
                    self.port = re.search(re_tpl, buf.strip(), re.U).groupdict()['port']
                    self.transport = None
                    self.tag = re.search(re_tpl, buf.strip(), re.U).groupdict()['tag']
                    self.epid = None
                except Exception:
                    try:  # From: <sip:1502@192.168.0.68>;tag=443f54eb7dcb273;epid=DP200b41
                        #         <sip:1500@10.3.5.44>;tag=4dbd0ce7b796cdc;epid=DP1e6e58
                        re_tpl = r'<sip:(?P<account>.+)@(?P<ip>.+)>;tag=(?P<tag>.+);epid=(?P<epid>.+)'
                        self.account = re.search(re_tpl, buf.strip(), re.U).groupdict()['account']
                        self.ip = re.search(re_tpl, buf.strip(), re.U).groupdict()['ip']
                        self.port = None
                        self.transport = None
                        self.tag = re.search(re_tpl, buf.strip(), re.U).groupdict()['tag']
                        self.epid = re.search(re_tpl, buf.strip(), re.U).groupdict()['epid']
                    except Exception:
                        try:  # From: <sip:1502@192.168.0.68>;tag=443f54eb7dcb273
                            re_tpl = r'<sip:(?P<account>.+)@(?P<ip>.+)>;tag=(?P<tag>.+)'
                            self.account = re.search(re_tpl, buf.strip(), re.U).groupdict()['account']
                            self.ip = re.search(re_tpl, buf.strip(), re.U).groupdict()['ip']
                            self.port = None
                            self.transport = None
                            self.tag = re.search(re_tpl, buf.strip(), re.U).groupdict()['tag']
                            self.epid = None
                        except Exception:
                            print('parse From header err!!')
                            self.account = None
                            self.ip = None
                            self.port = None
                            self.transport = None
                            self.tag = None
                            self.epid = None


class To(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        try:  # To: <sip:1500@192.168.0.68:5060>;tag=7a7c8b24;epid=DP200b41
            re_tpl = r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>[0-9]{1,6})>;tag=(?P<tag>.+);epid=(?P<epid>.+)'
            self.account = re.search(re_tpl, buf.strip(), re.U).groupdict()['account']
            self.ip = re.search(re_tpl, buf.strip(), re.U).groupdict()['ip']
            self.port = re.search(re_tpl, buf.strip(), re.U).groupdict()['port']
            self.tag = re.search(re_tpl, buf.strip(), re.U).groupdict()['tag']
            self.epid = re.search(re_tpl, buf.strip(), re.U).groupdict()['epid']
        except Exception:
            try:  # To: <sip:1500@192.168.0.68:5060>;tag=7a7c8b24
                re_tpl = r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>[0-9]{1,6})>;tag=(?P<tag>.+)'
                self.account = re.search(re_tpl, buf.strip(), re.U).groupdict()['account']
                self.ip = re.search(re_tpl, buf.strip(), re.U).groupdict()['ip']
                self.port = re.search(re_tpl, buf.strip(), re.U).groupdict()['port']
                self.tag = re.search(re_tpl, buf.strip(), re.U).groupdict()['tag']
                self.epid = None
            except Exception:
                try:  # To: <sip:1500@192.168.0.68:5060>
                    re_tpl = r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>[0-9]{1,6})>'
                    self.account = re.search(re_tpl, buf.strip(), re.U).groupdict()['account']
                    self.ip = re.search(re_tpl, buf.strip(), re.U).groupdict()['ip']
                    self.port = re.search(re_tpl, buf.strip(), re.U).groupdict()['port']
                    self.tag = None
                    self.epid = None
                except Exception:
                    try:  # To: <sip:1500@192.168.0.68>;tag=7a7c8b24
                        re_tpl = r'<sip:(?P<account>.+)@(?P<ip>.+)>;tag=(?P<tag>.+)'
                        self.account = re.search(re_tpl, buf.strip(), re.U).groupdict()['account']
                        self.ip = re.search(re_tpl, buf.strip(), re.U).groupdict()['ip']
                        self.port = None
                        self.tag = re.search(re_tpl, buf.strip(), re.U).groupdict()['tag']
                        self.epid = None
                    except Exception:
                        try:  # To: <sip:1500@192.168.0.68>
                            re_tpl = r'<sip:(?P<account>.+)@(?P<ip>.+)>'
                            self.account = re.search(re_tpl, buf.strip(), re.U).groupdict()['account']
                            self.ip = re.search(re_tpl, buf.strip(), re.U).groupdict()['ip']
                            self.port = None
                            self.tag = None
                            self.epid = None
                        except Exception:
                            print('parse To header err!!')
                            self.account = None
                            self.ip = None
                            self.port = None
                            self.tag = None
                            self.epid = None


class CallID(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        self.call_id = buf


class CSeq(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        try:  # CSeq: 21 INVITE
            re_tpl = r'(?P<number>[0-9]{1,6}) (?P<method>.+)'
            self.number = re.search(re_tpl, buf.strip(), re.U).groupdict()['number']
            self.method = re.search(re_tpl, buf.strip(), re.U).groupdict()['method']
        except Exception:
            print('parse CSeq header err!!')
            self.number = None
            self.method = None


class Contact(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        try:  # Contact: <sip:1501@10.20.0.14:5060;transport=UDP>
            re_tpl = r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>[0-9]{1,6});transport=UDP>'
            self.account = re.search(re_tpl, buf.strip(), re.U).groupdict()['account']
            self.ip = re.search(re_tpl, buf.strip(), re.U).groupdict()['ip']
            self.port = re.search(re_tpl, buf.strip(), re.U).groupdict()['port']
        except Exception:
            try:  # Contact: <sip:1501@10.20.0.14:5060>
                re_tpl = r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>[0-9]{1,6})>'
                self.account = re.search(re_tpl, buf.strip(), re.U).groupdict()['account']
                self.ip = re.search(re_tpl, buf.strip(), re.U).groupdict()['ip']
                self.port = re.search(re_tpl, buf.strip(), re.U).groupdict()['port']
            except Exception:
                print('parse Contact header err!!')
                self.account = None
                self.ip = None
                self.port = None


class ProxyAuthorization(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        try:  # Proxy-Authorization: Digest username="1502", realm="3CXPhoneSystem", nonce="414d535c17a29e5d29:b13fa2d3ccd383ff1240b3bbebbc0524", uri="sip:1500@192.168.0.68:5060", response="b32b6532fde25e2f9c47364afedfd55e", algorithm=MD5
            pass
        except Exception:
            pass


class MaxForwards(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        # Max-Forwards: 70
        self.max_forwards = buf


class UserAgent(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        # User-Agent: Htek UC912G 001fc1200b41
        self.user_agent = buf


class ContentDisposition(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        # Content-Disposition: signal; handling=required
        self.content_disposition = buf


class Diversion(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        # Diversion: <sip:1500@10.20.0.82:81;transport=UDP>;reason=unconditional
        self.diversion = buf


class ReferTo(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        try:  # Refer-To: <sip:1503@192.168.0.68:5060?Replaces=58078934b97ce3e%4010.20.0.16%3Bfrom-tag%3D61b54724c706ec6%3Bto-tag%3D74385a24>
            pass
        except Exception:
            pass


class ReferredBy(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        try:  # Referred-By: <sip:1500@192.168.0.68>
            pass
        except Exception:
            pass


class Replaces(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        try:  # Replaces: i7dH2Mnnmv85_YP4zJtBqA..;to-tag=4ab94a62a6b02d4;from-tag=bf38ac21
            pass
        except Exception:
            pass


class Supported(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        try:  # Supported: replaces
            pass
        except Exception:
            pass


class Subject(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        try:  # Subject: SIP Call
            pass
        except Exception:
            pass


class Expires(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        try:  # Expires: 120
            pass
        except Exception:
            pass


class AllowEvents(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        try:  # Allow-Events: talk,hold,conference,refer,check-sync
            pass
        except Exception:
            pass


class Allow(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        try:  # Allow: INVITE, ACK, UPDATE, INFO, CANCEL, BYE, OPTIONS, REFER, SUBSCRIBE, NOTIFY, MESSAGE, PRACK
            pass
        except Exception:
            pass


class Event(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        try:  # Event: refer
            pass
        except Exception:
            pass


class Warning_(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        # Warning: 499 WIN-7PKJ6575AD0 "Busy"
        pass


class ContentType(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        try:  # Content-Type: application/sdp
            pass
        except Exception:
            pass


class ContentLength(HeaderLine):
    def __init__(self, buf):
        super().__init__(buf)
        try:  # Content-Length: 423
            pass
        except Exception:
            pass
