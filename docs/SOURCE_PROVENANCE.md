# Source provenance and exclusions

## Materials reviewed

This consolidation was made from the writable project mirror at the current ChatGPT project mirror, especially the reports and archives listed below. The project `sources/` folder contained no files in the accessible mirror. The separate Linux path named in the request (the Linux project directory named in the request) was not reachable: that path did not exist in the Windows session, and WSL returned access denied. Therefore, this package does not claim to be a full audit of files that may exist only at that Linux location.

Selected source bundles:

- `pearl_millet_complete_research_execution.zip` — complete execution report, descriptive outputs, analysis and future-input scripts, schemas.
- `pearl_millet_ultimate_execution_20261022.zip` — consolidated status, phenotype/QC summaries, candidate/event status, power and feasibility decisions.
- `pearl_millet_2026_cohort_validation.zip` — cohort validation report, crosswalk summaries, validation checks, event-definition audit.
- Root-level `pearl_millet_2026_association_feasibility_report.md`, `pearl_millet_publication_readiness_REPORT.md`, `FINAL_5_CANDIDATE_EVIDENCE_AUDIT.tsv`, `pearl_millet_candidate_novelty_assessment.tsv`, and `SCORING_PROVENANCE_AUDIT.md`.

The referenced task 13–15, original SV recovery, publication readiness, public validation, targeted investigation, and research-opportunity packages were inventoried by archive listing. They are not duplicated here; the consolidated status reports incorporate the relevant decisions accessible in the execution summaries. This selective packaging is not a claim that every historical intermediate file has been individually reproduced or re-audited.

## Excluded materials

- Raw reads, large SNP VCFs and other large datasets.
- Original Excel workbooks and source data files embedded in archives.
- Individual-level matched plot phenotype records and full accession crosswalks.
- Duplicate ZIP archives and repeated copies of the same reports.
- Temporary extraction files, logs not needed to interpret results, and generated clutter.
- Credentials, private information, and local machine/user configuration.

No credentials or secrets were intentionally copied. This is a manual curation from available file inventories; the isolated Linux project could not be scanned.

## Task decisions and scripts

Task 13–15 final decisions, selected supporting tables, and historical reproduction/validation scripts were included under `docs/decisions/`, `results/`, and `methods/historical/`. The archive inventory records every member path in the available ZIP packages, including files excluded from this clean repository. The related later human-disease opportunity packages are deliberately out of scope for the Pearl millet repository.
