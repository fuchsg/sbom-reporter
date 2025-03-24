#!/bin/bash

product="ngcp"
version="$(cat /etc/ngcp_version)-$(date +'%Y%m%d')"

distro2sbom \
  --distro deb \
  --system \
  --format json \
  --sbom spdx \
  --product-type application \
  --product-name "$product" \
  --product-version "$version" \
  --product-author "sipwise" \
  --output-file "$product-$version.spdx.json"

sbomaudit \
  --input-file "$product-$version.spdx.json" \
  --output-file "$product-$version-sbomaudit.json"
