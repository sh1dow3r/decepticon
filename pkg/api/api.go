// Package api provides REST API handlers for the honeypot service
package api

import (
	"daas/pkg/honeypot"
	"encoding/json"
	"net/http"
	"sync"
	"time"
)

// AdminAPI represents the admin API for the honeypot service
type AdminAPI struct {
	honeypotService *honeypot.HoneypotService
	server          *http.Server
	mutex           sync.Mutex
}

// NewAdminAPI creates a new admin API
func NewAdminAPI(address string, honeypotService *honeypot.HoneypotService) *AdminAPI {
	api := &AdminAPI{
		honeypotService: honeypotService,
	}

	// Create HTTP server
	api.server = &http.Server{
		Addr:    address,
		Handler: api.createRouter(),
	}

	return api
}

// Start starts the admin API server
func (a *AdminAPI) Start() error {
	return a.server.ListenAndServe()
}

// createRouter creates the HTTP router for the admin API
func (a *AdminAPI) createRouter() http.Handler {
	// Create router
	mux := http.NewServeMux()

	// Register API routes
	mux.HandleFunc("/api/stats", a.handleStats)
	mux.HandleFunc("/api/health", a.handleHealth)

	// Register web console routes
	mux.HandleFunc("/", a.handleRoot)

	return mux
}

// handleRoot serves the web console
func (a *AdminAPI) handleRoot(w http.ResponseWriter, r *http.Request) {
	// Create a simple HTML response directly
	if r.URL.Path == "/" {
		w.Header().Set("Content-Type", "text/html")
		w.Write([]byte(`
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Honeypot Management Console</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }
        .card {
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            padding: 15px;
        }
        .card h2 {
            margin-top: 0;
            color: #444;
            font-size: 18px;
        }
        .status {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 14px;
            font-weight: bold;
        }
        .status.ok {
            background-color: #d4edda;
            color: #155724;
        }
        .status.error {
            background-color: #f8d7da;
            color: #721c24;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        .refresh-btn {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 15px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            margin: 10px 0;
            cursor: pointer;
            border-radius: 3px;
        }
        .refresh-btn:hover {
            background-color: #45a049;
        }
        .timestamp {
            color: #666;
            font-size: 14px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Honeypot Management Console</h1>
        <div class="timestamp">Last updated: <span id="lastUpdated">-</span></div>
        <button class="refresh-btn" onclick="refreshData()">Refresh Data</button>

        <div class="card">
            <h2>System Status</h2>
            <div>
                <strong>Status:</strong> <span id="systemStatus" class="status">-</span>
            </div>
            <div>
                <strong>Version:</strong> <span id="systemVersion">-</span>
            </div>
            <div>
                <strong>Elasticsearch:</strong> <span id="esStatus" class="status">-</span>
            </div>
        </div>

        <div class="card">
            <h2>Honeypot Statistics</h2>
            <div>
                <strong>Total Connections:</strong> <span id="totalConnections">-</span>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>IP Address</th>
                        <th>Connection Count</th>
                    </tr>
                </thead>
                <tbody id="connectionsByIP">
                    <!-- Will be populated by JavaScript -->
                </tbody>
            </table>
        </div>
    </div>

    <script>
        // Function to fetch health data
        async function fetchHealth() {
            try {
                const response = await fetch('/api/health');
                const data = await response.json();

                // Update system status
                document.getElementById('systemStatus').textContent = data.status;
                document.getElementById('systemStatus').className = 'status ' + (data.status === 'ok' ? 'ok' : 'error');
                document.getElementById('systemVersion').textContent = data.version;

                // Update Elasticsearch status
                document.getElementById('esStatus').textContent = data.elasticsearch.status;
                document.getElementById('esStatus').className = 'status ' + (data.elasticsearch.status === 'ok' ? 'ok' : 'error');

                // Update statistics
                document.getElementById('totalConnections').textContent = data.stats.total_connections;

                // Update connections by IP
                const connectionsByIPTable = document.getElementById('connectionsByIP');
                connectionsByIPTable.innerHTML = '';

                Object.entries(data.stats.connections_by_ip).forEach(([ip, count]) => {
                    const row = document.createElement('tr');
                    row.innerHTML = '<td>' + ip + '</td><td>' + count + '</td>';
                    connectionsByIPTable.appendChild(row);
                });

                // Update timestamp
                document.getElementById('lastUpdated').textContent = new Date().toLocaleString();
            } catch (error) {
                console.error('Error fetching health data:', error);
            }
        }

        // Function to refresh all data
        function refreshData() {
            fetchHealth();
        }

        // Initial data load
        document.addEventListener('DOMContentLoaded', () => {
            refreshData();
            // Refresh data every 30 seconds
            setInterval(refreshData, 30000);
        });
    </script>
</body>
</html>
`))
		return
	}

	// For other paths, return 404
	http.NotFound(w, r)
}

// handleStats handles requests to the /api/stats endpoint
func (a *AdminAPI) handleStats(w http.ResponseWriter, r *http.Request) {
	// Only allow GET requests
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Get statistics
	stats := a.honeypotService.GetStatistics()

	// Marshal statistics to JSON
	statsJSON, err := json.Marshal(stats)
	if err != nil {
		http.Error(w, "Internal server error", http.StatusInternalServerError)
		return
	}

	// Set content type
	w.Header().Set("Content-Type", "application/json")

	// Write response
	w.Write(statsJSON)
}

// handleHealth handles requests to the /api/health endpoint
func (a *AdminAPI) handleHealth(w http.ResponseWriter, r *http.Request) {
	// Only allow GET requests
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Check Elasticsearch connection
	esStatus := "ok"
	esError := ""

	// Try to connect to Elasticsearch
	resp, err := http.Get(a.honeypotService.GetElasticsearchURL() + "/_cluster/health")
	if err != nil || resp.StatusCode >= 400 {
		esStatus = "error"
		if err != nil {
			esError = err.Error()
		} else {
			esError = "Elasticsearch returned status: " + resp.Status
		}
	}
	if resp != nil {
		resp.Body.Close()
	}

	// Create health response
	health := map[string]interface{}{
		"status":    "ok",
		"version":   "1.0.0",
		"timestamp": time.Now().UTC().Format(time.RFC3339),
		"elasticsearch": map[string]interface{}{
			"status": esStatus,
			"error":  esError,
		},
		"stats": a.honeypotService.GetStatistics(),
	}

	// Marshal health to JSON
	healthJSON, err := json.Marshal(health)
	if err != nil {
		http.Error(w, "Internal server error", http.StatusInternalServerError)
		return
	}

	// Set content type
	w.Header().Set("Content-Type", "application/json")

	// Write response
	w.Write(healthJSON)
}
