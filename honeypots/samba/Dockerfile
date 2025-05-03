# Use Ubuntu as base image
FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install Samba and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    samba \
    samba-common \
    smbclient \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Create directories
RUN mkdir -p /opt/honeypot/shares/public
RUN mkdir -p /opt/honeypot/shares/private
RUN mkdir -p /opt/honeypot/logs

# Create sample files
RUN echo "This is a sample file" > /opt/honeypot/shares/public/sample.txt
RUN echo "This is a confidential file" > /opt/honeypot/shares/private/confidential.txt

# Create users
RUN useradd -m honeypot
RUN echo 'honeypot:Password123' | chpasswd

# Copy Samba configuration
COPY smb.conf /etc/samba/smb.conf

# Validate Samba configuration
RUN testparm -s /etc/samba/smb.conf

# Add Samba user after configuration is in place
RUN (echo "Password123"; echo "Password123") | smbpasswd -a honeypot -s

# Expose SMB ports
EXPOSE 445

# Start Samba
CMD ["smbd", "--foreground", "--no-process-group", "--debug-stdout"]
