# Decepticon: Advanced Deception-as-a-Service Platform

Decepticon is a comprehensive cyber deception platform that simulates multiple services to detect and analyze attack patterns. This project provides a modular approach to honeypot deployment using Docker Compose, with centralized logging and visualization through Elasticsearch and Kibana.

## Features

- **HTTP Honeypot**: Custom Go implementation that detects and responds to common web attacks
- **SSH Honeypot**: Based on Cowrie, simulates a vulnerable SSH server
- **SMB Honeypot**: Samba-based honeypot with public and private shares
- **FTP Honeypot**: vsftpd-based honeypot with anonymous access
- **Centralized Logging**: All honeypot activity is logged to Elasticsearch
- **Dashboard**: Kibana dashboard for visualizing attack patterns and statistics
- **Admin API**: REST API for monitoring honeypot activity
- **Web Console**: Web-based management console for monitoring the honeypot system
- **Utility Tools**: Tools for simulating attacks, generating configurations, and analyzing logs

## Architecture

The system consists of the following components:

1. **Main Go Application**: Handles HTTP requests and provides the admin API
2. **Honeypot Services**: Independent containers for SSH, SMB, and FTP honeypots
3. **Elasticsearch**: Stores all honeypot logs and provides search capabilities
4. **Kibana**: Provides visualization and dashboard for honeypot activity
5. **Web Console**: Provides a simple web interface for monitoring the system

## Prerequisites

- Docker and Docker Compose
- At least 4GB of RAM available for the containers
- Port 8080, 8081, 8082, 5601, 2222, 445, and 21 available on the host

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sh1dow3r/decepticon.git
   cd decepticon
   ```

2. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

## Usage

### Accessing the Services

- **HTTP Honeypot**: `http://localhost:8080`
- **Admin API**: `http://localhost:8081`
- **Web Console**: `http://localhost:8082`
- **Kibana Dashboard**: `http://localhost:5601`
- **SSH Honeypot**: `ssh -p 2222 root@localhost`
- **SMB Honeypot**: `smb://localhost`
- **FTP Honeypot**: `ftp://localhost`

### Admin API Endpoints

- **GET /api/stats**: Returns statistics about honeypot activity
- **GET /api/health**: Returns the health status of the honeypot service

Example:
```bash
curl http://localhost:8081/api/stats
```

### Viewing Logs

All honeypot activity is logged to Elasticsearch and can be viewed in Kibana. The following index patterns are available:

- **honeypot-logs**: Logs from the HTTP honeypot
- **cowrie**: Logs from the SSH honeypot

## Tools

The project includes several utility tools to help with testing, configuration, and analysis:

### Honeypot Activity Simulator

Located in the `tools/simulator` directory, this tool simulates various types of attacks on the honeypot system for testing purposes.

```bash
python tools/simulator/simulator.py --host localhost --port 8080 --count 20
```

### Honeypot Configuration Generator

Located in the `tools/generator` directory, this tool generates configuration files for different honeypot services.

```bash
python tools/generator/generator.py --output ./configs
```

### Honeypot Log Analyzer

Located in the `tools/analyzer` directory, this tool analyzes honeypot logs to extract useful information and generate reports.

```bash
python tools/analyzer/analyzer.py /path/to/honeypot.log --csv report.csv --charts ./charts
```

For more information about these tools, see the [Tools README](tools/README.md).

## Customization

### Adding New Honeypots

To add a new honeypot service:

1. Create a new directory in the `honeypots` directory
2. Add a Dockerfile and configuration files
3. Add the service to the `docker-compose.yml` file

### Modifying Existing Honeypots

Each honeypot can be customized by modifying its configuration files:

- **SSH Honeypot**: `honeypots/cowrie/cowrie.cfg`
- **SMB Honeypot**: `honeypots/samba/smb.conf`
- **FTP Honeypot**: `honeypots/ftp/vsftpd.conf`

## Troubleshooting

### Common Issues

1. **Elasticsearch fails to start**: Increase the memory available to Docker
2. **Kibana can't connect to Elasticsearch**: Check that Elasticsearch is running and accessible
3. **Honeypot services not accessible**: Check that the ports are not being used by other services

## Security Considerations

**IMPORTANT**: This system is designed for research and educational purposes only. It intentionally exposes vulnerable services and should never be deployed in a production environment or exposed directly to the internet.

Recommended deployment options:
- Use in an isolated network environment
- Deploy behind a firewall with strict access controls
- Use for research and educational purposes only

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Cowrie](https://github.com/cowrie/cowrie) for the SSH honeypot
- [Elastic](https://www.elastic.co/) for Elasticsearch and Kibana
