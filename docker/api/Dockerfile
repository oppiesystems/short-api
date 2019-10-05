FROM nvidia/cuda:9.0-cudnn7-runtime

LABEL version="0.3.0" maintainer="Pat Migliaccio <pat@oppie.io>"

RUN apt-get update -y
RUN apt-get install -y \
  curl \
  git-core \
  python \
  python-pip \
  python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt
RUN python -c 'import nltk; nltk.download("punkt")'

COPY . /app

# Mount Google Cloud Storage models
ARG GCSFUSE_REPO="gcsfuse-stretch"
RUN apt-get install --yes --no-install-recommends \
    ca-certificates \
    curl && \
    echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" \
      | tee /etc/apt/sources.list.d/gcsfuse.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg \
      | apt-key add -
RUN apt-get update
RUN apt-get install --yes gcsfuse && \
    echo 'user_allow_other' > /etc/fuse.conf

# Clean up.
USER root
RUN apt-get remove --yes \
    git-core && \
    apt-get autoremove --yes && \
    apt-get clean

# Reference: https://stackoverflow.com/a/34517230/5199198
ENV PYTHONIOENCODING "UTF-8"

COPY entrypoint.sh /entrypoint.sh
RUN ["chmod", "+x", "/entrypoint.sh" ]
ENTRYPOINT [ "/entrypoint.sh" ]