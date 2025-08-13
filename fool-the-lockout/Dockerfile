# References base image by SHA to avoid drift. This is Python 3.12. You will
# probably want to update the hash when working on a new challenge.

## --- Challenge base --- ##
FROM python@sha256:2fba8e70a87bcc9f6edd20dda0a1d4adb32046d2acbca7361bc61da5a106a914 AS base

# Create challenge dir for metadata.json and other file artifacts
RUN mkdir /challenge && chmod 700 /challenge
COPY config-builder.py creds-dump.txt app/app.py /challenge/

# Bring in cmgr args
ARG FLAG

# Generate configs & artifacts for challenge
WORKDIR /challenge
RUN python3 config-builder.py
RUN tar czvf /challenge/artifacts.tar.gz creds-dump.txt app.py

## --- App --- ##
FROM base AS challenge

# Return to root
WORKDIR /

# Copy app & set working directory
COPY ./app /app/ 
WORKDIR /app

# Install python requirements
RUN pip install -r requirements.txt

# Expose port (note CMGR reads the 'publish' comment)
EXPOSE 8000
# PUBLISH 8000 AS app

# Start flask app 
CMD ["python3", "app.py"]









