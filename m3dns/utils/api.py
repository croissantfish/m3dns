from urllib.request import urlopen


def get_public_ip_addr_ver4() -> str:
    ip = urlopen('https://api-ipv4.ip.sb/ip').read()  # 使用IP.SB的接口获取ipv4地址
    return str(ip, encoding='utf-8')


def get_public_ip_addr_ver6() -> str:
    ip = urlopen('https://api-ipv6.ip.sb/ip').read()  # 使用IP.SB的接口获取ipv6地址
    return str(ip, encoding='utf-8')


__all__ = [
    'get_public_ip_addr_ver4',
    'get_public_ip_addr_ver6',
]