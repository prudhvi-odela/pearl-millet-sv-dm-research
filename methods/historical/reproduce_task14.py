#!/usr/bin/env python3
"""Build Task 14 recovery decision package from local audit evidence."""
from pathlib import Path
from datetime import datetime,timezone
import csv,hashlib,subprocess

P=Path(__file__).resolve().parents[2]
T13=P/'results/task13_research_opportunity_20261022T184158Z'
BASE=P/'results/ultimate_execution_20261022T180431Z'
OLD=P/'results/original_sv_record_recovery_20261022T173607Z'
RAW=P/'data/raw'
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
OUT=P/'results'/f'task14_exact_pangenome_SV_recovery_{STAMP}'
OUT.mkdir(parents=True,exist_ok=False)
IDS=['PGLA1542300','PGLA1557868','PGLA1564064','PGLA1457537','PGLA1545539']

def read(path,sep='\t'):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=sep))
def write(name,header,rows):
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(header);w.writerows(rows)
def md(name,s): (OUT/name).write_text(s.strip()+'\n',encoding='utf-8')

# Read only source artifacts. IDs were previously exact-scanned in every worksheet of official workbook.
events=read(T13/'sv_recovery_results.tsv')
assert len(events)==5 and {r['candidate_id'] for r in events}==set(IDS)
header=list(events[0])
write('event_definition_recovery.tsv',header,[[r[k] for k in header] for r in events])

call_rows=[]
for r in events:
    call_rows.append([r['candidate_id'],'Not recovered','Not recovered','Not recovered','Not recovered','Not reported for this candidate','No matrix file/accession located in audited public/local sources','Yan methods state graph-mapped reads were used for population SV genotyping, but no candidate-specific calls are exposed by S19','No exact cohort call; zero/low counts in prior 20-sample matrix are not authoritative population PAV calls','Not testable'])
write('accession_level_call_availability.tsv',['candidate_id','candidate_event_key','sample_identifiers','reference_accession_ids','genotype_or_PAV_calls','missing_call_encoding','candidate_call_quality','available_public_resource','local_call_evidence','status'],call_rows)

# Exact, transparent shared-field intersection. No fuzzy matching or inferred aliases.
yan=read(P/'metadata/Yan2023_S1_NCBI_matched.tsv')
cohort=read(BASE/'genotype_sample_crosswalk.tsv')
yan_keys=['ID','SRRnumber','Run','Sample','BioSample','SampleName']
cohort_keys=['GID','Library_ID','Sample names_x','Sample names_y','SampleName','LibraryName','Run','Sample','BioSample']
norm=lambda x:(x or '').strip()
def vals(row,keys):return {norm(row.get(k,'')) for k in keys if norm(row.get(k,'')) and norm(row.get(k,'')) not in {'-','NA','nan','None'}}
yin={k:set() for k in yan_keys}; cin={k:set() for k in cohort_keys}
for r in yan:
    for k in yan_keys: yin[k].add(norm(r.get(k,'')))
for r in cohort:
    for k in cohort_keys: cin[k].add(norm(r.get(k,'')))
match_map=[]
for yr in yan:
    for cr in cohort:
        common=vals(yr,yan_keys)&vals(cr,cohort_keys)
        if common: match_map.append((yr,cr,common))
# Record dataset sizes, exact overlap, ambiguous candidate links and unmatched records explicitly.
yan_id_values=set().union(*(vals(r,yan_keys) for r in yan))
cohort_id_values=set().union(*(vals(r,cohort_keys) for r in cohort))
ambiguous_yan=sum(1 for yr in yan if sum(bool(vals(yr,yan_keys)&vals(cr,cohort_keys)) for cr in cohort)>1)
ambiguous_cohort=sum(1 for cr in cohort if sum(bool(vals(cr,cohort_keys)&vals(yr,yan_keys)) for yr in yan)>1)
rows=[
 ['dataset_size','Yan2023_S1_NCBI_matched.tsv','genotype_sample_crosswalk.tsv',len(yan),len(cohort),0,0,'Yan source accessions and 2026 sequenced cohort records compared using only exact strings across the listed stable identifier/name fields'],
 ['exact_overlap',';'.join(yan_keys),';'.join(cohort_keys),len(yan_id_values),len(cohort_id_values),len(match_map),0,'No exact shared identifier value/record pair was found; no approximate name matching used'],
 ['ambiguous_links','all tested fields','all tested fields',ambiguous_yan,ambiguous_cohort,0,ambiguous_yan+ambiguous_cohort,'No exact one-to-many ambiguous link was found because there were no exact linked records'],
 ['unmatched_records','Yan rows','2026 cohort rows',len(yan),len(cohort),len(yan),len(cohort),'All records remain unmatched at exact string level; this does not prove biological accessions are different, only that an authoritative crosswalk is absent']]
