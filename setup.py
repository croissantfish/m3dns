from distutils.core import setup

setup(
    name='m3dns',
    version='1.0.2',
    description='Multiple Devices Dynamic DNS(`m3dns`) is a python package to updating nameservers for multiple devices'
                ' in a subnet, especially for a IPv6 subnet with a prefix shorter than 64.',
    author='croissantfish',
    author_email='croissantfish@outlook.com',
    url='https://github.com/croissantfish/m3dns',
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
