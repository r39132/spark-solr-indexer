# 🚀 Spark Solr Indexer

A production-ready data pipeline that generates synthetic data and indexes it into Apache Solr using Apache Spark. Supports both local development and cloud deployment on Google Cloud Platform.

## ✨ Features

- 🎲 **Synthetic Data Generation** – Create realistic test data with Faker
- ⚡ **Spark-powered Indexing** – Fast, distributed data processing
- 🏠 **Local Development** – Quick setup with local Solr and Spark
- ☁️ **Cloud Deployment** – Full GCP integration with Dataproc and Compute Engine
- 📊 **Interactive Notebooks** – Step-by-step Jupyter workflows
- 🛠️ **Make Automation** – One-command pipeline execution

## 📋 Prerequisites

### For Local Development
- **Python 3.12+**
- **uv** – [Install](https://github.com/astral-sh/uv)
- **Java 11 or 17** – For Solr and Spark
- **Apache Spark** – In your PATH
- **jenv** (optional) – [Install](https://www.jenv.be/)

### For Cloud Deployment
- **Google Cloud SDK** – `gcloud` CLI
- **GCP Project** with billing enabled
- **APIs enabled**: Dataproc, Compute Engine, Cloud Storage

## 🚀 Quick Start

### Local Pipeline (Make)

Run the complete pipeline in one command:

```bash
make all
```

This will:
1. Generate synthetic data
2. Download and start Solr
3. Index data with Spark
4. Verify indexing

**Other useful commands:**
```bash
make help              # See all available commands
make verify-indexing   # Check if data was indexed
make stop-solr         # Stop Solr server
make clean-all         # Reset everything
```

### Interactive Notebooks

Choose your deployment target:

#### 🏠 Local Development (`pipeline_local.ipynb`)

Perfect for local testing without cloud costs.

```bash
uv run jupyter notebook notebooks/pipeline_local.ipynb
```

**What it does:**
- ✓ Verifies Java/Spark environment
- ✓ Generates synthetic data
- ✓ Starts local Solr (port 8983)
- ✓ Indexes data with local Spark
- ✓ Runs verification queries

**Requirements:** Java 11/17, Spark in PATH, Python 3.12+

#### ☁️ GCP Cloud (`pipeline_gcp.ipynb`)

Production-scale deployment on Google Cloud Platform.

**Setup:**
```bash
cp .env.example .env      # Copy template
# Edit .env with your GCP settings
uv run jupyter notebook notebooks/pipeline_gcp.ipynb
```

**What it does:**
- ✓ Authenticates with GCP
- ✓ Creates Cloud Storage bucket
- ✓ Provisions Solr VM (Compute Engine)
- ✓ Creates Dataproc cluster
- ✓ Uploads and indexes data
- ✓ Verifies results
- ⚠️ **Cleanup resources to avoid charges!**

**Costs:** ~$0.60-1.20/hour when running (Dataproc + VM + Storage)

**Configuration:** Edit `.env` file with your GCP project ID, region, and preferences. The notebook loads settings automatically.



## 🧹 Code Quality

This project uses modern Python tooling for code quality:

- **[Ruff](https://github.com/astral-sh/ruff)** – Ultra-fast linter and formatter
- **[mypy](https://mypy-lang.org/)** – Static type checker
- **[pre-commit](https://pre-commit.com/)** – Git hooks for automated checks

### Setup

Install dev dependencies and pre-commit hooks:

```bash
uv sync --dev              # Install all dependencies including dev tools
uv run pre-commit install  # Set up git hooks
```

### Usage

```bash
# Format code
uv run ruff format .

# Lint and auto-fix
uv run ruff check --fix .

# Type check
uv run mypy data_gen/ spark_job/

# Run all pre-commit hooks manually
uv run pre-commit run --all-files
```

Pre-commit hooks will automatically run on `git commit` to ensure code quality.

## 🛠️ Make Commands

### Pipeline Commands

| Target | Description |
|--------|-------------|
| `make all` | Run full pipeline (gen-data → setup-solr → index) |
| `make gen-data` | Generate dummy JSON data |
| `make setup-solr` | Download and start Solr |
| `make index` | Run Spark indexing job |
| `make verify-indexing-worked` | Verify documents in Solr |
| `make stop-solr` | Stop Solr server |
| `make restart-solr` | Restart Solr |
| `make check-env` | Verify Java 17 and Python 3.8+ |
| `make clean` | Remove generated data |
| `make clean-all` | Remove data, Solr, and Ivy cache |

### Code Quality Commands

| Target | Description |
|--------|-------------|
| `make format` | Format code with Ruff |
| `make lint` | Lint code with Ruff |
| `make lint-fix` | Lint and auto-fix issues |
| `make typecheck` | Type check with mypy |
| `make qa` | Run all quality checks (lint + typecheck) |
| `make precommit` | Run all pre-commit hooks |

## ⚙️ Configuration

### Environment Variables (.env)

For GCP deployments, configure your settings in `.env`:

```bash
cp .env.example .env    # Copy template
# Edit .env with your settings
```

**Key variables:**
- `GCP_PROJECT_ID` – Your GCP project
- `GCP_REGION` – Deployment region (e.g., us-central1)
- `GCS_BUCKET_NAME` – Cloud Storage bucket
- `DATAPROC_WORKER_COUNT` – Number of Spark workers
- `SOLR_VM_NAME` – Solr VM instance name

💡 See `.env.example` for all available options.

⚠️ **Never commit `.env`** – it's gitignored and contains your credentials.

## 📁 Project Structure

```
spark-solr-indexer/
├── data_gen/          # Synthetic data generation
├── spark_job/         # PySpark indexing jobs
├── scripts/           # Solr management scripts
├── notebooks/         # Jupyter workflows
│   ├── pipeline_local.ipynb   # Local development
│   └── pipeline_gcp.ipynb     # Cloud deployment
├── .env.example       # GCP configuration template
├── Makefile          # Task automation
└── pyproject.toml    # Python dependencies
```

## ⚡ Performance

### Dependency Caching

Spark downloads ~240 dependencies from Maven Central on first run.

**First run:** 2-5 minutes (downloads and caches JARs to `~/.ivy2/`)

**Subsequent runs:** Near-instant (uses cached JARs)

**Optional pre-caching:**
```bash
./scripts/cache_dependencies.sh  # Download dependencies ahead of time
```

## License

MIT
