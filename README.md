# Pearl millet SV and downy-mildew research audit

**Status: completed feasibility and descriptive audit; original association objective remains inconclusive.**

This repository consolidates the verifiable work available in the Pearl millet research project mirror. It documents five previously catalogued structural-variant markers, reconciles a public multi-site disease phenotype cohort with WGS metadata, summarizes descriptive phenotype results, and records why candidate-level downy-mildew (DM) association testing could not be performed.

## Main findings

- The five candidates—PGLA1542300, PGLA1557868, PGLA1564064, PGLA1457537 and PGLA1545539—have prior records in non-DM trait context. They are exploratory markers, not newly discovered SVs or validated resistance variants.
- The reviewed evidence tables did not establish a direct DM association for any of the five candidates. This finite audit is not proof that no such evidence exists anywhere.
- A public cohort contains 288 accessions and 3,456 plot records across four Senegal sites and three replicates. An exact run/library/sample/GID crosswalk identifies 231 WGS accessions with 2,772 corresponding phenotype records; 57 accessions are phenotype-only.
- The generated phenotype work is descriptive: site summaries and accession-ranking concordance. Plot rows are repeated measures, not independent accessions.
- Disease GWAS was not run. No candidate SV event definitions, accession-level candidate calls, population structure matrix, or validated phenotype denominator model were available.
- No causal gene, direct downy-mildew association, or climate-adaptation result was demonstrated. Climate association analysis was not run.

See [project status and limitations](docs/PROJECT_STATUS.md), [methods and reproducibility](methods/REPRODUCIBILITY.md), and the [results index](results/INDEX.md).

## Repository map

```text
 data/processed/     Curated five-candidate evidence tables
 docs/               Status, limitations, scoring audit, decision records
 methods/            Analysis description, scripts, schemas, model notes
 references/         Evidence matrix and source bibliography/provenance
 results/            Reports, aggregate phenotype results, validation tables
```

No raw sequencing reads, large VCFs, original workbooks, credentials, or individual-level plot phenotype table are included. The included summary files are small, derived audit outputs. File-by-file descriptions are in [results/INDEX.md](results/INDEX.md).

## Reproducibility

The scripts and schemas are preserved as evidence of completed work and future input checks. Their original large/input data are not redistributed here, so the complete historical pipeline cannot be rerun from this repository alone. See [methods/REPRODUCIBILITY.md](methods/REPRODUCIBILITY.md) for dependencies, missing inputs and scope. Existing reported outputs were consolidated; they were not regenerated for this repository.

## Citation and use

Consult [references/README.md](references/README.md) for primary studies and data resources. Cite the underlying publications and dataset records for scientific claims; this repository is an audit and feasibility package, not a peer-reviewed association study. No license was inferred from unavailable upstream materials; see [LICENSE_STATUS.md](docs/LICENSE_STATUS.md).
