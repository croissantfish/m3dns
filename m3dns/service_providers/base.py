from abc import ABC, abstractmethod
from typing import TextIO, Union


class BaseDdnsService(ABC):
    def __init__(
            self,
            domain: str,
            token_file: Union[str, TextIO],
    ):
        self._domain = domain
        self._token_file = token_file

    @abstractmethod
    def get_existed_records(self, subname: str, ver4: bool = True) -> dict:
        pass

    @abstractmethod
    def update_name_records(self, rr: str, ip: str, ver4: bool = True) -> None:
        pass
