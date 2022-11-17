import select
import socket
from threading import Thread

from SipTool.CallInfoManger import CallInfoManger
from SipTool.MessageParser import SipMessage
from SipTool.Register import Register
from SipTool.common.UniqueQueue import UniqueQueue


class SipServer:
    def __init__(self,
                 host_ip: str,
                 host_sip_port: int,
                 host_audio_port: int,
                 host_video_port:int,
                 remote_ip: str = None,
                 remote_port: int = None):
        self.host_ip = host_ip
        self.host_sip_port = host_sip_port
        self.host_audio_port = host_audio_port
        self.host_video_port = host_video_port
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        # 创建udp socket 并配置复用
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(True)
        self.socket.bind((host_ip, host_sip_port))
        # 配置rtp转发线程
        # self.audio_thread = RtpThread(self.host_ip,self.rtp_port)
        # self.video_thread = RtpThread(self.host_ip,self.rtp_port)
        # 配置call info队列
        self.input = UniqueQueue()
        self.call_manger = CallInfoManger()
        # 启动sip应答线程
        # self.sip_message_map = SipBaseMessage()
        self.sip_thread = Thread(target=self.auto_sip)
        self.sip_thread.setDaemon(True)
        self.sip_thread.start()
        # 注册信息
        self.register = Register()

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
                    cur_call = self.call_manger.get_call(cur_message)
                    method = cur_message.method_line.method
                    # 接收处理注册信息：
                    if method == 'REGISTER':
                        if cur_message.headers.CSeq.number == '1':
                            cur_call.send_message('407', cur_message)
                            continue
                        else:
                            self.send_message('200_reg', cur_message)
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
                        self.send_message('200_info', cur_message)
                        continue
                    elif method == 'OPTION':
                        continue

                    # 打印收到的message
                    print('\r\n↓↓↓↓↓↓↓↓↓↓↓↓↓ rev message from %s:%s ↓↓↓↓↓↓\r\n%s' % (
                        dut_ip, dut_port, buf.decode('utf-8')))
                    print('↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑\r\n')
                    cur_call = self.all_call.add(cur_message)
                    if method == 'INVITE':
                        # 放入buf 取得incoming call
                        print('向队列中放入【%s】消息' % method)
                        if cur_message.is_hold:
                            self.send_message('200_hold', cur_message)
                        elif cur_message.is_resume:
                            self.send_message('200', cur_message)
                        else:
                            self.send_message('100', cur_message)
                            self.send_message('180', cur_message)
                    elif method == '180':
                        # do update to tag
                        pass
                    elif method == '200':
                        if cur_message.headers.CSeq.method == 'INVITE':
                            self.send_message('ack_invite', cur_message)
                    elif method == '302':
                        self.send_message('ack_invite', cur_message)
                    elif method == '486':
                        self.send_message('ack_invite', cur_message)
                    elif method == '487':
                        self.send_message('ack_487', cur_message)
                    elif method == 'CANCEL':
                        self.send_message('200_cancel', cur_message)
                    elif method == 'BYE':
                        self.send_message('200_bye', cur_message)
                    elif method == 'REFER':
                        self.send_message('202', cur_message)
                        self.send_message('notify_trying', cur_message)


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
