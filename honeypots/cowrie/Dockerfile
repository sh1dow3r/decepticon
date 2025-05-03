# Use Python 3.10 as base image
FROM python:3.10-slim-bullseye

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    libssl-dev \
    libffi-dev \
    build-essential \
    libsnappy-dev \
    authbind \
    virtualenv \
    python3-virtualenv \
    python3-setuptools \
    python3-wheel \
    net-tools \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Create cowrie user
RUN useradd -ms /bin/bash cowrie

# Set working directory
WORKDIR /home/cowrie

# Clone Cowrie repository
RUN git clone https://github.com/cowrie/cowrie.git

# Change directory ownership
RUN chown -R cowrie:cowrie /home/cowrie/cowrie

# Create necessary directories
RUN mkdir -p /home/cowrie/cowrie/var/run /home/cowrie/cowrie/var/log/cowrie /home/cowrie/cowrie/downloads /home/cowrie/cowrie/share/cowrie
RUN chown -R cowrie:cowrie /home/cowrie/cowrie/var /home/cowrie/cowrie/downloads /home/cowrie/cowrie/share

# Switch to cowrie user
USER cowrie

# Set working directory to cowrie
WORKDIR /home/cowrie/cowrie

# Create and activate virtual environment
RUN python3 -m venv cowrie-env && \
    . cowrie-env/bin/activate && \
    pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install --upgrade wheel && \
    # Install twisted first (the main dependency)
    pip install twisted && \
    # Install other dependencies without strict version requirements
    pip install bcrypt cryptography hyperlink service_identity tftpy treq

# Copy configuration files
COPY --chown=cowrie:cowrie cowrie.cfg etc/cowrie.cfg
COPY --chown=cowrie:cowrie userdb.txt etc/userdb.txt
COPY --chown=cowrie:cowrie start.sh ./start.sh

# Make startup script executable
RUN chmod +x start.sh

# Create a simple test file to verify volumes are working
RUN echo "Honeypot test file" > /home/cowrie/cowrie/share/test.txt

# Create necessary directories
RUN mkdir -p var/run var/log/cowrie downloads

# Expose SSH port
EXPOSE 2222

# Start Cowrie with the startup script
CMD ["./start.sh"]
