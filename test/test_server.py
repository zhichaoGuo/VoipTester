from SipTool.BaseServer import SipServer
from SipTool.MessageParser import parser_buf


class DUT:
    """
    DUT account:1505
    ip: 10.20.0.13
    host account:1501
    """
    Inivte = b'INVITE sip:1501@192.168.0.68:5060 SIP/2.0\r\n' \
             b'Via: SIP/2.0/UDP 10.20.0.13:5060;branch=z9hG4bK4ae566b4\r\n' \
             b'From: <sip:1505@192.168.0.68:5060>;tag=1cd26e954e8545b;epid=DP142f0d\r\n' \
             b'To: <sip:1501@192.168.0.68:5060>\r\n' \
             b'Call-ID: 8d00ec747e46f97@10.20.0.13\r\n' \
             b'CSeq: 21 INVITE\r\n' \
             b'Contact: <sip:1505@10.20.0.13:5060;transport=UDP>\r\n' \
             b'Proxy-Authorization: Digest username="1505", realm="3CXPhoneSystem", nonce="414d535c1a469adb00:3f36141d11099417778c7f314279a418", uri="sip:1501@192.168.0.68:5060", response="bdef901b433dd582cecfb96f69c47eec", algorithm=MD5\r\n' \
             b'Max-Forwards: 70\r\n' \
             b'User-Agent: IPPHONE UCV20 V5.23.3.13.112 f26dcc142f0d\r\n' \
             b'Supported: replaces\r\n' \
             b'Expires: 120\r\n' \
             b'Allow-Events: talk,hold,conference,refer,check-sync\r\n' \
             b'Allow: INVITE, ACK, UPDATE, INFO, CANCEL, BYE, OPTIONS, REFER, SUBSCRIBE, NOTIFY, MESSAGE, PRACK\r\n' \
             b'Content-Type: application/sdp\r\n' \
             b'Content-Length: 653\r\n\r\n' \
             b'v=0\r\n' \
             b'o=- 781 780 IN IP4 10.20.0.13\r\n' \
             b's=SDP data\r\n' \
             b'c=IN IP4 10.20.0.13\r\n' \
             b't=0 0\r\n' \
             b'm=audio 12100 RTP/AVP 0 8 9 97 120 102 101\r\n' \
             b'a=rtpmap:0 PCMU/8000\r\n' \
             b'a=ptime:20\r\n' \
             b'a=rtpmap:8 PCMA/8000\r\n' \
             b'a=rtpmap:9 G722/8000\r\n' \
             b'a=rtpmap:97 iLBC/8000\r\n' \
             b'a=fmtp:97 mode=20\r\n' \
             b'a=rtpmap:120 opus/48000/2\r\n' \
             b'a=fmtp:120 useinbandfec=1; usedtx=1; maxaveragebitrate=64000\r\n' \
             b'a=rtpmap:102 G726-32/8000\r\n' \
             b'a=rtpmap:101 telephone-event/8000\r\n' \
             b'a=fmtp:101 0-11,16\r\n' \
             b'a=sendrecv\r\n' \
             b'm=video 12150 RTP/AVP 96 97\r\n' \
             b'b=AS:2098\r\n' \
             b'b=TIAS:2097152\r\n' \
             b'a=rtpmap:96 H264/90000\r\n' \
             b'a=fmtp:96 profile-level-id=428016;max-fs=792;max-mbps=19800; packetization-mode=1\r\n' \
             b'a=rtpmap:97 VP8/90000\r\n' \
             b'a=fmtp:97 max-fr=30;max-fs=792\r\n' \
             b'a=sendrecv\r\n'

    m_200bye = b''

    Bye = b'BYE sip:1501@192.168.0.68:5060 SIP/2.0\r\n' \
          b'Via: SIP/2.0/UDP 10.20.0.13:5060;branch=z9hG4bK4ae566b4\r\n' \
          b'From: <sip:1505@192.168.0.68:5060>;tag=1cd26e954e8545b;epid=DP142f0d\r\n' \
          b'To: <sip:1501@192.168.0.68:5060>;tag=6774c96e\r\n' \
          b'Call-ID: 8d00ec747e46f97@10.20.0.13\r\n' \
          b'CSeq: 26 BYE\r\n' \
          b'Contact: <sip:1505@10.20.0.13:5060;transport=UDP>\r\n' \
          b'Proxy-Authorization: Digest username="1505", realm="3CXPhoneSystem", nonce="414d535c1a46de1911:ec8ada1a3ce6ce91709694a83ebde231", uri="sip:1501@192.168.0.68:5060", response="e500f61d73e1074382cbecceaf2cabef", algorithm=MD5\r\n' \
          b'Max-Forwards: 70\r\n' \
          b'User-Agent: IPPHONE UCV20 V5.23.3.13.112 f26dcc142f0d\r\n' \
          b'Content-Length: 0\r\n\r\n'


