
FROM ubuntu@sha256:626ffe58f6e7566e00254b638eb7e0f3b11d4da9675088f4781a50ae288f3322 AS challenge

# Install challenge dependencies within the image
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3 \
    python3-pip \
    socat

# Create challenge dir for metadata.json and other file artifacts  
RUN mkdir /challenge && chmod 700 /challenge
COPY config-builder.py /challenge/ 
COPY ./model /challenge/

# Bring in cmgr args
ARG FLAG

# Generates flag.txt in /challenge
RUN python3 /challenge/config-builder.py

# Copy over chatbot
COPY ./app /app/       
RUN pip install -r /app/requirements.txt

# Publish app
EXPOSE 5555
#PUBLISH 5555 AS app

# Start challenge
CMD socat TCP-LISTEN:5555,reuseaddr,fork EXEC:"python3 /app/chatbot.py",pty,stderr



 
