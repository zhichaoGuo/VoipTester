import socket
import time

from test.DemoBuffer import REV


def send_sip_buffer(method):
    if method == 'register':
        buf = REV.audio.Register
    elif method == 'register2':
        buf = REV.audio.Register2
    elif method == 'invite':
        buf = REV.audio.Invite
    elif method == '100':
        buf = REV.audio.m_100
    elif method == '180':
        buf = REV.audio.m_180
    elif method == 'hold':
        buf = REV.audio.Hold
    elif method == 'resume':
        buf = REV.audio.Resume
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(True)
    s.bind((send_by_ip, send_by_port))
    s.sendto(buf, (server_ip, server_port))
    time.sleep(0.1)
    s.close()


if __name__ == '__main__':
    send_by_ip = '10.3.3.49'
    send_by_port = 5555
    server_ip = '10.3.3.49'
    server_port = 5666
    send_sip_buffer('register')
    send_sip_buffer('register2')
    send_sip_buffer('invite')

