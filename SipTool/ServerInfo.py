class ServerInfo:
    def __init__(self, remote_ip: str, host_ip: str, sip_port: int, audio_port: int, video_port: int):
        self.remote_ip = remote_ip
        self.host_ip = host_ip
        self.sip_port = sip_port
        self.audio_port = audio_port
        self.video_port = video_port
