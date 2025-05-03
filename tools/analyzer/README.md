# Honeypot Log Analyzer

This tool analyzes honeypot logs to extract useful information and generate reports.

## Overview

The Honeypot Log Analyzer processes JSON log files from the honeypot system and provides:
- Analysis of attacker IP addresses
- Analysis of attack types
- Analysis of requested URLs and query parameters
- Analysis of user agents
- Analysis of activity by time
- CSV report generation
- Chart generation

## Requirements

- Python 3.6+
- matplotlib (for chart generation)

Install the required libraries:

```bash
pip install matplotlib
```

## Usage

```bash
python analyzer.py LOG_FILE [--csv CSV_FILE] [--charts CHARTS_DIR]
```

### Options

- `LOG_FILE`: Path to the JSON log file to analyze
- `--csv`: Generate a CSV report and save it to the specified file
- `--charts`: Generate charts and save them to the specified directory

### Examples

Analyze a log file:

```bash
python analyzer.py /path/to/honeypot.log
```

Analyze a log file and generate a CSV report:

```bash
python analyzer.py /path/to/honeypot.log --csv report.csv
```

Analyze a log file, generate a CSV report, and create charts:

```bash
python analyzer.py /path/to/honeypot.log --csv report.csv --charts ./charts
```

## Output

The tool provides the following output:

1. **Console Output**:
   - Number of log entries
   - Top 10 attacker IP addresses
   - Attack types and counts
   - Top 10 requested paths
   - Top 10 query parameters
   - Top 10 user agents
   - Activity by hour
   - Peak activity time

2. **CSV Report** (if `--csv` is specified):
   - A CSV file with timestamp, source, IP, protocol, and description for each log entry

3. **Charts** (if `--charts` is specified):
   - Top 10 attacker IP addresses (bar chart)
   - Attack types (bar chart)
   - Activity by hour (line chart)

## Notes

- The tool expects JSON log files in the format produced by the honeypot system
- Each line in the log file should be a valid JSON object
- The tool will ignore lines that cannot be parsed as JSON
