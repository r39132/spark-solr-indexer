import json
import os
import random

from faker import Faker

fake = Faker()


def generate_document(doc_id):
    return {
        "id": str(doc_id),
        "title": fake.sentence(),
        "description": fake.paragraph(),
        "author": fake.name(),
        "category": random.choice(["Technology", "Science", "Art", "History", "Music"]),
        "created_at": fake.date_time_between(start_date="-1y", end_date="now").isoformat(),
        "price": round(random.uniform(10.0, 500.0), 2),
        "in_stock": random.choice([True, False]),
    }


def main():
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "dummy_data.json")

    documents = []
    print("Generating 1000 dummy documents...")
    for i in range(1000):
        documents.append(generate_document(i))

    with open(output_file, "w") as f:
        # Write as JSON Lines (newline-delimited JSON) - one JSON object per line
        # This is the format Spark's JSON reader expects
        for doc in documents:
            f.write(json.dumps(doc) + "\n")

    print(f"Successfully generated {len(documents)} documents to {output_file}")


if __name__ == "__main__":
    main()
