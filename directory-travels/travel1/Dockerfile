# LAUNCH ssh_host

FROM ubuntu@sha256:626ffe58f6e7566e00254b638eb7e0f3b11d4da9675088f4781a50ae288f3322 AS builder_base

# Install challenge dependencies within the image
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3

# Create challenge dir for metadata.json and other file artifacts
RUN mkdir /challenge && chmod 700 /challenge
COPY config-builder.py /challenge/

FROM builder_base as builder
# Bring in cmgr args
ARG SEED
ARG FLAG

RUN python3 /challenge/config-builder.py

#######################
#### Host: sshHost ####
#######################
FROM ubuntu@sha256:626ffe58f6e7566e00254b638eb7e0f3b11d4da9675088f4781a50ae288f3322 AS ssh_host_base

# Install challenge dependencies within the image
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    openssh-server \
    python3 \
    socat

COPY config-sshhost.py /challenge/
COPY start.sh /opt/
COPY profile /home/ctf-player/.profile
COPY instructions.txt /home/ctf-player/
COPY --from=builder /challenge/flag.txt /home/ctf-player/flag/.flag.txt


FROM ssh_host_base AS ssh_host
COPY --from=builder /challenge/password.txt /tmp/

# Configure sshhost and wipe /challenge/ folder
RUN python3 /challenge/config-sshhost.py && \
    rm -rf /challenge/

EXPOSE 5555
# PUBLISH 5555 AS ssh
CMD ["/opt/start.sh"]
