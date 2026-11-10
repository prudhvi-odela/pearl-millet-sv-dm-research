# Project status and limitations

## Research question and scope

The original objective was to evaluate five pearl millet PGLA structural-variant markers as candidates for downy-mildew (DM) resistance and possible climate adaptation. The work completed is a candidate evidence audit, public cohort reconciliation, descriptive phenotype summary, and feasibility assessment. It did not reach a valid candidate-association test.

## Verified results

1. **Candidate evidence:** all five candidate IDs have prior catalogued association context for traits other than DM. In the audited tables, no exact candidate-level DM match was found. Evidence is bounded by the reviewed sources and filters.
2. **Cohort reconciliation:** 288 accessions have 12 plot observations each (four sites × three replicates), totaling 3,456 rows. Exact metadata joins identify 231 WGS accessions and their 2,772 plot rows. The other 57 accessions/684 plot rows lack WGS in this cohort.
3. **Phenotype fields:** DM is supplied as an infected-plant proportion from 0 to 1. Infected and total plant counts are not provided in the audited workbook. Repeated site/replicate observations must not be treated as independent genotypes.
4. **Descriptive work:** a descriptive analysis recomputed site summaries and pairwise accession rank concordance across sites for the 231-accession WGS subset. This is not an inferential association result.
5. **Coordinate and genotype resource review:** the audited metadata lists 843B and updated-Tift SNP callsets of approximately 32.43 GB and 41.42 GB, respectively. They were not downloaded or analyzed. No genotype QC, PCs, kinship, GWAS, candidate PAV calls, or climate analysis was run.

## Five exploratory markers

| Candidate | PI537069 coordinate and type | Carriers in legacy 20-accession matrix | Interpretation |
|---|---|---:|---|
| PGLA1542300 | chr5:108807419 INS | 8/20; 1 missing | Previously catalogued; candidate calls in the 2026 cohort unknown |
| PGLA1557868 | chr6:186317093 INS | 0/20 | Zero carriers only in the legacy 20; do not extrapolate to 2026 cohort |
| PGLA1564064 | chr7:3564528 DEL | 9/20 | Previously catalogued; candidate calls in the 2026 cohort unknown |
| PGLA1457537 | chr1:36302664 DEL | 1/20 | Previously catalogued; candidate calls in the 2026 cohort unknown |
| PGLA1545539 | chr5:173268404 INS | 4/20 | Previously catalogued; candidate calls in the 2026 cohort unknown |

Coordinates are in the PI537069 namespace as recorded by the source evidence. They are not event-resolved breakpoints. Exact event identity, sequence/allele representation, event length, reference harmonization, and accession-level calls remain missing. Legacy counts are descriptive and are not association estimates.

## Decisions

- **Five-SV disease association:** not estimable with current evidence. Do not claim direct DM association, causality, resistance validation, or a novel SV.
- **Confirmatory disease GWAS:** no-go at the audited stage. A future exploratory SNP scan is conditional on a defensible repeated-measures phenotype model, a single reference build, genotype QC, structure/kinship, and power checks.
- **Climate adaptation:** untested. Recorded coordinates have incomplete coverage and unresolved biological provenance; no climate variables or GEA were analyzed.
- **Novelty:** historical DM QTL and GWAS studies exist. Avoid “first-ever” DM genetics/GWAS claims. The project-specific gap is whether these exact SV events can be defined and tested in a suitable cohort.

## Required inputs to advance

1. Authoritative event definitions for each candidate, including reference assembly, coordinate convention, interval/breakpoints, allele sequence or PAV definition, and provenance.
2. Per-accession candidate calls and a documented sample/accession crosswalk for the phenotype cohort.
3. For a broader SNP scan: a manageable, indexed, QC-filtered genotype matrix on one reference build, plus PCs/kinship and variant QC.
4. Phenotype denominator counts (infected/total plants) or a pre-justified model for bounded ratios with zeros and ones, preserving site and replicate structure.
5. A prespecified analysis plan, multiple-testing correction, effect estimates/uncertainty, diagnostics, and independent validation where feasible.

The included validator and schemas can check data formatting and cross-file consistency; they cannot prove biological identity or validate the supplied calls.

## Decision history

The available package sequence records these completed decision points:

- **Candidate evidence/scoring audit:** corrected the interpretation of Yan S13 expression context and selected-table absence; neither establishes climate evidence or variant novelty.
- **Task 13:** paused original discovery claims and prioritized authoritative event-level records and a sample crosswalk; no large VCF download or association test.
- **Task 14:** closed the five-SV recovery workstream after exact event definitions, calls, and a validated crosswalk could not be recovered; an author request was prepared but not sent.
- **Task 15:** retained the reproducibility/portfolio package as the current output; any SNP scan remains conditional on phenotype, genotype QC, structure, and power gates; climate remains blocked by coordinate provenance.
- **2026-10-22 execution:** verified/reused the cohort and candidate audits, added machine-readable schemas and a future-data validator, and recomputed descriptive site summaries/rank concordance for the 231-accession matched subset. No full GWAS or climate analysis was run.
- **Cohort validation:** reconciled 288 phenotype accessions with 231 exact WGS matches and recorded validation checks.

A later research-opportunity selection discussion evaluated unrelated human disease projects (fibrotic lung and QKI-linked pancreatic cancer). Those candidates are not Pearl millet analyses and are not included as research results here.
