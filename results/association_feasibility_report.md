# Association feasibility report

## What is now verified
The published cohort has 288 accessions with plot-level downy mildew observations and 231 with WGS. The 2026 phenotype workbook and metadata join on the workbook-defined unique GID for all 288 accessions. NCBI SRA runinfo contains 231 unique runs, BioSamples and SampleNames. Every WGS row exactly matches the Zenodo metadata by LibraryName = Library_ID, SampleName = Sample names, and the numeric suffix of LibraryName = GID. All 231 WGS accessions therefore have phenotype records. The remaining 57 are explicitly labelled Non-genotyped.

Phenotype data contain 3,456 plot records: 288 accessions, four Senegal sites, three replicates at each site, and 12 observations per accession. DM is the proportion of infected plants per plot, from 0 to 1; all 3,456 DM values are present. The workbook says nine blocks within each replicate. The workbook does not provide infected and total plant counts, only the ratio. Site means differ substantially, so site and repeated plot design must be modeled.

Three phenotype sample-name strings differ from the metadata while their GIDs match exactly: metadata SL_169 / phenotype SL169 (GID 4939), SL_28 / SL28 (4938), and SL_423 / SL423 (4940). These are flagged. Join on the documented unique GID; do not use fuzzy name correction.

## Legacy candidate-genotype overlap
No exact accession alias was found between the 2026 sample names and the reviewed Varshney Table 40 aliases or the local 238-accession mini-core crosswalk. The 2026 metadata labels 93 accessions as PMiGAP, 88 of which have WGS, but the category label is not an individual PMiGAP ID. The biological overlap with the old 20-accession PGLA genotype matrix remains unresolved; do not infer overlap or non-overlap from cohort labels.

## Candidate status
| Candidate | PI537069 coordinate and type | Carriers in old 20 | Exact call in 2026 | Test status |
|---|---|---:|---|---|
| PGLA1542300 | chr5:108807419 INS | 8/20 | No exact 2026 call | Not estimable |
| PGLA1557868 | chr6:186317093 INS | 0/20 | No exact 2026 call | Not estimable |
| PGLA1564064 | chr7:3564528 DEL | 9/20 | No exact 2026 call | Not estimable |
| PGLA1457537 | chr1:36302664 DEL | 1/20 | No exact 2026 call | Not estimable |
| PGLA1545539 | chr5:173268404 INS | 4/20 | No exact 2026 call | Not estimable |

The candidate identifiers occur in Yan et al. 2023 Supplementary Table 19, which reports chromosome, position, INS/DEL type and association context. Its Start/End fields are the surrounding 100-kb signal interval, not event breakpoints. The reviewed record does not provide event-level REF/ALT sequence, precise SV interval/length or a validated lift-over to the 843B or updated Tift references. Thus coordinate-only matching cannot establish identity. The released VCFs are filtered biallelic variant files associated with those two assemblies; they are not advertised as a PAV callset for these five identifiers. The VCFs were not downloaded or searched. No genotypes were fabricated.

PGLA1557868 was absent among the old 20 accessions, but its carrier status in the 2026 panel is unknown; do not carry that zero forward.

## Statistical design decision
No candidate association is run. Candidate genotypes and structure/kinship covariates are not available, so all five candidate tests are not estimable. The WGS-to-phenotype matched table records sequencing availability and plot phenotypes while explicitly marking all five candidate calls unavailable; it is not a candidate-genotype matrix.

Once exact alleles and candidate genotypes are established, use the plot-level repeated design with site, replicate/block and accession effects. Prefer a binomial mixed model if infected and total plant counts can be recovered. With ratios only, use a model suitable for bounded proportions with zeros and ones, and preserve site/repeated measures; do not treat 3,456 plots as independent accessions. Derive PCs/kinship from QC-filtered genome-wide SNPs or use verified structure covariates. Prespecify five candidate tests, diagnostics and family-wise/FDR correction, report effect sizes and intervals, and seek independent validation. None of these tests has been executed here.

Climate adaptation is outside this disease-cohort analysis.
