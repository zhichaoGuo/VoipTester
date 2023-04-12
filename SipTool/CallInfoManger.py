from socket import socket
from typing import Union

from SipTool.Register import Register
from SipTool.ServerInfo import ServerInfo
from SipTool.SipCall import SipCall
from SipTool.SipMessage import Message3cx, SipMessage


class CallInfoManger:
    """
    用于管理Call实例，取出对应的Sip Call
    """

    def __init__(self, sip_socket: socket, server_info: ServerInfo, register: Register):
        self.socket = sip_socket
        self.server_info = server_info
        self.register = register
        self.dict = {}
        self.all_call_id = set()

    def make_call(self, aim_account: str, use_account: str) -> Union[bool, SipCall]:  # Todo: make a new call
        remote_port = self.register.query(aim_account)
        if not remote_port:
            print('%s do not register!' % aim_account)
            return False
        msg = Message3cx().gen_invite_message(aim_account, use_account, self.server_info, remote_port)
        cur_call = SipCall(self.socket, msg, self.server_info, remote_port, aim_account)
        self.socket.sendto(msg.encode('utf-8'), (self.server_info.remote_ip, remote_port))
        return cur_call

    def get_call(self, cur_message: SipMessage, remote_port: int) -> SipCall:
        """
        从集合中取出cur message相同call id的sip call，如果没有则新建一个
        :param cur_message:
        :param remote_port:
        :return:
        """
        call_id = cur_message.headers.CallID.call_id
        # 是新的一路call id，创建sip call
        if call_id not in self.all_call_id:
            self.all_call_id.add(call_id)
            self.dict[call_id] = SipCall(self.socket, cur_message, self.server_info, remote_port,
                                         cur_message.headers.From.account)
        else:
            self.dict[call_id].put(cur_message)
        return self.dict[call_id]

    def remove_call(self, cur_message: SipMessage) -> bool:  # Todo: 实现去除call
        pass
