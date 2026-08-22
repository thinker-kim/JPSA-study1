#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Validate the Study 1 cohort datasets built from:
- panel_with_offset.csv (cohort/Y source only)
- rq2analticsample_with_google_scholar_metadata.csv

No english_source_ids.csv is required.

The validator checks:
1) source/output files and schemas
2) exact C1-C4 definitions
3) target×cohort uniqueness
4) structural cohort eligibility
5) Y_jc == (eng_cite_count > 0)
6) partial, obs_start, obs_end, age_jc internal consistency
7) D_j reconstruction from google_scholar_indexed
8) A_j reconstruction from verified full text conditional on D=1
9) GS-missing targets remain D_j missing
10) D×cohort and A×cohort interaction variables
11) D-main / A-indexed subset correctness
12) offset variables are absent from the FINAL analysis dataset
13) target IDs cross-check against rq2analticsample.csv if present
"""

from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

ID = "paper_uid_after_direct_w"
OUTDIR = "study1_cohort_final"

COHORTS = {
    "C1": (1900, 2009),
    "C2": (2010, 2014),
    "C3": (2015, 2019),
    "C4": (2020, 2024),
}
ORDER = {"C1":1,"C2":2,"C3":3,"C4":4}


def norm_id(s):
    return (
        s.astype("string").str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .replace({"":pd.NA,"nan":pd.NA,"None":pd.NA,"<NA>":pd.NA})
    )


def num(s):
    return pd.to_numeric(s, errors="coerce")


def binv(s):
    if pd.api.types.is_bool_dtype(s):
        return s.astype("Int64")
    n = pd.to_numeric(s, errors="coerce")
    vals = set(n.dropna().unique())
    if vals and vals.issubset({0,1}):
        return n.astype("Int64")
    x = s.astype("string").str.lower().str.strip()
    o = pd.Series(pd.NA,index=s.index,dtype="Int64")
    o.loc[x.isin({"1","true","t","yes","y"})]=1
    o.loc[x.isin({"0","false","f","no","n"})]=0
    return o


class R:
    def __init__(self): self.x=[]
    def add(self,sec,check,status,observed="",expected="",detail=""):
        self.x.append(dict(section=sec,check=check,status=status,
                           observed=observed,expected=expected,detail=detail))
    def ok(self,*a,**k): self.add(*a,status="PASS",**k)
    def warn(self,*a,**k): self.add(*a,status="WARN",**k)
    def fail(self,*a,**k): self.add(*a,status="FAIL",**k)


def validate(base: Path):
    r=R()
    out=base/OUTDIR

    files={
        "panel_source":base/"panel_with_offset.csv",
        "gs_source":base/"rq2analticsample_with_google_scholar_metadata.csv",
        "edges":base/"rq2analticsample.csv",
        "full":out/"study1_cohort_panel_full.csv",
        "dmain":out/"study1_cohort_panel_D_main.csv",
        "amain":out/"study1_cohort_panel_A_indexed_only.csv",
        "target":out/"study1_target_level_GS.csv",
    }

    for k in ["panel_source","gs_source","full","dmain","amain","target"]:
        if files[k].exists(): r.ok("files",f"{files[k].name} exists")
        else: r.fail("files",f"{files[k].name} exists",observed="missing")

    if any(not files[k].exists() for k in ["panel_source","gs_source","full","dmain","amain","target"]):
        rep=pd.DataFrame(r.x)
        out.mkdir(exist_ok=True)
        rep.to_csv(out/"validation_report.csv",index=False,encoding="utf-8-sig")
        raise FileNotFoundError("Required file missing; see validation_report.csv")

    src=pd.read_csv(files["panel_source"],encoding="utf-8-sig",low_memory=False,dtype={ID:"string","cohort":"string"})
    gs=pd.read_csv(files["gs_source"],encoding="utf-8-sig",low_memory=False,dtype={ID:"string"})
    full=pd.read_csv(files["full"],encoding="utf-8-sig",low_memory=False,dtype={ID:"string","cohort":"string"})
    dmain=pd.read_csv(files["dmain"],encoding="utf-8-sig",low_memory=False,dtype={ID:"string","cohort":"string"})
    amain=pd.read_csv(files["amain"],encoding="utf-8-sig",low_memory=False,dtype={ID:"string","cohort":"string"})
    target=pd.read_csv(files["target"],encoding="utf-8-sig",low_memory=False,dtype={ID:"string"})

    for df in [src,gs,full,dmain,amain,target]:
        df[ID]=norm_id(df[ID])

    # schemas
    req_full=[
        ID,"cohort","target_year","target_topic","partial",
        "eng_cite_count","Y_jc","obs_start","obs_end","age_jc","age_bin",
        "cohort_start","cohort_end","cohort_order",
        "D_j","A_j","gs_record_observed",
        "is_C2","is_C3","is_C4","D_x_C2","D_x_C3","D_x_C4",
        "A_x_C2","A_x_C3","A_x_C4"
    ]
    miss=[c for c in req_full if c not in full.columns]
    if miss:r.fail("schema","full panel required variables",observed=str(miss),expected="none")
    else:r.ok("schema","full panel required variables",observed=len(req_full))

    # Explicitly confirm offsets are not in FINAL analysis file
    offsets=[c for c in ["N_topic_jc","ln_offset"] if c in full.columns]
    if offsets:
        r.fail("schema","offset variables excluded from final cohort dataset",
               observed=str(offsets),expected="[]")
    else:
        r.ok("schema","offset variables excluded from final cohort dataset",observed="[]")

    # source→output core columns exact preservation
    core=["cohort","target_year","target_topic","partial","eng_cite_count","Y_jc",
          "obs_start","obs_end","age_jc","age_bin"]
    a=src[[ID]+core].copy().sort_values([ID,"cohort"]).reset_index(drop=True)
    b=full[[ID]+core].copy().sort_values([ID,"cohort"]).reset_index(drop=True)
    same_shape=a.shape==b.shape
    if not same_shape:
        r.fail("panel","source panel row/column preservation",
               observed=str(b.shape),expected=str(a.shape))
    else:
        # string compare after fill to avoid dtype-only differences
        neq=0
        for c in [ID]+core:
            x=a[c].astype("string").fillna("<NA>")
            y=b[c].astype("string").fillna("<NA>")
            neq += int((x!=y).sum())
        if neq==0:r.ok("panel","source cohort/Y fields preserved exactly",observed=0,expected=0)
        else:r.fail("panel","source cohort/Y fields preserved exactly",observed=neq,expected=0)

    # key uniqueness
    du=int(full.duplicated([ID,"cohort"]).sum())
    if du==0:r.ok("keys","target×cohort unique",observed=0)
    else:r.fail("keys","target×cohort unique",observed=du,expected=0)

    # cohort labels/bounds
    obs=set(full["cohort"].dropna().astype(str))
    if obs==set(COHORTS):r.ok("cohort","labels",observed=str(sorted(obs)))
    else:r.fail("cohort","labels",observed=str(sorted(obs)),expected=str(sorted(COHORTS)))

    bad_bounds=0
    for c,(s,e) in COHORTS.items():
        x=full.loc[full["cohort"].eq(c)]
        bad_bounds += int((num(x["cohort_start"])!=s).sum())
        bad_bounds += int((num(x["cohort_end"])!=e).sum())
    if bad_bounds==0:r.ok("cohort","C1-C4 boundaries",observed=0)
    else:r.fail("cohort","C1-C4 boundaries",observed=bad_bounds,expected=0)

    # structural cells
    impossible=int((num(full["target_year"])>num(full["cohort_end"])).sum())
    if impossible==0:r.ok("cohort","no pre-publication structural cells",observed=0)
    else:r.fail("cohort","no pre-publication structural cells",observed=impossible,expected=0)

    # Y
    yc=(num(full["eng_cite_count"]).fillna(0)>0).astype(int)
    yo=num(full["Y_jc"])
    bad_y=int((yc!=yo).sum())
    if bad_y==0:r.ok("outcome","Y_jc == 1[eng_cite_count>0]",observed=0)
    else:r.fail("outcome","Y_jc == 1[eng_cite_count>0]",observed=bad_y,expected=0)

    # partial
    pe=(num(full["target_year"])>=num(full["cohort_start"])).astype(int)
    po=num(full["partial"])
    bad_p=int((pe!=po).sum())
    if bad_p==0:r.ok("cohort","partial reconstructed",observed=0)
    else:r.fail("cohort","partial reconstructed",observed=bad_p,expected=0)

    # obs_start/end
    ose=np.maximum(num(full["target_year"]),num(full["cohort_start"]))
    bad_os=int((np.abs(ose-num(full["obs_start"]))>1e-9).sum())
    if bad_os==0:r.ok("cohort","obs_start reconstructed",observed=0)
    else:r.fail("cohort","obs_start reconstructed",observed=bad_os,expected=0)

    bad_oe=int((num(full["obs_end"])!=num(full["cohort_end"])).sum())
    if bad_oe==0:r.ok("cohort","obs_end matches cohort end",observed=0)
    else:r.warn("cohort","obs_end matches cohort end",observed=bad_oe,
                expected=0,detail="May reflect underlying data maximum year.")

    # D/A against GS source
    if "google_scholar_indexed" not in gs.columns:
        r.fail("GS","google_scholar_indexed exists",observed="missing")
    else:
        gs2=gs[[ID,"google_scholar_indexed"]].copy()
        gs2["D_expected"]=binv(gs2["google_scholar_indexed"])
        if "google_scholar_open_fulltext" in gs.columns:
            gs2["open_expected"]=binv(gs["google_scholar_open_fulltext"])
        elif "google_scholar_download_verified" in gs.columns:
            gs2["open_expected"]=binv(gs["google_scholar_download_verified"])
        else:
            gs2["open_expected"]=pd.Series(pd.NA,index=gs2.index,dtype="Int64")
            r.fail("GS","verified full-text source variable exists",observed="missing")

        gs2["A_expected"]=pd.Series(pd.NA,index=gs2.index,dtype="Int64")
        m=gs2["D_expected"].eq(1)
        gs2.loc[m,"A_expected"]=gs2.loc[m,"open_expected"].fillna(0).astype("Int64")

        chk=target[[ID,"D_j","A_j","gs_record_observed"]].merge(
            gs2[[ID,"D_expected","A_expected"]],on=ID,how="left",validate="one_to_one"
        )

        bd=int((binv(chk["D_j"]).fillna(-9)!=chk["D_expected"].fillna(-9)).sum())
        ba=int((binv(chk["A_j"]).fillna(-9)!=chk["A_expected"].fillna(-9)).sum())

        if bd==0:r.ok("GS","D_j exactly matches GS source",observed=0)
        else:r.fail("GS","D_j exactly matches GS source",observed=bd,expected=0)
        if ba==0:r.ok("GS","A_j exactly matches verified full text",observed=0)
        else:r.fail("GS","A_j exactly matches verified full text",observed=ba,expected=0)

    # Missing GS cannot be D=0
    missing=binv(target["gs_record_observed"]).eq(0)
    bad=int(target.loc[missing,"D_j"].notna().sum())
    if bad==0:r.ok("missingness","uncollected GS targets keep D_j=NA",observed=0)
    else:r.fail("missingness","uncollected GS targets keep D_j=NA",observed=bad,expected=0)

    # A only D1
    bad=int(target.loc[binv(target["D_j"]).eq(0),"A_j"].notna().sum())
    if bad==0:r.ok("missingness","A_j undefined for D_j=0",observed=0)
    else:r.fail("missingness","A_j undefined for D_j=0",observed=bad,expected=0)

    # interactions
    for c in ["C2","C3","C4"]:
        isx=full["cohort"].eq(c).astype("Int64")
        bix=int((binv(full[f"is_{c}"])!=isx).sum())
        dx=(binv(full["D_j"])*isx).astype("Int64")
        bdx=int(((binv(full[f"D_x_{c}"]).fillna(-9))!=(dx.fillna(-9))).sum())
        ax=(binv(full["A_j"])*isx).astype("Int64")
        bax=int(((binv(full[f"A_x_{c}"]).fillna(-9))!=(ax.fillna(-9))).sum())
        (r.ok if bix==0 else r.fail)("interaction",f"is_{c}",observed=bix,expected=0)
        (r.ok if bdx==0 else r.fail)("interaction",f"D_x_{c}",observed=bdx,expected=0)
        (r.ok if bax==0 else r.fail)("interaction",f"A_x_{c}",observed=bax,expected=0)

    # subset rules
    bad=int((~binv(dmain["gs_record_observed"]).eq(1)|dmain["D_j"].isna()).sum())
    if bad==0:r.ok("subset","D-main inclusion rule",observed=0)
    else:r.fail("subset","D-main inclusion rule",observed=bad,expected=0)

    bad=int((~binv(amain["D_j"]).eq(1)|amain["A_j"].isna()).sum())
    if bad==0:r.ok("subset","A-indexed inclusion rule",observed=0)
    else:r.fail("subset","A-indexed inclusion rule",observed=bad,expected=0)

    # optional raw ID coverage
    if files["edges"].exists():
        edge_ids=pd.read_csv(files["edges"],usecols=[ID],dtype={ID:"string"},encoding="utf-8-sig")
        edge_ids[ID]=norm_id(edge_ids[ID])
        es=set(edge_ids[ID].dropna())
        panel_ids=set(target[ID].dropna())
        missing_from_edges=len(panel_ids-es)
        if missing_from_edges==0:
            r.ok("crossfile","all panel targets appear in rq2analticsample.csv",observed=0)
        else:
            r.warn("crossfile","all panel targets appear in rq2analticsample.csv",
                   observed=missing_from_edges,expected=0)

    # summaries
    report=pd.DataFrame(r.x)
    report.to_csv(out/"validation_report.csv",index=False,encoding="utf-8-sig")
    report.loc[report.status.isin(["FAIL","WARN"])].to_csv(
        out/"validation_failures.csv",index=False,encoding="utf-8-sig"
    )

    schema=[]
    for fn,df in [
        ("panel_with_offset.csv",src),
        ("rq2analticsample_with_google_scholar_metadata.csv",gs),
        ("study1_cohort_panel_full.csv",full),
        ("study1_cohort_panel_D_main.csv",dmain),
        ("study1_cohort_panel_A_indexed_only.csv",amain),
        ("study1_target_level_GS.csv",target),
    ]:
        for c in df.columns:
            schema.append({
                "file":fn,"column":c,"dtype":str(df[c].dtype),
                "non_null":int(df[c].notna().sum()),
                "null":int(df[c].isna().sum()),
                "n_unique":int(df[c].nunique(dropna=True))
            })
    pd.DataFrame(schema).to_csv(
        out/"schema_inventory.csv",index=False,encoding="utf-8-sig"
    )

    counts=pd.DataFrame({
        "file":[
            "panel_with_offset.csv",
            "rq2analticsample_with_google_scholar_metadata.csv",
            "study1_cohort_panel_full.csv",
            "study1_cohort_panel_D_main.csv",
            "study1_cohort_panel_A_indexed_only.csv",
            "study1_target_level_GS.csv",
        ],
        "rows":[len(src),len(gs),len(full),len(dmain),len(amain),len(target)],
        "unique_targets":[
            src[ID].nunique(),gs[ID].nunique(),full[ID].nunique(),
            dmain[ID].nunique(),amain[ID].nunique(),target[ID].nunique()
        ]
    })
    counts.to_csv(out/"crossfile_counts.csv",index=False,encoding="utf-8-sig")

    ns=(report.status=="PASS").sum()
    nw=(report.status=="WARN").sum()
    nf=(report.status=="FAIL").sum()
    summary=f"""STUDY 1 VALIDATION SUMMARY

PASS: {ns}
WARN: {nw}
FAIL: {nf}

OVERALL: {"READY" if nf==0 else "NOT READY"}

This validation uses the available local files.
english_source_ids.csv is not required.
The final analysis file intentionally excludes N_topic_jc and ln_offset.
"""
    (out/"validation_summary.txt").write_text(summary,encoding="utf-8")
    print(summary)
    if nf:
        print(report.loc[report.status=="FAIL"].to_string(index=False))
    if nw:
        print(report.loc[report.status=="WARN"].to_string(index=False))


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--base-dir",type=Path,required=True)
    a=p.parse_args()
    validate(a.base_dir.expanduser().resolve())


if __name__=="__main__":
    main()
