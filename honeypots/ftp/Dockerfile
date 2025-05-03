# Use Ubuntu as base image
FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install vsftpd and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    vsftpd \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Create directories
RUN mkdir -p /opt/honeypot/ftp/pub
RUN mkdir -p /var/log/vsftpd
RUN mkdir -p /var/run/vsftpd/empty

# Create sample files
RUN echo "This is a sample file" > /opt/honeypot/ftp/pub/sample.txt
RUN echo "This is a README file" > /opt/honeypot/ftp/pub/README.txt

# Create users
RUN useradd -m ftpuser
RUN echo 'ftpuser:Password123' | chpasswd
RUN usermod -d /opt/honeypot/ftp ftpuser

# Copy vsftpd configuration
COPY vsftpd.conf /etc/vsftpd.conf

# Expose FTP ports
EXPOSE 21

# Start vsftpd
CMD ["vsftpd", "/etc/vsftpd.conf"]
