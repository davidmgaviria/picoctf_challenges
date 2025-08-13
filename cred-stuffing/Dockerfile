
FROM ubuntu@sha256:626ffe58f6e7566e00254b638eb7e0f3b11d4da9675088f4781a50ae288f3322 AS challenge

# Install challenge dependencies within the image
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3 \
    socat

# Create challenge dir for metadata.json and other file artifacts  
RUN mkdir /challenge && chmod 700 /challenge
COPY config-builder.py creds-dump.txt /challenge/  
COPY bank_app.py /app/       

# Bring in cmgr args
ARG SEED
ARG FLAG

# Generates flag.txt & profile.json in /challenge
RUN python3 /challenge/config-builder.py

# Generate artifacts for challenge
WORKDIR /challenge
RUN tar czvf /challenge/artifacts.tar.gz creds-dump.txt

# Publish app
EXPOSE 5555
#PUBLISH 5555 AS app

# Start challenge
CMD socat TCP-LISTEN:5555,reuseaddr,fork EXEC:"python3 /app/bank_app.py",pty,stderr



 