from invoke import task

@task
def gen_data(c):
    """Generate dummy data using the Python script."""
    print("Generating data...")
    c.run("python3 data_gen/generate_data.py")

@task
def setup_solr(c):
    """Download and start Solr."""
    print("Setting up Solr...")
    c.run("./scripts/setup_solr.sh")

@task
def index(c):
    """Submit the Spark job to index data to Solr."""
    print("Running Spark job...")
    c.run("spark-submit --conf spark.jars.ivy=/tmp/antigravity_ivy --packages com.lucidworks.spark:spark-solr:4.0.0 spark_job/index_to_solr.py")

@task
def stop_solr(c):
    """Stop the running Solr instance."""
    print("Stopping Solr...")
    c.run("./solr-dist/solr-9.7.0/bin/solr stop -all", warn=True)

@task
def clean(c):
    """Remove generated data."""
    print("Cleaning up data...")
    c.run("rm -rf data")

@task(pre=[gen_data, setup_solr, index])
def all(c):
    """Run the entire pipeline: generate data, setup solr, and index."""
    print("Pipeline complete!")
