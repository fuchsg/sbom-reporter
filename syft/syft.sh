#!/bin/bash

product="ngcp"
version="$(cat /etc/ngcp_version)"
timestamp="$(date +'%Y%m%d-%H%M%S')"

basefilename="$product-$version-$timestamp"

syft scan dir:/ \
  --config syft.yml \
  --select-catalogers debian \
  --source-name "$product" \
  --source-version "$version" \
  -o cyclonedx-json="$basefilename.cdx.json"
