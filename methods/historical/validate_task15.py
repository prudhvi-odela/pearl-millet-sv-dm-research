#!/usr/bin/env python3
from pathlib import Path
import csv
p=Path(__file__).resolve().parent
req=["final_author_data_request.md","alternative_disease_genetics_resources.tsv","marker_validation_feasibility.md","climate_reassessment.md","research_direction_comparison.tsv","task15_final_decision.md","source_manifest.tsv","execution_log.txt"]
assert all((p/x).is_file() for x in req)
with (p/"alternative_disease_genetics_resources.tsv").open(encoding="utf-8",newline="") as f:r=list(csv.DictReader(f,delimiter="\t"))
assert len(r)>=8 and any("Subedi et al. 2026" in x["study_or_resource"] for x in r)
with (p/"research_direction_comparison.tsv").open(encoding="utf-8",newline="") as f:d=list(csv.DictReader(f,delimiter="\t"))
assert len(d)==5 and any(x["option"].startswith("E.") for x in d)
t=(p/"final_author_data_request.md").read_text()
for x in ["PGLA1542300","PGLA1557868","PGLA1564064","PGLA1457537","PGLA1545539"]: assert x in t
assert "not sent" in t.lower()
print(f"VALID: {len(req)} required outputs, {len(r)} resources, five direction options, all candidates in unsent request.")
