// Package honeypot provides core honeypot functionality
package honeypot

import (
	"daas/internal/log"
	"daas/pkg/config"
	"fmt"
	"net"
	"net/http"
	"strings"
	"sync"
	"time"
)

// HoneypotService represents the main honeypot service
type HoneypotService struct {
	config *config.Config
	logger *log.Logger
	stats  *Statistics
}

// Statistics holds honeypot activity statistics
type Statistics struct {
	TotalConnections int            `json:"total_connections"`
	ConnectionsByIP  map[string]int `json:"connections_by_ip"`
	mutex            sync.Mutex
}

// NewHoneypotService creates a new honeypot service
func NewHoneypotService(cfg *config.Config, logger *log.Logger) *HoneypotService {
	return &HoneypotService{
		config: cfg,
		logger: logger,
		stats: &Statistics{
			TotalConnections: 0,
			ConnectionsByIP:  make(map[string]int),
		},
	}
}

// StartHTTPHoneypot starts the HTTP honeypot server
func (h *HoneypotService) StartHTTPHoneypot() error {
	// Create HTTP server
	server := &http.Server{
		Addr:         h.config.ServerAddress,
		Handler:      h,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

	// Start HTTP server
	fmt.Printf("Starting HTTP honeypot on %s\n", h.config.ServerAddress)
	return server.ListenAndServe()
}

// ServeHTTP handles HTTP requests to the honeypot
func (h *HoneypotService) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	// Get client IP
	ip := getClientIP(r)

	// Update statistics
	h.updateStats(ip)

	// Log request
	h.logRequest(r, ip)

	// Respond with a fake server banner
	w.Header().Set("Server", "Microsoft-IIS/8.5")
	w.Header().Set("Content-Type", "text/html")
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("<html><body><h1>It works!</h1></body></html>"))
}

// GetStatistics returns the current honeypot statistics
func (h *HoneypotService) GetStatistics() *Statistics {
	return h.stats
}

// GetElasticsearchURL returns the Elasticsearch URL
func (h *HoneypotService) GetElasticsearchURL() string {
	return h.config.ElasticsearchURL
}

// updateStats updates the honeypot statistics
func (h *HoneypotService) updateStats(ip string) {
	h.stats.mutex.Lock()
	defer h.stats.mutex.Unlock()

	h.stats.TotalConnections++
	h.stats.ConnectionsByIP[ip]++
}

// logRequest logs an HTTP request to the honeypot
func (h *HoneypotService) logRequest(r *http.Request, ip string) {
	// Create raw data
	rawData := map[string]interface{}{
		"method":     r.Method,
		"url":        r.URL.String(),
		"headers":    r.Header,
		"user_agent": r.UserAgent(),
	}

	// Log request
	description := fmt.Sprintf("HTTP %s request to %s", r.Method, r.URL.String())
	h.logger.LogHoneypotActivity("http", ip, "http", description, rawData)
}

// getClientIP extracts the client IP from an HTTP request
func getClientIP(r *http.Request) string {
	// Check X-Forwarded-For header
	xForwardedFor := r.Header.Get("X-Forwarded-For")
	if xForwardedFor != "" {
		// X-Forwarded-For can contain multiple IPs, use the first one
		ips := strings.Split(xForwardedFor, ",")
		if len(ips) > 0 {
			return strings.TrimSpace(ips[0])
		}
	}

	// Check X-Real-IP header
	xRealIP := r.Header.Get("X-Real-IP")
	if xRealIP != "" {
		return xRealIP
	}

	// Use RemoteAddr
	ip, _, err := net.SplitHostPort(r.RemoteAddr)
	if err != nil {
		return r.RemoteAddr
	}
	return ip
}