class SERVER:
    m_100 = b'SIP/2.0 100 Trying\r\n' \
            b'Via: SIP/2.0/UDP 10.20.0.13:5060;branch=z9hG4bK4ae566b4\r\n' \
            b'To: <sip:1501@192.168.0.68:5060>\r\n' \
            b'From: <sip:1505@192.168.0.68:5060>;tag=1cd26e954e8545b;epid=DP142f0d\r\n' \
            b'Call-ID: 8d00ec747e46f97@10.20.0.13\r\n' \
            b'CSeq: 21 INVITE\r\n' \
            b'Content-Length: 0\r\n\r\n'

    m_180 = b'SIP/2.0 180 Ringing\r\n' \
            b'Via: SIP/2.0/UDP 10.20.0.13:5060;branch=z9hG4bK4ae566b4\r\n' \
            b'Contact: <sip:1501@192.168.0.68:5060>\r\n' \
            b'To: <sip:1501@192.168.0.68:5060>;tag=e173c348\r\n' \
            b'From: <sip:1505@192.168.0.68:5060>;tag=1cd26e954e8545b;epid=DP142f0d\r\n' \
            b'Call-ID: 8d00ec747e46f97@10.20.0.13\r\n' \
            b'CSeq: 21 INVITE\r\n' \
            b'User-Agent: 3CXPhoneSystem 18.0.7.312 (312)\r\n' \
            b'Content-Length: 0\r\n\r\n'

    m_200invite = b'SIP/2.0 200 OK\r\n' \
                  b'Via: SIP/2.0/UDP 10.20.0.13:5060;branch=z9hG4bK4ae566b4\r\n' \
                  b'Contact: <sip:1501@192.168.0.68:5060>\r\n' \
                  b'To: <sip:1501@192.168.0.68:5060>;tag=e173c348\r\n' \
                  b'From: <sip:1505@192.168.0.68:5060>;tag=1cd26e954e8545b;epid=DP142f0d\r\n' \
                  b'Call-ID: 8d00ec747e46f97@10.20.0.13\r\n' \
                  b'CSeq: 21 INVITE\r\n' \
                  b'Allow: INVITE, ACK, CANCEL, OPTIONS, BYE, REGISTER, SUBSCRIBE, NOTIFY, REFER, INFO, MESSAGE, UPDATE\r\n' \
                  b'Content-Type: application/sdp\r\n' \
                  b'Supported: replaces, timer\r\n' \
                  b'User-Agent: 3CXPhoneSystem 18.0.7.312 (312)\r\n' \
                  b'Content-Length: 237\r\n\r\n' \
                  b'v=0\r\n' \
                  b'o=3cxPS 258335571968 280582160385 IN IP4 192.168.0.68\r\n' \
                  b's=3cxPS Audio call\r\n' \
                  b'c=IN IP4 10.3.2.58\r\n' \
                  b't=0 0\r\n' \
                  b'm=audio 12100 RTP/AVP 0 101\r\n' \
                  b'a=rtpmap:0 PCMU/8000\r\n' \
                  b'a=ptime:20\r\n' \
                  b'a=rtpmap:101 telephone-event/8000\r\n' \
                  b'a=fmtp:101 0-11,16\r\n' \
                  b'a=sendrecv\r\n'

    Bye = b'BYE sip:1505@10.20.0.13:5060;transport=UDP SIP/2.0\r\n' \
          b'Via: SIP/2.0/UDP 192.168.0.68:5060;branch=z9hG4bK4ae566b4\r\n' \
          b'Max-Forwards: 70\r\n' \
          b'Contact: <sip:1501@192.168.0.68:5060>\r\n' \
          b'To: <sip:1505@192.168.0.68:5060>;tag=1cd26e954e8545b;epid=DP142f0d\r\n' \
          b'From: <sip:1501@192.168.0.68:5060>;tag=e173c348\r\n' \
          b'Call-ID: 8d00ec747e46f97@10.20.0.13\r\n' \
          b'CSeq: 2 BYE\r\n' \
          b'User-Agent: 3CXPhoneSystem 18.0.7.312 (312)\r\n' \
          b'Content-Length: 0\r\n\r\n'

    m_200bye = b'SIP/2.0 200 OK\r\n' \
               b'Via: SIP/2.0/UDP 10.20.0.13:5060;branch=z9hG4bK4ae566b4\r\n' \
               b'Contact: <sip:1501@192.168.0.68:5060>\r\n' \
               b'To: <sip:1501@192.168.0.68:5060>;tag=6774c96e\r\n' \
               b'From: <sip:1505@192.168.0.68:5060>;tag=1cd26e954e8545b;epid=DP142f0d\r\n' \
               b'Call-ID: 8d00ec747e46f97@10.20.0.13\r\n' \
               b'CSeq: 26 BYE\r\n' \
               b'User-Agent: 3CXPhoneSystem 18.0.7.312 (312)\r\n' \
               b'Content-Length: 0\r\n\r\n'


