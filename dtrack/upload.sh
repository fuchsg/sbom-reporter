#!/bin/bash

curl -v -X POST "http://localhost:8080/api/v1/bom" \
  -H "X-Api-Key: $DTRACK_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F "projectName=NGCP" \
  -F "projectVersion=mr13.2" \
  -F "autoCreate=true" \
  -F "bom=@$1;type=application/json"
