// Package main is the entry point for the honeypot service
package main

import (
	"daas/internal/log"
	"daas/pkg/api"
	"daas/pkg/config"
	"daas/pkg/honeypot"
	"fmt"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	// Load configuration
	cfg := config.LoadConfig()

	// Create logger
	logger, err := log.NewLogger(cfg)
	if err != nil {
		fmt.Printf("Failed to create logger: %v\n", err)
		os.Exit(1)
	}

	// Create honeypot service
	honeypotService := honeypot.NewHoneypotService(cfg, logger)

	// Create admin API
	adminAPI := api.NewAdminAPI(cfg.AdminAPIAddress, honeypotService)

	// Start admin API in a goroutine
	go func() {
		fmt.Printf("Starting admin API on %s\n", cfg.AdminAPIAddress)
		if err := adminAPI.Start(); err != nil {
			fmt.Printf("Failed to start admin API: %v\n", err)
			os.Exit(1)
		}
	}()

	// Start HTTP honeypot in a goroutine
	go func() {
		fmt.Printf("Starting HTTP honeypot on %s\n", cfg.ServerAddress)
		if err := honeypotService.StartHTTPHoneypot(); err != nil {
			fmt.Printf("Failed to start HTTP honeypot: %v\n", err)
			os.Exit(1)
		}
	}()

	// Wait for interrupt signal
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
	<-sigCh

	fmt.Println("Shutting down...")
}
