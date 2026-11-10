#!/usr/bin/env python3
"""Create Task 15 package using verified local audit inputs."""
from pathlib import Path
from datetime import datetime, timezone
import csv, hashlib, subprocess, shutil

P=Path(__file__).resolve().parents[2]
T13=P/'results/task13_research_opportunity_20261022T184158Z'
T14=P/'results/task14_exact_pangenome_SV_recovery_20261022T184715Z'
U=P/'results/ultimate_execution_20261022T180431Z'
OUT=P/'results'/f"task15_research_direction_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}"
OUT.mkdir(parents=True,exist_ok=False)
def md(n,s): (OUT/n).write_text(s.strip()+'\n',encoding='utf-8')
def tsv(n,head,rows):
    with (OUT/n).open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(head);w.writerows(rows)

md('final_author_data_request.md', '''# Final author data request — draft only; not sent

**To:** Shilin Tian (tianshilin@novogene.com); Linkai Huang (huanglinkai@sicau.edu.cn)
**Subject:** Targeted request for event definitions and accession-level PAV calls for five pearl millet VariationIDs

Dear Dr. Tian and Dr. Huang,

I am conducting a reproducible computational study of five structural-variation association markers reported in the pearl millet pangenome study: **PGLA1542300, PGLA1557868, PGLA1564064, PGLA1457537 and PGLA1545539**. I checked Supplementary Table 19 and the article’s public data records. I can recover the PI537069 chromosome, reported position and INS/DEL label for each marker, but not the event-level definition or accession-level calls needed to compare them responsibly with a public multi-site downy-mildew cohort.

Could you point me to a public file/API or share, if available, a compact table or data extract for these five IDs containing:

1. **Event definition:** exact SV/PAV type and allele interpretation; reference assembly accession/version; chromosome/contig; start/end, coordinate convention and breakpoints/junctions; event length; REF/ALT or presence/absence sequence; inserted/deleted or flanking sequence where available; alternate catalogue/graph identifiers.
2. **Methods and quality:** event-calling and validation methods; per-event quality/confidence metrics and limitations; read/graph support if available; and the filtering criteria used for the published PAV set.
3. **Accession-level calls:** genotype/PAV state for each sample, sample and accession identifiers, explicit missing-call encoding, per-call quality/missingness, and variant/sample filtering details.
4. **Crosswalk and context:** a documented mapping among sample IDs, PI/PMiGAP or other germplasm accession names, and SRR/SRS/SAMN identifiers; relevant population labels; and any available direct downy-mildew phenotype, pathotype or association information for these events or accessions.

A stable repository link with query instructions or a small TSV/CSV plus data dictionary is sufficient. I am not requesting raw reads or a whole-cohort VCF. A verified accession crosswalk is essential: row order and approximate name similarity cannot establish that a pangenome call belongs to a 2026 cohort accession. The purpose is a qualified cross-study assessment; I will cite the source and follow reuse conditions. I will not interpret these markers as causal disease-resistance or climate-adaptation variants without appropriate evidence.

If these PGLA IDs are association-table labels rather than stable event keys, please identify the authoritative event identifier or source record that resolves them.

Thank you for your time and for making the pangenome resource available.

Best regards,\n[Your name]\n[Institution/project affiliation, if applicable]\n[Contact information]

**Verification note:** the article identifies Shilin Tian and Linkai Huang as corresponding authors and prints the addresses above. This is an unsent draft; no email or form was submitted.''')

