# Task 14 final decision

## Decision: C — Records unavailable; stop the five-SV recovery workstream

The targeted review verified that all five exact PGLA identifiers occur in the Yan et al. 2023 S19 association summary. For each, the recovered record gives only the PI537069 reference namespace, reported chromosome/position, and INS/DEL class. No candidate-specific breakpoints, sequence, length, exact allele definition, event quality record, accession-level PAV call, or cross-study sample mapping is in the audited supplementary/public/local exports. The article documents a graph-genotyping workflow and public source reads, but not a downloadable PAV matrix or event-record endpoint. MilletDB's documented API schema lacks query parameters and the prior direct request timed out. No new targeted public route was established.

The official article identifies Shilin Tian and Linkai Huang as corresponding authors and publishes their contact details. The included data request is ready to send, but was not sent. A direct reply could change the decision; until then, close this workstream and do not test the candidates.

The 2026 phenotype crosswalk was compared by exact identifier strings against the Yan/SRP metadata fields. The attached TSV records exact overlaps if any; these identify shared technical identifiers only and do not create a PAV call matrix. No approximate accession matches were treated as confirmed. Even a positive accession-name overlap would not establish event genotype.

**Strongest alternative:** retain the existing cohort reconciliation and five-candidate evidence audit as a reproducible portfolio/research resource, and develop the disease-genetics question only after compatible genotype data are obtained and QC/ancestry controls pass. The 231-accession panel is a potential exploratory multi-environment resource, but current public callsets are large, SNP-only, and unindexed; phenotype ratios lack denominator provenance. Therefore no disease association test is currently defensible. Climate analysis remains separately blocked by coordinate provenance.

**Single next action:** send the prepared targeted request to the corresponding authors for the five event records, genotype calls, and exact sample crosswalk. If the authors cannot provide these or a stable query endpoint, archive the five IDs as external non-DM association markers and stop further recovery attempts. Do not claim downy-mildew resistance or climate adaptation.
