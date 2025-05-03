// Package honeypot provides specific handler logic for different types of attacks
package honeypot

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
)

// AttackType represents the type of attack
type AttackType string

const (
	// SQLInjection represents a SQL injection attack
	SQLInjection AttackType = "sql_injection"

	// XSS represents a cross-site scripting attack
	XSS AttackType = "xss"

	// CommandInjection represents a command injection attack
	CommandInjection AttackType = "command_injection"

	// PathTraversal represents a path traversal attack
	PathTraversal AttackType = "path_traversal"

	// Unknown represents an unknown attack
	Unknown AttackType = "unknown"
)

// DetectAttack detects the type of attack from an HTTP request
func DetectAttack(r *http.Request) AttackType {
	// Check URL and query parameters
	url := r.URL.String()
	query := r.URL.Query()

	// Check for SQL injection
	sqlPatterns := []string{
		"'", "UNION", "SELECT", "DROP", "INSERT", "DELETE", "UPDATE", "1=1", "OR 1=1",
	}
	for _, pattern := range sqlPatterns {
		if strings.Contains(strings.ToUpper(url), pattern) {
			return SQLInjection
		}

		// Check query parameters
		for _, values := range query {
			for _, value := range values {
				if strings.Contains(strings.ToUpper(value), pattern) {
					return SQLInjection
				}
			}
		}
	}

	// Check for XSS
	xssPatterns := []string{
		"<script>", "javascript:", "onerror=", "onload=", "eval(", "alert(",
	}
	for _, pattern := range xssPatterns {
		if strings.Contains(strings.ToLower(url), pattern) {
			return XSS
		}

		// Check query parameters
		for _, values := range query {
			for _, value := range values {
				if strings.Contains(strings.ToLower(value), pattern) {
					return XSS
				}
			}
		}
	}

	// Check for command injection
	cmdPatterns := []string{
		";", "|", "&&", "||", "`", "$(",
	}
	for _, pattern := range cmdPatterns {
		if strings.Contains(url, pattern) {
			return CommandInjection
		}

		// Check query parameters
		for _, values := range query {
			for _, value := range values {
				if strings.Contains(value, pattern) {
					return CommandInjection
				}
			}
		}
	}

	// Check for path traversal
	pathPatterns := []string{
		"../", "..\\", "/etc/passwd", "C:\\Windows\\",
	}
	for _, pattern := range pathPatterns {
		if strings.Contains(url, pattern) {
			return PathTraversal
		}

		// Check query parameters
		for _, values := range query {
			for _, value := range values {
				if strings.Contains(value, pattern) {
					return PathTraversal
				}
			}
		}
	}

	return Unknown
}

// GenerateResponse generates a response for a specific attack type
func GenerateResponse(w http.ResponseWriter, attackType AttackType) {
	switch attackType {
	case SQLInjection:
		// Simulate a database error
		w.Header().Set("Content-Type", "text/plain")
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("Error executing database query: syntax error"))

	case XSS:
		// Return a sanitized response
		w.Header().Set("Content-Type", "text/html")
		w.Header().Set("X-XSS-Protection", "1; mode=block")
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("<html><body>Input has been sanitized</body></html>"))

	case CommandInjection:
		// Simulate a command execution error
		w.Header().Set("Content-Type", "text/plain")
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("Error executing command: permission denied"))

	case PathTraversal:
		// Simulate a file not found error
		w.Header().Set("Content-Type", "text/plain")
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("File not found"))

	default:
		// Default response
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		// Create a fake API response
		response := map[string]interface{}{
			"status": "success",
			"data": map[string]interface{}{
				"message": "Request processed successfully",
			},
		}

		// Marshal response to JSON
		responseJSON, _ := json.Marshal(response)
		w.Write(responseJSON)
	}
}

// HandleAttack handles an attack and logs it
func (h *HoneypotService) HandleAttack(w http.ResponseWriter, r *http.Request) {
	// Get client IP
	ip := getClientIP(r)

	// Detect attack type
	attackType := DetectAttack(r)

	// Update statistics
	h.updateStats(ip)

	// Log attack
	h.logAttack(r, ip, attackType)

	// Generate response
	GenerateResponse(w, attackType)
}

// logAttack logs an attack to the honeypot
func (h *HoneypotService) logAttack(r *http.Request, ip string, attackType AttackType) {
	// Create raw data
	rawData := map[string]interface{}{
		"method":      r.Method,
		"url":         r.URL.String(),
		"headers":     r.Header,
		"user_agent":  r.UserAgent(),
		"attack_type": attackType,
	}

	// Log attack
	description := fmt.Sprintf("Detected %s attack from %s", attackType, ip)
	h.logger.LogHoneypotActivity("http", ip, "http", description, rawData)
}
