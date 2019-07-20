FROM ubuntu:16.04

LABEL version="0.2.0" maintainer="Pat Migliaccio <pat@oppie.io>"

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

# Clean up.
USER root
RUN apt-get remove --yes \
    git-core && \
    apt-get autoremove --yes && \
    apt-get clean

ENTRYPOINT [ "python" ]
CMD [ "main.py" ]