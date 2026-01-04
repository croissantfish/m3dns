import multiprocessing as mp
import subprocess
import time
from typing import Optional
from urllib.request import urlopen
import netaddr


def ip_sb_v4(result_queue: Optional[mp.Queue] = None) -> Optional[str]:
    myip = str(urlopen('https://api-ipv4.ip.sb/ip').read(), encoding='utf-8')
    if result_queue is not None:
        result_queue.put(myip)
    return myip

def ip_sb_v6(result_queue: Optional[mp.Queue] = None) -> Optional[str]:
    myip = str(urlopen('https://api-ipv6.ip.sb/ip').read(), encoding='utf-8')
    try:
        myip = netaddr.IPAddress(myip).format(dialect=netaddr.ipv6_verbose)
        if result_queue is not None:
            result_queue.put(myip)
        return myip
    except:
        pass

def ipify_v4(result_queue: Optional[mp.Queue] = None) -> Optional[str]:
    myip = str(urlopen('https://api.ipify.org').read(), encoding='utf-8')
    if result_queue is not None:
        result_queue.put(myip)
    return myip

def ipify_v6(result_queue: Optional[mp.Queue] = None) -> Optional[str]:
    myip = str(urlopen('https://api6.ipify.org').read(), encoding='utf-8')
    try:
        myip = netaddr.IPAddress(myip).format(dialect=netaddr.ipv6_verbose)
        if result_queue is not None:
            result_queue.put(myip)
        return myip
    except:
        pass

def icanhazip_v4(result_queue: Optional[mp.Queue] = None) -> Optional[str]:
    myip = str(urlopen('https://icanhazip.com').read(), encoding='utf-8')
    if result_queue is not None:
        result_queue.put(myip)
    return myip

def icanhazip_v6(result_queue: Optional[mp.Queue] = None) -> Optional[str]:
    myip = str(urlopen('https://ipv6.icanhazip.com').read(), encoding='utf-8')
    try:
        myip = netaddr.IPAddress(myip).format(dialect=netaddr.ipv6_verbose)
        if result_queue is not None:
            result_queue.put(myip)
        return myip
    except:
        pass

def ifconfig_co_v4(result_queue: Optional[mp.Queue] = None) -> Optional[str]:
    myip = ''
    try:
        subproc = subprocess.run(['curl', '-4', 'https://ifconfig.co'], timeout=5, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        myip = str(subproc.stdout, encoding='utf-8')
    except subprocess.TimeoutExpired:
        pass
    if result_queue is not None:
        result_queue.put(myip)
    return myip

def ifconfig_co_v6(result_queue: Optional[mp.Queue] = None) -> Optional[str]:
    myip = ''
    try:
        subproc = subprocess.run(['curl', '-6', 'https://ifconfig.co'], timeout=5, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        myip = str(subproc.stdout, encoding='utf-8')
        myip = netaddr.IPAddress(myip).format(dialect=netaddr.ipv6_verbose)
        if result_queue is not None:
            result_queue.put(myip)
        return myip
    except:
        pass

API_V4 = [ip_sb_v4, ipify_v4, icanhazip_v4, ifconfig_co_v4]
API_V6 = [ip_sb_v6, ipify_v6, icanhazip_v6, ifconfig_co_v6]

def get_public_ip_addr_ver4() -> str:
    ip2ret = ''
    shared_queue = mp.Queue()
    processes = []
    for api in API_V4:
        p = mp.Process(target=api, args=(shared_queue,))
        p.start()
        processes.append(p)
    processes[0].join(timeout=5)
    if not shared_queue.empty():
        ip2ret = shared_queue.get()
    for p in processes:
        p.terminate()
    return ip2ret

def get_public_ip_addr_ver6() -> str:
    ip2ret = ''
    shared_queue = mp.Queue()
    processes = []
    for api in API_V6:
        p = mp.Process(target=api, args=(shared_queue,))
        p.start()
        processes.append(p)
    while shared_queue.empty():
        time.sleep(0.1)
    if not shared_queue.empty():
        ip2ret = shared_queue.get()
    for p in processes:
        p.terminate()
    return ip2ret


__all__ = [
    'get_public_ip_addr_ver4',
    'get_public_ip_addr_ver6',
]