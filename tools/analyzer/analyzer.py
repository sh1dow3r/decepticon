#!/usr/bin/env python3
"""
Honeypot Log Analyzer

This script analyzes honeypot logs to extract useful information and generate reports.
"""

import argparse
import json
import os
import sys
import re
import csv
import datetime
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from urllib.parse import urlparse, parse_qs

def parse_json_log(log_file):
    """Parse a JSON log file and return a list of log entries."""
    entries = []
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    entries.append(entry)
                except json.JSONDecodeError:
                    print(f"Warning: Could not parse line: {line.strip()}")
    except FileNotFoundError:
        print(f"Error: Log file not found: {log_file}")
        sys.exit(1)
    
    return entries

def extract_ip_addresses(entries):
    """Extract IP addresses from log entries."""
    ip_addresses = []
    
    for entry in entries:
        if 'ip' in entry:
            ip_addresses.append(entry['ip'])
    
    return ip_addresses

def extract_attack_types(entries):
    """Extract attack types from log entries."""
    attack_types = []
    
    for entry in entries:
        if 'raw_data' in entry and 'attack_type' in entry['raw_data']:
            attack_types.append(entry['raw_data']['attack_type'])
        elif 'description' in entry:
            # Try to infer attack type from description
            description = entry['description'].lower()
            if 'sql' in description:
                attack_types.append('sql_injection')
            elif 'xss' in description:
                attack_types.append('xss')
            elif 'command' in description:
                attack_types.append('command_injection')
            elif 'path' in description:
                attack_types.append('path_traversal')
            else:
                attack_types.append('unknown')
    
    return attack_types

def extract_urls(entries):
    """Extract URLs from log entries."""
    urls = []
    
    for entry in entries:
        if 'raw_data' in entry and 'url' in entry['raw_data']:
            urls.append(entry['raw_data']['url'])
    
    return urls

def extract_user_agents(entries):
    """Extract user agents from log entries."""
    user_agents = []
    
    for entry in entries:
        if 'raw_data' in entry and 'user_agent' in entry['raw_data']:
            user_agents.append(entry['raw_data']['user_agent'])
        elif 'raw_data' in entry and 'headers' in entry['raw_data'] and 'User-Agent' in entry['raw_data']['headers']:
            user_agents.append(entry['raw_data']['headers']['User-Agent'])
    
    return user_agents

def extract_timestamps(entries):
    """Extract timestamps from log entries."""
    timestamps = []
    
    for entry in entries:
        if 'timestamp' in entry:
            try:
                timestamp = datetime.datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
                timestamps.append(timestamp)
            except ValueError:
                print(f"Warning: Could not parse timestamp: {entry['timestamp']}")
    
    return timestamps

def analyze_ip_addresses(ip_addresses):
    """Analyze IP addresses."""
    ip_count = Counter(ip_addresses)
    top_ips = ip_count.most_common(10)
    
    print("\n=== Top 10 Attacker IP Addresses ===")
    for ip, count in top_ips:
        print(f"{ip}: {count} attacks")
    
    return ip_count

def analyze_attack_types(attack_types):
    """Analyze attack types."""
    attack_count = Counter(attack_types)
    
    print("\n=== Attack Types ===")
    for attack_type, count in attack_count.items():
        print(f"{attack_type}: {count} attacks")
    
    return attack_count

def analyze_urls(urls):
    """Analyze URLs."""
    # Extract paths
    paths = [urlparse(url).path for url in urls]
    path_count = Counter(paths)
    top_paths = path_count.most_common(10)
    
    print("\n=== Top 10 Requested Paths ===")
    for path, count in top_paths:
        print(f"{path}: {count} requests")
    
    # Extract query parameters
    query_params = []
    for url in urls:
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        for param in params:
            query_params.append(param)
    
    param_count = Counter(query_params)
    top_params = param_count.most_common(10)
    
    print("\n=== Top 10 Query Parameters ===")
    for param, count in top_params:
        print(f"{param}: {count} occurrences")
    
    return path_count, param_count

def analyze_user_agents(user_agents):
    """Analyze user agents."""
    ua_count = Counter(user_agents)
    top_uas = ua_count.most_common(10)
    
    print("\n=== Top 10 User Agents ===")
    for ua, count in top_uas:
        print(f"{ua}: {count} requests")
    
    return ua_count

