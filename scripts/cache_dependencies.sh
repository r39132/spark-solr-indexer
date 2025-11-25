#!/usr/bin/env bash
set -e

# Pre-download Spark dependencies to speed up subsequent runs
echo "Pre-downloading spark-solr dependencies..."
JAVA_HOME=$(jenv prefix) uv run spark-submit \
    --conf spark.jars.ivy=$HOME/.ivy2 \
    --packages com.lucidworks.spark:spark-solr:4.0.0 \
    --help > /dev/null 2>&1 || true

echo "✓ Dependencies cached in ~/.ivy2/"
echo "  Subsequent 'make index' runs will be much faster!"
