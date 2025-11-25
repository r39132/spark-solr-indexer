#!/usr/bin/env python3
"""
Check if indexing is complete by comparing:
1. Document count in JSON file vs Solr
2. Sample document match between JSON and Solr
"""
import json
import sys
import requests

def get_local_doc_count():
    """Count lines in the JSON file"""
    try:
        with open("data/dummy_data.json", "r") as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return 0

def get_local_sample_doc():
    """Get a sample document from the JSON file"""
    try:
        with open("data/dummy_data.json", "r") as f:
            first_line = f.readline()
            return json.loads(first_line)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def get_solr_doc_count():
    """Get document count from Solr"""
    try:
        response = requests.get(
            "http://localhost:8983/solr/dummy_data/select?q=*:*&rows=0",
            timeout=5
        )
        if response.status_code == 200:
            return response.json()['response']['numFound']
    except Exception:
        pass
    return 0

def check_solr_doc_exists(doc_id):
    """Check if a specific document exists in Solr"""
    try:
        response = requests.get(
            f"http://localhost:8983/solr/dummy_data/select?q=id:{doc_id}&rows=1",
            timeout=5
        )
        if response.status_code == 200:
            result = response.json()
            return result['response']['numFound'] > 0
    except Exception:
        pass
    return False

def main():
    local_count = get_local_doc_count()
    solr_count = get_solr_doc_count()
    
    if local_count == 0:
        print("✗ No local data found")
        sys.exit(1)
    
    if solr_count == 0:
        print("✗ No documents in Solr")
        sys.exit(1)
    
    if local_count != solr_count:
        print(f"✗ Document count mismatch: Local={local_count}, Solr={solr_count}")
        sys.exit(1)
    
    # Check if sample document exists
    sample_doc = get_local_sample_doc()
    if sample_doc and not check_solr_doc_exists(sample_doc['id']):
        print(f"✗ Sample document not found in Solr")
        sys.exit(1)
    
    print(f"✓ Indexing complete: {solr_count} documents verified")
    sys.exit(0)

if __name__ == "__main__":
    main()
