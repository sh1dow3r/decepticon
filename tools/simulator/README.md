# Honeypot Activity Simulator

This tool simulates various types of attacks on the honeypot system for testing purposes.

## Overview

The Honeypot Activity Simulator sends HTTP requests to the honeypot services with different attack patterns:
- SQL Injection
- Cross-Site Scripting (XSS)
- Command Injection
- Path Traversal

It uses random IP addresses and user agents to simulate different attackers.

## Requirements

- Python 3.6+
- `requests` library

Install the required library:

```bash
pip install requests
```

## Usage

```bash
python simulator.py [--host HOST] [--port PORT] [--count COUNT] [--type {sql,xss,cmd,path,random}]
```

### Options

- `--host`: Honeypot host (default: localhost)
- `--port`: Honeypot port (default: 8080)
- `--count`: Number of random attacks to simulate (default: 10)
- `--type`: Type of attack to simulate (default: random)
  - `sql`: SQL Injection
  - `xss`: Cross-Site Scripting
  - `cmd`: Command Injection
  - `path`: Path Traversal
  - `random`: Random mix of all attack types

### Examples

Simulate 10 random attacks:

```bash
python simulator.py
```

Simulate SQL injection attacks:

```bash
python simulator.py --type sql
```

Simulate 20 random attacks on a specific host and port:

```bash
python simulator.py --host 192.168.1.100 --port 8080 --count 20
```

## Notes

- This tool is for testing purposes only
- It should only be used against your own honeypot system
- The tool does not perform actual exploits, it only sends requests with attack patterns