resources=[
['Jones et al. 1995 DM QTL','Linkage mapping; pathotype-specific family/population','Legacy linkage-group QTL; no sequence-resolved allele/modern physical coordinate verified','Disease reaction to defined pathogen populations in publication','Family marker data reported; no compatible 2026 calls located','Not established','No exact accession crosswalk','Historical linkage evidence, not cohort validation','Different population/map/pathotypes; cannot transfer from LG label alone'],
['Saritha et al. 2017 QTL','295 RILs; greenhouse Sg445, Sg519, Sg526; three replicates','SSR/linkage-map QTL; no verified 843B/Tift physical allele','Pathotype-specific incidence/resistance reported','Study-specific SSR/map genotypes; no machine-readable matched calls found','No verified physical harmonization','No exact crosswalk','QTL evidence in family','Different biparental population and controlled isolates'],
['Chelpuri et al. 2019 QTL','187 F8 RILs; 88 SSR markers; three Indian isolates','53 map loci and five LG4 QTLs; no validated modern physical allele mapping','Seedling greenhouse disease response across Sg445/Sg519/Sg526','Study-specific SSR genotypes/map; no 2026 calls','No sequence/build bridge established','No exact crosswalk','Family QTL replication only','High effects in one RIL population may not transfer to diverse African material'],
['Taunk et al. 2018 introgression','Marker-assisted breeding in HHB 197 background','Three target resistance loci on LG1/LG2/LG4','Breeding resistance context, not open matched panel data','No compatible accession genotype table found','No exact allele/coordinate bridge','No crosswalk','Breeding evidence, not cohort validation','Different background and selection design'],
['Jogaiah et al. 2014 SCAR ISSR 863','Two parents/F2 plus small validation set','1.4 kb ISSR-derived SCAR band, 0.72 cM linkage; exact modern locus not verified','Seven resistant and five susceptible lines in abstract','PCR marker assay; no panel-wide calls located','Could be sequence mapped if exact primer/sequence recovered; not done','No exact crosswalk','Small prior marker validation','Not ready for computational cohort validation'],
['Kanfany 2017 Senegal thesis','77-genotype association analysis across two Senegal locations','Thesis reports 16 significant SNPs across four linkage groups; exact alleles/build coordinates not established here','Disease association and phenotype described in public thesis record','81.94 MB thesis PDF public; no machine-readable genotype matrix/crosswalk verified','Not established','No exact crosswalk','Published association summary, not independent cohort validation','Potential lead only; identities, genotypes and metadata need verification'],
['Ramu et al. 2023 Corteva DMY GWAS context','GWAS in breeding germplasm','DM MTAs reported as colocalizing with known QTL; compatible exact alleles/coordinates not recovered here','DM phenotype in Corteva panel; no matched open table found','No compatible per-accession calls in current project','Not established for 2026 references','No crosswalk','GWAS precedent, not current validation resource','Panel and genotype/phenotype data access gap'],
['Subedi et al. 2026 cohort','288 phenotype accessions; 231 WGS; four Senegal sites, three reps','Not a prior marker study; SNP-only callsets for 843B and updated Tift','Public plot-level incidence ratio 0–1; 2024 season; 231 exact WGS overlap','32.43 GB 843B and 41.42 GB Tift SNP VCFs; no index listed in audited record','Same-panel SNP tests potentially possible; not the five PGLA SV calls','Exact internal 2026 cohort crosswalk verified; no exact overlap with Yan pangenome IDs','Potential exploratory panel; no association run','N=231 independent accessions, structure, repeated proportions and no local numerator/denominator; QC/PC/kinship absent']]
tsv('alternative_disease_genetics_resources.tsv',['study_or_resource','design_and_population','published_marker_definition','phenotype_access','genotype_access','coordinate_compatibility_to_2026','exact_crosswalk_to_2026','validation_status','feasibility_and_limit'],resources)

md('marker_validation_feasibility.md','''# Marker validation feasibility

Published pearl millet downy-mildew genetics includes pathotype-specific QTL mapping, marker-assisted introgression, a small SCAR validation report, a Senegal 77-genotype GWAS thesis, and a breeding-panel GWAS. These are important precedents, but use different populations, pathogen isolates, marker systems and phenotype protocols. Linkage-group labels or overlap with an earlier QTL do not identify the same allele in a modern reference.

The 2026 cohort is the best public candidate panel found: 288 accessions phenotyped at four Senegal sites with three replicates, and 231 sequenced accessions exactly joined to phenotype records. The plot response is infected/total ratio from 0 to 1, but the local workbook lacks numerator and denominator fields and no denominator lookup was found. The article reports population groups and a genome-wide SNP PCA; ancestry must therefore be modeled.

**No published disease-resistance marker is ready for in-silico validation against the current files.** Legacy QTL/SSR markers are linkage-map-defined and not yet harmonized as exact alleles/coordinates. The Kanfany thesis and Ramu breeding-panel report provide association summaries, not a verified machine-readable marker-call table plus exact sample crosswalk into this 2026 panel. The five PGLA IDs are different-trait pangenome markers and have no cohort PAV calls.

The cohort VCFs are filtered biallelic SNPs with indels excluded, so cannot establish PAV genotypes for the five candidates. The 843B file is 32.43 GB and updated Tift is 41.42 GB; no index was listed in the audited Zenodo record. Do not download them for marker validation until exact marker alleles, reference build and a targeted extraction path are established.

## New SNP GWAS gate

The independent sample size is 231, not the 2,772 repeated plot records. Prior best-case power estimates for about 22.2 million markers across four site tests required very large effects for 80% power (approximately 0.66 SD/allele at MAF 0.5 and 1.50 SD at MAF 0.05 under optimistic independent-normal assumptions and strict multiplicity correction). Real power is lower with structure, missingness and repeated-site uncertainty. Current allele frequencies were not computed because no VCF was retrieved or QCed.

An explicitly exploratory single-reference scan could be revisited only after sample/build verification, genotype and MAF/missingness QC, PC/kinship estimation, review of germplasm/morphotype confounding, phenotype denominator provenance or a justified continuous-proportion model, a site/replicate/block model, and a prespecified power/multiplicity plan. Current decision: no-go for download and association testing.''')

