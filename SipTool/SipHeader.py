import re

from SipTool.common.Utils import cut_in


class SipHeader:
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
    def __init__(self, buf, attr_list, re_tpl_list):
        self.buf = buf
        if re_tpl_list:
            for re_tpl in re_tpl_list:
                try:
                    re_dic = re.search(re_tpl, buf.strip(), re.U).groupdict()
                    for attr in attr_list:
                        setattr(self, attr, re_dic.get(attr))
                    return
                except Exception:
                    continue
            raise AttributeError('Header:%s 解析失败！' % self.__class__)

    def __str__(self):
        return self.buf


class Via(HeaderLine):
    """
    Via: SIP/2.0/UDP 192.168.0.68:5060;branch=z9hG4bK-524287-1---405e1b7d2300f323;rport=5060
    Via: SIP/2.0/UDP 192.168.0.68:5060;branch=z9hG4bK-524287-1---405e1b7d2300f323;rport
    Via: SIP/2.0/UDP 10.20.0.16:5060;branch=z9hG4bK1938747582
    """

    def __init__(self, buf):
        attr_list = ['ip', 'port', 'branch', 'rport']
        self.port = None
        self.ip = None
        self.branch = None
        self.rport = None
        re_tpl_list = [r'SIP/2.0/UDP (?P<ip>.+):(?P<port>[0-9]{1,6});branch=(?P<branch>.+);rport=(?P<rport>.+)',
                       r'SIP/2.0/UDP (?P<ip>.+):(?P<port>[0-9]{1,6});branch=(?P<branch>.+);rport',
                       r'SIP/2.0/UDP (?P<ip>.+):(?P<port>[0-9]{1,6});branch=(?P<branch>.+)']
        super().__init__(buf, attr_list, re_tpl_list)


class From(HeaderLine):
    """
    目前可解析一下五种格式的from
    From: <sip:1502@192.168.0.68:5060;transport=UDP>;tag=443f54eb7dcb273;epid=DP200b41'
    From: <sip:1502@192.168.0.68:5060>;tag=443f54eb7dcb273;epid=DP200b41'
    From: <sip:1502@192.168.0.68:5060>;tag=443f54eb7dcb273'
    From: <sip:1502@192.168.0.68>;tag=443f54eb7dcb273;epid=DP200b41'
    From: <sip:1502@192.168.0.68>;tag=443f54eb7dcb273'

    返回'account', 'ip', 'port', 'transport', 'tag', 'epid'属性
    """

    def __init__(self, buf):
        attr_list = ['account', 'ip', 'port', 'transport', 'tag', 'epid']
        self.account = None
        self.ip = None
        self.port = None
        self.transport = None
        self.tag = None
        self.epid = None
        re_tpl_list = [
            r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>[0-9]{1,6});transport=(?P<transport>.+)>;tag=(?P<tag>.+);epid=(?P<epid>.+)',
            r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>[0-9]{1,6})>;tag=(?P<tag>.+);epid=(?P<epid>.+)',
            r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>[0-9]{1,6})>;tag=(?P<tag>.+)',
            r'<sip:(?P<account>.+)@(?P<ip>.+)>;tag=(?P<tag>.+);epid=(?P<epid>.+)',
            r'<sip:(?P<account>.+)@(?P<ip>.+)>;tag=(?P<tag>.+)']
        super().__init__(buf, attr_list, re_tpl_list)


class To(HeaderLine):
    """
    To: <sip:1500@192.168.0.68:5060>;tag=7a7c8b24;epid=DP200b41
    To: <sip:1500@192.168.0.68:5060>;tag=7a7c8b24
    To: <sip:1500@192.168.0.68:5060>
    To: <sip:1500@192.168.0.68>;tag=7a7c8b24
    To: <sip:1500@192.168.0.68>
    """
    def __init__(self, buf):
        attr_list = ['account','ip','port','tag','epid']
        self.account = None
        self.ip = None
        self.port = None
        self.tag = None
        self.epid = None
        re_tpl_list = [r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>[0-9]{1,6})>;tag=(?P<tag>.+);epid=(?P<epid>.+)',
                       r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>[0-9]{1,6})>;tag=(?P<tag>.+)',
                       r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>[0-9]{1,6})>',
                       r'<sip:(?P<account>.+)@(?P<ip>.+)>;tag=(?P<tag>.+)',
                       r'<sip:(?P<account>.+)@(?P<ip>.+)>']
        super().__init__(buf, attr_list, re_tpl_list)


