from socket import socket

from SipTool.MessageParser import SipMessage
from SipTool.SipCall import SipCall


class CallInfoManger:
    """
    用于管理Call实例，取出对应的Sip Call
    """

    def __init__(self, sip_socket: socket, host_ip, host_sip_port, host_audio_port, host_video_port):
        self.socket = sip_socket
        self.server_info = {'ip': host_ip,
                            'sip_port': host_sip_port,
                            'audio_port': host_audio_port,
                            'video_port': host_video_port}
        self.dict = {}
        self.all_call_id = set()

    def gen_call(self, aim_account: str) -> SipCall:
        pass

    def get_call(self, cur_message: SipMessage) -> SipCall:
        call_id = cur_message.headers.CallID.call_id
        if call_id not in self.all_call_id:
            self.all_call_id.add(call_id)
            self.dict[call_id] = SipCall(self.socket, cur_message,self.server_info)
        else:
            self.dict[call_id].put(cur_message)
        return self.dict[call_id]

    def remove_call(self, cur_message: SipMessage) -> bool:  # Todo 实现去除call
        pass
