#!/usr/bin/env python3
from pathlib import Path
import csv, hashlib
root=Path(__file__).resolve().parent
need=["sv_recovery_results.tsv","sv_recovery_limitations.md","coordinate_provenance_audit.md","climate_variable_plan.tsv","climate_feasibility_decision.md","alternative_genetic_analysis_assessment.md","updated_literature_gap.md","research_direction_comparison.tsv","task13_final_recommendation.md","source_manifest.tsv","execution_log.txt"]
missing=[x for x in need if not (root/x).is_file()]
assert not missing, f"missing deliverables: {missing}"
with (root/"sv_recovery_results.tsv").open(encoding="utf-8",newline="") as f: rows=list(csv.DictReader(f,delimiter="\t"))
assert len(rows)==5 and len({r["candidate_id"] for r in rows})==5
assert all(r["definition_class"].startswith("3 - Only association-table") for r in rows)
assert all(r["start_breakpoint"]=="Unknown/not reported" for r in rows)
with (root/"climate_variable_plan.tsv").open(encoding="utf-8",newline="") as f: climate=list(csv.DictReader(f,delimiter="\t"))
assert len(climate)>=8 and all(r["status"]=="Not extracted" for r in climate)
print(f"VALID: {len(need)} required deliverables; five unique candidates; no invented event calls; {len(climate)} climate variables marked not extracted.")
