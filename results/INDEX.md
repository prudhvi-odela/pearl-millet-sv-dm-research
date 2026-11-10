# Results index

All artifacts below were copied from the project mirror or named result-package archives. They are retained as reported outputs; no analyses were rerun during repository assembly.

## Reports and decisions

- `results/master_execution_report.md` — scope of completed work, principal findings and blocked analyses.
- `results/master_project_status.md` — verified project status from the consolidated execution package.
- `results/cohort_validation_report.md` — cohort join, sample count and association feasibility report.
- `results/association_feasibility_report.md` — updated cohort and five-SV feasibility findings.
- `results/publication_readiness_report_2026-10-22.md` — publication-readiness decision and recommended next analysis.
- `results/phenotype_model_and_descriptive_results.md` — descriptive analysis interpretation and modeling constraints.

## Candidate evidence

- `data/processed/five_candidate_evidence.tsv` — curated five-candidate evidence and score context.
- `data/processed/five_candidate_novelty.tsv` — novelty scope, other-trait evidence, legacy counts, and limits.
- `results/five_sv_updated_evidence.tsv` — updated consolidated evidence status.
- `results/candidate_variant_definition_audit.tsv` and `results/sv_event_definition_audit.tsv` — unresolved event identity and definition records.
- `results/crosswalk_status_summary.tsv` — summarized cohort/crosswalk checks.

## Phenotype and feasibility outputs

- `results/phenotype_site_recomputed.tsv` — site-level descriptive summary from the execution package.
- `results/phenotype_site_rank_correlations.tsv` — pairwise rank concordance of accession summaries between sites.
- `results/phenotype_summary.txt` — concise descriptive result and interpretation boundary.
- `results/phenotype_summary_by_site.tsv` — site summary from the later consolidated audit.
- `results/phenotype_qc_summary.tsv` — phenotype QC summary; inspect its fields before reusing.
- `results/statistical_power_assessment.tsv` — planning calculation for a hypothetical scan; not a power result for a fitted model.
- `results/validation_checks.txt` — recorded validation checks from the cohort package.

## Source packages represented

Selected text, scripts, schemas, and small aggregate outputs were curated from `pearl_millet_complete_research_execution.zip`, `pearl_millet_ultimate_execution_20261022.zip`, and `pearl_millet_2026_cohort_validation.zip`. Source archives are not copied into this repository to avoid duplicate bundles and embedded source workbooks. Their available names and exclusions are documented in `docs/SOURCE_PROVENANCE.md`.

## Additional decision records and scripts

- `docs/decisions/task13_research_route.md`, `task14_sv_recovery.md`, and `task15_research_direction.md` preserve the sequential stop/go decisions.
- `docs/decisions/original_sv_recovery_methods.md` records event recovery scope; `public_data_validation_limitations.md` records validation boundaries; `climate_reassessment.md` records why climate analysis was not ready.
- `results/research_direction_comparison.tsv`, `results/task15_research_direction_comparison.tsv`, `results/event_definition_recovery.tsv`, `results/cohort_crosswalk_assessment.tsv`, and `results/candidate_event_definition.tsv` preserve selected support tables.
- `methods/SCRIPT_INVENTORY.md` explains each included script and its missing inputs. `docs/archive_inventory.tsv` lists all members from available ZIP archives and their curation disposition.
