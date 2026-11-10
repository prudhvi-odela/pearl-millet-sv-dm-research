#!/usr/bin/env python3
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
