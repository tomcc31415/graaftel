FROM fedora:latest
MAINTAINER Matthew Farrellee <matt@redhat.com>

ADD requirements.txt /

RUN dnf install -y gcc redhat-rpm-config python2 python-devel libffi-devel openssl-devel cyrus-sasl-plain && \
    pip install -r /requirements.txt && \
    dnf -y remove gcc redhat-rpm-config python-devel libffi-devel openssl-devel && \
    dnf clean all

ADD app.py /

ENTRYPOINT ["/bin/python2", "/app.py", "--address"]

