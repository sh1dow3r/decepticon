# Honeypot Management Console

This directory contains the static files for the Honeypot Management Console, a web-based interface for monitoring the honeypot system.

## Overview

The Honeypot Management Console provides a simple web interface for viewing:
- System status
- Honeypot statistics
- Recent attacks

## Usage

The console is automatically served by the admin API at the root path (`/`). You can access it by navigating to:

```
http://localhost:8081/
```

## Standalone Deployment

You can also deploy the console as a standalone web application using the provided Dockerfile:

```bash
docker build -t honeypot-console .
docker run -p 8082:80 honeypot-console
```

Then access the console at:

```
http://localhost:8082/
```

Note: When deployed standalone, you'll need to configure the API endpoint in the JavaScript code.
