# Task 13 final recommendation

## Recommendation: E — Pause original discovery claims until additional data are obtained

The five SVs remain prioritized candidates with external non-DM GWAS context, not confirmed downy mildew resistance variants. Every candidate has only an association-table ID/coordinate and INS/DEL label in the audited source; no exact event sequence, breakpoint definition, accession-level PAV matrix, or validated 2026 cohort call was recovered. There is no scientifically valid way to infer those calls from the SNP VCFs or neighboring annotations.

A climate analysis is also not ready: fewer than two-thirds of the sequenced cohort has coordinates, the coordinate source and uncertainty are undocumented, the points are geographically imbalanced, and no matched genetic structure data or climate values are available. A disease GWAS/replication is not ready either: no local compatible marker genotypes or ancestry controls exist, and the phenotype ratios lack denominator provenance. Prior DM QTL and GWAS already exist, so a “first association” claim is false.

### Minimum missing inputs

1. For SV work: an authoritative event-level record for each VariationID (assembly accession/version, breakpoints or sequence/alleles, event type/length) and an accession-level PAV/genotype matrix with a verified cohort crosswalk.
2. For climate work: validated accession-origin coordinates plus source, precision and uncertainty; matched genotypes with ancestry controls.
3. For disease genetics: compatible cohort marker genotypes or a documented targeted query, genotype QC/PCs/kinship, and phenotype denominators or equivalent count data; exact published marker alleles/builds for replication.

### Single next action with highest expected value

Do not download either full VCF and do not run association tests. First pursue one focused provenance retrieval from the public pangenome source: obtain the event-level PAV/graph genotype resource (or a documented query for the five exact VariationIDs) together with its sample ID crosswalk. This resolves the most central ambiguity without spending compute on unrelated SNPs. If the source cannot provide those records, formally close the five-SV validation route and retain the candidates only as literature-prioritized markers. The existing 2026 cohort reconciliation and candidate evidence audit should remain a reproducibility/portfolio package, not be presented as a novel discovery paper by itself.

The accurate present description is: **five externally prioritized pearl millet SV association markers were audited against a multi-site downy mildew cohort; exact event identity and cohort genotypes remain unresolved, so no candidate-level disease association or climate-adaptation claim is made.**
