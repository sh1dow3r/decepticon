// Package config provides configuration loading from environment variables
package config

import (
	"os"
	"strings"
)

// Config holds the application configuration
type Config struct {
	// Server configuration
	ServerAddress string

	// Logging configuration
	LogFilePath string

	// Elasticsearch configuration
	ElasticsearchURL   string
	ElasticsearchIndex string

	// Admin API configuration
	AdminAPIAddress string
}

// LoadConfig loads configuration from environment variables
func LoadConfig() *Config {
	return &Config{
		// Server configuration with default values
		ServerAddress: getEnv("SERVER_ADDRESS", ":8080"),

		// Logging configuration
		LogFilePath: getEnv("LOG_FILE_PATH", "/root/honeypot.log"),

		// Elasticsearch configuration
		ElasticsearchURL:   getEnv("ELASTICSEARCH_URL", "http://elasticsearch:9200"),
		ElasticsearchIndex: getEnv("ELASTICSEARCH_INDEX", "honeypot-logs"),

		// Admin API configuration
		AdminAPIAddress: getEnv("ADMIN_API_ADDRESS", ":8081"),
	}
}

// getEnv retrieves an environment variable or returns a default value if not set
func getEnv(key, defaultValue string) string {
	value := os.Getenv(key)
	if len(strings.TrimSpace(value)) == 0 {
		return defaultValue
	}
	return value
}
