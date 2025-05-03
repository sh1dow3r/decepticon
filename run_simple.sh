#!/bin/bash
# Script to run the simplified version of the honeypot system

# Stop any running containers
echo "Stopping any running containers..."
docker-compose down

# Copy the simplified index.html
echo "Copying simplified web console..."
cp pkg/api/static/index.html.simple pkg/api/static/index.html

# Build and run the simplified version
echo "Building and running the simplified version..."
docker-compose -f docker-compose.simple.yml up --build -d

# Wait for services to start
echo "Waiting for services to start..."
sleep 10

# Check if services are running
echo "Checking if services are running..."
docker-compose -f docker-compose.simple.yml ps

echo "Web console is available at: http://localhost:8082"
echo "Admin API is available at: http://localhost:8081"
echo "HTTP honeypot is available at: http://localhost:8080"
echo "Kibana is available at: http://localhost:5601"