def analyze_timestamps(timestamps):
    """Analyze timestamps."""
    if not timestamps:
        print("\n=== Timestamp Analysis ===")
        print("No timestamps found in log entries.")
        return None
    
    # Group by hour
    hours = [ts.replace(minute=0, second=0, microsecond=0) for ts in timestamps]
    hour_count = Counter(hours)
    
    # Sort by hour
    sorted_hours = sorted(hour_count.items())
    
    print("\n=== Activity by Hour ===")
    for hour, count in sorted_hours:
        print(f"{hour.strftime('%Y-%m-%d %H:00')}: {count} events")
    
    # Find peak hours
    peak_hour = max(hour_count.items(), key=lambda x: x[1])
    print(f"\nPeak activity: {peak_hour[1]} events at {peak_hour[0].strftime('%Y-%m-%d %H:00')}")
    
    return hour_count

def generate_csv_report(entries, output_file):
    """Generate a CSV report from log entries."""
    if not entries:
        print(f"Error: No log entries to generate report.")
        return
    
    try:
        with open(output_file, 'w', newline='') as f:
            # Determine fields from the first entry
            fields = ['timestamp', 'source', 'ip', 'protocol', 'description']
            
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
            writer.writeheader()
            
            for entry in entries:
                writer.writerow(entry)
        
        print(f"\nCSV report generated: {output_file}")
    except Exception as e:
        print(f"Error generating CSV report: {e}")

def generate_charts(ip_count, attack_count, hour_count, output_dir):
    """Generate charts from analysis results."""
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        # IP address chart
        plt.figure(figsize=(10, 6))
        top_ips = dict(ip_count.most_common(10))
        plt.bar(top_ips.keys(), top_ips.values())
        plt.title('Top 10 Attacker IP Addresses')
        plt.xlabel('IP Address')
        plt.ylabel('Number of Attacks')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'top_ips.png'))
        plt.close()
        
        # Attack type chart
        plt.figure(figsize=(10, 6))
        plt.bar(attack_count.keys(), attack_count.values())
        plt.title('Attack Types')
        plt.xlabel('Attack Type')
        plt.ylabel('Number of Attacks')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'attack_types.png'))
        plt.close()
        
        # Activity by hour chart
        if hour_count:
            plt.figure(figsize=(12, 6))
            hours = [h.strftime('%Y-%m-%d %H:00') for h, _ in sorted(hour_count.items())]
            counts = [c for _, c in sorted(hour_count.items())]
            plt.plot(hours, counts, marker='o')
            plt.title('Activity by Hour')
            plt.xlabel('Hour')
            plt.ylabel('Number of Events')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'activity_by_hour.png'))
            plt.close()
        
        print(f"\nCharts generated in: {output_dir}")
    except Exception as e:
        print(f"Error generating charts: {e}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Honeypot Log Analyzer")
    parser.add_argument("log_file", help="Path to the log file to analyze")
    parser.add_argument("--csv", help="Generate a CSV report")
    parser.add_argument("--charts", help="Generate charts and save them to the specified directory")
    
    args = parser.parse_args()
    
    print(f"Analyzing log file: {args.log_file}")
    
    # Parse log file
    entries = parse_json_log(args.log_file)
    print(f"Found {len(entries)} log entries.")
    
    # Extract data
    ip_addresses = extract_ip_addresses(entries)
    attack_types = extract_attack_types(entries)
    urls = extract_urls(entries)
    user_agents = extract_user_agents(entries)
    timestamps = extract_timestamps(entries)
    
    # Analyze data
    ip_count = analyze_ip_addresses(ip_addresses)
    attack_count = analyze_attack_types(attack_types)
    if urls:
        path_count, param_count = analyze_urls(urls)
    else:
        print("\n=== URL Analysis ===")
        print("No URLs found in log entries.")
    
    ua_count = analyze_user_agents(user_agents)
    hour_count = analyze_timestamps(timestamps)
    
    # Generate CSV report
    if args.csv:
        generate_csv_report(entries, args.csv)
    
    # Generate charts
    if args.charts:
        generate_charts(ip_count, attack_count, hour_count, args.charts)

if __name__ == "__main__":
    main()
