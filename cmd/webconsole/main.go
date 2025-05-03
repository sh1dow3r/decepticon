package main

import (
	"fmt"
	"net/http"
	"os"
)

func main() {
	// Get port from environment variable or use default
	port := os.Getenv("PORT")
	if port == "" {
		port = "8082"
	}

	// Create file server
	fs := http.FileServer(http.Dir("pkg/api/static"))

	// Create HTTP server
	http.Handle("/", fs)

	// Start server
	fmt.Printf("Starting web console on port %s...\n", port)
	err := http.ListenAndServe(":"+port, nil)
	if err != nil {
		fmt.Printf("Error starting server: %v\n", err)
		os.Exit(1)
	}
}
