# Axial Blazar: Solr Data Pipeline

A complete data pipeline project that generates synthetic data, sets up a local Apache Solr instance, and indexes data using Apache Spark.

## Features

*   **Data Generation**: Creates realistic dummy data using `Faker`.
*   **Automated Infrastructure**: Downloads and configures a local Solr Cloud instance.
*   **Spark Integration**: Uses `spark-solr` to index data efficiently.
*   **Multiple Task Runners**: Choose your preferred workflow tool (`Make`, `Python`, or `Invoke`).

## Prerequisites

*   **Python 3.8+**
*   **Java 8/11** (Required for Solr and Spark)
*   **Apache Spark** (Installed and available in PATH)

## Quick Start

You can run the entire pipeline (Generate -> Setup Solr -> Index) with a single command. Choose your preferred method:

### Option 1: Using Make (Recommended)
```bash
make all
```

### Option 2: Using Python Script
```bash
python manage.py all
```

### Option 3: Using Invoke
```bash
# Requires: pip install invoke
invoke all
```

## Project Structure

*   `data_gen/`: Python scripts for generating synthetic JSON data.
*   `spark_job/`: PySpark jobs for data processing and indexing.
*   `scripts/`: Shell scripts for Solr management.
*   `Makefile`: Main task runner configuration.
*   `manage.py`: Pure Python task runner alternative.
*   `tasks.py`: Invoke task runner configuration.

## Manual Usage

If you prefer to run steps individually:

1.  **Generate Data**:
    ```bash
    make gen-data
    ```
2.  **Start Solr**:
    ```bash
    make setup-solr
    ```
3.  **Run Indexing Job**:
    ```bash
    make index
    ```
4.  **Stop Solr**:
    ```bash
    make stop-solr
    ```
5.  **Clean Up**:
    ```bash
    make clean
    ```

## License

MIT
