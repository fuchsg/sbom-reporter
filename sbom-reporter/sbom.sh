#!/bin/bash

product="ngcp"
version="$(cat /etc/ngcp_version)"
timestamp="$(date +'%Y%m%d-%H%M%S')"

#sbomformat='spdx'
#sbomformatextension='spdx'
sbomformat='cyclonedx'
sbomformatextension='cdx'

basefilename="$product-$version-$timestamp"

distro2sbom \
  --distro deb \
  --system \
  --format json \
  --sbom "$sbomformat" \
  --product-type application \
  --product-name "$product" \
  --product-version "$version" \
  --product-author "sipwise" \
  --output-file "$basefilename.$sbomformatextension.json"

sbomaudit \
  --input-file "$basefilename.$sbomformatextension.json" \
  --output-file "$basefilename-sbomaudit.json"
