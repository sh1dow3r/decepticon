# Honeypot Configuration Generator

This tool generates configuration files for different honeypot services.

## Overview

The Honeypot Configuration Generator creates configuration files for:
- SSH Honeypot (Cowrie)
- SMB Honeypot (Samba)
- FTP Honeypot (vsftpd)
- HTTP Honeypot (Go application)

It generates random values for hostnames, passwords, and other settings to create unique honeypot configurations.

## Requirements

- Python 3.6+

## Usage

```bash
python generator.py [--output OUTPUT] [--type {ssh,smb,ftp,http,all}]
```

### Options

- `--output`: Output directory for configuration files (default: ./generated_configs)
- `--type`: Type of honeypot configuration to generate (default: all)
  - `ssh`: SSH Honeypot (Cowrie)
  - `smb`: SMB Honeypot (Samba)
  - `ftp`: FTP Honeypot (vsftpd)
  - `http`: HTTP Honeypot (Go application)
  - `all`: All honeypot types

### Examples

Generate all honeypot configurations:

```bash
python generator.py
```

Generate SSH honeypot configuration:

```bash
python generator.py --type ssh
```

Generate all configurations in a specific directory:

```bash
python generator.py --output /path/to/configs
```

## Output

The tool creates a directory structure with configuration files for each honeypot type:

```
generated_configs/
├── ssh/
│   ├── cowrie.cfg
│   └── userdb.txt
├── smb/
│   └── smb.conf
├── ftp/
│   └── vsftpd.conf
└── http/
    └── http_config.json
```

## Notes

- The generated configurations include random values for hostnames and other settings
- The configurations are compatible with the honeypot services in this project
- You can use these configurations as a starting point and customize them as needed
