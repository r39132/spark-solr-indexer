.PHONY: all gen-data setup-solr index stop-solr clean

all: gen-data setup-solr index

gen-data:
	python3 data_gen/generate_data.py

setup-solr:
	./scripts/setup_solr.sh

index:
	spark-submit --conf spark.jars.ivy=/tmp/antigravity_ivy --packages com.lucidworks.spark:spark-solr:4.0.0 spark_job/index_to_solr.py

stop-solr:
	./solr-dist/solr-9.7.0/bin/solr stop -all

clean:
	rm -rf data
