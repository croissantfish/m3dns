import datetime
import logging
import os

from flask import Flask
from flask_apscheduler import APScheduler

from m3dns.service_providers import get_impl_by_name, AVAILABLE_PROVIDERS
from m3dns.utils.utils import load_rr_mac
from m3dns.utils import get_public_ip_addr_ver4, get_public_ip_addr_ver6
from m3dns.utils import mac2eui64

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
)

ENV_IPV4 = True if 'IPV4' in os.environ else False
ENV_IPV6 = True if 'IPV6' in os.environ else False
assert ENV_IPV4 or ENV_IPV6, 'Either IPV4 or IPV6 should be set at least one.'
ENV_TOKEN_FILE = os.environ['TOKEN_FILE'] if 'TOKEN_FILE' in os.environ else None
assert ENV_TOKEN_FILE is not None, 'The environment variable TOKEN_FILE is not set.'
ENV_RM_FILE = os.environ['RM_FILE'] if 'RM_FILE' in os.environ else None
assert ENV_RM_FILE is not None, 'The environment variable RM_FILE is not set.'
ENV_DOMAIN = os.environ['DOMAIN'] if 'DOMAIN' in os.environ else None
assert ENV_DOMAIN is not None, 'The environment variable DOMAIN is not set.'
ENV_PROVIDER = os.environ['PROVIDER'] if 'PROVIDER' in os.environ else None
assert ENV_PROVIDER is not None, 'The environment variable PROVIDER is not set.'
assert ENV_PROVIDER in AVAILABLE_PROVIDERS.keys(), \
        f'The environment variable PROVIDER should be one of {AVAILABLE_PROVIDERS.keys()}'

app = Flask(__name__)
app.config['ipv4'] = ENV_IPV4
app.config['ipv6'] = ENV_IPV6
app.config['token_file'] = ENV_TOKEN_FILE
app.config['rr_list_file'] = ENV_RM_FILE
app.config['domain'] = ENV_DOMAIN
app.config['provider'] = ENV_PROVIDER
scheduler = APScheduler()  # 定时任务调度器
scheduler.init_app(app)
scheduler.start()  # 定时任务开始


@app.route('/')
def index() -> str:
    return 'm3dns service is running.'


@scheduler.task(
    'interval', id='update_ddns_records', seconds=300,
    misfire_grace_time=900, next_run_time=datetime.datetime.now(),
)
@app.route('/healthcheck')
def update_records():
    ipv4 = app.config['ipv4']
    ipv6 = app.config['ipv6']
    token_file = app.config['token_file']
    rr_list_file = app.config['rr_list_file']
    domain = app.config['domain']
    provider = app.config['provider']
    service_impl = get_impl_by_name(provider)(domain, token_file)
    logging.info('Starting updating dns records.')
    logging.info('Getting IPv4 address via API.')
    public_ipv4_addr = get_public_ip_addr_ver4().strip() if ipv4 else None
    if ipv4 and public_ipv4_addr == '':
        logging.info('Cannot get IPv6 address from API.')
        return 'Cannot get IPv4 address from API.', 200
    logging.info('Getting IPv6 prefix via API.')
    public_ipv6_addr = get_public_ip_addr_ver6().strip() if ipv6 else None
    if ipv6 and public_ipv6_addr == '':
        logging.info('Cannot get IPv6 address from API.')
        return 'Cannot get IPv6 address from API.', 200
    ipv6_prefix = ':'.join(public_ipv6_addr.split(':')[:4]) + '::/64' if ipv6 else None

    for rr, mac in load_rr_mac(rr_list_file):
        if ipv4:
            service_impl.update_name_records(rr, public_ipv4_addr, ver4=True)
        if ipv6:
            persistent_ipv6_addr = mac2eui64(mac, ipv6_prefix)
            service_impl.update_name_records(rr, persistent_ipv6_addr, ver4=False)
    logging.info('All records are processed.')
    return 'Good', 200


if __name__ == '__main__':
    app.run()
