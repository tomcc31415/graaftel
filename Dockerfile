FROM fedora:latest
MAINTAINER Matthew Farrellee <matt@redhat.com>

ADD requirements.txt /

RUN dnf install -y gcc redhat-rpm-config python3 python3-devel libffi-devel openssl-devel cyrus-sasl-plain && \
    pip3 install -r /requirements.txt && \
    dnf -y remove gcc redhat-rpm-config python3-devel libffi-devel openssl-devel && \
    dnf clean all

ADD app.py /

ENTRYPOINT ["/bin/python3", "/app.py", "--address"]

