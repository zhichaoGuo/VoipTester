import time

from SipTool.MessageBuilder import SipMessageBuilder, SipBodyBuilder
from SipTool import SipCall
from SipTool.common.Utils import gen_tag


class Message3cx:
    """
    用于确定sip包格式
    """
    def __init__(self):
        self.call = None
        self.msg = None
        self.body = None

    def gen_message(self, call: SipCall, method):
        self.call = call
        self.msg = SipMessageBuilder()
        if method == 'INVITE':
            self.msg.add_state_line_request('INVITE')
            return self.msg.buf
        elif method == 'REFER':
            pass
        elif method == 'BYE':
            pass
        elif method == 'CANCEL':
            pass
        elif method == 'NOTIFY':
            pass
        elif method == 'ACK':
            pass
        elif method == '100':
            self.msg.add_state_line_responses('100')
            self.msg.add_Via(self.call.cur_message.headers.Via)
            self.msg.add_To(self.call.cur_message.headers.To)
            self.msg.add_From(self.call.cur_message.headers.From)
            self.msg.add_CallId(self.call.cur_message.headers.CallID)
            self.msg.add_CSeq(self.call.cur_message.headers.CSeq)
            self.msg.add_body()
            self.msg.build_message()
            return self.msg.buf
        elif method == '180':
            self.msg.add_state_line_responses('180')
            self.msg.add_Via(self.call.cur_message.headers.Via)
            self.msg.add_Contact(f'<sip:{self.call.cur_message.headers.To.account}@{self.call.server_info["ip"]}:{self.call.server_info["sip_port"]}>')
            self.msg.add_To(self.call.cur_message.headers.To, tag=gen_tag())
            self.msg.add_From(self.call.cur_message.headers.From)
            self.msg.add_CallId(self.call.cur_message.headers.CallID)
            self.msg.add_CSeq(self.call.cur_message.headers.CSeq)
            self.msg.add_UserAgent('3CXPhoneSystem 18.0.1.234 (234)')
            self.msg.add_body()
            self.msg.build_message()
        elif method == '200':
            self.body = SipBodyBuilder()
            if self.call.cur_message.method_line.method == 'INVITE':
                self.body.add_v('0')
                self.body.add_o(f'3cxPS {int(time.time())} {int(time.time())} IN IP4 {self.call.server_info["ip"]}')
                self.body.add_s('3cxPS Audio call')
                self.body.add_c(f'IN IP4 {self.call.server_info["ip"]}')
                self.body.add_t('0 0')
                match_codec = self.call.cur_message.body.m_audio.first_codec_code()
                self.body.add_m(f'audio {self.call.server_info["audio_port"]} RTP/AVP {match_codec} {self.call.cur_message.body.a.dtmf_code}')
                self.body.add_a(f'{self.call.cur_message.body.a.find_codec_by_code(match_codec)}')
                self.body.add_a(f'{self.call.cur_message.body.a.ptime}')
                self.body.add_a(f'{self.call.cur_message.body.a.find_dtmf()}')
                self.body.add_a('sendrecv')

            self.msg.add_state_line_responses('200')
            self.msg.add_Via(self.call.cur_message.headers.Via)
            if self.call.cur_message.headers.CSeq.method == 'REGISTER':
                self.msg.add_Contact(
                    f'<sip:{self.call.cur_message.headers.To.account}@{self.call.server_info["ip"]}:{self.call.server_info["sip_port"]};transport=UDP>;expires=900')
            elif self.call.cur_message.method_line.method == 'INVITE' or 'CANCEL':
                self.msg.add_Contact(f'<sip:{self.call.cur_message.headers.To.account}@{self.call.server_info["ip"]}:{self.call.server_info["sip_port"]}>')
            self.msg.add_To(self.call.cur_message.headers.To, tag=gen_tag())
            self.msg.add_From(self.call.cur_message.headers.From)
            self.msg.add_CallId(self.call.cur_message.headers.CallID)
            self.msg.add_CSeq(self.call.cur_message.headers.CSeq.buf)
            if self.call.cur_message.method_line.method == 'INVITE':
                self.msg.add_Allow('INVITE, ACK, CANCEL, OPTIONS, BYE, REGISTER, SUBSCRIBE, NOTIFY, REFER, INFO, MESSAGE, UPDATE')
                self.msg.add_ContentType('application/sdp')
                self.msg.add_Supported('replaces, timer')
            self.msg.add_UserAgent('3CXPhoneSystem 18.0.1.234 (234)')
            self.msg.add_body(self.body.buf)
            self.msg.build_message()
        elif method == '202':
            pass
        elif method == '401':
            pass
        elif method == '404':
            pass
        elif method == '407':
            self.msg.add_state_line_responses('407')
            self.msg.add_Via(self.call.cur_message.headers.Via)
            self.msg.add_ProxyAuthorization('Digest nonce="414d535c19866b8711:c3653d05329d0a86bbd5baf0f9f9862a",algorithm=MD5,realm="3CXPhoneSystem"')
            self.msg.add_To(self.call.cur_message.headers.To, tag=gen_tag())
            self.msg.add_From(self.call.cur_message.headers.From)
            self.msg.add_CallId(self.call.cur_message.headers.CallID)
            self.msg.add_CSeq(self.call.cur_message.headers.CSeq.buf)
            self.msg.add_body()
            self.msg.build_message()
        return self.msg.buf
