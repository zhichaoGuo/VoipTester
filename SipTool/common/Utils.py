import uuid


def cut_in(line: str, flag: str = ':') -> (str, str):
    """
        将header分割为 header_method 和 header_body,如Via: something 分割为Via something
        :param line: 待分割header line
        :param flag: 分隔符,默认为':'
        :return: header_method 和 header_body
        """
    flag_num = line.find(flag)
    if flag_num == -1:
        return None, None
    method = line[:flag_num].strip()
    body = line[flag_num + 1:].strip()
    return method, body

def gen_call_id():
    """
    生成15位的随机字符串作为call_id
    :return: str
    """
    call_id = ''.join(str(uuid.uuid1()).split('-'))
    return call_id[:15]


def gen_branch():
    """
    生成z9hG4bK开头的随机branch
    :return: str
    """
    branch = ''.join(str(uuid.uuid1()).split('-'))
    return 'z9hG4bK' + branch[:12]


def gen_tag():
    tag = ''.join(str(uuid.uuid1()).split('-'))
    return tag[:15]


def gen_epid():
    from random import choice
    epid = "".join([choice("0123456789abcdef") for i in range(6)])
    return "DP" + epid