class CallID(HeaderLine):
    """
    Call-ID: ae8dfd2bc1bdf54@10.20.0.29
    """
    def __init__(self, buf):
        attr_list = ['call_id']
        self.call_id = buf
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)



class CSeq(HeaderLine):
    """
    CSeq: 21 INVITE
    """
    def __init__(self, buf):
        attr_list = ['call_id']
        self.number = None
        self.method = None
        re_tpl_list = [r'(?P<number>[0-9]{1,6}) (?P<method>.+)']
        super().__init__(buf, attr_list, re_tpl_list)


class Contact(HeaderLine):
    """
    Contact: <sip:1501@10.20.0.14:5060;transport=UDP>
    Contact: <sip:1501@10.20.0.14:5060>
    """
    def __init__(self, buf):
        attr_list = ['account','ip','port']
        self.account = None
        self.ip = None
        self.port = None
        re_tpl_list = [r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>[0-9]{1,6});transport=UDP>',
                       r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>[0-9]{1,6})>']
        super().__init__(buf, attr_list, re_tpl_list)


class ProxyAuthorization(HeaderLine):
    def __init__(self, buf):
        # Proxy-Authorization: Digest username="1502", realm="3CXPhoneSystem", nonce="414d535c17a29e5d29:b13fa2d3ccd383ff1240b3bbebbc0524", uri="sip:1500@192.168.0.68:5060", response="b32b6532fde25e2f9c47364afedfd55e", algorithm=MD5
        attr_list = []
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)


class MaxForwards(HeaderLine):
    def __init__(self, buf):
        # Max-Forwards: 70
        self.max_forwards = buf
        attr_list = []
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)


class UserAgent(HeaderLine):
    def __init__(self, buf):
        # User-Agent: Htek UC912G 001fc1200b41
        self.user_agent = buf
        attr_list = []
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)


class ContentDisposition(HeaderLine):
    def __init__(self, buf):
        # Content-Disposition: signal; handling=required
        self.content_disposition = buf
        attr_list = []
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)


class Diversion(HeaderLine):
    def __init__(self, buf):
        # Diversion: <sip:1500@10.20.0.82:81;transport=UDP>;reason=unconditional
        self.diversion = buf
        attr_list = []
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)


class ReferTo(HeaderLine):
    def __init__(self, buf):
        # Refer-To: <sip:1503@192.168.0.68:5060?Replaces=58078934b97ce3e%4010.20.0.16%3Bfrom-tag%3D61b54724c706ec6%3Bto-tag%3D74385a24>
        attr_list = []
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)


class ReferredBy(HeaderLine):
    def __init__(self, buf):
        # Referred-By: <sip:1500@192.168.0.68>
        attr_list = []
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)


class Replaces(HeaderLine):
    def __init__(self, buf):
        # Replaces: i7dH2Mnnmv85_YP4zJtBqA..;to-tag=4ab94a62a6b02d4;from-tag=bf38ac21
        attr_list = []
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)


class Supported(HeaderLine):
    def __init__(self, buf):
        # Supported: replaces
        attr_list = []
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)


class Subject(HeaderLine):
    def __init__(self, buf):
        # Subject: SIP Call
        attr_list = []
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)


class Expires(HeaderLine):
    def __init__(self, buf):
        # Expires: 120
        attr_list = []
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)


class AllowEvents(HeaderLine):
    def __init__(self, buf):
        # Allow-Events: talk,hold,conference,refer,check-sync
        attr_list = []
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)


class Allow(HeaderLine):
    def __init__(self, buf):
        # Allow: INVITE, ACK, UPDATE, INFO, CANCEL, BYE, OPTIONS, REFER, SUBSCRIBE, NOTIFY, MESSAGE, PRACK
        attr_list = []
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)


class Event(HeaderLine):
    def __init__(self, buf):
        # Event: refer
        attr_list = []
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)


class Warning_(HeaderLine):
    def __init__(self, buf):
        # Warning: 499 WIN-7PKJ6575AD0 "Busy"
        attr_list = []
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)


class ContentType(HeaderLine):
    def __init__(self, buf):
        # Content-Type: application/sdp
        attr_list = []
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)


class ContentLength(HeaderLine):
    def __init__(self, buf):
        # Content-Length: 423
        attr_list = []
        re_tpl_list = []
        super().__init__(buf, attr_list, re_tpl_list)
