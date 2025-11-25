#!/bin/bash
# Check if dummy data file exists and has content

DATA_FILE="data/dummy_data.json"

if [ -f "$DATA_FILE" ]; then
    line_count=$(wc -l < "$DATA_FILE" | tr -d ' ')
    if [ "$line_count" -gt 0 ]; then
        echo "✓ Data exists: $line_count documents"
        exit 0
    fi
fi

echo "✗ No data found"
exit 1
