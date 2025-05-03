#!/usr/bin/env python3
"""
Honeypot Activity Simulator

This script simulates various types of attacks on the honeypot system for testing purposes.
It sends HTTP requests to the honeypot services and logs the activity.
"""

import argparse
import random
import requests
import time
import ipaddress
from datetime import datetime

# Attack patterns
SQL_INJECTION_PATTERNS = [
    "' OR 1=1 --",
    "'; DROP TABLE users; --",
    "' UNION SELECT username, password FROM users --",
    "admin' --",
    "1' OR '1'='1",
]

XSS_PATTERNS = [
    "<script>alert('XSS')</script>",
    "<img src='x' onerror='alert(\"XSS\")'>",
    "javascript:alert('XSS')",
    "<svg/onload=alert('XSS')>",
    "<body onload='alert(\"XSS\")'>",
]

COMMAND_INJECTION_PATTERNS = [
    "; cat /etc/passwd",
    "| ls -la",
    "`id`",
    "$(cat /etc/shadow)",
    "&& whoami",
]

PATH_TRAVERSAL_PATTERNS = [
    "../../../etc/passwd",
    "..\\..\\..\\Windows\\system.ini",
    "/etc/passwd",
    "C:\\Windows\\win.ini",
    "../../../../../../../../etc/hosts",
]

# User agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    "curl/7.64.1",
    "Wget/1.20.3 (linux-gnu)",
    "Nmap Scripting Engine",
]

def generate_random_ip():
    """Generate a random IP address."""
    # Exclude private IP ranges
    while True:
        ip = str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))
        if not ipaddress.IPv4Address(ip).is_private:
            return ip

def simulate_sql_injection(host, port):
    """Simulate SQL injection attacks."""
    print(f"[{datetime.now()}] Simulating SQL injection attacks...")
    
    for pattern in SQL_INJECTION_PATTERNS:
        ip = generate_random_ip()
        user_agent = random.choice(USER_AGENTS)
        
        try:
            url = f"http://{host}:{port}/login?username=admin&password={pattern}"
            headers = {"User-Agent": user_agent, "X-Forwarded-For": ip}
            
            response = requests.get(url, headers=headers)
            print(f"[{datetime.now()}] SQL Injection from {ip}: {pattern} - Status: {response.status_code}")
            
            # Sleep to avoid overwhelming the server
            time.sleep(random.uniform(0.5, 2.0))
        except Exception as e:
            print(f"[{datetime.now()}] Error: {e}")

def simulate_xss(host, port):
    """Simulate XSS attacks."""
    print(f"[{datetime.now()}] Simulating XSS attacks...")
    
    for pattern in XSS_PATTERNS:
        ip = generate_random_ip()
        user_agent = random.choice(USER_AGENTS)
        
        try:
            url = f"http://{host}:{port}/search?q={pattern}"
            headers = {"User-Agent": user_agent, "X-Forwarded-For": ip}
            
            response = requests.get(url, headers=headers)
            print(f"[{datetime.now()}] XSS from {ip}: {pattern} - Status: {response.status_code}")
            
            # Sleep to avoid overwhelming the server
            time.sleep(random.uniform(0.5, 2.0))
        except Exception as e:
            print(f"[{datetime.now()}] Error: {e}")

def simulate_command_injection(host, port):
    """Simulate command injection attacks."""
    print(f"[{datetime.now()}] Simulating command injection attacks...")
    
    for pattern in COMMAND_INJECTION_PATTERNS:
        ip = generate_random_ip()
        user_agent = random.choice(USER_AGENTS)
        
        try:
            url = f"http://{host}:{port}/execute?cmd={pattern}"
            headers = {"User-Agent": user_agent, "X-Forwarded-For": ip}
            
            response = requests.get(url, headers=headers)
            print(f"[{datetime.now()}] Command Injection from {ip}: {pattern} - Status: {response.status_code}")
            
            # Sleep to avoid overwhelming the server
            time.sleep(random.uniform(0.5, 2.0))
        except Exception as e:
            print(f"[{datetime.now()}] Error: {e}")

def simulate_path_traversal(host, port):
    """Simulate path traversal attacks."""
    print(f"[{datetime.now()}] Simulating path traversal attacks...")
    
    for pattern in PATH_TRAVERSAL_PATTERNS:
        ip = generate_random_ip()
        user_agent = random.choice(USER_AGENTS)
        
        try:
            url = f"http://{host}:{port}/download?file={pattern}"
            headers = {"User-Agent": user_agent, "X-Forwarded-For": ip}
            
            response = requests.get(url, headers=headers)
            print(f"[{datetime.now()}] Path Traversal from {ip}: {pattern} - Status: {response.status_code}")
            
            # Sleep to avoid overwhelming the server
            time.sleep(random.uniform(0.5, 2.0))
        except Exception as e:
            print(f"[{datetime.now()}] Error: {e}")

def simulate_random_attacks(host, port, count):
    """Simulate random attacks."""
    print(f"[{datetime.now()}] Simulating {count} random attacks...")
    
    attack_functions = [
        simulate_sql_injection,
        simulate_xss,
        simulate_command_injection,
        simulate_path_traversal,
    ]
    
    for _ in range(count):
        attack_function = random.choice(attack_functions)
        attack_function(host, port)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Honeypot Activity Simulator")
    parser.add_argument("--host", default="localhost", help="Honeypot host (default: localhost)")
    parser.add_argument("--port", type=int, default=8080, help="Honeypot port (default: 8080)")
    parser.add_argument("--count", type=int, default=10, help="Number of random attacks to simulate (default: 10)")
    parser.add_argument("--type", choices=["sql", "xss", "cmd", "path", "random"], default="random", help="Type of attack to simulate (default: random)")
    
    args = parser.parse_args()
    
    print(f"[{datetime.now()}] Starting Honeypot Activity Simulator...")
    print(f"[{datetime.now()}] Target: http://{args.host}:{args.port}")
    
    if args.type == "sql":
        simulate_sql_injection(args.host, args.port)
    elif args.type == "xss":
        simulate_xss(args.host, args.port)
    elif args.type == "cmd":
        simulate_command_injection(args.host, args.port)
    elif args.type == "path":
        simulate_path_traversal(args.host, args.port)
    else:
        simulate_random_attacks(args.host, args.port, args.count)
    
    print(f"[{datetime.now()}] Simulation completed.")

if __name__ == "__main__":
    main()
