import queue

from socket import socket

from SipTool.ServerInfo import ServerInfo
from SipTool.SipMessage import SipMessage
from SipTool.common.LogInfo import print_send_buf
from SipTool.common.Utils import gen_tag


class SipCall:
    """
    用于承担一路通话的主要责任，包括发送sip信息，确认收取sip信息
    """

    def __init__(self, sip_socket: socket, message: SipMessage, server_info: ServerInfo, remote_port: int,
                 remote_account: str):
        from SipTool.SipMessageFormat import Format3cx
        self.socket = sip_socket
        self.sip_message_format = Format3cx()
        self.cur_message = message
        self.call_id = message.headers.CallID
        self.server_info = server_info
        self.remote_ip = server_info.remote_ip
        self.remote_port = remote_port
        self.remote_account = remote_account
        self.history_message = queue.Queue()
        self.tag = gen_tag()

    def put(self, message: SipMessage):
        """
        将sip message加入历史记录中，并更新cur message
        :param message:
        :return:
        """
        self.history_message.put(self.cur_message)
        self.cur_message = message

    def rev_message(self, method):  # Todo 完善rev机制
        pass

    def gen_message(self, method: str):
        """
        用于测试生成message是否正确，通常在程序中不使用
        :param method:
        :return:
        """
        return self.sip_message_format.gen_message(self, method)

    def send_message(self, method: str):
        """
        发送sip消息
        :param method:期待生成的sip消息的method
        :return:
        """
        print('send [ %s ] message' % method)
        self._send(self.sip_message_format.gen_message(self, method))

    def _send(self, buf):
        print_send_buf(self.remote_ip, int(self.remote_port), buf)
        self.socket.sendto(buf.encode(encoding='utf-8'), (self.remote_ip, int(self.remote_port)))
