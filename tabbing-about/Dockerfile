# LAUNCH ssh_host

FROM ubuntu@sha256:626ffe58f6e7566e00254b638eb7e0f3b11d4da9675088f4781a50ae288f3322 AS builder_base

# Install challenge dependencies within the image
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3

# Create challenge dir for metadata.json and other file artifacts
RUN mkdir /challenge && chmod 700 /challenge
COPY bin/config-builder.py /challenge/

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

COPY bin/config-sshhost.py bin/name_scrambler.py /challenge/
COPY bin/start.sh /opt/
COPY data/profile /home/ctf-player/.profile
COPY data/bashrc /home/ctf-player/.bashrc
COPY data/instructions.txt /home/ctf-player/

COPY --from=builder /challenge/flag_1of2.txt /home/ctf-player/
COPY --from=builder /challenge/flag_2of2.txt /home/ctf-player/dir2/

# Scramble directory & file names
RUN python3 /challenge/name_scrambler.py

FROM ssh_host_base AS ssh_host
COPY --from=builder /challenge/password.txt /tmp/

# Configure sshhost and wipe /challenge/ folder
RUN python3 /challenge/config-sshhost.py && \
    rm -rf /challenge/

EXPOSE 5555
# PUBLISH 5555 AS ssh
CMD ["/opt/start.sh"]
