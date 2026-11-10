#!/usr/bin/env python3
"""Validate Task 14 outputs and exact candidate set."""
from pathlib import Path
import csv,hashlib
r=Path(__file__).resolve().parent
required=["event_definition_recovery.tsv","accession_level_call_availability.tsv","cohort_crosswalk_assessment.tsv","data_source_contact_assessment.md","draft_data_request.md","sv_association_feasibility.md","task14_final_decision.md","source_manifest.tsv","execution_log.txt"]
assert all((r/x).is_file() for x in required)
with (r/"event_definition_recovery.tsv").open(encoding="utf-8",newline="") as f: e=list(csv.DictReader(f,delimiter="\t"))
assert len(e)==5 and len({x["candidate_id"] for x in e})==5
assert all(x["start_breakpoint"]=="Unknown/not reported" and x["accession_presence_absence_matrix"]=="Not recovered" for x in e)
with (r/"accession_level_call_availability.tsv").open(encoding="utf-8",newline="") as f: c=list(csv.DictReader(f,delimiter="\t"))
assert len(c)==5 and all(x["status"]=="Not testable" for x in c)
print(f"VALID: {len(required)} deliverables; exactly five candidates; no inferred genotypes.")
