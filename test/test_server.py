import time

from SipTool.BaseServer import SipServer

if __name__ == '__main__':
    server_ip = '10.3.3.49'
    server_sip_port = 5666
    server_audio_port = 12102
    server_video_port = 12152
    send_by_ip = '10.3.3.49'
    send_by_port = 5555
    server = SipServer(server_ip, server_sip_port, server_audio_port, server_video_port, send_by_ip, send_by_port)
    time.sleep(660)
