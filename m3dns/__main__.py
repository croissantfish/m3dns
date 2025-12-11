import logging

from m3dns.service_providers import get_impl_by_name
from m3dns.utils import get_public_ip_addr_ver4, get_public_ip_addr_ver6, mac2eui64
from m3dns.utils.args import get_argument_parser, check_arguments
from m3dns.utils.utils import load_rr_mac

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
)


if __name__ == '__main__':
    parser = get_argument_parser()
    args = parser.parse_args()
    check_arguments(args)
    ipv4 = args.ipv4
    ipv6 = args.ipv6
    token_file = args.token_file
    rr_list_file = args.rr_list_file
    domain = args.domain
    provider = args.provider
    service_impl = get_impl_by_name(provider)(domain, token_file)
    logging.info('Starting updating dns records.')
    logging.info('Getting IPv4 address via API.')
    public_ipv4_addr = get_public_ip_addr_ver4().strip() if ipv4 else None
    logging.info('Getting IPv6 prefix via API.')
    public_ipv6_addr = get_public_ip_addr_ver6().strip() if ipv6 else None
    ipv6_prefix = ':'.join(public_ipv6_addr.split(':')[:4]) + '::/64' if ipv6 else None

    for rr, mac in load_rr_mac(rr_list_file):
        if ipv4:
            service_impl.update_name_records(rr, public_ipv4_addr, ver4=True)
        if ipv6:
            persistent_ipv6_addr = mac2eui64(mac, ipv6_prefix)
            service_impl.update_name_records(rr, persistent_ipv6_addr, ver4=False)
    logging.info('All records are processed.')
