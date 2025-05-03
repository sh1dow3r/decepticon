# SSH Honeypot (Cowrie)

This directory contains the configuration for the SSH honeypot based on [Cowrie](https://github.com/cowrie/cowrie).

## Overview

Cowrie is a medium to high interaction SSH and Telnet honeypot designed to log brute force attacks and the shell interaction performed by the attacker. In medium interaction mode (shell) it emulates a UNIX system in Python, in high interaction mode (proxy) it functions as an SSH and telnet proxy to observe attacker behavior to another system.

## Configuration

The honeypot is configured using the following files:

- `Dockerfile`: Builds the Cowrie container with all necessary dependencies
- `cowrie.cfg`: Main configuration file for Cowrie
- `userdb.txt`: Contains fake user credentials that attackers can use to "successfully" login
- `start.sh`: Startup script that initializes the environment and starts Cowrie

## Fake Credentials

The honeypot is configured with several fake user accounts that attackers can use to "successfully" login. These credentials are defined in the `userdb.txt` file.

Some example credentials:
- Username: `root`, Password: any (will accept any password)
- Username: `admin`, Password: `password123`, `123456`, or `admin123`
- Username: `user`, Password: `password` or `user123`

## Logging

All SSH interaction is logged to:
- JSON logs in `/home/cowrie/cowrie/var/log/cowrie/cowrie.json`
- Elasticsearch index `cowrie`

## Customization

To add more fake users or modify existing ones, edit the `userdb.txt` file.

To change the SSH server banner or other settings, edit the `cowrie.cfg` file.
