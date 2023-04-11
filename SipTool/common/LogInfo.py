import copy


def print_send_buf(ip, port, buf: str):
    print(f'\r\n↓↓↓↓↓↓↓↓↓↓↓↓↓ send message to {ip}:{port} ↓↓↓↓↓↓\r\n')
    print(buf)


def print_rev_buf(ip, port, buf: bytes):
    blank = '                                                           '
    print(f'\r\n{blank}↓↓↓↓↓↓↓↓↓↓↓↓↓ rev message from {ip}:{port} ↓↓↓↓↓↓')
    print(f'{blank}%s' % buf.decode("utf-8").replace("\r\n", f"\r\n{blank}"))