class TestDutInvite:
    server_ip = '192.168.0.68'
    server_sip_port = 5060
    server_audio_port = 12102
    server_video_port = 12152
    send_by_ip = '10.20.0.13'
    send_by_port = 5060
    server = SipServer(server_ip, server_sip_port, server_audio_port, server_video_port, send_by_ip, send_by_port, True)
    server.register.add('1501', 5060)
    input_msg = parser_buf(DUT.Inivte)

    def test_gen_100(self):
        msg = self.server.call_manger.get_call(self.input_msg, 5060).gen_message('100')
        assert msg.encode('utf-8') == SERVER.m_100

    def test_gen_180(self):
        msg = self.server.call_manger.get_call(self.input_msg, 5060).gen_message('180')
        gen_msg = parser_buf(msg.encode('utf-8'))
        hope_msg = parser_buf(SERVER.m_180)
        assert str(gen_msg.method_line) == str(hope_msg.method_line)
        assert str(gen_msg.headers.Via) == str(hope_msg.headers.Via)
        assert str(gen_msg.headers.Contact) == str(hope_msg.headers.Contact)
        assert str(gen_msg.headers.To.account) == str(hope_msg.headers.To.account)
        assert str(gen_msg.headers.To.ip) == str(hope_msg.headers.To.ip)
        assert str(gen_msg.headers.To.port) == str(hope_msg.headers.To.port)
        assert str(gen_msg.headers.From) == str(hope_msg.headers.From)
        assert str(gen_msg.headers.CallID) == str(hope_msg.headers.CallID)
        assert str(gen_msg.headers.CSeq) == str(hope_msg.headers.CSeq)

    def test_gen_200invite(self):
        msg = self.server.call_manger.get_call(self.input_msg, 5060).gen_message('200')
        gen_msg = parser_buf(msg.encode('utf-8'))
        hope_msg = parser_buf(SERVER.m_200invite)
        assert str(gen_msg.method_line) == str(hope_msg.method_line)
        assert str(gen_msg.headers.Via) == str(hope_msg.headers.Via)
        assert str(gen_msg.headers.Contact) == str(hope_msg.headers.Contact)
        assert str(gen_msg.headers.To.account) == str(hope_msg.headers.To.account)
        assert str(gen_msg.headers.To.ip) == str(hope_msg.headers.To.ip)
        assert str(gen_msg.headers.To.port) == str(hope_msg.headers.To.port)
        assert str(gen_msg.headers.From) == str(hope_msg.headers.From)
        assert str(gen_msg.headers.CallID) == str(hope_msg.headers.CallID)
        assert str(gen_msg.headers.CSeq) == str(hope_msg.headers.CSeq)
        assert str(gen_msg.headers.Allow) == str(hope_msg.headers.Allow)
        assert str(gen_msg.headers.ContentType) == str(hope_msg.headers.ContentType)
        assert str(gen_msg.headers.Supported) == str(hope_msg.headers.Supported)
        assert str(gen_msg.body.v) == str(hope_msg.body.v)
        assert str(gen_msg.body.s) == str(hope_msg.body.s)
        assert str(gen_msg.body.t) == str(hope_msg.body.t)
        assert str(gen_msg.body.m_audio.transport) == str(hope_msg.body.m_audio.transport)
        assert str(gen_msg.body.m_audio.fmt_list) == str(hope_msg.body.m_audio.fmt_list)
        assert str(gen_msg.body.m_audio.first_codec_code()) == str(hope_msg.body.m_audio.first_codec_code())
        assert str(gen_msg.body.a.ptime) == str(hope_msg.body.a.ptime)

    def test_gen_200bye(self):
        msg = self.server.call_manger.get_call(parser_buf(DUT.Bye), 5060).gen_message('200')
        gen_msg = parser_buf(msg.encode('utf-8'))
        hope_msg = parser_buf(SERVER.m_200bye)
        assert str(gen_msg.method_line) == str(hope_msg.method_line)
        assert str(gen_msg.headers.Via) == str(hope_msg.headers.Via)
        assert str(gen_msg.headers.Contact) == str(hope_msg.headers.Contact)
        assert str(gen_msg.headers.To) == str(hope_msg.headers.To)
        assert str(gen_msg.headers.From) == str(hope_msg.headers.From)
        assert str(gen_msg.headers.CallID) == str(hope_msg.headers.CallID)
        assert str(gen_msg.headers.CSeq) == str(hope_msg.headers.CSeq)
        assert str(gen_msg.headers.UserAgent) == str(hope_msg.headers.UserAgent)

    def test_gen_bye(self):
        msg = self.server.call_manger.get_call(self.input_msg, 5060).gen_message('BYE')
        gen_msg = parser_buf(msg.encode('utf-8'))
        hope_msg = parser_buf(SERVER.Bye)
        print(msg)
        assert str(gen_msg.method_line) == str(hope_msg.method_line)
        assert str(gen_msg.headers.Via.ip) == str(hope_msg.headers.Via.ip)
        assert str(gen_msg.headers.Via.port) == str(hope_msg.headers.Via.port)
        assert str(gen_msg.headers.To) == str(hope_msg.headers.To)
        assert str(gen_msg.headers.From.account) == str(hope_msg.headers.From.account)
        assert str(gen_msg.headers.From.ip) == str(hope_msg.headers.From.ip)
        assert str(gen_msg.headers.From.port) == str(hope_msg.headers.From.port)
        assert str(gen_msg.headers.CallID) == str(hope_msg.headers.CallID)
        assert str(gen_msg.headers.CSeq) == str(hope_msg.headers.CSeq)
        assert str(gen_msg.headers.UserAgent) == str(hope_msg.headers.UserAgent)

    def test_gen_100hold(self):
        pass

    def test_gen_200hold(self):
        pass

    def test_gen_hold(self):
        pass


if __name__ == '__main__':
    test = TestDutInvite()
    test.test_gen_100()
    test.test_gen_180()
    test.test_gen_200invite()
    test.test_gen_200bye()
    test.test_gen_bye()
