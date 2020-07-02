FROM python:3.7-slim-stretch

LABEL maintainer="Nuno Diogo da Silva <diogosilva.nuno@gmail.com>"

ENV PATH=/root/.local/bin:$PATH

RUN pip install pipx && \
    pipx install pylint && \
    pipx install black && \
    pipx install poetry

# Install git, process tools
RUN apt-get update && apt-get -y install git procps

# Clean up
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Set workspace space
RUN mkdir /workspace
WORKDIR /workspace

COPY *.toml /workspace/
COPY poetry.lock /workspace/

# Install project dependencies
RUN poetry install
