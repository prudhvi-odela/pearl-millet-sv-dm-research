# Phenotype model assessment

DM is a bounded 0-1 incidence ratio with many exact zeros and some ones; source workbook has no infected/total counts. A binomial or beta-binomial likelihood cannot be reconstructed without denominators. Standard beta regression also excludes exact boundary values unless a boundary-inflated model is specified.

Plots are repeated within accession and site, with replicate/block structure; genotype is constant per accession. Do not count 2,772 observations as independent genotype samples. Site means differ greatly (see phenotype_summary_by_site.tsv), so a pooled raw mean without site adjustment is confounded by environment.

If downstream analysis proceeds, first evaluate fractional-logit quasi-likelihood with site and replicate/block fixed effects, ancestry PCs, accession-clustered uncertainty and genotype-by-site sensitivity; this can admit 0/1 fractions but assumes the ratio is meaningful at equal observation weight and does not recover denominator precision. Alternatively use a multivariate/accession-by-site phenotype with a mixed model and explicit kinship; two-stage BLUP analysis must account for first-stage uncertainty. The final model is not selected until distribution, residual/calibration and genotype QC are reviewed. Site-specific analyses should be secondary and corrected for multiplicity.
