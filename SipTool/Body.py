import re


class Body:
    def __init__(self, buf: str):
        sdp_list = buf.split('\r\n')
        body_a_list = []
        body_b_list = []
        for sdp_line in sdp_list:
            if sdp_line == '':  # skip '' line
                continue
            method, option = sdp_line.strip().split('=', 1)
            if method == 'v':
                self.v = Body_v(option)
            elif method == 'o':
                self.o = Body_o(option)
            # elif method == 'i':
            #     self.i=Body_i(option)
            # elif method == 'u':
            #     self.u=Body_u(option)
            # elif method == 'e':
            #     self.e=Body_e(option)
            # elif method == 'p':
            #     self.p=Body_p(option)
            elif method == 'b':
                body_b_list.append(option)
            # elif method == 'z':
            #     self.z=Body_z(option)
            # elif method == 'k':
            #     self.k=Body_k(option)
            elif method == 's':
                self.s = Body_s(option)
            elif method == 'c':
                self.c = Body_c(option)
            elif method == 't':
                self.t = Body_t(option)
            elif (method == 'm') and ('audio' in option):
                self.m_audio = Body_m(option)
            elif (method == 'm') and ('video' in option):
                self.m_video = Body_m(option)
            elif method == 'a':
                body_a_list.append(option)
            else:
                print('can not match sdp body %s' % method)
        self.a = Body_a(body_a_list)
        self.b = Body_b(body_b_list)


class BodyBase:
    def __init__(self, buf):
        self.buf = buf

    def __str__(self):
        return self.buf


class Body_v(BodyBase):
    """
    protocol version
    协议版本
    v=0
    """

    def __init__(self, buf):
        super().__init__(buf)
        self.version = buf


class Body_o(BodyBase):
    """
    owner/creator and session identifier
    所有者/创建者和会话标识符
    o=<username> <sessionid> <version> <network type> <address type> <address>
    """

    def __init__(self, buf):
        super().__init__(buf)
        try:
            re_tpl = r'(?P<username>.+) (?P<sessionid>.+) (?P<version>.+) (?P<network_type>.+) (?P<address_type>.+) (?P<address>.+)'
            self.username = re.search(re_tpl, buf.strip(), re.U).groupdict()['username']
            self.sessionid = re.search(re_tpl, buf.strip(), re.U).groupdict()['sessionid']
            self.version = re.search(re_tpl, buf.strip(), re.U).groupdict()['version']
            self.network_type = re.search(re_tpl, buf.strip(), re.U).groupdict()['network_type']
            self.address_type = re.search(re_tpl, buf.strip(), re.U).groupdict()['address_type']
            self.address = re.search(re_tpl, buf.strip(), re.U).groupdict()['address']
        except Exception:
            print('parse o body err!!')


class Body_i(BodyBase):
    """
    session information
    会话信息
    """

    def __init__(self, buf):
        super().__init__(buf)
        pass


class Body_u(BodyBase):
    """
    URI of description
    URI 描述
    """

    def __init__(self, buf):
        super().__init__(buf)
        pass


class Body_e(BodyBase):
    """
    email address
    Email 地址
    """

    def __init__(self, buf):
        super().__init__(buf)
        pass


class Body_p(BodyBase):
    """
    phone number
    电话号码
    """

    def __init__(self, buf):
        super().__init__(buf)
        pass


class Body_b(BodyBase):
    """
    zero or more bandwidth information lines
    带宽信息
    eg: b=AS:2098
    """

    def __init__(self, b_list: list):
        super().__init__(b_list)

    def __str__(self):
        buf = ''
        for b in self.buf:
            buf += f'b={b}\r\n'
        return buf


class Body_z(BodyBase):
    """
    time zone adjustments
    时区调整
    """

    def __init__(self, buf):
        super().__init__(buf)
        pass


class Body_k(BodyBase):
    """
    encryption key
    加密密钥
    k=已定义的方法有:
    k=clear:<加密密钥>密钥没有变换;
    k=base64:<编码密钥>已编码，因为它含有SDP禁用的字符;
    k=uri:<获得密钥的URI>;
    k=prompt。SDP没有提供密钥但该会话或媒体流是要求加密的。
    """

    def __init__(self, buf):
        super().__init__(buf)
        pass


class Body_s(BodyBase):
    """
    session name
    会话名称
    s=<sessionname>

    """

    def __init__(self, buf):
        super().__init__(buf)
        self.session_name = buf


class Body_c(BodyBase):
    """
    connection information - not required if included in all media
    接信息 ― 如果包含在所有媒体中，则不需要该字段
    c=<networktype> <address type> <connection address>
    """

    def __init__(self, buf):
        super().__init__(buf)
        try:
            re_tpl = r'(?P<network_type>.+) (?P<address_type>.+) (?P<connection_address>.+)'
            self.network_type = re.search(re_tpl, buf.strip(), re.U).groupdict()['network_type']
            self.address_type = re.search(re_tpl, buf.strip(), re.U).groupdict()['address_type']
            self.connection_address = re.search(re_tpl, buf.strip(), re.U).groupdict()['connection_address']
        except Exception:
            print('parse c body err!!')


