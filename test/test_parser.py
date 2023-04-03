from SipTool.MessageParser import parser_buf
from SipTool.SipHeader import Via, From, To, CallID, CSeq, Contact
from test.DemoBuffer import REV


class TestParser:

    def test_method(self):
        sip_message = parser_buf(REV.Invite)
        assert sip_message.method_line.method == 'INVITE'
        assert sip_message.method_line.is_responses is False
        sip_message = parser_buf(REV.m_100)
        assert sip_message.method_line.method == '100'
        assert sip_message.method_line.is_responses is True

    def test_via(self):
        _via = ['SIP/2.0/UDP 192.168.0.68:5060;branch=z9hG4bK-524287-1---405e1b7d2300f323;rport=5060',
                'SIP/2.0/UDP 192.168.0.68:5060;branch=z9hG4bK-524287-1---405e1b7d2300f323;rport',
                'SIP/2.0/UDP 192.168.0.68:5060;branch=z9hG4bK1938747582']
        hope = [['192.168.0.68', '5060', 'z9hG4bK-524287-1---405e1b7d2300f323', '5060'],
                ['192.168.0.68', '5060', 'z9hG4bK-524287-1---405e1b7d2300f323', None],
                ['192.168.0.68', '5060', 'z9hG4bK1938747582', None]]
        for i in range(len(_via)):
            demo = Via(_via[i])
            assert demo.ip == hope[i][0]
            assert demo.port == hope[i][1]
            assert demo.branch == hope[i][2]
            assert demo.rport == hope[i][3]

    def test_from(self):
        _from = ['<sip:1502@192.168.0.68:5060;transport=UDP>;tag=443f54eb7dcb273;epid=DP200b41',
                 '<sip:1502@192.168.0.68:5060>;tag=443f54eb7dcb273;epid=DP200b41',
                 '<sip:1502@192.168.0.68:5060>;tag=443f54eb7dcb273',
                 '<sip:1502@192.168.0.68>;tag=443f54eb7dcb273;epid=DP200b41',
                 '<sip:1502@192.168.0.68>;tag=443f54eb7dcb273']
        hope = [['1502', '192.168.0.68', '5060', 'UDP', '443f54eb7dcb273', 'DP200b41'],
                ['1502', '192.168.0.68', '5060', None, '443f54eb7dcb273', 'DP200b41'],
                ['1502', '192.168.0.68', '5060', None, '443f54eb7dcb273', None],
                ['1502', '192.168.0.68', None, None, '443f54eb7dcb273', 'DP200b41'],
                ['1502', '192.168.0.68', None, None, '443f54eb7dcb273', None]]
        for i in range(len(_from)):
            demo = From(_from[i])
            assert demo.account == hope[i][0]
            assert demo.ip == hope[i][1]
            assert demo.port == hope[i][2]
            assert demo.transport == hope[i][3]
            assert demo.tag == hope[i][4]
            assert demo.epid == hope[i][5]

    def test_to(self):
        _to = ['<sip:1500@192.168.0.68:5060>;tag=7a7c8b24;epid=DP200b41',
               '<sip:1500@192.168.0.68:5060>;tag=7a7c8b24',
               '<sip:1500@192.168.0.68:5060>',
               '<sip:1500@192.168.0.68>;tag=7a7c8b24',
               '<sip:1500@192.168.0.68>']
        hope = [['1500', '192.168.0.68', '5060', '7a7c8b24', 'DP200b41'],
                ['1500', '192.168.0.68', '5060', '7a7c8b24', None],
                ['1500', '192.168.0.68', '5060', None, None],
                ['1500', '192.168.0.68', None, '7a7c8b24', None],
                ['1500', '192.168.0.68', None, None, None]]
        for i in range(len(_to)):
            demo = To(_to[i])
            assert demo.account == hope[i][0]
            assert demo.ip == hope[i][1]
            assert demo.port == hope[i][2]
            assert demo.tag == hope[i][3]
            assert demo.epid == hope[i][4]

    def test_call_id(self):
        call_id = ['ae8dfd2bc1bdf54@10.20.0.29']
        hope = [['ae8dfd2bc1bdf54@10.20.0.29']]
        for i in range(len(call_id)):
            demo = CallID(call_id[i])
            assert demo.call_id == hope[i][0]

    def test_cseq(self):
        cseq = ['21 INVITE']
        hope = [['21','INVITE']]
        for i in range(len(cseq)):
            demo = CSeq(cseq[i])
            assert demo.number == hope[i][0]
            assert demo.method == hope[i][1]

    def test_contact(self):
        contact = ['<sip:1501@10.20.0.14:5060;transport=UDP>',
                   '<sip:1501@10.20.0.14:5060>']
        hope = [['1501','10.20.0.14','5060','UDP'],
                ['1501','10.20.0.14','5060',None]]
        for i in range(len(contact)):
            demo = Contact(contact)
            assert demo.account == hope[i][0]
            assert demo.ip == hope[i][1]
            assert demo.port == hope[i][2]
            assert demo.transport == hope[i][3]




if __name__ == '__main__':
    test = TestParser()
    test.test_method()
    test.test_via()
    test.test_from()
    test.test_to()
    test.test_call_id()