write('cohort_crosswalk_assessment.tsv',['comparison_type','Yan_field_or_fields','2026_field_or_fields','n_Yan_rows_or_values','n_2026_rows_or_values','n_exact_record_pairs_or_unmatched','n_ambiguous_records','interpretation'],rows)

md('data_source_contact_assessment.md',f'''# Data source and contact assessment\n\n## Authoritative owner\n\nThe primary source is Yan et al. (2023), *Nature Genetics*, “Pangenomic analysis identifies structural variation associated with heat tolerance in pearl millet.” The article identifies PI537069 as the reference accession (GenBank JAIFIR000000000), describes assembly-based SV discovery using MUMmer/NUCmer and SVMU, construction of a PI537069 graph with vg, and mapping public short reads to the graph for population SV genotyping. It reports filtering the PAV matrix at minor allele frequency ≥0.05 and missing rate ≤0.1 and using 124,532 PAVs in 242 accessions for GWAS.\n\nThe article's data-availability statement names NCBI assemblies and sequencing projects (including SRP063925), but does not identify a downloadable accession-level graph/PAV call matrix or an archive accession for the graph/genotype files. Supplementary Table 19 is the association summary and the locally stored workbook has already been exact-searched for all five IDs; each appears only as an association-table VariationID row with PI537069 chromosome/position and INS/DEL label. The article's supplementary workbook is hosted by Springer Nature; a fresh web fetch returned a cache miss, while the verified workbook is already present locally. No repeat or broad download is warranted.\n\nThe local MilletDB OpenAPI schema documents variation/detail endpoints but no query parameters; the prior exact retrieval audit recorded an API timeout and unavailable service response. That is an unsuccessful access attempt, not proof the records do not exist. The public article lists corresponding authors **Shilin Tian** and **Linkai Huang**. Their exact addresses are published in the article: tianshilin@novogene.com and huanglinkai@sicau.edu.cn. These are suitable contacts for the data request; **no message was sent and no form was submitted**.\n\n## Efficient recovery outcome\n\nNo small, documented public endpoint has been established for retrieving the five candidate event records and calls. NCBI raw-read availability is not a targeted genotype resource; processing it would require reconstructing calls from raw data and is not justified here. The official assemblies can support sequence comparison only after an event definition is supplied. Do not download raw-read collections, the large 2026 SNP VCFs, or unrelated pangenome assets for this query.\n\nSources: [Yan et al. article](https://www.nature.com/articles/s41588-023-01302-4), [NCBI PI537069 assembly](https://www.ncbi.nlm.nih.gov/nuccore/JAIFIR000000000), [NCBI SRA project SRP063925](https://www.ncbi.nlm.nih.gov/sra/?term=SRP063925), [local exact recovery audit](../original_sv_record_recovery_20261022T173607Z/methods_and_sources.md).''')

md('draft_data_request.md','''# Draft data request — not sent\n\n**To:** Shilin Tian; Linkai Huang (corresponding authors listed in Yan et al. 2023)\n**Subject:** Request for event-level records and PAV calls for five pearl millet VariationIDs\n\nDear Dr. Tian and Dr. Huang,\n\nI am conducting a computational pearl millet study that evaluates five structural-variation association markers reported in the Yan et al. 2023 pangenome resource against a publicly available multi-site downy-mildew phenotype cohort. The five exact VariationIDs are PGLA1542300, PGLA1557868, PGLA1564064, PGLA1457537, and PGLA1545539. I have reviewed Supplementary Table 19 and the public data-availability information. The table provides marker coordinates and INS/DEL labels, but I could not locate an event-level record or accession-level call matrix for these IDs.\n\nWould you be able to point me to a public download or, if shareable, provide the following targeted records for these five IDs?\n\n1. The exact event catalogue rows, including event type, reference assembly accession/version, chromosome/contig, start/end and coordinate convention, breakpoints/junctions, length, REF/ALT or presence/absence allele definition, and any alternate graph/catalogue identifiers.\n2. Inserted/deleted or breakpoint-flanking sequence, when available, and any event-level validation or quality metrics (including calling/validation method and known limitations).\n3. Per-accession PAV/genotype calls for these five events, with sample identifiers, explicit missing-call encoding, genotype confidence/quality, and the filtering criteria used.\n4. The sample crosswalk linking those identifiers to the corresponding PI/PMiGAP/germplasm accession names and, where applicable, SRR/SRS/SAMN identifiers. This crosswalk is essential because the comparison cohort uses its own validated GID, library and sample-name crosswalk; row order or approximate name matching would not establish sample identity.\n5. Any phenotype/population metadata needed to interpret which accessions were included in the published PAV-GWAS.\n\nA compact TSV/CSV and a short data dictionary, or a stable repository/API link with documented query syntax, would be sufficient; I am not requesting raw reads or a whole-cohort VCF. The intended use is a reproducible, carefully qualified cross-study comparison, not a claim that these variants cause downy-mildew resistance or climate adaptation. I will cite the source and follow any reuse conditions you specify.\n\nIf these five IDs are summary association markers rather than stable event keys, please let me know which authoritative event identifiers or source files would resolve them.\n\nThank you for your time and for making the pangenome resource available.\n\nBest regards,\n[Your name]\n[Institution or project affiliation, if applicable]\n[Contact information]''')

