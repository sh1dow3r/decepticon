# SMB Honeypot (Samba)

This directory contains the configuration for the SMB honeypot based on Samba.

## Overview

The SMB honeypot simulates a Windows file sharing service with public and private shares. It's designed to attract and log attempts to access shared folders and files via the SMB protocol.

## Configuration

The honeypot is configured using the following files:

- `Dockerfile`: Builds the Samba container with all necessary dependencies
- `smb.conf`: Main configuration file for Samba

## Shares

The honeypot exposes two shares:

1. **Public Share**: Available to anyone without authentication
   - Path: `/opt/honeypot/shares/public`
   - Contains a sample file

2. **Private Share**: Requires authentication
   - Path: `/opt/honeypot/shares/private`
   - Contains a "confidential" file
   - Credentials: Username: `honeypot`, Password: `Password123`

## Logging

All SMB interaction is logged to:
- Samba logs in `/opt/honeypot/logs/samba.log`

## Customization

To add more shares or modify existing ones, edit the `smb.conf` file.

To add more users or modify existing ones, edit the Dockerfile and add more `useradd` and `smbpasswd` commands.
