from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder.appName("SolrIndexer-GCP").getOrCreate()

    # Read JSON data from GCS
    input_file = "gs://family-tree-469815-spark-solr-data/data/dummy_data.json"
    print(f"Reading data from {input_file}")

    df = spark.read.json(input_file)

    print("Schema:")
    df.printSchema()

    # Solr configuration
    # Use Internal IP for ZooKeeper (accessible within VPC)
    zk_host = "10.128.0.2:9983"
    collection = "dummy_data"

    print(f"Indexing to Solr collection '{collection}' via ZK '{zk_host}'...")

    # Write to Solr using ZK (standard method)
    df.write.format("solr").option("zkhost", zk_host).option("collection", collection).option(
        "gen_uniq_key", "true"
    ).option("commit_within", "1000").mode("overwrite").save()

    print("Indexing complete.")
    spark.stop()


if __name__ == "__main__":
    main()
