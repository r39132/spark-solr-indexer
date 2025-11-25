#!/usr/bin/env bash
set -e

# Simple smoke test for spark-solr-indexer
# This script runs the full pipeline: generate data, start Solr, index with Spark, and verify indexing.

echo "=== Cleaning previous run ==="
make clean || true

echo "=== Running full pipeline (gen-data, setup-solr, index) ==="
make all

echo "=== Verifying indexing succeeded ==="
make verify-indexing-worked

echo "=== Smoke test completed successfully ==="
