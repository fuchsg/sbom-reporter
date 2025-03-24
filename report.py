#!/usr/bin/env python3

import json
import pandas as pd
import argparse
from jinja2 import Environment, FileSystemLoader

def load_spdx(spdx_path):
  """ Lädt die SBOM-Daten aus einer SPDX-JSON-Datei. """
  with open(spdx_path) as f:
    spdx_data = json.load(f)
  packages = spdx_data["packages"]
  return pd.DataFrame([{
    "name": p["name"],
    "version": p.get("versionInfo", ""),
    "license": p.get("licenseConcluded", ""),
    "supplier": p.get("supplier", ""),
    "summary": p.get("summary", "")
  } for p in packages])

def load_audit(audit_path):
  """ Lädt die Audit-Daten aus einer sbomaudit-JSON-Datei. """
  with open(audit_path) as f:
    audit_data = json.load(f)
  return pd.DataFrame([{
    "name": p["name"],
    "version": p["version"],
    "audit_result": "; ".join([r["text"] for r in p.get("reports", [])]),
  } for p in audit_data["packages"]])

def render_html(spdx_df, failed_df, passing_df, output_file="sbom-report.html"):
  """ Rendert den HTML-Report basierend auf den aufbereiteten Daten. """
  total_components = len(spdx_df)
  total_failures = len(failed_df)
  quality_score = round(100 * len(passing_df) / total_components) if total_components > 0 else 100

  # Lade Template aus dem `modules`-Verzeichnis
  env = Environment(loader=FileSystemLoader("modules"))
  template = env.get_template("template.html")

  html_output = template.render(
    failed_rows=failed_df.to_dict(orient="records"),
    passing_rows=passing_df.to_dict(orient="records"),
    total_components=total_components,
    total_failures=total_failures,
    quality_score=quality_score
  )

  with open(output_file, "w") as f:
    f.write(html_output)

  print(f"✅ HTML-Report geschrieben nach {output_file}")

def main():
  parser = argparse.ArgumentParser(description="Generate HTML report from SPDX SBOM and sbomaudit output.")
  parser.add_argument("-s", "--sbom", required=True, help="SPDX JSON SBOM file")
  parser.add_argument("-a", "--audit-file", required=True, help="Audit result JSON file")
  parser.add_argument("-o", "--output", default="sbom-report.html", help="Output HTML filename")

  args = parser.parse_args()

  # Lade die Daten
  spdx_df = load_spdx(args.sbom)
  audit_df = load_audit(args.audit_file)

  # Extrahiere Pakete mit Fehlern aus dem Audit-File
  failed_packages = audit_df[["name", "version"]].drop_duplicates()
  failed_df = spdx_df.merge(failed_packages, on=["name", "version"], how="inner")

  # Extrahiere Pakete, die NICHT im Audit-File sind (also OK)
  passing_df = spdx_df.merge(failed_packages, on=["name", "version"], how="left", indicator=True)
  passing_df = passing_df[passing_df["_merge"] == "left_only"].drop(columns=["_merge"])

  # Generiere den HTML-Report
  render_html(spdx_df, failed_df, passing_df, output_file=args.output)

if __name__ == "__main__":
  main()

