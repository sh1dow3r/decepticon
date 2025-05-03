#!/bin/bash
# Setup script for Kibana

# Wait for Elasticsearch to be available
echo "Waiting for Elasticsearch..."
until curl -s http://elasticsearch:9200 > /dev/null 2>&1; do
    echo "Waiting for Elasticsearch to be available..."
    sleep 10
done
echo "Elasticsearch is up!"

# Wait for Kibana to be available
echo "Waiting for Kibana..."
# First wait for Kibana to start
sleep 30
until curl -s http://localhost:5601/api/status > /dev/null 2>&1; do
    echo "Waiting for Kibana to be available..."
    sleep 10
done
echo "Kibana is up!"

# Create index patterns
echo "Creating index patterns..."
# Wait a bit more to ensure Kibana API is fully ready
sleep 30

# Create honeypot-logs index pattern
echo "Creating honeypot-logs index pattern..."
curl -X POST "http://localhost:5601/api/saved_objects/index-pattern/honeypot-logs" \
    -H "kbn-xsrf: true" \
    -H "Content-Type: application/json" \
    -d '{"attributes":{"title":"honeypot-logs*","timeFieldName":"timestamp"}}' || echo "Failed to create honeypot-logs index pattern"

# Create cowrie index pattern
echo "Creating cowrie index pattern..."
curl -X POST "http://localhost:5601/api/saved_objects/index-pattern/cowrie" \
    -H "kbn-xsrf: true" \
    -H "Content-Type: application/json" \
    -d '{"attributes":{"title":"cowrie*","timeFieldName":"timestamp"}}' || echo "Failed to create cowrie index pattern"

# Set default index pattern
echo "Setting default index pattern..."
curl -X POST "http://localhost:5601/api/kibana/settings" \
    -H "kbn-xsrf: true" \
    -H "Content-Type: application/json" \
    -d '{"changes":{"defaultIndex":"honeypot-logs"}}' || echo "Failed to set default index pattern"

# Import visualizations
echo "Importing visualizations..."
for viz in $(cat /usr/local/bin/visualizations.json | jq -c '.[]'); do
    id=$(echo $viz | jq -r '.id')
    type=$(echo $viz | jq -r '.type')
    echo "Importing $type: $id"
    curl -X POST "http://localhost:5601/api/saved_objects/$type/$id" \
        -H "kbn-xsrf: true" \
        -H "Content-Type: application/json" \
        -d "$viz" || echo "Failed to import $type: $id"
    # Add a small delay to avoid overwhelming the API
    sleep 2
done

# Import dashboard
echo "Importing dashboard..."
curl -X POST "http://localhost:5601/api/saved_objects/dashboard/honeypot-dashboard" \
    -H "kbn-xsrf: true" \
    -H "Content-Type: application/json" \
    -d "$(cat /usr/local/bin/dashboard.json)" || echo "Failed to import dashboard"

echo "Setup complete!"

# Keep the script running to maintain the container
tail -f /dev/null
