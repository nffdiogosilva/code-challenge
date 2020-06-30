FROM nffdiogosilva/pytools:3.7

LABEL mantainer="Nuno Diogo da Silva"

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

# Install project dependencies
RUN poetry install
