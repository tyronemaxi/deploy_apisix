FROM apache/apisix:3.10.0-debian

USER root

RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/* && \
    apt clean

