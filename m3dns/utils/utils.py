from collections import namedtuple
from typing import List


def get_record_type(ver4: bool = True) -> str:
    return 'A' if ver4 else 'AAAA'


NameAndMac = namedtuple(
    'NameAndMac',
    [
        'name',
        'mac',
    ]
)


def load_rr_mac(path: str) -> List[NameAndMac]:
    res = []
    with open(path, 'r') as f:
        for line in f.readlines()[1:]:
            name, mac = line.split(',')
            res.append(NameAndMac(name, mac))
    return res