md('sv_association_feasibility.md','''# SV association feasibility\n\n**Current decision: no association test.** The five records are not exact, sequence-resolved events and have no authoritative per-accession calls. Without stable event definitions and genotype encoding, matching a PAV to the 2026 phenotype panel is not possible. The 2026 public resources are filtered SNP callsets, not SV/PAV calls; no inference from SNPs or nearby markers is allowed.\n\nThe 2026 cohort has 231 exact WGS accessions linked to phenotypes, but this is only an upper bound for any future SV test. An actual matched sample count cannot be estimated until a PAV matrix and verified accession crosswalk arrive. The audited phenotype workbook has 2,772 plot records for those 231 accessions over four Senegal sites and three replicates; disease values are infected/total ratios with no numerator/denominator fields or denominator table located. Repeated plots do not raise independent genotype N. Prior power assessment found a genome-wide scan underpowered except for very large effects; a single prespecified candidate test would reduce multiplicity but not fix event identity, small carrier counts, phenotype precision or population structure. The old 20-sample descriptive SV matrix is not authoritative and cannot supply carrier counts for this cohort.\n\nBefore any test: (1) recover exact event allele/definition and quality metrics; (2) obtain per-accession calls and missingness; (3) exact-join sample identifiers to the 231-person crosswalk and report matched/carrier/noncarrier/missing counts; (4) verify phenotype denominator provenance and model plot-level replication/site effects; (5) calculate carrier balance, ancestry/kinship confounding and candidate-specific power; (6) prespecify a model and multiplicity handling. Even then, results would be association evidence, not causal validation.''')

md('task14_final_decision.md','''# Task 14 final decision\n\n## Decision: C — Records unavailable; stop the five-SV recovery workstream\n\nThe targeted review verified that all five exact PGLA identifiers occur in the Yan et al. 2023 S19 association summary. For each, the recovered record gives only the PI537069 reference namespace, reported chromosome/position, and INS/DEL class. No candidate-specific breakpoints, sequence, length, exact allele definition, event quality record, accession-level PAV call, or cross-study sample mapping is in the audited supplementary/public/local exports. The article documents a graph-genotyping workflow and public source reads, but not a downloadable PAV matrix or event-record endpoint. MilletDB's documented API schema lacks query parameters and the prior direct request timed out. No new targeted public route was established.\n\nThe official article identifies Shilin Tian and Linkai Huang as corresponding authors and publishes their contact details. The included data request is ready to send, but was not sent. A direct reply could change the decision; until then, close this workstream and do not test the candidates.\n\nThe 2026 phenotype crosswalk was compared by exact identifier strings against the Yan/SRP metadata fields. The attached TSV records exact overlaps if any; these identify shared technical identifiers only and do not create a PAV call matrix. No approximate accession matches were treated as confirmed. Even a positive accession-name overlap would not establish event genotype.\n\n**Strongest alternative:** retain the existing cohort reconciliation and five-candidate evidence audit as a reproducible portfolio/research resource, and develop the disease-genetics question only after compatible genotype data are obtained and QC/ancestry controls pass. The 231-accession panel is a potential exploratory multi-environment resource, but current public callsets are large, SNP-only, and unindexed; phenotype ratios lack denominator provenance. Therefore no disease association test is currently defensible. Climate analysis remains separately blocked by coordinate provenance.\n\n**Single next action:** send the prepared targeted request to the corresponding authors for the five event records, genotype calls, and exact sample crosswalk. If the authors cannot provide these or a stable query endpoint, archive the five IDs as external non-DM association markers and stop further recovery attempts. Do not claim downy-mildew resistance or climate adaptation.''')

# Source manifest records local file hashes and primary URLs, with no downloads implied.
manifest=[]
for f in [T13/'task13_final_recommendation.md',T13/'sv_recovery_results.tsv',T13/'source_manifest.tsv',OLD/'methods_and_sources.md',OLD/'targeted_genotype_retrieval_options.tsv',P/'data/raw/Yan2023_Supplementary_Tables.xlsx',P/'metadata/Yan2023_S1_NCBI_matched.tsv',BASE/'genotype_sample_crosswalk.tsv',BASE/'matched_plot_phenotypes.tsv',BASE/'gwas_feasibility_decision.md']:
    manifest.append([f.name,hashlib.sha256(f.read_bytes()).hexdigest(),str(f),'Local project artifact; read-only reused','2026-10-23'])
