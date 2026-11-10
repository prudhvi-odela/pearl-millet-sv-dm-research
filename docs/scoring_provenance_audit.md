# Candidate evidence and scoring provenance audit

## Scope

This note records the read-only review of candidate evidence and existing scoring scripts. No original scripts, source data, or prior result tables were edited or rerun.

The five candidates are PGLA1542300, PGLA1557868, PGLA1564064, PGLA1457537, and PGLA1545539. Their curated summary is in `data/processed/FINAL_5_CANDIDATE_EVIDENCE_AUDIT.tsv`.

## Evidence interpretation

- The audited external GWAS tables report these variants for traits other than downy mildew. This supports prioritization and context, not a downy mildew association.
- The audited Yan2023 S19 search found no direct DMY/downy-mildew phenotype match for the five candidates. This result is limited to that audited table and phenotype filter.
- No climate association has been established. Accession-origin coordinates and nearby-gene expression context are not climate association results.
- The 20-accession genotype counts are descriptive. PGLA1557868 has zero carriers in this cohort; PGLA1542300 has one missing call. These counts do not estimate resistance effects.
- Absence from a selected DMY subset does not establish novelty of the structural variant. The variants have external records for other traits.

## Script findings and recommended corrections

### `scripts/annotate_123_Yan_context.py`

The script searches Yan2023 S13, stores matches in `Yan_S13_heat_context`, converts that field to `HeatEvidence`, and adds one point to `PriorityScore`. The S13 table is expression-associated SV / nearby-gene context, not a climate or heat phenotype table. The field and score component are therefore mislabeled. The five audited candidates all have S13 context = NO, so this component did not increase their current scores; other candidates may be affected.

Recommended corrected version: name the field `Yan_S13_expression_context`; do not derive a climate/heat evidence variable from S13; recalculate a clearly labeled prioritization score without that component, preserving the original output separately.

### `scripts/novelty_validation.py`

`MilletDB_YanValidated` is assigned by overlap with `DM9_crossstudy_MilletDB_clean.tsv`, a selected nine-variant table. A NO in this column means absent from that selected table, not absent from the full MilletDB/Yan GWAS resources and not novel as an SV.

Recommended corrected version: rename the field to make the reference set explicit (for example, `In_selected_DM9_crossstudy_table`) and report absence as "not detected in this selected set."

### `scripts/final_DM_validation.py`

The script filters Yan2023 S19 to phenotype labels matching DMY/mildew/downy and defines `novel` as input variants not present in that filtered set. This supports "no match in the audited DMY phenotype subset," not general variant novelty or proof that input SVs cause downy mildew resistance. "Cross-study validated" should be phrased as an exact cross-study record overlap unless independent phenotype/genotype validation has been performed.

Recommended corrected version: retain the exact overlap calculation, but label outputs "DMY-subset overlap" and "not detected in the audited DMY subset"; do not label the complement as novel.

### `scripts/integrate_DM_candidate_evidence.py`

The output title calls the 123-row input "POTENTIALLY NOVEL DM-ASSOCIATED SVs." The script integrates carrier fraction, other-trait records, and GWAS records. Those inputs do not themselves establish a downy mildew association or SV novelty.

Recommended corrected version: title the output as integrated evidence for prioritized candidates, label each evidence source by trait/domain, and avoid interpreting a ranking score as a disease association.

## Climate-analysis status

The script scan found no independent climate-association analysis in the searched Python, R, or shell scripts. The existing S13-derived label is expression context. The climate/heat candidate file previously audited was header-only. Climate analysis requires identified accession-level environmental measurements, genotype overlap, adequate sample coverage, and a population-structure strategy.

## Next scientific step

Proceed with a public-data provenance and overlap audit for accession-level environmental data and compatible genotypes. Before any association test, report matched sample count, environmental coverage, genotype call quality, carrier counts, population structure, and power limitations. If these conditions are inadequate, keep the manuscript focused on transparent SV prioritization and genomic context, with downy mildew and climate associations stated as unestablished.
