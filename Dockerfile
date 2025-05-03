# Build stage
FROM golang:1.20-alpine AS build

# Set working directory
WORKDIR /app

# Install git for dependency resolution
RUN apk add --no-cache git

# Copy go.mod
COPY go.mod ./

# Create empty go.sum if it doesn't exist
RUN touch go.sum

# Copy source code
COPY . .

# Download dependencies
RUN go mod tidy

# Build the application with verbose output
RUN CGO_ENABLED=0 GOOS=linux go build -v -o /daas ./cmd/main.go

# Final stage
FROM alpine:latest

# Install ca-certificates and curl for healthchecks
RUN apk --no-cache add ca-certificates curl

# Set working directory
WORKDIR /root/

# Create log directory
RUN mkdir -p /root/logs

# Copy the binary from the build stage
COPY --from=build /daas /usr/local/bin/daas

# Expose ports
EXPOSE 8080
EXPOSE 8081

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8081/api/health || exit 1

# Run the application
CMD ["daas"]
