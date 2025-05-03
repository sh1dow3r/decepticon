// Package log provides logging utilities with Elasticsearch integration
package log

import (
	"bytes"
	"daas/pkg/config"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
)

// Logger represents a logger with file and Elasticsearch output
type Logger struct {
	fileLogger *log.Logger
	config     *config.Config
	httpClient *http.Client
}

// LogEntry represents a log entry to be stored in Elasticsearch
type LogEntry struct {
	Timestamp   string      `json:"timestamp"`
	Source      string      `json:"source"`
	IP          string      `json:"ip"`
	Protocol    string      `json:"protocol"`
	Description string      `json:"description"`
	RawData     interface{} `json:"raw_data,omitempty"`
}

// NewLogger creates a new logger with file and Elasticsearch output
func NewLogger(cfg *config.Config) (*Logger, error) {
	// Create log file
	file, err := os.OpenFile(cfg.LogFilePath, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		return nil, fmt.Errorf("failed to open log file: %v", err)
	}

	// Create file logger
	fileLogger := log.New(file, "", log.LstdFlags)

	// Create HTTP client for Elasticsearch
	httpClient := &http.Client{
		Timeout: 5 * time.Second,
	}

	return &Logger{
		fileLogger: fileLogger,
		config:     cfg,
		httpClient: httpClient,
	}, nil
}

// LogHoneypotActivity logs honeypot activity to file and Elasticsearch
func (l *Logger) LogHoneypotActivity(source, ip, protocol, description string, rawData interface{}) error {
	// Create log entry
	entry := LogEntry{
		Timestamp:   time.Now().UTC().Format(time.RFC3339),
		Source:      source,
		IP:          ip,
		Protocol:    protocol,
		Description: description,
		RawData:     rawData,
	}

	// Log to file
	entryJSON, err := json.Marshal(entry)
	if err != nil {
		return fmt.Errorf("failed to marshal log entry: %v", err)
	}
	l.fileLogger.Println(string(entryJSON))

	// Log to Elasticsearch
	return l.sendToElasticsearch(entry)
}

// sendToElasticsearch sends a log entry to Elasticsearch
func (l *Logger) sendToElasticsearch(entry LogEntry) error {
	// Marshal entry to JSON
	entryJSON, err := json.Marshal(entry)
	if err != nil {
		return fmt.Errorf("failed to marshal log entry: %v", err)
	}

	// Create Elasticsearch index URL
	url := fmt.Sprintf("%s/%s/_doc", l.config.ElasticsearchURL, l.config.ElasticsearchIndex)

	// Create request
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(entryJSON))
	if err != nil {
		return fmt.Errorf("failed to create request: %v", err)
	}
	req.Header.Set("Content-Type", "application/json")

	// Send request
	resp, err := l.httpClient.Do(req)
	if err != nil {
		return fmt.Errorf("failed to send log to Elasticsearch: %v", err)
	}
	defer resp.Body.Close()

	// Check response
	if resp.StatusCode >= 400 {
		return fmt.Errorf("Elasticsearch returned error status: %s", resp.Status)
	}

	return nil
}
