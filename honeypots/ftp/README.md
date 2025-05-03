# FTP Honeypot (vsftpd)

This directory contains the configuration for the FTP honeypot based on vsftpd (Very Secure FTP Daemon).

## Overview

The FTP honeypot simulates an FTP server with anonymous access and a user account. It's designed to attract and log attempts to access files via the FTP protocol.

## Configuration

The honeypot is configured using the following files:

- `Dockerfile`: Builds the vsftpd container with all necessary dependencies
- `vsftpd.conf`: Main configuration file for vsftpd

## Access

The honeypot allows two types of access:

1. **Anonymous Access**: Available to anyone without authentication
   - Username: `anonymous`
   - Password: any (or empty)
   - Root directory: `/opt/honeypot/ftp/pub`

2. **User Access**: Requires authentication
   - Username: `ftpuser`
   - Password: `Password123`
   - Home directory: `/opt/honeypot/ftp`

## Files

The honeypot contains the following sample files:
- `/opt/honeypot/ftp/pub/sample.txt`
- `/opt/honeypot/ftp/pub/README.txt`

## Logging

All FTP interaction is logged to:
- vsftpd logs in `/var/log/vsftpd/xferlog`
- Detailed logs with FTP commands in system logs

## Customization

To modify the FTP server configuration, edit the `vsftpd.conf` file.

To add more users or modify existing ones, edit the Dockerfile and add more `useradd` and `echo` commands for passwords.
