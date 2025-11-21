#!/usr/bin/env python3
import sys
import subprocess
import os

def run_command(command, ignore_errors=False):
    print(f"Running: {command}")
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError:
        if not ignore_errors:
            print(f"Error running command: {command}")
            sys.exit(1)
        else:
            print(f"Command failed but ignoring: {command}")

def gen_data():
    """Generate dummy data."""
    run_command("python3 data_gen/generate_data.py")

def setup_solr():
    """Setup and start Solr."""
    run_command("./scripts/setup_solr.sh")

def index():
    """Run Spark indexing job."""
    run_command("spark-submit --conf spark.jars.ivy=/tmp/antigravity_ivy --packages com.lucidworks.spark:spark-solr:4.0.0 spark_job/index_to_solr.py")

def stop_solr():
    """Stop Solr."""
    # Solr path might vary if version changes, but hardcoded for now based on Makefile
    run_command("./solr-dist/solr-9.7.0/bin/solr stop -all", ignore_errors=True)

def clean():
    """Clean generated data."""
    run_command("rm -rf data")

def run_all():
    """Run all steps."""
    gen_data()
    setup_solr()
    index()

COMMANDS = {
    "gen-data": gen_data,
    "setup-solr": setup_solr,
    "index": index,
    "stop-solr": stop_solr,
    "clean": clean,
    "all": run_all,
}

def print_usage():
    print("Usage: python manage.py <command>")
    print("\nAvailable commands:")
    for cmd, func in COMMANDS.items():
        print(f"  {cmd:<12} {func.__doc__}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1]
    if command not in COMMANDS:
        print(f"Unknown command: {command}")
        print_usage()
        sys.exit(1)
    
    COMMANDS[command]()
