FROM centos
MAINTAINER Matthew Farrellee <matt@redhat.com>

RUN yum install -y epel-release && \
    yum install -y python-flask python-qpid-proton && \
    yum clean all

ADD app.py /

ENTRYPOINT ["/bin/python", "/app.py"]

