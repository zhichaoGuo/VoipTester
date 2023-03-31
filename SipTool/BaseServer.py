import select
import socket
import time
from threading import Thread
from typing import Union

from SipTool.CallInfoManger import CallInfoManger
from SipTool.MessageParser import SipMessage
from SipTool.Register import Register
from SipTool.RtpThread import RtpThread
from SipTool.ServerInfo import ServerInfo
from SipTool.SipCall import SipCall
from SipTool.common.UniqueQueue import UniqueQueue


class SipServer:
    """
    用于接收sip消息，实现sip 通信
    """

    def __init__(self,
                 host_ip: str,
                 host_sip_port: int,
                 host_audio_port: int,
                 host_video_port: int,
                 remote_ip: str = None,
                 remote_port: int = None):
        self.host_ip = host_ip
        self.host_sip_port = host_sip_port
        self.host_audio_port = host_audio_port
        self.host_video_port = host_video_port
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.server_info = ServerInfo(remote_ip, host_ip, host_sip_port, host_audio_port, host_video_port)
        # 创建udp socket 并配置复用
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(True)
        self.socket.bind((host_ip, host_sip_port))
        # 配置rtp转发线程
        self.audio_thread = RtpThread(self.host_ip, self.host_audio_port)
        self.video_thread = RtpThread(self.host_ip, self.host_video_port)
        # 注册信息
        self.register = Register()
        # 配置call info队列
        self.input = UniqueQueue()
        self.call_manger = CallInfoManger(self.socket, self.server_info, self.register)
        # 启动sip应答线程
        self.sip_thread = Thread(target=self.auto_sip)
        self.sip_thread.setDaemon(True)
        self.sip_thread.start()

    def auto_sip(self):
        s_input = [self.socket, ]
        s_output = []
        while True:
            readable, writeable, exeptional = select.select(s_input, s_output, s_input)
            # 读取数据
            for s in readable:  # 每个s就是一个socket
                if s is self.socket:
                    # 接受信息,判断是否来自目标话机，以及是否为空
                    buf, (dut_ip, dut_port) = s.recvfrom(1500)
                    # 不是来自目标话机的skip
                    if dut_ip != self.remote_ip:
                        print('skip buf from %s:%s ,not from %s:%s' % (
                            dut_ip, dut_port, self.remote_ip, self.remote_port))
                        continue
                    # 跳过空行
                    if buf.decode('utf-8') == '\r\n\r\n':
                        continue
                    cur_message = SipMessage(buf)
                    cur_call = self.call_manger.get_call(cur_message, dut_port)
                    method = cur_message.method_line.method
                    # 接收处理注册信息：
                    if method == 'REGISTER':
                        if cur_message.headers.CSeq.number == '1':
                            cur_call.send_message('407')
                            continue
                        else:
                            cur_call.send_message('200')
                            # 添加或更新注册表
                            if dut_port not in self.register:
                                self.register.add(cur_message.headers.From.account, dut_port)
                                continue
                            else:
                                self.register.update(cur_message.headers.From.account, dut_port)
                                continue
                    # 不在注册表里的非注册信息 跳过
                    elif dut_port not in self.register:
                        continue
                    if method == 'INFO':
                        cur_call.send_message('200')
                        continue
                    elif method == 'OPTION':
                        cur_call.send_message('200')

                    # 打印收到的message
                    print('\r\n↓↓↓↓↓↓↓↓↓↓↓↓↓ rev message from %s:%s ↓↓↓↓↓↓\r\n%s' % (
                        dut_ip, dut_port, buf.decode('utf-8')))
                    print('↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑\r\n')
                    if method == 'INVITE':
                        # 放入buf 取得incoming call
                        print('向队列中放入【%s】消息' % method)
                        if cur_message.is_hold():
                            cur_call.send_message('100')
                            cur_call.send_message('200')
                        elif cur_message.is_resume():
                            cur_call.send_message('200')
                        else:
                            cur_call.send_message('100')
                            cur_call.send_message('180')
                    elif method == '180':  # Todo: update To tag
                        # do update to tag
                        pass
                    elif method == '200':
                        if cur_message.headers.CSeq.method == 'INVITE':
                            cur_call.send_message('ACK')
                    elif method == '302':
                        cur_call.send_message('ACK')
                    elif method == '486':
                        cur_call.send_message('ACK')
                    elif method == '487':
                        cur_call.send_message('ACK')
                    elif method == 'CANCEL':
                        cur_call.send_message('200')
                    elif method == 'BYE':
                        cur_call.send_message('200')
                    elif method == 'REFER':
                        cur_call.send_message('202')
                        cur_call.send_message('notify_trying')

    def send_invite(self, aim_account: str, use_account: str) -> Union[bool, SipCall]:  # Todo: 发起一路新的call
        if aim_account not in self.register:
            print('[ %s ] is not register!' % aim_account)
            return False
        return self.call_manger.make_call(aim_account, use_account)


class AllCallDict:
    def __init__(self):
        self.dict = {}
        self.all_call_id = set()

    def add(self, cur_message: SipMessage):
        call_id = cur_message.headers.CallID.call_id
        if call_id not in self.all_call_id:
            self.all_call_id.add(call_id)
        else:
            self.dict[call_id].put(cur_message)
        return self.dict[call_id]


if __name__ == '__main__':
    host_ip = '10.3.3.49'
    host_sip_port = 8060
    host_audio_port = 12100
    host_video_port = 12150
    remote_ip = '10.20.1.6'
    remote_port = 5060
    server = SipServer(host_ip, host_sip_port, host_audio_port, host_video_port, remote_ip, remote_port)
    while not server.register.is_register('1501'):
        time.sleep(1)
    server.call_manger.make_call('1501', '998')
    time.sleep(100)
