.PHONY: all gen-data setup-solr index stop-solr clean verify-indexing-worked help restart-solr check-env clean-all format lint lint-fix typecheck qa precommit
.DEFAULT_GOAL := help
# Run the full pipeline: Generate data -> Setup Solr -> Index
all: gen-data setup-solr index

# Generate dummy JSON data using Faker
gen-data:
	@if ./scripts/check_data_exists.sh 2>/dev/null; then \
		echo "⏭️  Skipping data generation (data already exists)"; \
	else \
		echo "Generating data..."; \
		uv run python3 data_gen/generate_data.py; \
	fi

# Download (if needed) and start Solr 8.11.3, creating the dummy_data collection
setup-solr:
	@if ./scripts/check_solr_running.sh 2>/dev/null; then \
		echo "⏭️  Skipping Solr setup (already running)"; \
	else \
		echo "Setting up Solr..."; \
		./scripts/setup_solr.sh; \
	fi

# Run the PySpark job to index data into Solr
# Uses local Ivy cache (~/.ivy2) to speed up dependency resolution
index:
	@if uv run python3 scripts/check_indexing_complete.py 2>/dev/null; then \
		echo "⏭️  Skipping indexing (data already indexed)"; \
	else \
		echo "Indexing data..."; \
		JAVA_HOME=$$(jenv prefix) uv run spark-submit --conf spark.jars.ivy=$(HOME)/.ivy2 --conf spark.jars.ivySettings=$(PWD)/scripts/ivysettings.xml --packages com.lucidworks.spark:spark-solr:4.0.0 spark_job/index_to_solr.py; \
	fi

# Stop the Solr server
stop-solr:
	./solr-dist/solr-8.11.3/bin/solr stop -all

# Remove generated data files
clean:
	rm -rf data

# Verify that documents were successfully indexed by querying Solr
verify-indexing-worked:
	@uv run python3 scripts/verify_indexing.py

# Restart Solr (Stop -> Start)
restart-solr: stop-solr setup-solr

# Verify that Java 17 and Python 3.8+ are correctly configured
check-env:
	@echo "Checking environment..."
	@java -version 2>&1 | grep "version \"17" > /dev/null || (echo "Error: Java 17 is required"; exit 1)
	@python3 --version | awk '{print $$2}' | awk -F. '{if ($$1 < 3 || ($$1 == 3 && $$2 < 8)) exit 1}' || (echo "Error: Python 3.8+ is required"; exit 1)
	@echo "Environment OK"

# Deep clean: Remove data, Solr distribution, and Ivy cache
clean-all: clean stop-solr
	rm -rf solr-dist
	rm -rf $(HOME)/.ivy2

# Format code with Ruff
format:
	uv run ruff format .

# Lint code with Ruff
lint:
	uv run ruff check .

# Lint and auto-fix issues
lint-fix:
	uv run ruff check --fix .

# Type check with mypy
typecheck:
	uv run mypy data_gen/ spark_job/

# Run all code quality checks
qa: lint typecheck
	@echo "✓ All quality checks passed"

# Run all pre-commit hooks
precommit:
	uv run pre-commit run --all-files

# List all available targets
help:
	@echo "Available targets:"
	@echo "  all                   : Run full pipeline (gen-data, setup-solr, index)"
	@echo "  gen-data              : Generate dummy data"
	@echo "  setup-solr            : Download and start Solr"
	@echo "  index                 : Run Spark indexing job"
	@echo "  stop-solr             : Stop Solr"
	@echo "  restart-solr          : Restart Solr"
	@echo "  check-env             : Verify Java 17 and Python 3.8+"
	@echo "  clean                 : Remove generated data"
	@echo "  clean-all             : Remove data, Solr, and Ivy cache"
	@echo "  verify-indexing-worked: Verify documents in Solr"
	@echo ""
	@echo "Code Quality:"
	@echo "  format                : Format code with Ruff"
	@echo "  lint                  : Lint code with Ruff"
	@echo "  lint-fix              : Lint and auto-fix issues"
	@echo "  typecheck             : Type check with mypy"
	@echo "  qa                    : Run all quality checks"
	@echo "  precommit             : Run all pre-commit hooks"
