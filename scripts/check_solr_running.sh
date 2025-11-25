#!/bin/bash
# Check if Solr is already running

if curl -s "http://localhost:8983/solr/admin/info/system" > /dev/null 2>&1; then
    echo "✓ Solr is already running"
    exit 0
else
    echo "✗ Solr is not running"
    exit 1
fi
