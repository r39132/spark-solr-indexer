# Spark Solr Indexer: Solr Data Pipeline

A complete data pipeline project that generates synthetic data, sets up a local Apache Solr instance, and indexes data using Apache Spark.

## Features

*   **Data Generation**: Creates realistic dummy data using `Faker`.
*   **Automated Infrastructure**: Downloads and configures a local Solr Cloud instance.
*   **Spark Integration**: Uses `spark-solr` to index data efficiently.

## Prerequisites

*   **Python 3.8+**
*   **uv** (Dependency Manager) - [Install uv](https://github.com/astral-sh/uv)
*   **Java 8/11/17** (Required for Solr and Spark)
*   **jenv** (Java Version Manager) - [Install jenv](https://www.jenv.be/)
*   **Apache Spark** (Installed and available in PATH)
*   **Google Cloud SDK** (`gcloud` CLI) - Required for Notebook GCP integration

## Quick Start

Ensure you have the correct Java version set:
```bash
jenv local 17.0
```

You can run the entire pipeline (Generate -> Setup Solr -> Index) with a single command. Choose your preferred method:

### Option 1: Using Make (Recommended)
```bash
make all
```
**Note:** Running `make` without arguments will invoke the `help` target, which lists all available commands.


### Option 2: Using Jupyter Notebooks (Interactive)

We provide two notebook options depending on your deployment target:

#### 2a. Local Development Notebook (`pipeline_local.ipynb`)
Perfect for local development and testing without cloud dependencies.

**Prerequisites:**
- Java 8/11/17 installed
- Apache Spark installed and in PATH
- Python 3.12+ with dependencies (`uv sync`)

**To run:**
```bash
uv run jupyter notebook notebooks/pipeline_local.ipynb
```

**Features:**
- Uses local Spark (`--master "local[*]"`)
- Uses local Solr (port 8983)
- Built-in environment verification
- Status checks and sample data display
- No cloud costs

**Workflow:**
1. Check Java/Spark environment
2. Generate dummy data locally
3. Setup local Solr instance
4. Index data with local Spark
5. Verify indexing with sample queries
6. Optional cleanup

#### 2b. GCP Cloud Notebook (`pipeline_gcp.ipynb`)
Designed for production-scale cloud deployments using Google Cloud Platform.

**Prerequisites:**
- Google Cloud SDK (`gcloud`) installed
- GCP project with billing enabled
- APIs enabled: Dataproc, Compute Engine, Cloud Storage
- Appropriate IAM permissions

**Setup:**
1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and set your GCP project details:
   ```bash
   GCP_PROJECT_ID=your-project-id
   GCP_REGION=us-central1
   # ... other settings
   ```

**To run:**
```bash
uv run jupyter notebook notebooks/pipeline_gcp.ipynb
```

**Configuration:**
The notebook automatically loads settings from `.env` file. You can also override values in the notebook if needed.

**Features:**
- Uses **GCP Dataproc** for distributed Spark processing
- Creates **Compute Engine VM** running Solr
- Stores data in **Cloud Storage (GCS)**
- Automated infrastructure provisioning
- Firewall and networking configuration
- Complete resource cleanup section

**Workflow:**
1. Authenticate with GCP
2. Create GCS bucket
3. Generate and upload data to GCS
4. Create Solr VM on Compute Engine
5. Create Dataproc cluster
6. Submit Spark job to Dataproc
7. Verify indexing on cloud Solr
8. Cleanup resources (important!)

**Cost Estimation:**
- Dataproc Cluster: ~$0.50-1.00/hour
- Solr VM: ~$0.10-0.20/hour
- Storage: ~$0.02/GB/month
- Network: Variable

⚠️ **Important:** Remember to run the cleanup section in the notebook to avoid ongoing charges!

### 5. Cleanup
Stops Solr and removes the entire `data` directory (all generated data).
```bash
make stop-solr
make clean
```

## Make Targets Reference

| Target | Description | When to use |
|--------|-------------|-------------|
| `make all` | Runs `gen-data`, `setup-solr`, and `index`. | To run the full pipeline in one go. |
| `make gen-data` | Generates dummy JSON data. | When you need fresh test data. |
| `make setup-solr` | Downloads and starts Solr. | To start the Solr server. |
| `make index` | Runs the Spark indexing job. | To index data into Solr. |
| `make verify-indexing-worked` | Queries Solr for document counts. | To confirm indexing succeeded. |
| `make stop-solr` | Stops the Solr server. | When finished working. |
| `make restart-solr` | Stops and starts Solr. | If Solr becomes unresponsive. |
| `make check-env` | Verifies Java/Python versions. | Before running the pipeline to check prerequisites. |
| `make clean` | Removes generated data. | To clear old data files. |
| `make clean-all` | Removes data, Solr, and cache. | To completely reset the project state. |
| `make help` | Lists available targets. | When you need a quick reminder of commands. |

## Configuration Files

### Environment Variables (GCP Notebook)

The GCP notebook uses environment variables for configuration management:

- **`.env.example`** - Template file with placeholder values (committed to git)
  - Contains all required configuration variables with example values
  - Safe to commit and share with collaborators

- **`.env`** - Your personal configuration file (gitignored)
  - Copy from `.env.example`: `cp .env.example .env`
  - Edit with your actual GCP project settings
  - **Never commit this file** - it contains your project-specific values
  - Automatically loaded by the GCP notebook using `python-dotenv`

**Configuration Variables:**
```bash
GCP_PROJECT_ID=your-project-id          # Your GCP project ID
GCP_REGION=us-central1                  # Preferred GCP region
GCP_ZONE=us-central1-a                  # Specific zone for VMs
GCS_BUCKET_NAME=your-bucket-name        # Cloud Storage bucket
DATAPROC_CLUSTER_NAME=spark-solr-cluster # Dataproc cluster name
DATAPROC_WORKER_COUNT=2                 # Number of worker nodes
SOLR_VM_NAME=solr-instance              # Solr VM name
# ... and more (see .env.example)
```

**Quick Setup:**
```bash
# 1. Copy the template
cp .env.example .env

# 2. Edit with your settings
nano .env  # or use your preferred editor

# 3. Run the notebook
uv run jupyter notebook notebooks/pipeline_gcp.ipynb
```

The notebook will automatically load your configuration on startup.

## Project Structure

*   `data_gen/`: Python scripts for generating synthetic JSON data.
*   `spark_job/`: PySpark jobs for data processing.
*   `scripts/`: Shell scripts for Solr management and verification.
*   `notebooks/`: Jupyter notebooks for interactive pipeline execution.
*   `.env.example`: Template configuration file for GCP deployments.
*   `Makefile`: Main task runner configuration.

## Performance Optimization

### Dependency Caching

The Spark job uses the `spark-solr` connector along with ~240 transitive dependencies from Maven Central. To avoid re-downloading these JARs on every run, the project is configured to cache them in `~/.ivy2/`.

**First Run:**
- **Expect 2-5 minutes** for Spark to resolve and download all dependencies
- You'll see many `found <artifact> in central` messages
- JARs are saved to `~/.ivy2/cache/` and `~/.ivy2/jars/`

**Subsequent Runs:**
- **Near-instant startup** – Spark uses the locally cached JARs
- Only a quick resolution check happens (no downloads)

**Optional: Pre-cache dependencies**

To download everything ahead of time without running the full job:

```bash
./scripts/cache_dependencies.sh
```

This one-time script populates your Ivy cache, making your first real `make index` run much faster.

## License

MIT
