#!/bin/bash

SOLR_VERSION="8.11.3"
SOLR_DIR="solr-dist"
SOLR_ZIP="solr-$SOLR_VERSION.tgz"
SOLR_URL="https://archive.apache.org/dist/lucene/solr/$SOLR_VERSION/$SOLR_ZIP"

mkdir -p $SOLR_DIR

if [ ! -d "$SOLR_DIR/solr-$SOLR_VERSION" ]; then
    if [ ! -f "$SOLR_DIR/$SOLR_ZIP" ]; then
        echo "Downloading Solr $SOLR_VERSION..."
        curl -L -o "$SOLR_DIR/$SOLR_ZIP" "$SOLR_URL"
    fi
    echo "Extracting Solr..."
    tar -xzf "$SOLR_DIR/$SOLR_ZIP" -C "$SOLR_DIR"
fi

SOLR_BIN="$SOLR_DIR/solr-$SOLR_VERSION/bin/solr"

echo "Starting Solr..."
"$SOLR_BIN" start -c -p 8983

echo "Creating collection 'dummy_data'..."
"$SOLR_BIN" create_collection -c dummy_data -s 1 -rf 1 || echo "Collection might already exist"

echo "Solr setup complete. UI available at http://localhost:8983/solr"
