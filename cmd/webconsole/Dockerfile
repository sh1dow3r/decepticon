# Build stage
FROM golang:1.20-alpine AS build

# Set working directory
WORKDIR /app

# Copy source code
COPY . .

# Build the application
RUN go build -o /webconsole ./cmd/webconsole/main.go

# Final stage
FROM alpine:latest

# Copy the binary from the build stage
COPY --from=build /webconsole /usr/local/bin/webconsole

# Copy static files
COPY pkg/api/static /pkg/api/static

# Expose port
EXPOSE 8082

# Run the application
CMD ["webconsole"]
