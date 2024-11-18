#!/bin/bash

# This script expects a container started with the following command.
# docker run -p 8983:8983 --name mia_solr -v ${PWD}:/data -d solr:9 solr-precreate drugs

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@schema.json" \
    http://localhost:8983/solr/drugs/schema

# Populate collection using mapped path inside container.
docker exec -it mia_solr bin/post -c drugs drugs.json
