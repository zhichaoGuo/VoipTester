import socket
from threading import Thread


class RtpThread:
    """
    rtp转发线程，初始化时应申请本地rtp接收端口和解析出远端rtp接收端口
    """

    def __init__(self, host_ip: str, rtp_port: int):
        self.rtp_port = rtp_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 进行socket配置，使其支持端口复用，否则发送方绑定5066，则无法使用该端口进行接收
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(True)
        self.socket.bind((host_ip, self.rtp_port))
        print('look!!!!!!!!!!start rtp thread at %s:%s' % (host_ip, self.rtp_port))
        self.transfer_flag = True

    def transfer(self, remote_ip, remote_port):
        """
        set remote ip and remote port
        """
        self.remote_ip = remote_ip
        self.remote_port = int(remote_port)
        self.start()

    def _transfer(self):
        print('look!!!!!!!!!!transfer rtp thread to %s:%s' % (self.remote_ip, self.remote_port))
        while True:
            if self.transfer_flag is False:
                print('look!!! transfer flag is False thread return!')
                return False
            try:
                buf, (dut_ip, dut_port) = self.socket.recvfrom(512)
                # print('look!! rtp thread rev a buf from %s:%s'%(dut_ip, dut_port))
                if (dut_ip == self.remote_ip) & (dut_port == self.remote_port):
                    # print('look! rtp thread transfer buf to aim path')
                    self.socket.sendto(buf, (self.remote_ip, self.remote_port))
            except OSError:
                print('exit transfer thread!')
                return False

    def start(self):
        """
        start a new thread to transfer rtp to remote port
        """
        self.transfer_flag = True
        thread = Thread(target=self._transfer)
        # 设置成守护线程
        thread.setDaemon(True)
        # 启动线程
        thread.start()

    def stop(self):
        """
        socket.close
        """
        self.transfer_flag = False
        print('look! set transfer flag = False')
        # self.socket.close()

    def kill(self):
        self.socket.close()