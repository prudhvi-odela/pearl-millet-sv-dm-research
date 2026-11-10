# Prespecified candidate model specification (not executed)

Use one accession-level adjusted DM mean per site, estimated from the three plot replicates with site block/replicate nuisance terms. Analyze the four site-specific traits separately with a kinship-aware linear mixed model: accession phenotype as response, additive SNP dosage and prespecified ancestry PCs as fixed effects, genomic kinship as random covariance. Replicate plots contribute to entry-mean precision; they are not counted as independent genotypes. This avoids assuming binomial counts from a proportion with absent denominators.

Check boundary-heavy per-site means, residual distribution, heteroskedasticity and calibration before any scan. If Gaussian MLM assumptions fail and no validated bounded-response kinship model is available, stop. A secondary cross-site consistency/meta-analysis may combine site-specific effects, but all four environments must be included in the family-wise testing burden. Adjust using Bonferroni over actual QC-passed markers x four sites; BH FDR is descriptive secondary. Report effect estimates, SE, allele frequency, call count and QQ calibration. Before execution, simulate power using actual MAF, missingness and accession/site design.

This is a candidate protocol, not a validated or executed analysis.
