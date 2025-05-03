#!/usr/bin/env python3
"""
Honeypot Configuration Generator

This script generates configuration files for different honeypot services.
"""

import argparse
import os
import random
import string
import ipaddress
import json
from datetime import datetime

def generate_random_password(length=12):
    """Generate a random password."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_-+=<>?"
    return ''.join(random.choice(chars) for _ in range(length))

def generate_random_hostname():
    """Generate a random hostname."""
    prefixes = ["srv", "web", "db", "app", "mail", "file", "auth", "proxy", "dev", "test", "prod"]
    suffixes = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
    return random.choice(prefixes) + random.choice(suffixes)

def generate_cowrie_config(output_dir):
    """Generate Cowrie SSH honeypot configuration."""
    print(f"[{datetime.now()}] Generating Cowrie SSH honeypot configuration...")
    
    # Generate configuration
    config = f"""# Cowrie SSH honeypot configuration
# Generated on {datetime.now()}

[honeypot]
hostname = {generate_random_hostname()}
log_path = var/log/cowrie
download_path = downloads
share_path = share
state_path = var/lib/cowrie
etc_path = etc
contents_path = honeyfs
txtcmds_path = txtcmds
ttylog = true
ttylog_path = var/lib/cowrie/tty
interactive_timeout = 180
authentication_timeout = 120
backend = shell
timezone = UTC

# Fake users and passwords
userdb = etc/userdb.txt

[shell]
filesystem = share/cowrie/fs.pickle
processes = share/cowrie/cmdoutput.json
arch = linux-x64-lsb
kernel_version = 4.9.0-7-amd64
kernel_build_string = #1 SMP Debian 4.9.110-3+deb9u2 (2018-08-13)
hardware_platform = x86_64
operating_system = GNU/Linux

[ssh]
enabled = true
version = SSH-2.0-OpenSSH_7.9p1 Debian-10
listen_endpoints = tcp:2222:interface=0.0.0.0
sftp_enabled = true
forwarding = true
forward_redirect = false

[telnet]
enabled = false

[output_elasticsearch]
enabled = true
host = elasticsearch
port = 9200
index = cowrie
# ES 7.x compatibility
index_type = _doc

[output_jsonlog]
enabled = true
logfile = var/log/cowrie/cowrie.json
epoch_timestamp = false
"""
    
    # Generate userdb.txt
    userdb = """root:x:*
admin:x:password123,123456,admin123
user:x:password,user123
oracle:x:oracle,oracle123
postgres:x:postgres,postgres123
mysql:x:mysql,mysql123
ubuntu:x:ubuntu,ubuntu123
debian:x:debian,debian123
centos:x:centos,centos123
fedora:x:fedora,fedora123
pi:x:raspberry,raspberry123
test:x:test,test123
guest:x:guest,guest123
ftpuser:x:ftpuser,ftpuser123
jenkins:x:jenkins,jenkins123
tomcat:x:tomcat,tomcat123
webmaster:x:webmaster,webmaster123
administrator:x:administrator,administrator123
"""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Write configuration files
    with open(os.path.join(output_dir, "cowrie.cfg"), "w") as f:
        f.write(config)
    
    with open(os.path.join(output_dir, "userdb.txt"), "w") as f:
        f.write(userdb)
    
    print(f"[{datetime.now()}] Cowrie SSH honeypot configuration generated in {output_dir}")

def generate_samba_config(output_dir):
    """Generate Samba SMB honeypot configuration."""
    print(f"[{datetime.now()}] Generating Samba SMB honeypot configuration...")
    
    # Generate configuration
    config = f"""# Samba configuration for honeypot
# Generated on {datetime.now()}

[global]
   workgroup = WORKGROUP
   server string = File Server
   server role = standalone server
   log file = /opt/honeypot/logs/samba.log
   max log size = 50
   dns proxy = no
   path = /opt/honeypot/shares
   
   # Security settings
   security = user
   encrypt passwords = true
   passdb backend = tdbsam
   
   # Disable printing
   load printers = no
   printing = bsd
   printcap name = /dev/null
   disable spoolss = yes
   
   # Logging
   log level = 2
   
   # Network settings
   socket options = TCP_NODELAY IPTOS_LOWDELAY SO_RCVBUF=65536 SO_SNDBUF=65536
   
   # Disable NetBIOS
   disable netbios = yes
   
   # Use SMB1 protocol (older, less secure version for honeypot)
   server min protocol = NT1
   server max protocol = NT1

[public]
   comment = Public Shares
   path = /opt/honeypot/shares/public
   browseable = yes
   writable = yes
   guest ok = yes
   read only = no
   create mask = 0777
   directory mask = 0777