md('climate_reassessment.md','''# Climate feasibility reassessment

Coordinates exist for 148/231 sequenced accessions (145 distinct pairs; 20 countries); 93/148 are assigned to Senegal and 83 lack coordinates. The metadata do not establish whether these are original collection sites, reported origin locations, centroids or another geocoding product. Coordinate source, precision, uncertainty and reference date are absent. Decimal places do not establish positional accuracy.

These coordinates cannot yet be treated as verified accession-origin climate. The four Senegal trial locations describe where disease was measured, not where accessions originated. WorldClim 2.1 or CHELSA v2.1 could supply long-term normals in principle, but extraction now would add false precision.

Genetic inputs are also not analysis-ready: the PAV matrix/calls are unavailable; the cohort SNP files are large and unindexed in the audited metadata; there are no local genotype QC, PCs or kinship; and no exact Yan-to-2026 pangenome sample crosswalk was found. Geographic clustering and ancestry can confound GEA. A GEA is not proof of local adaptation.

Minimum inputs: authoritative origin locality and coordinate provenance/uncertainty; exact sample joins to usable genotype calls; genotype QC and ancestry/spatial controls; one justified climate product/baseline and a priori variables; adequate effective sample size. No climate download or test is justified now.''')

directions=[
['A. Wait for exact pangenome SV data','Event records with alleles/breakpoints/sequences; per-accession PAV calls and quality/missingness; exact crosswalk','Task 14 found only S19 marker rows; no PAV matrix/API query; author request ready but unsent','Low until new response/source','Could resolve five marker identities and permit focused replication','External response uncertain; calls still require matched phenotype and carrier power','User may send final request; no more broad searches'],
['B. Validate known DM markers','Exact marker alleles/coordinates/build; cohort calls; phenotype and population controls','QTL/GWAS literature exists, but legacy linkage markers and private breeding MTAs lack compatible 2026 calls','Low today; moderate only if definitions/calls found','Focused replication of established resistance loci','No marker passes compatibility gate; different isolates/populations','Obtain exact lead markers and targeted query/index before any VCF download'],
['C. New SNP DMY association','One compatible SNP matrix; sample QC; PCs/kinship; phenotype model, power and denominator plan','2026 cohort has 231 exact matches, four-site phenotype and public SNP VCFs','Conditional exploratory only; no-go now','Could be a multi-environment pilot in an African diversity panel','N=231, ~22M markers, structure, phenotype denominators absent locally, low power','Resolve phenotype/model; complete prespecified QC/power gate before considering one VCF'],
['D. Genotype–environment association','Verified origin coordinates/uncertainty; matched genotypes; ancestry/spatial controls; environmental coverage','148/231 coordinates but provenance unclear and Senegal-skewed; no genetic structure files','No-go','Could evaluate environmental gradients if origin data and model are valid','Unknown coordinate semantics; spatial/ancestry confounding; correlation is not adaptation','Get coordinate data dictionary and uncertainty before extraction'],
['E. Maintain audit while seeking better data','Reproducible evidence package, targeted request, explicit analysis gates','Tasks 1–15 establish cohort reconciliation, candidate evidence, missing inputs and feasibility boundaries','Ready now; primary recommendation','Strong training/portfolio value and safeguards future original research','Audit alone is not a biological discovery paper','Keep as support package; pursue C only after QC/phenotype gates and user may send A request']]
tsv('research_direction_comparison.tsv',['option','required_inputs','available_evidence','feasibility_now','expected_scientific_value','principal_limitations','next_action'],directions)

md('task15_final_decision.md','''# Task 15 final decision

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

Do not download both large VCFs, run GWAS/GEA now, or claim resistance causality or climate adaptation.''')

# Manifest local hashes and sources checked.
manifest=[]
for f in [T14/'draft_data_request.md',T14/'data_source_contact_assessment.md',T14/'cohort_crosswalk_assessment.tsv',T14/'sv_association_feasibility.md',T13/'coordinate_provenance_audit.md',U/'phenotype_reconciliation.md',U/'genotype_retrieval_assessment.md',U/'gwas_feasibility_decision.md',U/'statistical_power_assessment.tsv',U/'literature_evidence_matrix.tsv']:
    manifest.append([f.name,hashlib.sha256(f.read_bytes()).hexdigest(),str(f),'Local audited artifact; read-only','2026-10-23'])
