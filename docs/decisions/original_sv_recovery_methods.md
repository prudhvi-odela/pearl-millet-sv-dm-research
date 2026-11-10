# Methods and sources

Read-only audit on 2026-10-22 UTC in the original Linux project directory. Five user-specified candidates only. No source files changed, no 74 GB VCFs downloaded, no raw reads processed, no genotypes inferred, and no association tests run.

The included script scans all worksheets in data/raw/Yan2023_Supplementary_Tables.xlsx for exact candidate strings, extracts S19 VariationID rows, verifies the expected chromosome/position/type, and cross-checks exact VariationID records in local MilletDB CSV/JSON. It reads the prior event-recovery output, API schema, source manifest and cohort validation artifacts; outputs in this timestamp folder are new. No fuzzy alias matching was used.

Primary sources:
- Yan et al. 2023 article and data availability: https://www.nature.com/articles/s41588-023-01302-4
- Yan et al. Supplementary tables source: https://static-content.springer.com/esm/art%3A10.1038%2Fs41588-023-01302-4/MediaObjects/41588_2023_1302_MOESM3_ESM.xlsx
- MilletDB resource description: https://onlinelibrary.wiley.com/doi/10.1111/pbi.14136
- 2026 WGS and phenotype dataset paper: https://doi.org/10.1016/j.dib.2026.112746
- Zenodo dataset: https://zenodo.org/records/18602603
- PI537069 GenBank record: https://www.ncbi.nlm.nih.gov/nuccore/JAIFIR000000000
- 2023 platinum assembly files: https://doi.org/10.6084/m9.figshare.21261129.v1
- MilletDB API base: http://milletdb.novogene.com/api

The article data-availability section lists assembly accessions and raw read projects; it does not identify a downloadable graph/SV genotype matrix accession. The Nature paper methods say reads from SRP063925 were genotyped against the graph. The local MilletDB API schema lists GET endpoints /mongo/var/ and /mongo/var_detail/ with no documented query parameters. A direct GET to /api/mongo/var_detail/ timed out after 15 s; the query result is therefore unknown, not a negative variant search.

Local input sizes and SHA256 are recorded in checksums.sha256. The prior audit data/source manifests are references and were not modified. Software: Python 3.11.15; openpyxl 3.1.5; platform Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.39.