[private]
   comment = Private Shares
   path = /opt/honeypot/shares/private
   browseable = yes
   writable = yes
   guest ok = no
   read only = no
   valid users = honeypot
   create mask = 0770
   directory mask = 0770
"""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Write configuration file
    with open(os.path.join(output_dir, "smb.conf"), "w") as f:
        f.write(config)
    
    print(f"[{datetime.now()}] Samba SMB honeypot configuration generated in {output_dir}")

def generate_ftp_config(output_dir):
    """Generate FTP honeypot configuration."""
    print(f"[{datetime.now()}] Generating FTP honeypot configuration...")
    
    # Generate configuration
    config = f"""# vsftpd configuration for honeypot
# Generated on {datetime.now()}

# Run in the foreground to keep the container running
background=NO

# Allow anonymous FTP
anonymous_enable=YES

# Allow local users to log in
local_enable=YES

# Enable write access for local users
write_enable=YES

# Default umask for local users
local_umask=022

# Enable logging
xferlog_enable=YES
xferlog_file=/var/log/vsftpd/xferlog
xferlog_std_format=YES

# Enable verbose logging
log_ftp_protocol=YES
syslog_enable=NO

# Restrict users to their home directories
chroot_local_user=YES
allow_writeable_chroot=YES

# Set the name of the PAM service
pam_service_name=vsftpd

# Listen on IPv4 only
listen=YES
listen_ipv6=NO

# Set the port range for passive mode
pasv_min_port=30000
pasv_max_port=30100

# Set the banner
ftpd_banner=Welcome to FTP Server

# Set the root directory for anonymous users
anon_root=/opt/honeypot/ftp/pub

# Allow anonymous users to upload files
anon_upload_enable=YES
anon_mkdir_write_enable=YES

# Set the maximum rate for anonymous users (in bytes per second)
anon_max_rate=30000

# Set the maximum rate for local users (in bytes per second)
local_max_rate=50000

# Enable ASCII mangling
ascii_upload_enable=YES
ascii_download_enable=YES

# Enable logging of uploads and downloads
dual_log_enable=YES

# Set the maximum number of clients
max_clients=10

# Set the maximum number of connections per IP
max_per_ip=5

# Set the idle timeout (in seconds)
idle_session_timeout=600

# Set the data connection timeout (in seconds)
data_connection_timeout=120
"""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Write configuration file
    with open(os.path.join(output_dir, "vsftpd.conf"), "w") as f:
        f.write(config)
    
    print(f"[{datetime.now()}] FTP honeypot configuration generated in {output_dir}")

def generate_http_config(output_dir):
    """Generate HTTP honeypot configuration."""
    print(f"[{datetime.now()}] Generating HTTP honeypot configuration...")
    
    # Generate configuration
    config = {
        "server": {
            "address": ":8080",
            "admin_api_address": ":8081",
            "log_file_path": "/root/logs/honeypot.log"
        },
        "elasticsearch": {
            "url": "http://elasticsearch:9200",
            "index": "honeypot-logs"
        },
        "honeypot": {
            "hostname": generate_random_hostname(),
            "server_banner": "Microsoft-IIS/8.5",
            "content_type": "text/html",
            "response_body": "<html><body><h1>It works!</h1></body></html>"
        }
    }
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Write configuration file
    with open(os.path.join(output_dir, "http_config.json"), "w") as f:
        json.dump(config, f, indent=4)
    
    print(f"[{datetime.now()}] HTTP honeypot configuration generated in {output_dir}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Honeypot Configuration Generator")
    parser.add_argument("--output", default="./generated_configs", help="Output directory for configuration files (default: ./generated_configs)")
    parser.add_argument("--type", choices=["ssh", "smb", "ftp", "http", "all"], default="all", help="Type of honeypot configuration to generate (default: all)")
    
    args = parser.parse_args()
    
    print(f"[{datetime.now()}] Starting Honeypot Configuration Generator...")
    
    if args.type == "ssh" or args.type == "all":
        generate_cowrie_config(os.path.join(args.output, "ssh"))
    
    if args.type == "smb" or args.type == "all":
        generate_samba_config(os.path.join(args.output, "smb"))
    
    if args.type == "ftp" or args.type == "all":
        generate_ftp_config(os.path.join(args.output, "ftp"))
    
    if args.type == "http" or args.type == "all":
        generate_http_config(os.path.join(args.output, "http"))
    
    print(f"[{datetime.now()}] Configuration generation completed.")

if __name__ == "__main__":
    main()
