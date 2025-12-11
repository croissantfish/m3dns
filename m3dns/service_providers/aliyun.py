import json
import logging
from typing import Tuple, Union, TextIO

from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DeleteSubDomainRecordsRequest import DeleteSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkcore.client import AcsClient

from .base import BaseDdnsService
from ..utils.utils import get_record_type


def load_access_token(path: Union[str, TextIO]) -> Tuple[str, str]:
    if isinstance(path, str):
        with open(path, 'r') as f:
            second_line = f.readlines()[1].strip()
    else:
        second_line = path.readlines()[1].strip()
    key_id, secret = second_line.split(',')[2:]
    return key_id, secret


class Aliyun(BaseDdnsService):
    def __init__(
            self,
            domain: str,
            token_file: Union[str, TextIO],
    ):
        super().__init__(domain, token_file)
        self.access_key_id, self.access_secret = load_access_token(self._token_file)

    @property
    def _client(self):
        return AcsClient(self.access_key_id, self.access_secret, 'cn-hangzhou')

    def get_existed_records(self, subname: str, ver4: bool = True):
        request = DescribeSubDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(self._domain)
        request.set_SubDomain(subname + '.' + self._domain)
        request.set_Type(get_record_type(ver4))
        response = self._client.do_action_with_exception(request)
        return json.loads(response)

    def _update(self, record_id, rr, ip, ver4: bool = True):
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')
        request.set_RecordId(record_id)
        request.set_RR(rr)
        request.set_Type(get_record_type(ver4))
        request.set_Value(ip)
        self._client.do_action_with_exception(request)

    def _add(self, rr, ip, ver4: bool = True):
        request = AddDomainRecordRequest()
        request.set_accept_format('json')
        request.set_DomainName(self._domain)
        request.set_RR(rr)
        request.set_Type(get_record_type(ver4))
        request.set_Value(ip)
        self._client.do_action_with_exception(request)

    def _delete(self, rr, ver4: bool = True):
        request = DeleteSubDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(self._domain)
        request.set_RR(rr)
        request.set_Type(get_record_type(ver4))
        self._client.do_action_with_exception(request)

    def update_name_records(self, rr: str, ip: str, ver4: bool = True):
        logging.info(
            'Updating the domain resolution record, DOMAIN:%s.%s, new ip:(%s), type: %s',
            rr, self._domain, ip, get_record_type(ver4),
        )
        domain_list = self.get_existed_records(rr, ver4)
        if domain_list['TotalCount'] == 0:
            logging.info(f'No existed records of {rr}.{self._domain}, adding a new record.')
            self._add(rr, ip, ver4)
            logging.info('Operation succeeded.')
        elif domain_list['TotalCount'] == 1:
            logging.info(f'Detected one existed record of {rr}.{self._domain}')
            if domain_list['DomainRecords']['Record'][0]['Value'].strip() != ip.strip():
                logging.info(
                    f'Old value: {domain_list["DomainRecords"]["Record"][0]["Value"].strip()}, '
                    f'new value: {ip.strip()}, updating the record.'
                )
                self._update(domain_list['DomainRecords']['Record'][0]['RecordId'], rr, ip, ver4)
                logging.info('Operation succeeded.')
            else:
                logging.info(
                    f'Old value({domain_list["DomainRecords"]["Record"][0]["Value"].strip()}) '
                    f'is equal to the new ip, keep the record.'
                )
        elif domain_list['TotalCount'] > 1:
            logging.info(f'Detected more records of {rr}.{self._domain}, deleting the old records.')
            self._delete(rr, ver4)
            logging.info(f'Old records deleted, adding a new record.')
            self._add(rr, ip, ver4)
            logging.info('Operation succeeded.')
