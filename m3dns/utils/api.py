import multiprocessing as mp
import subprocess
import time
from typing import Optional
import netaddr


def ip_sb_v4(result_queue: Optional[mp.Queue] = None) -> Optional[str]:
    myip = ''
    try:
        subproc = subprocess.run(['curl', '-4', 'https://api-ipv4.ip.sb/ip'], timeout=5, stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL)
        myip = str(subproc.stdout, encoding='utf-8')
    except subprocess.TimeoutExpired:
        pass
    if result_queue is not None:
        result_queue.put(myip)
    return myip

def ip_sb_v6(result_queue: Optional[mp.Queue] = None) -> Optional[str]:
    myip = ''
    try:
        subproc = subprocess.run(['curl', '-6', 'https://api-ipv6.ip.sb/ip'], timeout=5, stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL)
        myip = netaddr.IPAddress(myip).format(dialect=netaddr.ipv6_verbose)
        if result_queue is not None:
            result_queue.put(myip)
        return myip
    except:
        pass
    return myip

def ipify_v4(result_queue: Optional[mp.Queue] = None) -> Optional[str]:
    myip = ''
    try:
        subproc = subprocess.run(['curl', '-4', 'https://api.ipify.org'], timeout=5, stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL)
        myip = str(subproc.stdout, encoding='utf-8')
    except subprocess.TimeoutExpired:
        pass
    if result_queue is not None:
        result_queue.put(myip)
    return myip

def ipify_v6(result_queue: Optional[mp.Queue] = None) -> Optional[str]:
    myip = ''
    try:
        subproc = subprocess.run(['curl', '-6', 'https://api6.ipify.org'], timeout=5, stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL)
        myip = str(subproc.stdout, encoding='utf-8')
        myip = netaddr.IPAddress(myip).format(dialect=netaddr.ipv6_verbose)
        if result_queue is not None:
            result_queue.put(myip)
        return myip
    except:
        pass
    return myip


def icanhazip_v4(result_queue: Optional[mp.Queue] = None) -> Optional[str]:
    myip = ''
    try:
        subproc = subprocess.run(['curl', '-4', 'https://icanhazip.com'], timeout=5, stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL)
        myip = str(subproc.stdout, encoding='utf-8')
    except subprocess.TimeoutExpired:
        pass
    if result_queue is not None:
        result_queue.put(myip)
    return myip

def icanhazip_v6(result_queue: Optional[mp.Queue] = None) -> Optional[str]:
    myip = ''
    try:
        subproc = subprocess.run(['curl', '-6', 'https://ipv6.icanhazip.com'], timeout=5, stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL)
        myip = str(subproc.stdout, encoding='utf-8')
        myip = netaddr.IPAddress(myip).format(dialect=netaddr.ipv6_verbose)
        if result_queue is not None:
            result_queue.put(myip)
        return myip
    except:
        pass
    return myip


def ifconfig_co_v4(result_queue: Optional[mp.Queue] = None) -> Optional[str]:
    myip = ''
    try:
        subproc = subprocess.run(['curl', '-4', 'https://ifconfig.co'], timeout=5, stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL)
        myip = str(subproc.stdout, encoding='utf-8')
    except subprocess.TimeoutExpired:
        pass
    if result_queue is not None:
        result_queue.put(myip)
    return myip

def ifconfig_co_v6(result_queue: Optional[mp.Queue] = None) -> Optional[str]:
    myip = ''
    try:
        subproc = subprocess.run(['curl', '-6', 'https://ifconfig.co'], timeout=5, stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL)
        myip = str(subproc.stdout, encoding='utf-8')
        myip = netaddr.IPAddress(myip).format(dialect=netaddr.ipv6_verbose)
        if result_queue is not None:
            result_queue.put(myip)
        return myip
    except:
        pass
    return myip

API_V4 = [ip_sb_v4, ipify_v4, icanhazip_v4, ifconfig_co_v4]
API_V6 = [ip_sb_v6, ipify_v6, icanhazip_v6, ifconfig_co_v6]

def get_public_ip_addr(vers: int = 4) -> str:
    if vers == 4:
        APIs = API_V4
    else:
        APIs = API_V6
    ip2ret = ''
    shared_queue = mp.Queue()
    processes = []
    for api in APIs:
        p = mp.Process(target=api, args=(shared_queue,))
        p.start()
        processes.append(p)
    while shared_queue.empty():
        time.sleep(0.1)
        if not any(p.is_alive() for p in processes):
            break
    if not shared_queue.empty():
        ip2ret = shared_queue.get()
    for p in processes:
        p.terminate()
    return ip2ret

def get_public_ip_addr_ver4() -> str:
    return get_public_ip_addr(4)

def get_public_ip_addr_ver6() -> str:
    return get_public_ip_addr(6)


__all__ = [
    'get_public_ip_addr_ver4',
    'get_public_ip_addr_ver6',
]