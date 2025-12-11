from typing import Type

from .base import BaseDdnsService
from .aliyun import Aliyun

AVAILABLE_PROVIDERS = {
    'aliyun': Aliyun
}


def get_impl_by_name(name: str) -> Type[BaseDdnsService]:
    return AVAILABLE_PROVIDERS[name]


__all__ = [
    'AVAILABLE_PROVIDERS',
    'get_impl_by_name',
]