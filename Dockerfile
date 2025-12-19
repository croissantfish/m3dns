FROM python:3.12-alpine
RUN --mount=type=cache,target=/root/.cache/pip <<EOF
sed -i 's/dl-cdn.alpinelinux.org/mirrors.bfsu.edu.cn/g' /etc/apk/repositories
pip config set global.index-url https://mirrors.bfsu.edu.cn/pypi/web/simple
pip install flask waitress Flask-APScheduler requests aliyun-python-sdk-core-v3 aliyun-python-sdk-domain aliyun-python-sdk-alidns
pip cache purge
EOF
ADD m3dns /ddns/m3dns
ADD ddns.py /ddns/ddns.py
WORKDIR /ddns
ENTRYPOINT ["waitress-serve", "ddns:app"]
