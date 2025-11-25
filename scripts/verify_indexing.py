#!/usr/bin/env python3
import sys

import requests


def verify_indexing():
    """Verifies that the indexing worked by querying Solr."""
    print("Querying Solr to verify indexing...")
    try:
        # 1. Check total count
        response = requests.get("http://localhost:8983/solr/dummy_data/select?q=*:*&rows=0&wt=json")
        response.raise_for_status()
        num_found = response.json()["response"]["numFound"]
        print(f"Total Documents found: {num_found}")

        if num_found == 0:
            print("✗ No documents found in Solr.")
            sys.exit(1)

        # 2. Category Facet (Distribution)
        print("\n--- Category Distribution ---")
        facet_resp = requests.get(
            "http://localhost:8983/solr/dummy_data/select?q=*:*&rows=0&facet=true&facet.field=category&wt=json"
        )
        facet_resp.raise_for_status()
        facets = facet_resp.json()["facet_counts"]["facet_fields"]["category"]
        # Solr returns list [val, count, val, count], convert to dict for display
        for i in range(0, len(facets), 2):
            print(f"  {facets[i]}: {facets[i + 1]}")

        # 3. Expensive Items (Price > 300)
        print("\n--- Expensive Items (Price > 300) ---")
        price_resp = requests.get(
            "http://localhost:8983/solr/dummy_data/select?q=price:[300%20TO%20*]&rows=0&wt=json"
        )
        price_resp.raise_for_status()
        print(f"  Count: {price_resp.json()['response']['numFound']}")

        # 4. In Stock Items
        print("\n--- In Stock Items ---")
        stock_resp = requests.get(
            "http://localhost:8983/solr/dummy_data/select?q=in_stock:true&rows=0&wt=json"
        )
        stock_resp.raise_for_status()
        print(f"  Count: {stock_resp.json()['response']['numFound']}")

        print("\n✓ Indexing verification successful!")

    except Exception as e:
        print(f"✗ Error verifying indexing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    verify_indexing()
