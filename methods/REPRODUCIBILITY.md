# Methods and reproducibility

## Completed workflow

The consolidated work drew on existing project packages and reports. It included: (i) a targeted literature/candidate evidence audit for five fixed PGLA IDs; (ii) review of prior scoring and phenotype-label provenance; (iii) reconciliation of the 2026 phenotype workbook, metadata, runinfo and sample names using exact documented identifiers (including GID); (iv) descriptive phenotype summaries and accession rank concordance across sites for the WGS-matched subset; and (v) a feasibility review of candidate event recovery, public genotype resources, phenotype design, population structure, power, and climate data.

No fuzzy-name correction was used to establish genotype identity. Three name-string discrepancies were flagged while GID matched exactly (SL_169/SL169, SL_28/SL28, SL_423/SL423). The join is based on the documented GID/metadata relationship, not spelling similarity.

## Phenotype analysis

The analyzed WGS subset has 231 accessions × 12 plots per accession = 2,772 repeated plot rows. Summaries are descriptive. Site and replicate structure is retained in interpretation. No association p-values, genotype effect estimates, causal effects, or climate estimates were calculated. Since numerator and denominator counts are absent, a binomial model cannot be fit from the supplied proportions alone. A bounded-proportion model would need to handle exact zero and one values and repeated measures explicitly.

## Candidate variant evidence

Candidate coordinates/types were taken verbatim from reviewed evidence in the PI537069 namespace. The catalog's surrounding signal interval is not an event breakpoint. No event-level sequence or breakpoint harmonization, exact accession-level candidate genotype calls, or genotype-to-phenotype candidate matrix was available. Consequently, no candidate association test was estimable.

## Scripts and inputs

- `phenotype_descriptive_analysis.py` describes the historical computation, but requires the original 2,772-row matched plot input, which is intentionally not redistributed. It expects columns `GID`, `SITE`, `REP`, `BLOCK`, `DM` and validates expected row counts.
- `reproduce_master_execution.py` belongs to the original execution package and depends on historical input paths/data not included here. It is preserved for provenance, not guaranteed to run as-is in this curated repository.
- `validate_future_sv_data.py` and the three JSON schemas support future supplied SV event/call/crosswalk files. The validator checks structure and consistency only. Its optional self-test uses synthetic temporary records; this repository assembly did not run it.

Python environment versions for the historical execution were not fully captured in the materials available here. The descriptive script imports pandas and NumPy. The exact source workbooks and large genotype callsets are not bundled.

## Reproduction boundary

This repository is an archival consolidation, not a fully self-contained computational capsule. Reproducing the reported outputs from source requires the original public/source workbooks and data, the original package inputs, and environment information. Consult `docs/SOURCE_PROVENANCE.md` and `references/README.md`. Do not interpret a schema pass as biological validation.

The historical scripts under `methods/historical/` preserve the Task 13–15 reproduction and validation utilities. They depend on original package inputs that are not included and should be treated as provenance artifacts until those inputs and environments are restored. The repository's `docs/archive_inventory.tsv` lists archive entries reviewed and whether an artifact was selected for this package.
