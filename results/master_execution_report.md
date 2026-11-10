# Complete research execution report

## Execution completed

Read and reused the master/ultimate cohort audits and Task 13–15 packages; verified prior package checksums; confirmed the five PGLA rows and their missing event/call fields; reviewed primary pangenome, disease QTL/GWAS, phenotype cohort and climate-source evidence; inspected current disk/RAM/CPU and available tools; wrote machine-readable schemas and a future-input validator; self-tested the validator with temporary synthetic records only; recomputed a descriptive four-site phenotype summary and pairwise accession rank correlations for the exact 231-accession matched subset. Source files and prior outputs were not modified.

## Results and blocked work

- **Five SVs:** all five are catalogued association markers in Yan S19/external contexts; none has an event-resolved allele/PAV record or matched cohort genotype. No SV test was performed. Existing catalogue status means they are not novel variants; no direct DMY association was established in checked tables. They are not biologically disproven.
- **Disease GWAS/replication:** 231 sequenced accessions exactly match phenotype data; 2,772 plots are repeated observations, not independent genotypes. A GWAS was not run. There is no local SNP VCF, QC/PC/kinship matrix or powered model. The two public reference-specific callsets are approximately 32.43/41.42 GB, are SNP-only and have no index listed in the audited metadata. Denominator counts are missing from the phenotype table. Confirmatory GWAS is NO-GO; exploratory scan remains conditional.
- **Disease phenotype:** observed values are bounded incidence ratios with many zeros and exact ones, over four sites and three reps. Site means range substantially; current descriptive analysis reports rank concordance across sites. No inferential genotype association or pathotype claim follows. Sharma 2015's article abstract describes 238 mini-core accessions x eight pathotypes and 62 multi-pathotype-resistant accessions, but the local metadata file is header-only and is not the full accession-level table.
- **Climate:** coordinate provenance and uncertainty unresolved (148/231 only, strong Senegal skew). No climate download or GEA was run. Coordinates cannot be assumed to be collection origins.
- **Literature:** DM QTL, marker-assisted selection, a Senegal 77-genotype GWAS thesis and breeding-panel GWAS all predate this work. No “first” claim is justified.

## Current conclusion

Strongest supported finding: the project has a reproducible 231-accession multi-site DM phenotype/WGS overlap and a high-confidence audit showing that the five candidate PGLA IDs are not currently testable as DM SVs. The only additional biological data result generated here is descriptive accession ranking across sites. No resistance variant, causal gene, climate adaptation or new association has been demonstrated.

Primary next research direction: a gated exploratory SNP-based multi-environment DMY analysis on one reference build, only after phenotype-model and genotype-QC/structure gates pass. The smallest high-value dependencies are denominator provenance (or a justified ratio model) and a validated, QCed genotype matrix with PCs/kinship. Separately, the user may send the prepared SV data request; no message was sent.
