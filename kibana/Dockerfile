# Use Kibana as base image
FROM docker.elastic.co/kibana/kibana:7.17.0

# Install curl and jq for the setup script
USER root
RUN apt-get update && apt-get install -y curl jq && rm -rf /var/lib/apt/lists/*

# Copy configuration files
COPY kibana.yml /usr/share/kibana/config/kibana.yml

# Copy setup script and dashboard files
COPY setup_kibana.sh /usr/local/bin/setup_kibana.sh
COPY dashboard.json /usr/local/bin/dashboard.json
COPY visualizations.json /usr/local/bin/visualizations.json

# Make setup script executable
RUN chmod +x /usr/local/bin/setup_kibana.sh

# Set environment variables
ENV ELASTICSEARCH_HOSTS=http://elasticsearch:9200

# Switch back to kibana user
USER kibana

# Expose Kibana port
EXPOSE 5601

# Start Kibana and run setup script
CMD ["/bin/bash", "-c", "/usr/local/bin/setup_kibana.sh & /usr/local/bin/kibana-docker"]
