import argparse

from ..service_providers import AVAILABLE_PROVIDERS


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='A script to add name resolution to service_providers via service_providers-sdk.',
    )
    parser.add_argument(
        '-p', '--provider', type=str,
        default='aliyun',
        help=f'the name of service_provider, available providers: {",".join(AVAILABLE_PROVIDERS.keys())}',
    )
    parser.add_argument(
        '-4', '--ipv4', action='store_true',
        help='adding ipv4 address to name resolutions.',
    )
    parser.add_argument(
        '-6', '--ipv6', action='store_true',
        help='adding ipv6 address to name resolutions.',
    )
    parser.add_argument(
        '-d', '--domain',
        type=str,
        required=True,
        help='The domain to add resolutions.'
    )
    parser.add_argument(
        '-t', '--token_file',
        type=str,
        required=True,
        help='The path to the file of service_providers access token. '
             'The file should be directly downloaded from service_providers.',
    )
    parser.add_argument(
        '-rl', '--rr_list_file',
        type=str,
        required=True,
        help='The path to the names and corresponding MAC addresses for adding name resolutions of subdomains.\n'
             'It had better have @ and * records.\n'
             'The corresponding MAC addresses are used to derive EUI64 addresses when setting resolutions for ipv6,\n'
             'and they are ignored when setting resolutions for ipv4.'
    )
    return parser


def check_arguments(args):
    assert args.ipv4 or args.ipv6, '--ipv4 and --ipv6 should be set at least one.'
    assert args.provider in AVAILABLE_PROVIDERS.keys(), \
        f'Error: --provider should be one of {AVAILABLE_PROVIDERS.keys()}'
