#!/bin/bash
# Startup script for Cowrie SSH honeypot

set -e  # Exit on error
set -x  # Print commands for debugging

echo "Starting Cowrie SSH honeypot setup..."

# Activate virtual environment
source cowrie-env/bin/activate

# Create necessary directories
mkdir -p var/run var/log/cowrie downloads
mkdir -p share/cowrie

# Install dependencies directly
echo "Installing Cowrie dependencies..."
pip install --no-cache-dir bcrypt cryptography hyperlink service_identity tftpy treq twisted

# Initialize the filesystem if it doesn't exist
if [ ! -f "share/cowrie/fs.pickle" ]; then
    echo "Initializing filesystem..."
    bin/fsctl generate
fi

# Check if twisted is installed
if ! pip list | grep -q twisted; then
    echo "Installing twisted..."
    pip install twisted
fi

# Check if the configuration file exists
if [ ! -f "etc/cowrie.cfg" ]; then
    echo "Configuration file not found. Using default..."
    cp etc/cowrie.cfg.dist etc/cowrie.cfg
fi

# Start Cowrie in foreground mode
echo "Starting Cowrie SSH honeypot..."
bin/cowrie start -n
