# arxiv-knowledge-repo

## Creating a sample subset

To extract only the `cs` papers from the [metadata dataset on kaggle](https://www.kaggle.com/Cornell-University/arxiv) we can pipe the file through `jq`
```sh
# get all the papers from Computer Science
jq '. | select(.categories | test("cs.(AI|AL|CC|CE|CG|GT|CV|CY|CR|DB|DB|DL|DM|DC|ET|FL|GL|AR|HC|IR|IT|LO|LG|MS|MA|MM|NI|NE|NA|OS|OH|PF|PL|RO|SI|SE|SD|SC|SY)")) | .' arxiv-metadata-oai-snapshot.json > arxiv-sample.json

# filter the papers by year of first publishing
jq 'select(.versions[]| select(.version | test("v1$")) .created | test("2010|2011|2012|2013|2014|2015|2016|2017|2018|2019|2020|2021")) ' arxiv-sample.json > arxiv-sample-by-date.json

# get just the first 100 records
jq -s '.[:100]' arxiv-sample-by-date.json > arxiv-sample-cs.json
```

## Running the elastic stack locally

The application requires an available elasticsearch and kibana. An easy way to provision this is to use `docker` with `docker-compose` with the provided `docker-compose.yml`. To get started

1. `git clone` the repository
2. Ensure `docker` and `docker-compose` are installed. It is also possible to use `podman` with the respective compose command.
```
➜  arxiv-knowledge-repo git:(main) ✗ docker -v
Docker version 20.10.7, build 20.10.7-0ubuntu5~21.04.2
➜  arxiv-knowledge-repo git:(main) ✗ docker-compose -v
docker-compose version 1.25.0, build unknown
```
3. Run `docker-compose up` from the root directory of the repository. This will provision a three node elastic cluster with kibana. For troubleshooting steps see the [Elastic Getting Started Guide with Docker](https://www.elastic.co/guide/en/elastic-stack-get-started/current/get-started-docker.html) and the [podman homepage](https://podman.io/)
4. Once provisioned you can use `curl` to verify the cluster is up
```
➜  arxiv-knowledge-repo git:(main) ✗ curl -X GET "localhost:9200/_cat/nodes?v&pretty"
ip         heap.percent ram.percent cpu load_1m load_5m load_15m node.role   master name
172.18.0.5           61          96  10    1.81    2.27     2.38 cdfhilmrstw *      es01
172.18.0.2           22          96  10    1.81    2.27     2.38 cdfhilmrstw -      es03
172.18.0.3           50          96  10    1.81    2.27     2.38 cdfhilmrstw -      es02
```
5. Now the elasticsearch API should be available via `http://localhost:9200/` and the kibana interface should be reachable via `http://localhost:5601/`


## Building Knowledge Repo and Loading data

Run `main.py` with the required arguments.

```
-h                       for help
-i index_name            to create new index
-s schemapath            path to schema definition file
-d datapath              path to data file
-p port                  server port number (default -9200)
```

*Run the following command to create an index 'arxiv' and load the data*

`python3 main.py -i arxiv -s meta/schema.json -d data/arxiv-sample-cs.json`

## Quantitative Evaluation

```sh
# Evaluate the total time taken to ingest json document
time -p python3 main.py -i test -s meta/schema.json -d data/arxiv-sample-cs.json
# Evaluate the total time taken to run queries on kibana dashboard
time -p bash query_time.sh
```