import os

from pyspark.sql import SparkSession


def main():
    # Ensure we have the spark-solr package
    # In a real run, this is passed via --packages to spark-submit
    spark = SparkSession.builder.appName("SolrIndexer").master("local[*]").getOrCreate()

    # Read JSON data
    input_file = os.path.abspath("data/dummy_data.json")
    print(f"Reading data from {input_file}")

    df = spark.read.json(input_file)

    print("Schema:")
    df.printSchema()

    # Solr configuration
    zk_host = "localhost:9983"  # Default embedded ZK port for Solr cloud -c
    collection = "dummy_data"

    print(f"Indexing to Solr collection '{collection}' at ZK '{zk_host}'...")

    # Write to Solr
    df.write.format("solr").option("zkhost", zk_host).option("collection", collection).option(
        "gen_uniq_key", "true"
    ).option("commit_within", "1000").mode("overwrite").save()

    print("Indexing complete.")
    spark.stop()


if __name__ == "__main__":
    main()
