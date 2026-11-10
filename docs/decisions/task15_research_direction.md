# Task 15 final decision

## Primary direction: E — maintain the reproducibility/portfolio package while seeking better data

This is the strongest defensible choice today. The project has a validated 288-accession phenotype / 231-accession WGS reconciliation, exact within-cohort sample crosswalk, corrected five-candidate audit and explicit stop/go criteria. It does not have exact candidate SV events/calls, compatible published DMY marker alleles in this cohort, genotype QC/structure outputs or phenotype denominator provenance. The audit is useful for applications and reproducible training, but is not by itself a novel biological discovery paper.

## Conditional secondary: C — gated exploratory SNP-based disease analysis

The 2026 panel is the most promising public disease-genetics resource because it pairs four-site downy-mildew measurements with 231 exactly matched WGS accessions. This is not an immediate scan authorization. The independent N is modest for about 22 million markers; the panel has population structure; plot responses are repeated proportions without numerator/denominator in the local workbook; and genotype QC is not done. First settle phenotype denominator/model details and prespecify QC, structure, power and multiplicity. Then decide whether one-reference exploratory analysis warrants its data cost. Any result needs independent or functional follow-up.

## SV request and other routes

The revised author request is saved as `final_author_data_request.md` and remains unsent. The published article names Shilin Tian and Linkai Huang as corresponding authors. It requests exact event definitions/sequences, sample-level PAV calls and quality, reference/coordinate conventions, a sample crosswalk and any relevant DM phenotypes/associations. The user decides whether to send it. If records arrive, option A can reopen; for now the five PGLA markers remain external non-DM-context candidates, not resistance variants.

Option B is not ready because published QTL/markers are defined in different RIL or breeding panels and are not harmonized as exact alleles with 2026 genotype calls. Option D is blocked because 148 coordinate records lack verified origin provenance and uncertainty, are Senegal-skewed, and have no matched ancestry/spatial controls. No climate extraction is justified.

## Minimum work to advance toward an original contribution

1. The user decides whether to send the author request; no contact is claimed until sent and confirmed.
2. Resolve phenotype numerator/denominator provenance or justify a model for bounded plot proportions; prespecify repeated-measures/site/block handling.
3. If continuing disease genetics, choose one reference, verify VCF/sample identity, run genotype QC and derive PCs/kinship, then recalculate power before retrieval or scan.
4. For known-marker replication, obtain exact lead alleles/builds and a targeted call route; for climate, validate accession-origin coordinates first.

Do not download both large VCFs, run GWAS/GEA now, or claim resistance causality or climate adaptation.
