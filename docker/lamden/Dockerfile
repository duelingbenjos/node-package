FROM python:3.6.9

ARG LAMDEN_TAG
ARG CONTRACTING_TAG
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y libhdf5-dev
RUN pip install packaging

workdir /
RUN git clone https://github.com/Lamden/contracting && cd contracting && git checkout tags/${CONTRACTING_TAG} && python setup.py install && cd ..
RUN git clone https://github.com/Lamden/lamden.git && cd lamden && git checkout tags/${LAMDEN_TAG} && pip install aiohttp==3.8.1 && python setup.py install && cd ..
