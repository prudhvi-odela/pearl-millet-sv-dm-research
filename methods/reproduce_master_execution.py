#!/usr/bin/env python3
"""Build an integrated execution package for the Pearl millet research project."""
from pathlib import Path
from datetime import datetime,timezone
import csv,hashlib,json,subprocess,shutil,sys

P=Path(__file__).resolve().parents[1]
U=P/'results/ultimate_execution_20261022T180431Z'
T13=P/'results/task13_research_opportunity_20261022T184158Z'
T14=P/'results/task14_exact_pangenome_SV_recovery_20261022T184715Z'
T15=P/'results/task15_research_direction_20261022T190126Z'
OUT=P/'results'/f"complete_research_execution_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}"
OUT.mkdir(parents=True,exist_ok=False)
IDS=['PGLA1542300','PGLA1557868','PGLA1564064','PGLA1457537','PGLA1545539']
def md(n,s):(OUT/n).write_text(s.strip()+'\n',encoding='utf-8')
def tsv(n,h,rows):
    with (OUT/n).open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(h);w.writerows(rows)

# Input/checksum verification: existing audit outputs are preserved and only read.
checks=[]
for pkg in [U,T13,T14,T15]:
    mf=pkg/'checksums.sha256'; ok=True; n=0; bad=[]
    for line in mf.read_text().splitlines():
        digest,name=line.split('  ',1); path=pkg/name;n+=1
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:ok=False;bad.append(name)
    checks.append([str(pkg),n,'PASS' if ok else 'FAIL',';'.join(bad)])
tsv('prior_package_checksum_verification.tsv',['package','files_checked','status','failed_paths'],checks)
candidate_rows=[]
for r in csv.DictReader((T14/'event_definition_recovery.tsv').open(encoding='utf-8'),delimiter='\t'):
    candidate_rows.append([r['candidate_id'],r['chromosome'],r['reported_position'],r['SV_label'],r['reference_name'],r['reference_sequence_accession'],r['start_breakpoint'],r['end_breakpoint'],r['length_bp'],r['REF_allele'],r['ALT_or_inserted_sequence'],r['accession_presence_absence_matrix'],r['other_trait_GWAS_catalogued'],r['strongest_trait_record'],r['direct_DMY_evidence'],r['validation_status']])
assert {r[0] for r in candidate_rows}==set(IDS)
tsv('five_candidate_status.tsv',['candidate_id','PI537069_chromosome','reported_position','S19_type','reference_accession_or_name','assembly_accession','start_breakpoint','end_breakpoint','event_length','reference_allele','alternate_or_event_sequence','PAV_matrix','external_GWAS_context','strongest_trait_context','direct_DMY_evidence','test_status'],candidate_rows)

inventory=[
 ['Five-SV event audit','Complete as targeted evidence audit','Task 7/14/15','All five occur in S19 with coordinate/type and non-DM GWAS context; event sequences/breakpoints/PAV calls unresolved','External author data / authoritative event matrix required'],
 ['Yan supplementary workbook','Available locally; exact IDs previously scanned','data/raw/Yan2023_Supplementary_Tables.xlsx','Exact IDs are S19 association-table rows; not complete event definitions','No additional broad search'],
 ['Legacy 20-accession SV genotype matrix','Available, descriptive only','data/processed/DM20_SV_genotype_matrix.tsv; DM20_SV_genotype_summary.tsv','Not authoritative calls for the 2026 panel; PGLA1557868 absent in all 20 there','Do not use to infer 2026 carriers'],
 ['2026 phenotype/genotype crosswalk','Complete exact WGS join','results/ultimate_execution_20261022T180431Z/genotype_sample_crosswalk.tsv','231 exact WGS accessions / 2,772 plot rows, across 4 sites x 3 reps','Valid internal cohort join only'],
 ['2026 phenotype QC','Complete and verified in prior audit','results/ultimate_execution_20261022T180431Z/phenotype_qc_summary.tsv','No missing/out-of-range DM or duplicate plot keys; proportions have boundary zeros and ones','Numerator/denominator fields not available locally'],
 ['Sharma 2015 phenotype file','Header-only local placeholder','data/phenotype/Sharma2015_DM_metadata.tsv','Not full accession-level incidence table; paper describes 238 accessions x 8 pathotypes and reports 62 multi-pathotype resistant accessions','No full 238x8 phenotypes recoverable locally'],
 ['2026 cohort SNP callsets','Public remote metadata only','Zenodo 18602603; not local','Separate 843B 32.43 GB and updated Tift 41.42 GB biallelic SNP VCFs; no index in audited metadata','No download: GWAS gates not passed'],
 ['Population structure','Partial published evidence; no local covariates','2026 article PCA and project structure plan','Germplasm groups/morphotypes structured; no local PC/kinship matrices','Requires genotype QC/one reference callset'],
 ['Climate/accession coordinates','Partial metadata','results/ultimate_execution_20261022T180431Z/climate_accession_coordinates.tsv','148/231 coordinate-linked, 145 distinct pairs, 20 countries; 93/148 Senegal; provenance/precision unclear','No extraction or GEA'],
 ['Climate/environment data','No local extraction','WorldClim 2.1 / CHELSA v2.1 options','Sources available, accession-origin coordinates not validated','No climate download'],
 ['Disease literature','Reviewed and summarized','literature_evidence_matrix.tsv included','DM QTL, marker selection, GWAS precedents exist; exact compatibility varies','No first-GWAS/first-marker novelty claim'],
 ['2026 phenotype descriptive analysis','Completed in this execution','phenotype_site_rank_descriptives.tsv; phenotype_accession_site_means.tsv','Recomputed site summaries and between-site accession rank correlations for 231 exactly matched accessions','Descriptive only; no association/cause claim']]
