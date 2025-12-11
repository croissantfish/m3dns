from distutils.core import setup

setup(
    name='m3dns',
    version='1.0.0',
    description='Multiple Devices Dynamic DNS(`m3dns`) is a python package to updating nameservers for multiple devices'
                ' in a subnet, especially for a IPv6 subnet with a prefix shorter than 64.',
    author='BreakVoid',
    author_email='fishtara@outlook.com',
    url='https://github.com/BreakVoid/m3dns',
    packages=['m3dns'],
    requires=[
        'requests',
        'flask',
        'waitress',
        'Flask-APScheduler',
        # Aliyun API requirements
        'aliyun-python-sdk-core-v3',
        'aliyun-python-sdk-domain',
        'aliyun-python-sdk-alidns',
    ]
)
