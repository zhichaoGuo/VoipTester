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
