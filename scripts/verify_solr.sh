#!/bin/bash

echo "Querying Solr for document count..."
RESPONSE=$(curl -s "http://localhost:8983/solr/dummy_data/select?q=*:*&rows=0")

echo "Response: $RESPONSE"

if [[ "$RESPONSE" == *"\"numFound\":1000"* ]]; then
    echo "SUCCESS: Found 1000 documents."
else
    echo "FAILURE: Did not find 1000 documents."
    exit 1
fi