for n,u,why in [
('Yan et al. 2023','https://www.nature.com/articles/s41588-023-01302-4','Official article: methods, data availability, supplement and corresponding authors'),
('Yan official supplementary workbook','https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41588-023-01302-4/MediaObjects/41588_2023_1302_MOESM3_ESM.xlsx','Already local and exact-scanned; fresh remote fetch cache miss'),
('Jones et al. 1995','https://pubmed.ncbi.nlm.nih.gov/24169834/','Primary pathotype-dependent QTL'),
('Saritha et al. 2017','https://oar.icrisat.org/10458/','Primary DM QTL'),
('Chelpuri et al. 2019','https://oar.icrisat.org/11314/1/chelpuri2019.pdf','Primary SSR QTL, 187 RILs / three isolates'),
('Taunk et al. 2018','https://pubmed.ncbi.nlm.nih.gov/30555073/','Primary marker-assisted introgression'),
('Jogaiah et al. 2014 SCAR','https://pubmed.ncbi.nlm.nih.gov/25156533/','Primary SCAR ISSR-863 report'),
('Kanfany 2017 thesis','https://ugspace.ug.edu.gh/items/beaa7e8b-5747-4d3d-a2ec-27366f832d90','Public thesis record reports 77-genotype DMY GWAS; machine-readable calls unverified'),
('Ramu et al. 2023','https://pmc.ncbi.nlm.nih.gov/articles/PMC10477261/','Primary breeding-panel DMY MTA context'),
('Subedi et al. 2026','https://doi.org/10.1016/j.dib.2026.112746','Public phenotype and WGS cohort design'),
('Zenodo 2026 cohort','https://zenodo.org/records/18602603','Public data and VCF metadata; large callsets not downloaded'),
('WorldClim 2.1','https://www.worldclim.org/data/worldclim21.html','Climate option; no download'),
('CHELSA v2.1','https://www.chelsa-climate.org/datasets/chelsa_bioclim','Climate option; no download')]:
    manifest.append([n,'',u,why,'2026-10-23'])
tsv('source_manifest.tsv',['source_name','sha256_if_local','source_url_or_path','provenance_and_scope','access_date'],manifest)

validator='''#!/usr/bin/env python3\nfrom pathlib import Path\nimport csv\np=Path(__file__).resolve().parent\nreq=["final_author_data_request.md","alternative_disease_genetics_resources.tsv","marker_validation_feasibility.md","climate_reassessment.md","research_direction_comparison.tsv","task15_final_decision.md","source_manifest.tsv","execution_log.txt"]\nassert all((p/x).is_file() for x in req)\nwith (p/"alternative_disease_genetics_resources.tsv").open(encoding="utf-8",newline="") as f:r=list(csv.DictReader(f,delimiter="\\t"))\nassert len(r)>=8 and any("Subedi et al. 2026" in x["study_or_resource"] for x in r)\nwith (p/"research_direction_comparison.tsv").open(encoding="utf-8",newline="") as f:d=list(csv.DictReader(f,delimiter="\\t"))\nassert len(d)==5 and any(x["option"].startswith("E.") for x in d)\nt=(p/"final_author_data_request.md").read_text()\nfor x in ["PGLA1542300","PGLA1557868","PGLA1564064","PGLA1457537","PGLA1545539"]: assert x in t\nassert "not sent" in t.lower()\nprint(f"VALID: {len(req)} required outputs, {len(r)} resources, five direction options, all candidates in unsent request.")\n'''
(OUT/'validate_task15.py').write_text(validator,encoding='utf-8')
shutil.copy2(Path(__file__),OUT/'reproduce_task15.py')
md('execution_log.txt',f'''Task 15 execution log\nUTC package timestamp: {OUT.name}\nInputs reused read-only: Task 13/14 packages; cohort phenotype/genotype reconciliation, crosswalk, power audit and literature matrix.\nWeb review: official Yan article/supplement metadata; primary DM QTL, SCAR and marker-assisted studies; Kanfany Senegal thesis record; Ramu 2023 breeding-panel MTA context; Subedi 2026 cohort paper and Zenodo; WorldClim/CHELSA pages.\nNo messages sent. No original data modified. No large VCF or climate data downloaded. No GWAS/GEA run. No Git initialized.\n''')
subprocess.run(['python3',str(OUT/'validate_task15.py')],check=True)
items=[]
for f in sorted(OUT.iterdir()):
    if f.is_file() and f.name!='checksums.sha256':items.append(f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}')
(OUT/'checksums.sha256').write_text('\n'.join(items)+'\n',encoding='utf-8')
for line in (OUT/'checksums.sha256').read_text().splitlines():
    digest,name=line.split('  ',1);assert hashlib.sha256((OUT/name).read_bytes()).hexdigest()==digest
print(OUT)