class Body_t(BodyBase):
    """
    time the session is active
    会话活动时间
    t=<start time> <stop time>
    """

    def __init__(self, buf):
        super().__init__(buf)
        try:
            re_tpl = r'(?P<start_time>.+) (?P<stop_time>.+)'
            self.start_time = re.search(re_tpl, buf.strip(), re.U).groupdict()['start_time']
            self.stop_time = re.search(re_tpl, buf.strip(), re.U).groupdict()['stop_time']
        except Exception:
            print('parse t body err!!')


class Body_m(BodyBase):
    """
    media name and transport address
    媒体名称和传输地址
    m=<media> <port> <transport> <fmt list>
    <media>表示媒体类型。有"audio", “video”,“application”（例白板信息）, “data”（不向用户显示的数据） 和"control"（描述额外的控制通道）
    <port>媒体流发往传输层的端口。取决于c=行规定的网络类型和接下来的传输层协议：对UDP为1024-65535；对于RTP为偶数。
    <transport>传输协议，与c=行的地址类型有关。两种：RTP/AVP，表示RealtimeTransport Protocol using the Audio/Video profile carried over UDP；UDP
    <fmt list>媒体格式。对于音频和视频就是在RTP Audio/Video Profile定义的负载类型(payload type)。但第一个为缺省值。
    eg:  m=audio 12100 RTP/AVP 0 8 9 97 120 102 101
    """

    def __init__(self, buf):
        super().__init__(buf)
        try:
            re_tpl = r'(?P<media>^.+) (?P<port>\d+) (?P<transport>\D+) (?P<fmt_list>[\d ]+$)'
            self.media = re.search(re_tpl, buf.strip(), re.U).groupdict()['media']
            self.port = re.search(re_tpl, buf.strip(), re.U).groupdict()['port']
            self.transport = re.search(re_tpl, buf.strip(), re.U).groupdict()['transport']
            self.fmt_list = re.search(re_tpl, buf.strip(), re.U).groupdict()['fmt_list'].split(' ')
        except Exception:
            print('parse m body err!!')

    def first_codec_code(self):
        return self.fmt_list[0]


class Body_a(BodyBase):
    """
    zero or more media attribute lines
    0 个或多个会话属性行
    a=<attribute>
    a=<attribute>:<value>
    a=cat:<类别>给出点分层次式会话分类号,供接收方筛选会话
    a=keywds:<关键词>供接收方筛选会话
    a=tool:<工具名和版本号>创建会话描述的工具名和版本号
    a=recvonly/sendrecv/sendonly收发模式
    a=type:<会议类型>有:广播,聚会,主席主持,测试,H.323
    a=charset:<字符集>显示会话名和信息数据的字符集
    a=sdplang:<语言标记>描述所有语言
    a=lang:<语言标记>会话描述的缺省语言或媒体描述的语言
    a=framerate:<帧速率>1s播放几个rtp包，导数为一个rtp包承载的数据播放的时间单位s。单位:帧/秒音频的话 a=framerate:50 1byte8000hz20ms=160B，则每个rtp包的音频数据量为160B 时间戳增值为160
    a=quality:<质量>视频的建议质量(10/5/0)
    a=ptime:<分组时间>媒体分组的时长(单位:秒)
    a=orient:<白板方向>指明白板在屏莫上的方向
    a=rtpmap:<payload type> <encoding name>/<clock rate>[/<encodingparameters>]
    a=rtpmap:<负载类型> <编码名>/<时钟速率>[/<编码参数>]
    """

    def __init__(self, a_list: list):
        super().__init__(a_list)
        self.codec = []
        j = 0
        for i in range(len(a_list)):
            if a_list[i] in ['sendrecv', 'sendonly', 'recvonly']:
                self.sendrecv = a_list[i]
                continue
            if 'rtpmap' in a_list[i]:
                self.codec.append(a_list[i])
                j += 1
                continue
            if 'ptime' in a_list[i]:
                self.ptime = a_list[i]
                continue
            if 'fmtp' in a_list[i]:
                self.codec[j - 1] += '\r\na=' + a_list[i]
                continue
            print('can not match %s in sdp body a!' % a_list[i])
        if self._find_dtmf_code() is not False:
            self.dtmf_code = self._find_dtmf_code()

    def find_codec_by_code(self, code):
        for codec in self.codec:
            try:
                re_tpl = f'rtpmap:{code} (?P<codec>.+)'
                ret = re.search(re_tpl, codec.strip(), re.U).groupdict()['codec']
            except Exception:
                continue
            return codec
        print('can not find codec by %s' % code)
        return False

    def _find_dtmf_code(self):
        for codec in self.codec:
            # print(codec)
            try:
                re_tpl = f'rtpmap:(?P<code>.+) telephone-event'
                ret = re.search(re_tpl, codec.strip(), re.U).groupdict()['code']
                return ret
            except Exception:
                continue
        print('can not find dtmf in codec list')
        return False

    def find_dtmf(self):
        return self.find_codec_by_code(self.dtmf_code)

    def is_hold(self):
        if self.sendrecv == 'sendonly':
            return True
        else:
            return False
