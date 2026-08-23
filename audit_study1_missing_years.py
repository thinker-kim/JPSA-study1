#!/usr/bin/env python3
"""Audit Study 1 targets excluded because publication year is missing."""

from pathlib import Path
import math
import pandas as pd

BASE = Path(__file__).resolve().parent
ID = "paper_uid_after_direct_w"
OUT = BASE / "study1_analysis"
OUT.mkdir(exist_ok=True)

missing = pd.read_csv(
    BASE / "study1_sample_validation/panel_missing_targets.csv",
    usecols=[ID, "exclusion_reason"],
    dtype={ID: "string"},
)
missing = missing.loc[missing["exclusion_reason"].eq("missing_target_year")].copy()

cols = [
    ID, "ref_year", "search_pub_year", "kci_pub_year", "google_scholar_year",
    "google_scholar_match_status", "google_scholar_indexed",
    "google_scholar_citation_count", "kci_verified",
]
gs = pd.read_csv(
    BASE / "rq2analticsample_with_google_scholar_metadata.csv",
    usecols=cols,
    dtype={ID: "string"},
    low_memory=False,
).drop_duplicates(ID)
x = missing.merge(gs, on=ID, how="left", validate="one_to_one")

status = x["google_scholar_match_status"].astype("string").str.strip().str.lower()
d = pd.to_numeric(x["google_scholar_indexed"], errors="coerce").astype("Float64")
d.loc[status.eq("review")] = 0
d.loc[status.isin({"api_error", "processing_error", "missing_search_title"})] = pd.NA
x["D_j_audit"] = d

year_cols = ["kci_pub_year", "search_pub_year", "google_scholar_year", "ref_year"]
valid_years = {}
for col in year_cols:
    y = pd.to_numeric(x[col], errors="coerce")
    valid_years[col] = y.where(y.between(1900, 2024))

recovered = valid_years[year_cols[0]]
for col in year_cols[1:]:
    recovered = recovered.combine_first(valid_years[col])
x["recoverable_target_year"] = recovered
x["year_recovery_source"] = pd.NA
for col in year_cols:
    take = x["year_recovery_source"].isna() & valid_years[col].notna()
    x.loc[take, "year_recovery_source"] = col

included = pd.read_csv(
    BASE / "study1_cohort_final/study1_target_level_GS.csv",
    usecols=[ID, "D_j"],
    dtype={ID: "string"},
)
included_d = pd.to_numeric(included["D_j"], errors="coerce")

inc_d1 = int(included_d.eq(1).sum())
inc_d0 = int(included_d.eq(0).sum())
mis_d1 = int(x["D_j_audit"].eq(1).sum())
mis_d0 = int(x["D_j_audit"].eq(0).sum())
mis_err = int(x["D_j_audit"].isna().sum())

rate_missing_d1 = mis_d1 / (inc_d1 + mis_d1)
rate_missing_d0 = mis_d0 / (inc_d0 + mis_d0)
pooled = (mis_d1 + mis_d0) / (inc_d1 + inc_d0 + mis_d1 + mis_d0)
se = math.sqrt(
    pooled * (1 - pooled)
    * (1 / (inc_d1 + mis_d1) + 1 / (inc_d0 + mis_d0))
)
z = (rate_missing_d0 - rate_missing_d1) / se

summary = pd.DataFrame(
    [
        ("missing-year targets", len(x)),
        ("missing-year D=1", mis_d1),
        ("missing-year D=0", mis_d0),
        ("missing-year D error/NA", mis_err),
        ("indexed share among determinate missing-year targets", mis_d1 / (mis_d1 + mis_d0)),
        ("indexed share among included targets", inc_d1 / (inc_d1 + inc_d0)),
        ("publication-year missing rate among D=1", rate_missing_d1),
        ("publication-year missing rate among D=0", rate_missing_d0),
        ("D=0 / D=1 missingness risk ratio", rate_missing_d0 / rate_missing_d1),
        ("two-proportion z statistic", z),
        ("year recoverable from enriched metadata", int(recovered.notna().sum())),
        ("year still unavailable", int(recovered.isna().sum())),
    ],
    columns=["metric", "value"],
)

x.to_csv(OUT / "missing_year_target_audit.csv", index=False, encoding="utf-8-sig")
summary.to_csv(OUT / "missing_year_summary.csv", index=False, encoding="utf-8-sig")

print(summary.to_string(index=False))
