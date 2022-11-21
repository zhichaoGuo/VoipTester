import queue

from SipTool.MessageParser import SipMessage
from socket import socket

from SipTool.SipMessage import Message3cx


class SipCall:
    """
    用于承担一路通话的主要责任，包括发送sip信息，确认收取sip信息
    """
    def __init__(self, sip_socket: socket, message: SipMessage, server_info:dict):
        self.socket = sip_socket
        self.sip_message = Message3cx()
        self.cur_message = message
        self.server_info = server_info
        self.remote_ip = message.headers.Via.ip
        self.remote_port = message.headers.Via.port
        self.history_message = queue.Queue()

    def put(self, message: SipMessage):
        self.history_message.put(self.cur_message)
        self.cur_message = message

    def rev_message(self,method):  # Todo 完善rev机制
        pass

    def send_message(self, method: str):
        print('send [ %s ] message'% method)
        self._send(self.sip_message.gen_message(self,method))

    def _send(self, buf):
        print('send message to %s:%s' % (self.remote_ip, int(self.remote_port)))
        print(buf)
        self.socket.sendto(buf.encode(encoding='utf-8'),(self.remote_ip,int(self.remote_port)))
