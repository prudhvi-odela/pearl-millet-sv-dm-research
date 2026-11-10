# Script inventory

Scripts are preserved for provenance. Historical scripts require the original package inputs and may write outputs; they were not executed during this consolidation.

| Path | Purpose | Input status |
|---|---|---|
| `phenotype_descriptive_analysis.py` | Recomputes descriptive site summaries and accession rank concordance for the matched plot table | Original table omitted |
| `reproduce_master_execution.py` | Historical package assembly and checks | Original task/result directories omitted; not run |
| `validate_future_sv_data.py` | Structural consistency validator for future event, call, and crosswalk TSVs | Inputs are future author-provided data; optional synthetic self-test not run |
| `historical/reproduce_task13.py` | Rebuilds the Task 13 decision package | Original inputs omitted; not run |
| `historical/validate_task13.py` | Checks Task 13 package artifacts | Full package artifacts omitted; not run |
| `historical/reproduce_task14.py` | Rebuilds the Task 14 SV recovery package | Original inputs omitted; not run |
| `historical/validate_task14.py` | Checks Task 14 package artifacts | Full package artifacts omitted; not run |
| `historical/reproduce_task15.py` | Rebuilds the Task 15 direction package | Original inputs omitted; not run |
| `historical/validate_task15.py` | Checks Task 15 package artifacts | Full package artifacts omitted; not run |

The broader list of scripts that existed in all inventoried source ZIP files is available by filtering `docs/archive_inventory.tsv` to `.py`, `.R`, and `.sh` members. Not every historical helper was copied: scripts tied to omitted source datasets or duplicate intermediate packages are identified there as not selected.
