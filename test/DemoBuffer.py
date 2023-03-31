class REV:
    Register = b'REGISTER sip:192.168.0.68:5060 SIP/2.0\r\n' \
               b'Via: SIP/2.0/UDP 10.20.0.29:5060;branch=z9hG4bK3284170723\r\n' \
               b'From: <sip:1501@192.168.0.68:5060>;tag=c610e5ca55c5486;epid=DP1f34be\r\n' \
               b'To: <sip:1501@192.168.0.68:5060>\r\n' \
               b'Call-ID: ae8dfd2bc1bdf54@10.20.0.29\r\n' \
               b'CSeq: 1 REGISTER\r\n' \
               b'Contact: <sip:1501@10.20.0.29:5060;transport=UDP>\r\n' \
               b'Max-Forwards: 70\r\n' \
               b'Supported: path\r\n' \
               b'User-Agent: IPPHONE    V2.23.3.29.488 001fc11f34be\r\n' \
               b'Expires: 900\r\n' \
               b'Allow-Events: talk,hold,conference,refer,check-sync\r\n' \
               b'Allow: INVITE, ACK, UPDATE, INFO, CANCEL, BYE, OPTIONS, REFER, SUBSCRIBE, NOTIFY, MESSAGE, PRACK\r\n' \
               b'Content-Length: 0\r\n\r\n'

    Invite = b'INVITE sip:1506@192.168.0.68:5060 SIP/2.0\r\n' \
             b'Via: SIP/2.0/UDP 10.20.0.122:5060;branch=z9hG4bKadcae016\r\n' \
             b'From: <sip:1503@192.168.0.68:5060>;tag=82ec259976534a9;epid=DP142f0d\r\n' \
             b'To: <sip:1506@192.168.0.68:5060>\r\n' \
             b'Call-ID: 520769fcff24902@10.20.0.122\r\n' \
             b'CSeq: 21 INVITE\r\n' \
             b'Contact: <sip:1503@10.20.0.122:5060;transport=UDP>\r\n' \
             b'Proxy-Authorization: Digest username="1503", realm="3CXPhoneSystem", nonce="414d535c197c078b00:5f63503c2d8d814e5f902c768c300a5f", uri="sip:1506@192.168.0.68:5060", response="fdc54d2a3629b8bed7bbfaf4d8d687a0", algorithm=MD5\r\n' \
             b'Max-Forwards: 70\r\nUser-Agent: Htek UC V20 V5.22.10.25.245 f26dcc142f0d\r\n' \
             b'Supported: replaces\r\n' \
             b'Subject: SIP Call\r\n' \
             b'Expires: 120\r\n' \
             b'Allow-Events: talk,hold,conference,refer,check-sync\r\n' \
             b'Allow: INVITE, ACK, UPDATE, INFO, CANCEL, BYE, OPTIONS, REFER, SUBSCRIBE, NOTIFY, MESSAGE, PRACK\r\n' \
             b'Content-Type: application/sdp\r\n' \
             b'Content-Length: 655\r\n\r\n' \
             b'v=0\r\n' \
             b'o=- 780 779 IN IP4 10.20.0.122\r\n' \
             b's=SIP Call\r\n' \
             b'c=IN IP4 10.20.0.122\r\n' \
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

    m_100 = b'SIP/2.0 100 Trying\r\n' \
            b'Via: SIP/2.0/UDP 192.168.0.68:5060;branch=z9hG4bK-524287-1---55488846ef2d022f;rport=5060\r\n' \
            b'From: <sip:1501@192.168.0.68:5060>;tag=3114ad2e;epid=DP1f34be\r\n' \
            b'To: <sip:1503@192.168.0.68>\r\n' \
            b'Call-ID: EWVp62FKT2tuRmfJzheiqA..\r\n' \
            b'CSeq: 1 INVITE\r\n' \
            b'User-Agent: IPPHONE    V2.23.3.29.488 001fc120b9ed\r\n' \
            b'Allow: INVITE, ACK, UPDATE, INFO, CANCEL, BYE, OPTIONS, REFER, SUBSCRIBE, NOTIFY, MESSAGE, PRACK\r\n' \
            b'Content-Length: 0\r\n\r\n'

    m_180 = b'SIP/2.0 180 Ringing\r\n' \
            b'Via: SIP/2.0/UDP 192.168.0.68:5060;branch=z9hG4bK-524287-1---55488846ef2d022f;rport=5060\r\n' \
            b'From: <sip:1501@192.168.0.68:5060>;tag=3114ad2e;epid=DP1f34be\r\n' \
            b'To: <sip:1503@192.168.0.68>;tag=1cc5a65db326b87\r\n' \
            b'Call-ID: EWVp62FKT2tuRmfJzheiqA..\r\n' \
            b'CSeq: 1 INVITE\r\n' \
            b'Contact: <sip:1503@10.20.0.12:5060;transport=UDP>\r\n' \
            b'User-Agent: IPPHONE    V2.23.3.29.488 001fc120b9ed\r\n' \
            b'Allow-Events: talk,hold,conference,refer,check-sync\r\n' \
            b'Allow: INVITE, ACK, UPDATE, INFO, CANCEL, BYE, OPTIONS, REFER, SUBSCRIBE, NOTIFY, MESSAGE, PRACK\r\n' \
            b'Content-Length: 0\r\n\r\n'

    m_200Notify = b'SIP/2.0 200 OK\r\n' \
                  b'Via: SIP/2.0/UDP 192.168.0.68:5060;branch=z9hG4bK-524287-1---6553596b484c5231;rport=5060\r\n' \
                  b'From: <sip:9999@192.168.0.68:5060>;tag=ca0c9716\r\n' \
                  b'To: <sip:1501@10.20.0.29:5060;transport=UDP>;tag=a702c910c463076\r\n' \
                  b'Call-ID: f4iHKU879MNbzux400DI3A..\r\n' \
                  b'CSeq: 1 NOTIFY\r\n' \
                  b'User-Agent: IPPHONE    V2.23.3.29.488 001fc11f34be\r\n' \
                  b'Allow: INVITE, ACK, UPDATE, INFO, CANCEL, BYE, OPTIONS, REFER, SUBSCRIBE, NOTIFY, MESSAGE, PRACK\r\n' \
                  b'Content-Length: 0\r\n\r\n'

    m_200Bye = b'SIP/2.0 200 OK\r\n' \
               b'Via: SIP/2.0/UDP 192.168.0.68:5060;branch=z9hG4bK-524287-1---f92b3251e1466f28;rport=5060\r\n' \
               b'From: <sip:1503@192.168.0.68:5060>;tag=397d3a18\r\n' \
               b'To: <sip:1501@192.168.0.68:5060>;tag=9e572e30960f22a;epid=DP1f34be\r\n' \
               b'Call-ID: d122f020ca76ff8@10.20.0.29\r\n' \
               b'CSeq: 2 BYE\r\n' \
               b'User-Agent: IPPHONE    V2.23.3.29.488 001fc11f34be\r\n' \
               b'Allow: INVITE, ACK, UPDATE, INFO, CANCEL, BYE, OPTIONS, REFER, SUBSCRIBE, NOTIFY, MESSAGE, PRACK\r\n' \
               b'Content-Length: 0\r\n\r\n'


class Send:
    sendNotify = b'NOTIFY sip:1501@10.20.0.29:5060;transport=UDP SIP/2.0\r\n' \
                 b'Via: SIP/2.0/UDP 192.168.0.68:5060;branch=z9hG4bK-524287-1---6553596b484c5231;rport\r\n' \
                 b'Max-Forwards: 70\r\n' \
                 b'Contact: <sip:9999@192.168.0.68:5060>\r\n' \
                 b'To: <sip:1501@10.20.0.29:5060;transport=UDP>\r\n' \
                 b'From: <sip:9999@192.168.0.68:5060>;tag=ca0c9716\r\n' \
                 b'Call-ID: f4iHKU879MNbzux400DI3A..\r\n' \
                 b'CSeq: 1 NOTIFY\r\n' \
                 b'Allow: INVITE, ACK, CANCEL, OPTIONS, BYE, REGISTER, SUBSCRIBE, NOTIFY, REFER, INFO, MESSAGE, UPDATE\r\n' \
                 b'Content-Type: application/simple-message-summary\r\n' \
                 b'Supported: replaces, timer\r\n' \
                 b'Event: message-summary\r\n' \
                 b'Content-Length: 22\r\n\r\n' \
                 b'Messages-Waiting: no\r\n'