for name,url,why in [
('Yan et al. 2023 article','https://www.nature.com/articles/s41588-023-01302-4','Primary methods/data availability/corresponding authors'),
('Yan et al. supplementary tables workbook','https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41588-023-01302-4/MediaObjects/41588_2023_1302_MOESM3_ESM.xlsx','Official S1-S20; already local and exact-scanned; fresh web fetch cache miss'),
('PI537069 GenBank','https://www.ncbi.nlm.nih.gov/nuccore/JAIFIR000000000','Reference accession named by article'),
('SRP063925 SRA project','https://www.ncbi.nlm.nih.gov/sra/?term=SRP063925','Public reads used for graph genotyping; not downloaded'),
('MilletDB API schema','http://milletdb.novogene.com/api','Prior local OpenAPI schema; documented variation endpoints lack query params; prior call timed out'),
('2026 cohort Zenodo','https://zenodo.org/records/18602603','Public phenotype/SNP callset metadata; SNP VCFs not downloaded')]:
    manifest.append([name,'',url,why,'2026-10-23'])
write('source_manifest.tsv',['source_name','sha256_if_local','source_url_or_path','provenance_and_access_outcome','access_date'],manifest)

script='''#!/usr/bin/env python3\n"""Validate Task 14 outputs and exact candidate set."""\nfrom pathlib import Path\nimport csv,hashlib\nr=Path(__file__).resolve().parent\nrequired=["event_definition_recovery.tsv","accession_level_call_availability.tsv","cohort_crosswalk_assessment.tsv","data_source_contact_assessment.md","draft_data_request.md","sv_association_feasibility.md","task14_final_decision.md","source_manifest.tsv","execution_log.txt"]\nassert all((r/x).is_file() for x in required)\nwith (r/"event_definition_recovery.tsv").open(encoding="utf-8",newline="") as f: e=list(csv.DictReader(f,delimiter="\\t"))\nassert len(e)==5 and len({x["candidate_id"] for x in e})==5\nassert all(x["start_breakpoint"]=="Unknown/not reported" and x["accession_presence_absence_matrix"]=="Not recovered" for x in e)\nwith (r/"accession_level_call_availability.tsv").open(encoding="utf-8",newline="") as f: c=list(csv.DictReader(f,delimiter="\\t"))\nassert len(c)==5 and all(x["status"]=="Not testable" for x in c)\nprint(f"VALID: {len(required)} deliverables; exactly five candidates; no inferred genotypes.")\n'''
(OUT/'validate_task14.py').write_text(script,encoding='utf-8')
import shutil
shutil.copy2(Path(__file__),OUT/'reproduce_task14.py')
md('execution_log.txt',f'''Task 14 log\nUTC run timestamp: {STAMP}\nProject: {P}\nInputs read-only: Task 13 recommendation/evidence/source manifest; original event-recovery audit; Yan supplementary workbook already scanned in prior audit; Yan/SRA accession metadata; validated 2026 sample crosswalk and matched phenotype table; previous GWAS feasibility report.\nNew checks: official article page reviewed for methods, data availability, supplementary workbook, PAV filtering, public SRA project and listed corresponding authors; exact-string identifier comparison performed across Yan accession/SRA fields and 2026 WGS crosswalk fields.\nAccess outcomes: official supplementary XLSX web retrieval returned cache miss; local verified workbook retained and prior exact scan reused. MilletDB API query previously timed out; not repeated. No targeted PAV matrix/query endpoint found. Contact details came from the published article; no email/form was sent.\nNo source data modified. No raw reads, large SNP VCFs, or additional climate assets downloaded. No association test run. No Git initialized.\nValidation output: ''')
v=subprocess.run(['python3',str(OUT/'validate_task14.py')],capture_output=True,text=True,check=True)
with (OUT/'execution_log.txt').open('a',encoding='utf-8') as f:f.write(v.stdout)
lines=[]
for f in sorted(OUT.iterdir()):
    if f.is_file() and f.name!='checksums.sha256':lines.append(f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}')
(OUT/'checksums.sha256').write_text('\n'.join(lines)+'\n',encoding='utf-8')
for line in (OUT/'checksums.sha256').read_text().splitlines():
    h,n=line.split('  ',1);assert hashlib.sha256((OUT/n).read_bytes()).hexdigest()==h
print(OUT);print(v.stdout.strip())
