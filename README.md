This is an illustration of an SBOM creation and audit workflow on a _Debian_
system. The workflow uses external tools
[distro2sbom](https://github.com/anthonyharrison/distro2SBOM) and
[sbomaudit](https://github.com/anthonyharrison/sbomaudit), both _Python_ tools
developed by [Anthony Harrison](https://github.com/anthonyharrison).
Additionally an HTML report can be created from the audit output using the
_Python_ script `report.py` provided in here.

#### Use custom 'product' name and version

```
export product="myproduct"
export version="1.0"
```

#### Create SBOM from Debian system

https://github.com/anthonyharrison/distro2SBOM

```
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
```

#### Local SBOM audit

https://github.com/anthonyharrison/sbomaudit

```
sbomaudit --input-file "$product-$version.spdx.json"
```

There is also an online scanner:

```
curl -T "$product-$version.spdx.json" https://sbom.sh
```

#### Requirements

Install all _Python_ modules from `requirements.txt` to run everything in a
_Python_ `venv`.

```
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

#### Example Shell script

```
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
```

A summary of the script's output can be displayed using:

```
cat "$product-$version-sbomaudit.json" | jq '.summary'
```

If `jq` is installed, this will generate output like this:

```
[
  {
    "text": "NTIA Summary",
    "state": "Pass"
  },
  {
    "text": "Checks passed 8758",
    "state": "Pass"
  },
  {
    "text": "Checks failed 1151",
    "state": "Pass"
  },
  {
    "text": "Policy checks passed 0",
    "state": "Pass"
  },
  {
    "text": "Policy checks failed 0",
    "state": "Pass"
  }
]
```

#### HTML report generation

```
./report.py --sbom data/sbom.spdx.json --audit-file data/sbomaudit.json --output tmp/sbomaudit.html
```
