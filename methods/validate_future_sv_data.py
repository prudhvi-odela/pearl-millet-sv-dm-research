#!/usr/bin/env python3
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
