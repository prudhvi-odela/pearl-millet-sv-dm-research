# Phenotype model and descriptive analysis

## Verified structure

Prior QC confirms 3,456 records for 288 accessions, with 12 rows/accession (four 2024 Senegal sites x three reps); the exact WGS subset has 2,772 rows / 231 accessions, and 57 phenotype-only accessions / 684 rows were excluded from genotype analyses. In the matched 231 subset, all 2,772 DM values are present and within [0,1]; 1,946 are exact zero and 2 are exact one. The local reconciled table has no infected-plant/total-plant counts; `DM_num` is not an independently verified denominator.

Recomputed site summaries and rank correlations are in the two TSVs. Site means differ strongly in the existing summary: Nioro ≈0.340, Bambey ≈0.059, Sefa ≈0.061, Sinthiou malem ≈0.023. The site rank-correlation output measures descriptive agreement in accession ordering using site means; it is not an association test, marker effect, or adaptation test.

## Model choice gate

A binomial/beta-binomial model cannot be fit from ratios alone without denominators. Standard beta regression also cannot directly use exact 0 and 1 without boundary handling. A fractional-logit quasi-likelihood can accept boundary fractions but treats plot ratios as equally informative unless denominator weights are recovered. Repeated plot structure, site, replicate and block must be modeled, with accession-level genotype effects and PC/kinship controls. Site-specific mean differences indicate that pooled raw phenotype means are confounded by environment.

No phenotype-GWAS was run. Before a genotype scan, seek denominator metadata from existing public files/data dictionary (no contact sent) and compare fractional-logit/mixed or robust alternatives; prespecify site effects, block structure, genotype-by-site test and multiplicity. The descriptive analysis is supportive characterization only and does not add a novel resistance locus.