tsv('master_inventory.tsv',['workstream','status','authoritative_path_or_source','verified_result','remaining_dependency'],inventory)

# JSON schemas (JSON Schema Draft 2020-12)
event_schema={"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Pearl millet SV event record","type":"object","required":["candidate_id","event_id","reference_assembly","chromosome","start","end","coordinate_convention","sv_type","event_length","source_provenance"],"properties":{"candidate_id":{"enum":IDS},"event_id":{"type":"string","minLength":1},"reference_assembly":{"type":"string","minLength":1},"chromosome":{"type":"string","minLength":1},"start":{"type":"integer","minimum":0},"end":{"type":"integer","minimum":1},"coordinate_convention":{"enum":["1-based-closed","0-based-half-open"]},"sv_type":{"enum":["INS","DEL","PAV","INV","CNV","TRANS","OTHER"]},"event_length":{"type":"integer","minimum":0},"reference_allele":{"type":["string","null"]},"alternate_allele_or_sequence":{"type":["string","null"]},"deleted_sequence":{"type":["string","null"]},"left_flank":{"type":["string","null"]},"right_flank":{"type":["string","null"]},"breakpoint_start":{"type":["integer","null"],"minimum":0},"breakpoint_end":{"type":["integer","null"],"minimum":0},"graph_id":{"type":["string","null"]},"alternate_ids":{"type":"array","items":{"type":"string"}},"calling_method":{"type":["string","null"]},"validation_method":{"type":["string","null"]},"quality_metrics":{"type":"object"},"limitations":{"type":["string","null"]},"source_provenance":{"type":"string","minLength":1}},"additionalProperties":True}
call_schema={"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Accession-level PAV/genotype call","type":"object","required":["candidate_id","event_id","sample_id","accession_id","genotype_pav","missing_call","source_provenance"],"properties":{"candidate_id":{"enum":IDS},"event_id":{"type":"string","minLength":1},"sample_id":{"type":"string","minLength":1},"accession_id":{"type":"string","minLength":1},"reference_assembly":{"type":"string"},"genotype_pav":{"type":"string","minLength":1},"missing_call":{"type":"boolean"},"quality":{"type":["number","null"],"minimum":0},"depth":{"type":["integer","null"],"minimum":0},"filter_status":{"type":"string"},"sample_group":{"type":"string"},"phenotype_context":{"type":"string"},"source_provenance":{"type":"string","minLength":1}},"additionalProperties":True}
cross_schema={"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Pangenome-to-cohort sample crosswalk","type":"object","required":["sample_id","accession_id","source_provenance"],"properties":{"sample_id":{"type":"string","minLength":1},"accession_id":{"type":"string","minLength":1},"alternate_sample_ids":{"type":"array","items":{"type":"string"}},"germplasm_name":{"type":"string"},"srr":{"type":"string"},"srs":{"type":"string"},"samn":{"type":"string"},"confidence_or_match_method":{"type":"string"},"source_provenance":{"type":"string","minLength":1}},"additionalProperties":True}
for name,obj in [('sv_event_input.schema.json',event_schema),('pav_call_input.schema.json',call_schema),('sample_crosswalk_input.schema.json',cross_schema)]:
    (OUT/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')

validator=r'''#!/usr/bin/env python3
"""Validate future author-provided SV event, PAV-call and sample-crosswalk TSVs.
No biological data are bundled. Run with --self-test to use temporary synthetic fixtures.
"""
from pathlib import Path
import argparse,csv,tempfile,sys
IDS={"PGLA1542300","PGLA1557868","PGLA1564064","PGLA1457537","PGLA1545539"}
EVENT_REQ={"candidate_id","event_id","reference_assembly","chromosome","start","end","coordinate_convention","sv_type","event_length","source_provenance"}
CALL_REQ={"candidate_id","event_id","sample_id","accession_id","genotype_pav","missing_call","source_provenance"}
CROSS_REQ={"sample_id","accession_id","source_provenance"}
MISSING={".","./.",".|.","NA","N/A","N","NULL","NONE","MISSING"}
VALID={"0","1","2","0/0","0/1","1/0","1/1","0|0","0|1","1|0","1|1","P","A","PRESENT","ABSENT","PRESENCE","ABSENCE","." ,"./.",".|.","NA","N/A","N","NULL","NONE","MISSING"}
def load(p):
    with open(p,encoding="utf-8-sig",newline="") as f:
        sample=f.read(4096);f.seek(0);dialect=csv.Sniffer().sniff(sample,delimiters="\t,")
        return list(csv.DictReader(f,dialect=dialect))
def validate(events,calls,crosswalk):
    errors=[];warnings=[]
    def cols(rows,need,label):
        if not rows:errors.append(label+": empty file");return
        miss=need-set(rows[0]);
        if miss:errors.append(label+": missing columns "+",".join(sorted(miss)))
    cols(events,EVENT_REQ,"events");cols(calls,CALL_REQ,"calls");cols(crosswalk,CROSS_REQ,"crosswalk")
    if errors:return errors,warnings
    event_keys=set();event_defs={};assemblies=set()
    for i,r in enumerate(events,2):
        cid=r["candidate_id"].strip();eid=r["event_id"].strip();key=(cid,eid)
        if cid not in IDS:errors.append(f"events row {i}: unrecognized candidate_id {cid}")
        if key in event_keys:errors.append(f"events row {i}: duplicate candidate/event {key}")
        event_keys.add(key);assemblies.add(r["reference_assembly"].strip())
        try:st=int(r["start"]);en=int(r["end"]);ln=int(r["event_length"])
        except Exception:errors.append(f"events row {i}: start/end/event_length must be integers");continue
        cc=r["coordinate_convention"].strip()
        if cc not in {"1-based-closed","0-based-half-open"}:errors.append(f"events row {i}: invalid coordinate convention {cc}")
        if st<0 or en<0 or en<st or (cc=="1-based-closed" and st<1) or (cc=="0-based-half-open" and en<=st):errors.append(f"events row {i}: invalid interval {st}-{en} for {cc}")
        if ln<0:errors.append(f"events row {i}: negative event length")
        if r["sv_type"].strip().upper() not in {"INS","DEL","PAV","INV","CNV","TRANS","OTHER"}:errors.append(f"events row {i}: invalid SV type")
        definition=tuple(r.get(k,"").strip() for k in ["reference_assembly","chromosome","start","end","coordinate_convention","sv_type","event_length","reference_allele","alternate_allele_or_sequence","deleted_sequence","left_flank","right_flank"])
        if key in event_defs and event_defs[key]!=definition:errors.append(f"events row {i}: inconsistent event definition for {key}")
        event_defs[key]=definition
    if len(assemblies)>1:errors.append("events: mixed reference assemblies; split files or resolve assembly before analysis")
    cross={};cross_exact=set()
    for i,r in enumerate(crosswalk,2):
        s=r["sample_id"].strip();a=r["accession_id"].strip()
        if not s or not a:errors.append(f"crosswalk row {i}: sample_id/accession_id blank")
        if s in cross and cross[s]!=a:errors.append(f"crosswalk row {i}: sample_id maps to multiple accessions")
        if s in cross_exact:errors.append(f"crosswalk row {i}: duplicate sample_id")
        cross_exact.add(s);cross[s]=a
    seen_calls=set();missing_n=0
    for i,r in enumerate(calls,2):
        cid=r["candidate_id"].strip();eid=r["event_id"].strip();s=r["sample_id"].strip();a=r["accession_id"].strip();g=r["genotype_pav"].strip();miss=r["missing_call"].strip().lower()
        if cid not in IDS:errors.append(f"calls row {i}: unrecognized candidate_id {cid}")
        if (cid,eid) not in event_keys:errors.append(f"calls row {i}: event not defined in event file: {(cid,eid)}")
        k=(cid,eid,s)
        if k in seen_calls:errors.append(f"calls row {i}: duplicate candidate/event/sample {k}")
        seen_calls.add(k)
        if not s or s not in cross:errors.append(f"calls row {i}: sample_id absent from crosswalk: {s}")
        elif cross[s]!=a:errors.append(f"calls row {i}: accession_id conflicts with crosswalk for {s}")
        if g.upper() not in VALID:errors.append(f"calls row {i}: unsupported genotype/PAV encoding {g}")
        ismissing=g.upper() in MISSING
        if miss not in {"true","false","1","0","yes","no"}:errors.append(f"calls row {i}: missing_call must be boolean-like")
        elif (miss in {"true","1","yes"})!=ismissing:errors.append(f"calls row {i}: genotype encoding conflicts with missing_call flag")
        if ismissing:missing_n+=1
        q=r.get("quality","").strip()
        if q:
            try:
                if float(q)<0:errors.append(f"calls row {i}: quality must be >=0")
            except ValueError:errors.append(f"calls row {i}: quality must be numeric when present")
    missrate=missing_n/len(calls) if calls else 0
    warnings.append(f"calls: {missing_n}/{len(calls)} missing ({missrate:.3%}); inspect event/sample-specific call rates")
    warnings.append(f"events: {len(event_keys)} defined events; {len(assemblies)} reference assembly")
    warnings.append(f"crosswalk: {len(cross)} unique sample IDs and {len(set(cross.values()))} accession IDs")
    return errors,warnings
def selftest():
    # Clearly synthetic, ephemeral parser fixtures; no real biological data are written or analyzed.
    with tempfile.TemporaryDirectory(prefix="pearl_sv_validator_synthetic_") as d:
        d=Path(d)
        def put(name,rows):
            with (d/name).open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter="\t");w.writeheader();w.writerows(rows)
        ev=[{"candidate_id":"PGLA1542300","event_id":"SYNTHETIC_TEST_ONLY","reference_assembly":"SYNTHETIC_ASM","chromosome":"chr1","start":"10","end":"20","coordinate_convention":"1-based-closed","sv_type":"DEL","event_length":"11","source_provenance":"SYNTHETIC TEST ONLY"}]
        ca=[{"candidate_id":"PGLA1542300","event_id":"SYNTHETIC_TEST_ONLY","sample_id":"SYNTHETIC_S1","accession_id":"SYNTHETIC_A1","genotype_pav":"0/1","missing_call":"false","quality":"30","source_provenance":"SYNTHETIC TEST ONLY"}]
        cw=[{"sample_id":"SYNTHETIC_S1","accession_id":"SYNTHETIC_A1","source_provenance":"SYNTHETIC TEST ONLY"}]
        put("e.tsv",ev);put("c.tsv",ca);put("x.tsv",cw)
        e,c,x=(load(d/n) for n in ["e.tsv","c.tsv","x.tsv"]);errs,_=validate(e,c,x)
        assert not errs,errs
        ca[0]["genotype_pav"]="0/9";put("c.tsv",ca);errs,_=validate(e,load(d/"c.tsv"),x)
        assert any("unsupported genotype" in a for a in errs),errs
    print("SYNTHETIC SELF-TEST PASS (temporary fixtures deleted; not biological results)")
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--events");ap.add_argument("--calls");ap.add_argument("--crosswalk");ap.add_argument("--self-test",action="store_true");a=ap.parse_args()
    if a.self_test:selftest();return 0
    if not all([a.events,a.calls,a.crosswalk]):ap.error("provide --events, --calls and --crosswalk, or --self-test")
    errs,warns=validate(load(a.events),load(a.calls),load(a.crosswalk))
    for w in warns:print("INFO",w)
    for e in errs:print("ERROR",e)
    print("VALID" if not errs else "INVALID")
    return 0 if not errs else 2
if __name__=="__main__":sys.exit(main())
'''
(OUT/'validate_future_sv_data.py').write_text(validator,encoding='utf-8')
(OUT/'sv_input_schema_README.md').write_text('''# Future SV input schema\n\nUse the three JSON Schema files for event catalogue records, accession-level calls and the sample/accession crosswalk. TSV files accepted by `validate_future_sv_data.py` must use the schema property names as column headers. Required event fields: candidate_id, event_id, reference_assembly, chromosome, start, end, coordinate_convention, sv_type, event_length, source_provenance. Optional event fields include REF/ALT or event sequence, deleted/flanking sequence, breakpoints, graph/alternate IDs, methods, validation, quality metrics and limitations. Required call fields: candidate_id, event_id, sample_id, accession_id, genotype_pav, missing_call and source_provenance; quality/depth/filter metadata are optional but recommended. Required crosswalk fields: sample_id, accession_id and source_provenance; alternate IDs and exact match method are recommended.\n\nAccepted coordinate conventions are explicitly `1-based-closed` and `0-based-half-open`. Accepted call strings include 0/1/2 dosage; diploid 0/0, 0/1, 1/1 phased or unphased forms; presence/absence labels; and explicit missing labels. Missing state and missing_call flag must agree. The validator requires a unique sample ID mapping and consistent assembly/event definition. Accessions may have multiple distinct sample IDs if documented. A schema passing check establishes formatting consistency only, not biological validity or event identity. `--self-test` uses temporary synthetic parser fixtures explicitly labeled SYNTHETIC TEST ONLY and removes them after testing; those are never written into project data or result tables.''',encoding='utf-8')

# Lightweight descriptive phenotype analysis in the existing, exact WGS-matched 231 subset.
phenoscript=r'''#!/usr/bin/env python3
"""Descriptive site-level rank concordance; no association test or causal inference."""
from pathlib import Path
import pandas as pd,numpy as np,csv,sys
source=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(exist_ok=True)
d=pd.read_csv(source,sep="\t",dtype={"GID":str})
for c in ["GID","SITE","REP","BLOCK","DM"]:assert c in d.columns,c
d["DM"]=pd.to_numeric(d["DM"],errors="raise")
assert len(d)==2772 and d["GID"].nunique()==231 and d.groupby("GID").size().eq(12).all()
assert d["SITE"].nunique()==4 and d["REP"].nunique()==3 and d["DM"].between(0,1).all() and d["DM"].notna().all()
site=d.groupby("SITE").agg(accessions=("GID","nunique"),plots=("DM","size"),mean_DM=("DM","mean"),median_DM=("DM","median"),sd_plot_DM=("DM","std"),zeros=("DM",lambda x:int((x==0).sum())),ones=("DM",lambda x:int((x==1).sum())),q90=("DM",lambda x:float(x.quantile(.9)))).reset_index()
site.to_csv(out/"phenotype_site_recomputed.tsv",sep="\t",index=False,float_format="%.8g")
means=d.groupby(["GID","SITE"],as_index=False).agg(DM_mean=("DM","mean"),DM_sd=("DM","std"),n_plots=("DM","size"))
wide=means.pivot(index="GID",columns="SITE",values="DM_mean")
wide.to_csv(out/"phenotype_accession_site_means.tsv",sep="\t",float_format="%.8g")
sites=list(wide.columns);rows=[]
for i in range(len(sites)):
 for j in range(i+1,len(sites)):
  a=wide[sites[i]].rank(method="average").to_numpy();b=wide[sites[j]].rank(method="average").to_numpy()
  rho=float(np.corrcoef(a,b)[0,1])
  rows.append([sites[i],sites[j],len(wide),rho])
pd.DataFrame(rows,columns=["site_1","site_2","accessions","spearman_rho"]).to_csv(out/"phenotype_site_rank_correlations.tsv",sep="\t",index=False,float_format="%.6f")
alllow=int((wide<=.1).all(axis=1).sum());anyhigh=int((wide>.1).any(axis=1).sum())
with (out/"phenotype_summary.txt").open("w") as f:
 f.write(f"N accessions={len(wide)}; plot rows={len(d)}; four sites; three replicates per accession-site.\n")
 f.write(f"All four site means <=0.10: {alllow}/{len(wide)}. At least one site mean >0.10: {anyhigh}/{len(wide)}.\n")
 f.write("These are descriptive summaries of bounded plot ratios; no GWAS, p-values, genotype effect or adaptation claim was produced.\n")
print(f"DESCRIPTIVE_ONLY: {len(wide)} accessions, {len(d)} plots, {len(rows)} site pairs; all-four low={alllow}; any-site >0.1={anyhigh}")
'''
(OUT/'phenotype_descriptive_analysis.py').write_text(phenoscript,encoding='utf-8')
subprocess.run([sys.executable,str(OUT/'validate_future_sv_data.py'),'--self-test'],check=True,capture_output=True,text=True)
subprocess.run([sys.executable,str(OUT/'phenotype_descriptive_analysis.py'),str(U/'matched_plot_phenotypes.tsv'),str(OUT)],check=True)

# System/literature/candidate reports.
md('master_project_status.md','''# Verified project status\n\n**Current accurate title:** “Cross-study prioritization and feasibility assessment of five pearl millet structural-variant markers for downy-mildew research.” A future original genetic-analysis title must be chosen after results.\n\nThe five fixed PGLA IDs are present in Yan et al. 2023 S19 and other-trait association context. They are not novel catalogued SVs and are not verified resistance variants. Each has only a PI537069 chromosome/position and INS/DEL class in the local source record; breakpoints, sequence, event length, exact allele representation, graph paths and accession-level PAV calls remain unresolved. No valid SV association test was performed.\n\nThe 2026 cohort audit reconciled 3,456 plot rows / 288 accessions; exact run/library/sample/GID join gives 231 WGS accessions / 2,772 plot rows. The remaining 57 phenotype-only accessions (684 rows) are excluded from genotype analyses. All matched accessions have 12 plot records across four Senegal sites and three replicates. DM is a bounded infected/total ratio, but numerator/denominator data are missing. The descriptive analysis in this package recomputes site summaries and accession rank concordance only.\n\nPublic SNP callsets are distinct builds: 843B (~32.43 GB) and updated Tift (~41.42 GB), biallelic SNPs with indels excluded; no index was listed in the audited record. Neither was downloaded; no genotype QC/PC/kinship or GWAS was run. A confirmatory scan is NO-GO; an exploratory scan is conditional and has not passed phenotype/model and genotype-QC gates.\n\nCoordinates: 148/231 have recorded values; 145 distinct pairs; 93/148 assigned to Senegal. Their biological meaning and uncertainty are undocumented; no climate values/GEA exist.\n\nThe 2015 Sharma paper screened 238 mini-core accessions against eight pathotypes and reports 62 resistant to two or more, but the project’s local Sharma phenotype file is header-only; it is not a complete 238 x 8 accession-level data matrix. Historical DM QTL and marker studies and at least two GWAS precedents exist, so “first-ever” DM genetics claims are not supportable.\n\n**Primary path:** maintain the reproducible audit and pursue a carefully gated, single-reference exploratory DMY SNP analysis only after phenotype-model and genotype QC/structure gates. The Task 15 author request can be sent by the user; no contact was made. A separate climate study remains blocked by coordinate provenance.''')

literature=[
['Yan et al. 2023','Yan H et al. Pangenomic analysis identifies structural variation associated with heat tolerance in pearl millet. Nature Genetics 55:507–518. DOI 10.1038/s41588-023-01302-4','https://doi.org/10.1038/s41588-023-01302-4','11 representative assemblies; graph/PAV framework; 242-accession PAV-GWAS','PI537069 reference; PAVs genotyped by mapping reads to vg graph; S19 is trait association summary','PAV/SNP associations for agronomic traits; no direct five-candidate DM evidence in audited S19','Primary pangenome and GWAS','Supports existing catalog context and event method; not DMY association','Assemblies/read projects public; PAV matrix not explicitly archived in data statement; IDs still need event records'],
['Sharma et al. 2015','Sharma R et al. New Sources of Resistance to Multiple Pathotypes of Sclerospora graminicola in the Pearl Millet Mini Core Germplasm Collection. Crop Science 55.','https://oar.icrisat.org/8752/','238 mini-core accessions; eight Indian pathotypes','Screened pathotype phenotypes; repository abstract reports resistant accession counts; project local data file is header-only','62 accessions resistant to 2+ pathotypes; significant accession x pathotype differences','Primary multi-pathotype phenotype study','Defines relevant phenotype precedent, not full 2026 crosswalk','Full paper restricted to ICRISAT users per OAR; complete accession x pathotype table not locally recovered'],
['Jones et al. 1995','Jones ES et al. Mapping quantitative trait loci for downy mildew resistance in pearl millet. Theoretical and Applied Genetics (1995).','https://pubmed.ncbi.nlm.nih.gov/24169834/','Biparental mapping; pathogen population-specific resistance','Pathotype/disease QTL phenotype in mapping family','Resistance QTL mapped; effects depend on pathogen population','Primary QTL','Demonstrates prior DM genetic mapping','Legacy linkage map/population not harmonized to 2026 panel'],
['Saritha et al. 2017','Saritha A et al. Mapping host-plant resistance QTLs for downy mildew in pearl millet. IJPAB 5(5):1625–1631.','https://oar.icrisat.org/10458/','295 RILs; three isolate/pathotypes; three rep greenhouse screening','Sg445, Sg519, Sg526 incidence; SSR map','Reports QTL across linkage groups in family','Primary QTL','Disease genetics precedes current study','Study-specific SSR/map and RIL population; no cohort crosswalk'],
['Chelpuri et al. 2019','Chelpuri D et al. Mapping QTLs associated with resistance to major pathotype-isolates of pearl millet downy mildew pathogen. Eur J Plant Pathol 154:983–994. DOI 10.1007/s10658-019-01718-x','https://oar.icrisat.org/11314/1/chelpuri2019.pdf','187 F8 RILs; 88 SSR markers; three Indian isolates','Seedling greenhouse incidence/resistance','Five large-effect QTLs on LG4; Sg445/Sg519/Sg526','Primary QTL','Established pathogen-specific marker evidence','Linkage coordinates not directly modern assembly alleles; large family effects may not transfer'],
['Taunk et al. 2018','Taunk J et al. Molecular breeding of ameliorating commercial pearl millet hybrid for downy mildew resistance. DOI 10.1007/s12041-018-1016-7','https://pubmed.ncbi.nlm.nih.gov/30555073/','HHB 197 breeding background','Selection/introgression phenotypes','Targets resistance loci on LG1, LG2, LG4','Primary breeding','Marker-assisted resistance precedent','Breeding background not cohort call matrix'],
['Jogaiah et al. 2014','Jogaiah S et al. Development of SCAR marker associated with downy mildew disease resistance in pearl millet. DOI 10.1007/s11033-014-3675-7','https://pubmed.ncbi.nlm.nih.gov/25156533/','Parents/F2 and 12-line diversity validation','Resistance status in small panel','ISSR-derived SCAR ISSR-863, 0.72 cM linkage','Primary marker validation','Potential target for future exact sequence/primer work','Not a public 2026 genotype matrix; locus/build/crosswalk unresolved'],
['Kanfany 2017','Kanfany G. Genetic Studies of Pearl Millet Downy Mildew Resistance in Senegal. University of Ghana thesis (2017).','https://ugspace.ug.edu.gh/items/beaa7e8b-5747-4d3d-a2ec-27366f832d90','77-genotype association; two Senegal locations (per thesis abstract)','Downy mildew phenotype reported across sites','16 significant SNPs across four linkage groups per thesis record','Public thesis / primary research','DM GWAS precedent; not “first GWAS”','Public 81.94 MB PDF; no machine-readable calls/verified cohort crosswalk established'],
['Ramu et al. 2023','Ramu et al. Improved pearl millet genomes representing the global heterotic pool offer a framework for molecular breeding applications. Communications Biology 6:902.','https://pmc.ncbi.nlm.nih.gov/articles/PMC10477261/','Corteva breeding panel for DMY; large genome-resource cohort for other traits','DM resistance phenotype generated in breeding germplasm','Reports DMY MTAs colocalizing with known QTL','Primary GWAS/genome resource','GWAS precedent; prevents “first DM GWAS” claim','No exact 2026-compatible DMY marker call/phenotype table identified in this project'],
['Subedi et al. 2026','Subedi M et al. Whole genome sequence data on diverse pearl millet accessions across the African continent. Data in Brief 66:112746. DOI 10.1016/j.dib.2026.112746','https://doi.org/10.1016/j.dib.2026.112746','288 accession phenotype panel; 231 WGS; 4 Senegal sites, 3 replicates','2024 plot DM infected/total fraction, plus flowering and panicle length','Public data resource; no DMY GWAS result in the data paper','Primary dataset paper','Best available future discovery cohort; potential multi-environment GWAS needs independent validation','231 N; population structure; local phenotype denominators absent; SNP VCF large; no current QC'],
['WorldClim 2.1 / CHELSA v2.1','Climate normal products (not trait association studies)','https://www.worldclim.org/data/worldclim21.html ; https://www.chelsa-climate.org/datasets/chelsa_bioclim','Global long-term climatology pixels','Environmental normals only','No pearl millet candidate effect/association','Authoritative environmental databases','Could support environment covariates after valid origin provenance','Coordinates unverified; no GEA or adaptation evidence']]
tsv('literature_evidence_matrix.tsv',['source','full_citation','doi_or_stable_url','population_and_sample_size','genotype_resource','phenotype_design','principal_findings','source_type','relationship_to_question','limitations'],literature)

md('phenotype_model_and_descriptive_results.md', '''# Phenotype model and descriptive analysis\n\n## Verified structure\n\nPrior QC confirms 3,456 records for 288 accessions, with 12 rows/accession (four 2024 Senegal sites x three reps); the exact WGS subset has 2,772 rows / 231 accessions, and 57 phenotype-only accessions / 684 rows were excluded from genotype analyses. In the matched 231 subset, all 2,772 DM values are present and within [0,1]; 1,946 are exact zero and 2 are exact one. The local reconciled table has no infected-plant/total-plant counts; `DM_num` is not an independently verified denominator.\n\nRecomputed site summaries and rank correlations are in the two TSVs. Site means differ strongly in the existing summary: Nioro ≈0.340, Bambey ≈0.059, Sefa ≈0.061, Sinthiou malem ≈0.023. The site rank-correlation output measures descriptive agreement in accession ordering using site means; it is not an association test, marker effect, or adaptation test.\n\n## Model choice gate\n\nA binomial/beta-binomial model cannot be fit from ratios alone without denominators. Standard beta regression also cannot directly use exact 0 and 1 without boundary handling. A fractional-logit quasi-likelihood can accept boundary fractions but treats plot ratios as equally informative unless denominator weights are recovered. Repeated plot structure, site, replicate and block must be modeled, with accession-level genotype effects and PC/kinship controls. Site-specific mean differences indicate that pooled raw phenotype means are confounded by environment.\n\nNo phenotype-GWAS was run. Before a genotype scan, seek denominator metadata from existing public files/data dictionary (no contact sent) and compare fractional-logit/mixed or robust alternatives; prespecify site effects, block structure, genotype-by-site test and multiplicity. The descriptive analysis is supportive characterization only and does not add a novel resistance locus.''')

md('climate_decision_and_minimum_data.md','''# Climate decision and minimum data\n\nCoordinates reported for 148/231 accessions (145 distinct points, 20 countries; 93/148 Senegal) have no verified source field, locality semantics, geocoding method, uncertainty or date. Therefore they cannot currently be called original accession collection locations. Trial-site coordinates are not origin climate.\n\nNo climate grids were downloaded. Before any extraction, obtain an authoritative passport/data dictionary specifying origin coordinate type/source/accuracy, verify exact accession joins, assess duplicate/clustered locations and outliers, and establish matched genetic PCs/kinship and spatial dependence. Then preselect one source/baseline and a limited temperature/precipitation/aridity panel while checking collinearity and resolution against coordinate uncertainty. Even a GEA would indicate genotype-environment correlation, not prove adaptation without fitness/experimental validation.''')

md('research_question_and_publication_strategy.md','''# Research question, title and publication strategy\n\n## Supported now\n\nThe present contribution is a reproducible data/evidence reconciliation: exact 288-to-231 phenotype-genotype cohort accounting; phenotype QC and descriptive multi-site ranking; candidate SV evidence grading; and explicit analysis gates. It is useful as a portfolio/reproducibility resource but, by itself, does not establish a novel biological result suitable for a conventional original-research manuscript.\n\n## Best future primary question\n\nConditional question: **Do common SNPs in the 231-accession African pearl millet cohort associate with plot-level downy-mildew incidence across four Senegal environments, and are marker effects stable or environment-specific after controlling for ancestry and relatedness?** The answer is unknown. The design differs from prior pathotype QTL and the 77-genotype Senegal GWAS, but a different cohort alone is not sufficient novelty. A publishable result would require robust loci, adequate power, phenotype model, genotype QC, ancestry control, and independent or functional validation.\n\n## Secondary project\n\nA separate five-SV replication should proceed only if the author request or an authoritative data release supplies exact event alleles and accession PAV calls. Do not combine it with climate GEA absent one coherent causal model. Climate remains a future independent study.\n\n## Accurate current title\n\n“Reproducible phenotype–genotype resource reconciliation and evidence audit for pearl millet downy-mildew genetics.” Avoid “pangenome-wide discovery,” “SVs associated with resistance,” “climate adaptation,” and “first-ever” in the current title.''')

md('master_execution_report.md', '''# Complete research execution report\n\n## Execution completed\n\nRead and reused the master/ultimate cohort audits and Task 13–15 packages; verified prior package checksums; confirmed the five PGLA rows and their missing event/call fields; reviewed primary pangenome, disease QTL/GWAS, phenotype cohort and climate-source evidence; inspected current disk/RAM/CPU and available tools; wrote machine-readable schemas and a future-input validator; self-tested the validator with temporary synthetic records only; recomputed a descriptive four-site phenotype summary and pairwise accession rank correlations for the exact 231-accession matched subset. Source files and prior outputs were not modified.\n\n## Results and blocked work\n\n- **Five SVs:** all five are catalogued association markers in Yan S19/external contexts; none has an event-resolved allele/PAV record or matched cohort genotype. No SV test was performed. Existing catalogue status means they are not novel variants; no direct DMY association was established in checked tables. They are not biologically disproven.\n- **Disease GWAS/replication:** 231 sequenced accessions exactly match phenotype data; 2,772 plots are repeated observations, not independent genotypes. A GWAS was not run. There is no local SNP VCF, QC/PC/kinship matrix or powered model. The two public reference-specific callsets are approximately 32.43/41.42 GB, are SNP-only and have no index listed in the audited metadata. Denominator counts are missing from the phenotype table. Confirmatory GWAS is NO-GO; exploratory scan remains conditional.\n- **Disease phenotype:** observed values are bounded incidence ratios with many zeros and exact ones, over four sites and three reps. Site means range substantially; current descriptive analysis reports rank concordance across sites. No inferential genotype association or pathotype claim follows. Sharma 2015's article abstract describes 238 mini-core accessions x eight pathotypes and 62 multi-pathotype-resistant accessions, but the local metadata file is header-only and is not the full accession-level table.\n- **Climate:** coordinate provenance and uncertainty unresolved (148/231 only, strong Senegal skew). No climate download or GEA was run. Coordinates cannot be assumed to be collection origins.\n- **Literature:** DM QTL, marker-assisted selection, a Senegal 77-genotype GWAS thesis and breeding-panel GWAS all predate this work. No “first” claim is justified.\n\n## Current conclusion\n\nStrongest supported finding: the project has a reproducible 231-accession multi-site DM phenotype/WGS overlap and a high-confidence audit showing that the five candidate PGLA IDs are not currently testable as DM SVs. The only additional biological data result generated here is descriptive accession ranking across sites. No resistance variant, causal gene, climate adaptation or new association has been demonstrated.\n\nPrimary next research direction: a gated exploratory SNP-based multi-environment DMY analysis on one reference build, only after phenotype-model and genotype-QC/structure gates pass. The smallest high-value dependencies are denominator provenance (or a justified ratio model) and a validated, QCed genotype matrix with PCs/kinship. Separately, the user may send the prepared SV data request; no message was sent.\n''')

# manifests and execution log
manifest=[]
for f in [U/'master_project_status.md',U/'matched_plot_phenotypes.tsv',U/'genotype_sample_crosswalk.tsv',U/'phenotype_qc_summary.tsv',U/'phenotype_summary_by_site.tsv',U/'phenotype_model_assessment.md',U/'statistical_power_assessment.tsv',U/'five_sv_updated_evidence.tsv',T13/'coordinate_provenance_audit.md',T14/'event_definition_recovery.tsv',T14/'accession_level_call_availability.tsv',T14/'cohort_crosswalk_assessment.tsv',T15/'final_author_data_request.md']:
    manifest.append([f.name,hashlib.sha256(f.read_bytes()).hexdigest(),str(f),'Audited local source; read-only reused','2026-10-23'])
for n,url,note in [('Yan2023','https://www.nature.com/articles/s41588-023-01302-4','Primary pangenome paper; methods, S19 and data availability'),('Sharma2015','https://oar.icrisat.org/8752/','Primary mini-core x eight pathotype phenotype study; full paper restricted at repository'),('Subedi2026','https://doi.org/10.1016/j.dib.2026.112746','Primary 2026 phenotype/WGS resource paper'),('Jones1995','https://pubmed.ncbi.nlm.nih.gov/24169834/','Primary disease QTL study'),('Saritha2017','https://oar.icrisat.org/10458/','Primary disease QTL'),('Chelpuri2019','https://oar.icrisat.org/11314/1/chelpuri2019.pdf','Primary pathotype QTL study'),('Taunk2018','https://pubmed.ncbi.nlm.nih.gov/30555073/','Primary breeding marker study'),('Jogaiah2014','https://pubmed.ncbi.nlm.nih.gov/25156533/','Primary SCAR validation study'),('Kanfany2017','https://ugspace.ug.edu.gh/items/beaa7e8b-5747-4d3d-a2ec-27366f832d90','Public thesis record, 77-genotype GWAS'),('Ramu2023','https://pmc.ncbi.nlm.nih.gov/articles/PMC10477261/','Primary breeding-panel DM association context'),('WorldClim21','https://www.worldclim.org/data/worldclim21.html','Environmental option; not downloaded'),('CHELSAv21','https://www.chelsa-climate.org/datasets/chelsa_bioclim','Environmental option; not downloaded'),('Zenodo2026','https://zenodo.org/records/18602603','Cohort data record; large genotype files not downloaded')]:manifest.append([n,'',url,note,'2026-10-23'])
tsv('source_manifest.tsv',['source','sha256_if_local','source_path_or_URL','provenance_scope','access_date'],manifest)

md('reproduce_instructions.md', '''# Reproduction instructions\n\nRun from the project directory in the named conda environment. These steps validate local reports and run only the lightweight descriptive analysis; they do not download or alter source data.\n\n1. Verify prior packages: `sha256sum -c results/ultimate_execution_20261022T180431Z/checksums.sha256` (repeat for Task 13, 14 and 15 package directories).\n2. Test the future-data validator: `python results/THIS_DIRECTORY/validate_future_sv_data.py --self-test`. Synthetic fixtures are temporary and removed.\n3. Recompute phenotype descriptions: `python results/THIS_DIRECTORY/phenotype_descriptive_analysis.py results/ultimate_execution_20261022T180431Z/matched_plot_phenotypes.tsv results/THIS_DIRECTORY`.\n4. Confirm output hashes with `sha256sum -c results/THIS_DIRECTORY/checksums.sha256`.\n\nUse exact event/call/crosswalk TSV headers described in `sv_input_schema_README.md`. The validator checks format and consistency; it does not establish biological truth.''')

md('execution_log.txt',f'''Timestamp (UTC): {OUT.name}\nProject: {P}\nEnvironment: pearl_millet, Python 3.11.15, pandas 3.0.5, NumPy 2.4.6; bcftools 1.19, R 4.3.3; 11 GiB RAM, 8 CPUs, ~927 GB free disk at inspection. PLINK2 and GEMMA not found on PATH.\nActions: prior checksums checked; candidate and cohort status tables integrated; future input schemas and validator created; temporary synthetic self-test run; descriptive phenotype site summary and site-pair rank correlations recomputed from existing 2,772 matched plot rows.\nNo VCF/climate download, association test, raw-read processing, external message, git initialization or source modification.\n''')

# Ensure validator passes self-test and record versions / validation results.
test=subprocess.run([sys.executable,str(OUT/'validate_future_sv_data.py'),'--self-test'],capture_output=True,text=True,check=True)
with (OUT/'execution_log.txt').open('a',encoding='utf-8') as f:f.write(test.stdout)
failed=[r[0] for r in checks if r[2]!='PASS']
if failed: (OUT/'execution_log.txt').open('a').write('WARNING prior checksum mismatch: '+','.join(failed)+'\n')
entries=[]
for f in sorted(OUT.iterdir()):
    if f.is_file() and f.name!='checksums.sha256':entries.append(f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}')
(OUT/'checksums.sha256').write_text('\n'.join(entries)+'\n',encoding='utf-8')
for line in (OUT/'checksums.sha256').read_text().splitlines():
    h,n=line.split('  ',1);assert hashlib.sha256((OUT/n).read_bytes()).hexdigest()==h
print(OUT)
