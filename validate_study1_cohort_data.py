#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Study 1 cohort-data validator
=============================

Run this AFTER build_study1_cohort_data.py.

It checks:
- required files exist
- expected variable names exist
- IDs and target×cohort keys are unique where required
- source/target years are plausible
- cohort assignments are correct
- structurally impossible target×cohort cells are absent
- Y_jc is correctly reconstructed from English-source citation events
- D_j and A_j match the Google Scholar source file
- missing GS collection rows are not silently recoded as D_j=0
- D_j main sample and A_j indexed-only sample are proper subsets
- row counts and merge coverage are internally consistent
- output files can be used for Study 1 without silent schema mismatches

Outputs:
    study1_cohort_final/validation_report.csv
    study1_cohort_final/validation_failures.csv
    study1_cohort_final/schema_inventory.csv
    study1_cohort_final/crossfile_counts.csv
    study1_cohort_final/validation_summary.txt
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


ID = "paper_uid_after_direct_w"
SOURCE_ID = "src_논문"

EDGE_FILE = "rq2analticsample.csv"
SOURCE_FILE = "english_source_ids.csv"
GS_FILE = "rq2analticsample_with_google_scholar_metadata.csv"
TARGET_SAMPLE_FILE = "rq2_analytic_sample_korean_target_journal_or_na.csv"

OUT_DIR = "study1_cohort_final"
FULL_PANEL_FILE = "study1_cohort_panel_full.csv"
D_MAIN_FILE = "study1_cohort_panel_D_main.csv"
A_MAIN_FILE = "study1_cohort_panel_A_indexed_only.csv"
TARGET_GS_FILE = "study1_target_level_GS.csv"

COHORTS = pd.DataFrame(
    [
        ("C1", 1900, 2009),
        ("C2", 2010, 2014),
        ("C3", 2015, 2019),
        ("C4", 2020, 2024),
    ],
    columns=["cohort", "cohort_start", "cohort_end"],
)
COHORT_ORDER = {"C1": 1, "C2": 2, "C3": 3, "C4": 4}


# ---------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------

def norm_id(s: pd.Series) -> pd.Series:
    return (
        s.astype("string")
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "<NA>": pd.NA})
    )


def safe_num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(
        s.astype("string").str.replace(",", "", regex=False).str.strip(),
        errors="coerce",
    )


def to_bin(s: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(s):
        return s.astype("Int64")
    n = pd.to_numeric(s, errors="coerce")
    vals = set(n.dropna().unique())
    if vals and vals.issubset({0, 1}):
        return n.astype("Int64")
    x = s.astype("string").str.strip().str.lower()
    out = pd.Series(pd.NA, index=s.index, dtype="Int64")
    out.loc[x.isin({"1", "true", "t", "yes", "y"})] = 1
    out.loc[x.isin({"0", "false", "f", "no", "n"})] = 0
    return out


def find_col(cols, candidates) -> Optional[str]:
    cols = set(cols)
    for c in candidates:
        if c in cols:
            return c
    return None


def cohort_from_year(y):
    if pd.isna(y):
        return pd.NA
    for _, r in COHORTS.iterrows():
        if r["cohort_start"] <= y <= r["cohort_end"]:
            return r["cohort"]
    return pd.NA


class Reporter:
    def __init__(self):
        self.rows = []

    def add(self, section, check, status, observed="", expected="", detail=""):
        self.rows.append(
            {
                "section": section,
                "check": check,
                "status": status,
                "observed": observed,
                "expected": expected,
                "detail": detail,
            }
        )

    def pass_(self, section, check, observed="", expected="", detail=""):
        self.add(section, check, "PASS", observed, expected, detail)

    def warn(self, section, check, observed="", expected="", detail=""):
        self.add(section, check, "WARN", observed, expected, detail)

    def fail(self, section, check, observed="", expected="", detail=""):
        self.add(section, check, "FAIL", observed, expected, detail)

    def frame(self):
        return pd.DataFrame(self.rows)


def read_header(path: Path):
    return pd.read_csv(path, nrows=0, encoding="utf-8-sig").columns.tolist()


def schema_rows(path: Path, df: pd.DataFrame, role: str):
    rows = []
    for c in df.columns:
        rows.append(
            {
                "file": path.name,
                "role": role,
                "column": c,
                "dtype": str(df[c].dtype),
                "non_null": int(df[c].notna().sum()),
                "null": int(df[c].isna().sum()),
                "n_unique": int(df[c].nunique(dropna=True)),
            }
        )
    return rows


# ---------------------------------------------------------------------
# validator
# ---------------------------------------------------------------------

def validate(base_dir: Path):
    rep = Reporter()
    out_dir = base_dir / OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "edges": base_dir / EDGE_FILE,
        "source": base_dir / SOURCE_FILE,
        "gs": base_dir / GS_FILE,
        "target_sample": base_dir / TARGET_SAMPLE_FILE,
        "full": out_dir / FULL_PANEL_FILE,
        "dmain": out_dir / D_MAIN_FILE,
        "amain": out_dir / A_MAIN_FILE,
        "target_gs": out_dir / TARGET_GS_FILE,
    }

    # ================================================================
    # 1. File existence
    # ================================================================
    required = ["edges", "source", "gs", "full", "dmain", "amain", "target_gs"]
    for key in required:
        p = paths[key]
        if p.exists():
            rep.pass_("files", f"{p.name} exists", observed=str(p))
        else:
            rep.fail_("files", f"{p.name} exists", observed="missing")
    if paths["target_sample"].exists():
        rep.pass_("files", f"{TARGET_SAMPLE_FILE} exists", detail="optional file found")
    else:
        rep.warn_("files", f"{TARGET_SAMPLE_FILE} exists", observed="missing", detail="optional only")

    if any(not paths[k].exists() for k in required):
        report = rep.frame()
        report.to_csv(out_dir / "validation_report.csv", index=False, encoding="utf-8-sig")
        report.loc[report.status == "FAIL"].to_csv(
            out_dir / "validation_failures.csv", index=False, encoding="utf-8-sig"
        )
        raise FileNotFoundError("Required files are missing. See validation_report.csv")

    # ================================================================
    # 2. Load efficiently
    # ================================================================
    edges = pd.read_csv(
        paths["edges"],
        encoding="utf-8-sig",
        low_memory=False,
        dtype={ID: "string", SOURCE_ID: "string"},
    )
    source = pd.read_csv(paths["source"], encoding="utf-8-sig", low_memory=False)
    gs = pd.read_csv(paths["gs"], encoding="utf-8-sig", low_memory=False, dtype={ID: "string"})
    full = pd.read_csv(paths["full"], encoding="utf-8-sig", low_memory=False, dtype={ID: "string", "cohort": "string"})
    dmain = pd.read_csv(paths["dmain"], encoding="utf-8-sig", low_memory=False, dtype={ID: "string", "cohort": "string"})
    amain = pd.read_csv(paths["amain"], encoding="utf-8-sig", low_memory=False, dtype={ID: "string", "cohort": "string"})
    target_gs = pd.read_csv(paths["target_gs"], encoding="utf-8-sig", low_memory=False, dtype={ID: "string"})

    # ================================================================
    # 3. Schema checks
    # ================================================================
    edge_required = [ID, SOURCE_ID, "ref_year"]
    full_required = [
        ID, "cohort", "cohort_start", "cohort_end",
        "target_year", "partial", "obs_start", "obs_end",
        "eng_cite_count", "Y_jc", "cohort_order", "age_jc", "age_bin",
        "D_j", "A_j", "gs_record_observed",
        "main_D_sample", "access_A_sample",
        "is_C2", "is_C3", "is_C4",
        "D_x_C2", "D_x_C3", "D_x_C4",
        "A_x_C2", "A_x_C3", "A_x_C4",
    ]
    gs_required = [
        ID,
        "google_scholar_indexed",
        "google_scholar_match_accepted",
    ]

    for label, df, required_cols in [
        ("edges", edges, edge_required),
        ("GS", gs, gs_required),
        ("full panel", full, full_required),
    ]:
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            rep.fail_("schema", f"{label} required columns", observed=str(missing), expected="none missing")
        else:
            rep.pass_("schema", f"{label} required columns", observed=len(required_cols), expected=len(required_cols))

    # Special A source check
    if "google_scholar_open_fulltext" in gs.columns:
        rep.pass_("schema", "GS verified-open variable", observed="google_scholar_open_fulltext")
        gs_open_col = "google_scholar_open_fulltext"
    elif "google_scholar_download_verified" in gs.columns:
        rep.pass_("schema", "GS verified-open variable", observed="google_scholar_download_verified")
        gs_open_col = "google_scholar_download_verified"
    else:
        rep.fail_("schema", "GS verified-open variable", observed="missing")
        gs_open_col = None

    # ================================================================
    # 4. Normalize IDs and key uniqueness
    # ================================================================
    for df in [edges, gs, full, dmain, amain, target_gs]:
        if ID in df.columns:
            df[ID] = norm_id(df[ID])
    if SOURCE_ID in edges.columns:
        edges[SOURCE_ID] = norm_id(edges[SOURCE_ID])

    gs_dup = int(gs[ID].duplicated().sum())
    if gs_dup == 0:
        rep.pass_("keys", "GS one row per target", observed=0, expected=0)
    else:
        rep.fail_("keys", "GS one row per target", observed=gs_dup, expected=0)

    tg_dup = int(target_gs[ID].duplicated().sum())
    if tg_dup == 0:
        rep.pass_("keys", "target-level GS one row per target", observed=0, expected=0)
    else:
        rep.fail_("keys", "target-level GS one row per target", observed=tg_dup, expected=0)

    full_dup = int(full.duplicated([ID, "cohort"]).sum())
    if full_dup == 0:
        rep.pass_("keys", "full panel unique target×cohort", observed=0, expected=0)
    else:
        rep.fail_("keys", "full panel unique target×cohort", observed=full_dup, expected=0)

    # ================================================================
    # 5. Cohort definitions
    # ================================================================
    expected_cohorts = set(COHORTS["cohort"])
    observed_cohorts = set(full["cohort"].dropna().astype(str).unique())
    if observed_cohorts == expected_cohorts:
        rep.pass_("cohort", "cohort labels", observed=str(sorted(observed_cohorts)), expected=str(sorted(expected_cohorts)))
    else:
        rep.fail_("cohort", "cohort labels", observed=str(sorted(observed_cohorts)), expected=str(sorted(expected_cohorts)))

    # cohort boundaries
    bad_boundary = 0
    for _, r in full[["cohort", "cohort_start", "cohort_end"]].drop_duplicates().iterrows():
        m = COHORTS.loc[COHORTS["cohort"] == r["cohort"]]
        if len(m) != 1:
            bad_boundary += 1
            continue
        er = m.iloc[0]
        if int(r["cohort_start"]) != int(er["cohort_start"]) or int(r["cohort_end"]) != int(er["cohort_end"]):
            bad_boundary += 1

    if bad_boundary == 0:
        rep.pass_("cohort", "cohort start/end boundaries", observed=0, expected=0)
    else:
        rep.fail_("cohort", "cohort start/end boundaries", observed=bad_boundary, expected=0)

    # impossible cells: target published after cohort ends
    impossible = int((safe_num(full["target_year"]) > safe_num(full["cohort_end"])).sum())
    if impossible == 0:
        rep.pass_("cohort", "no structurally impossible cells", observed=0, expected=0)
    else:
        rep.fail_("cohort", "no structurally impossible cells", observed=impossible, expected=0)

    # partial flag recomputation
    expected_partial = (
        safe_num(full["target_year"]) >= safe_num(full["cohort_start"])
    ).astype("Int64")
    observed_partial = to_bin(full["partial"])
    mismatch_partial = int(((expected_partial != observed_partial) & expected_partial.notna() & observed_partial.notna()).sum())
    if mismatch_partial == 0:
        rep.pass_("cohort", "partial flag reconstruction", observed=0, expected=0)
    else:
        rep.fail_("cohort", "partial flag reconstruction", observed=mismatch_partial, expected=0)

    # cohort order
    expected_order = full["cohort"].map(COHORT_ORDER).astype("Int64")
    observed_order = safe_num(full["cohort_order"]).astype("Int64")
    mismatch_order = int(((expected_order != observed_order) & expected_order.notna() & observed_order.notna()).sum())
    if mismatch_order == 0:
        rep.pass_("cohort", "cohort_order reconstruction", observed=0, expected=0)
    else:
        rep.fail_("cohort", "cohort_order reconstruction", observed=mismatch_order, expected=0)

    # ================================================================
    # 6. Reconstruct Y_jc from raw files
    # ================================================================
    source_header = source.columns.tolist()
    source_id_col = find_col(source_header, ["논문 ID", SOURCE_ID, "paper_id", "source_paper_id"])
    source_year_col = find_col(source_header, ["발행연도", "publication_year", "pub_year", "year"])

    if source_id_col is None or source_year_col is None:
        rep.fail_("outcome", "source ID/year variables found", observed=f"id={source_id_col}, year={source_year_col}")
    else:
        rep.pass_("outcome", "source ID/year variables found", observed=f"id={source_id_col}, year={source_year_col}")

        src = source[[source_id_col, source_year_col]].copy()
        src = src.rename(columns={source_id_col: SOURCE_ID, source_year_col: "src_year"})
        src[SOURCE_ID] = norm_id(src[SOURCE_ID])
        src["src_year"] = safe_num(src["src_year"])
        src = src.dropna(subset=[SOURCE_ID]).drop_duplicates(SOURCE_ID)

        e = edges[[ID, SOURCE_ID]].copy()
        e = e.merge(src, on=SOURCE_ID, how="inner", validate="many_to_one")
        e["cohort"] = e["src_year"].apply(cohort_from_year)
        e = e.dropna(subset=["cohort"])

        y_rebuilt = (
            e.groupby([ID, "cohort"])
            .size()
            .rename("eng_cite_count_rebuilt")
            .reset_index()
        )

        check = full[[ID, "cohort", "eng_cite_count", "Y_jc"]].merge(
            y_rebuilt, on=[ID, "cohort"], how="left", validate="one_to_one"
        )
        check["eng_cite_count_rebuilt"] = check["eng_cite_count_rebuilt"].fillna(0).astype(int)
        check["Y_rebuilt"] = (check["eng_cite_count_rebuilt"] > 0).astype(int)

        count_mismatch = int(
            (safe_num(check["eng_cite_count"]).fillna(-999) != check["eng_cite_count_rebuilt"]).sum()
        )
        y_mismatch = int(
            (safe_num(check["Y_jc"]).fillna(-999) != check["Y_rebuilt"]).sum()
        )

        if count_mismatch == 0:
            rep.pass_("outcome", "eng_cite_count reconstructed from raw edges", observed=0, expected=0)
        else:
            rep.fail_("outcome", "eng_cite_count reconstructed from raw edges", observed=count_mismatch, expected=0)

        if y_mismatch == 0:
            rep.pass_("outcome", "Y_jc reconstructed from raw edges", observed=0, expected=0)
        else:
            rep.fail_("outcome", "Y_jc reconstructed from raw edges", observed=y_mismatch, expected=0)

    # ================================================================
    # 7. GS D_j / A_j reconstruction
    # ================================================================
    if all(c in gs.columns for c in ["google_scholar_indexed", "google_scholar_match_accepted"]):
        gs["D_rebuilt"] = to_bin(gs["google_scholar_indexed"])
        accepted = to_bin(gs["google_scholar_match_accepted"])
        d_internal_mismatch = int(
            (
                gs["D_rebuilt"].notna()
                & accepted.notna()
                & (gs["D_rebuilt"] != accepted)
            ).sum()
        )
        if d_internal_mismatch == 0:
            rep.pass_("GS", "google_scholar_indexed matches match_accepted", observed=0, expected=0)
        else:
            rep.warn_("GS", "google_scholar_indexed matches match_accepted", observed=d_internal_mismatch, expected=0,
                     detail="Inspect before treating D_j as final.")

        tg = target_gs[[ID, "D_j", "A_j", "gs_record_observed"]].copy()
        gs_small = gs[[ID, "D_rebuilt"]].copy()

        if gs_open_col is not None:
            gs_small["open_raw"] = to_bin(gs[gs_open_col])
            gs_small["A_rebuilt"] = pd.Series(pd.NA, index=gs_small.index, dtype="Int64")
            m = gs_small["D_rebuilt"].eq(1)
            gs_small.loc[m, "A_rebuilt"] = gs_small.loc[m, "open_raw"].fillna(0).astype("Int64")
        else:
            gs_small["A_rebuilt"] = pd.Series(pd.NA, index=gs_small.index, dtype="Int64")

        tg_check = tg.merge(gs_small[[ID, "D_rebuilt", "A_rebuilt"]], on=ID, how="left", validate="one_to_one")

        d_mismatch = int(
            (
                tg_check["D_j"].notna()
                & tg_check["D_rebuilt"].notna()
                & (to_bin(tg_check["D_j"]) != tg_check["D_rebuilt"])
            ).sum()
        )
        a_mismatch = int(
            (
                tg_check["A_j"].notna()
                & tg_check["A_rebuilt"].notna()
                & (to_bin(tg_check["A_j"]) != tg_check["A_rebuilt"])
            ).sum()
        )

        if d_mismatch == 0:
            rep.pass_("GS", "target-level D_j matches GS source", observed=0, expected=0)
        else:
            rep.fail_("GS", "target-level D_j matches GS source", observed=d_mismatch, expected=0)

        if a_mismatch == 0:
            rep.pass_("GS", "target-level A_j matches GS verified-open source", observed=0, expected=0)
        else:
            rep.fail_("GS", "target-level A_j matches GS verified-open source", observed=a_mismatch, expected=0)

    # Missing GS records must not be D=0
    missing_gs = target_gs["gs_record_observed"].eq(0)
    bad_missing_d = int(target_gs.loc[missing_gs, "D_j"].notna().sum())
    if bad_missing_d == 0:
        rep.pass_("missingness", "missing GS records remain D_j=NA", observed=0, expected=0)
    else:
        rep.fail_("missingness", "missing GS records remain D_j=NA", observed=bad_missing_d, expected=0)

    # A is conditional on D=1
    bad_A_when_D0 = int(target_gs.loc[to_bin(target_gs["D_j"]).eq(0), "A_j"].notna().sum())
    if bad_A_when_D0 == 0:
        rep.pass_("missingness", "A_j undefined when D_j=0", observed=0, expected=0)
    else:
        rep.fail_("missingness", "A_j undefined when D_j=0", observed=bad_A_when_D0, expected=0)

    # ================================================================
    # 8. Interaction reconstruction
    # ================================================================
    for c in ["C2", "C3", "C4"]:
        expected_is = full["cohort"].eq(c).astype("Int64")
        observed_is = to_bin(full[f"is_{c}"])
        bad_is = int(((expected_is != observed_is) & observed_is.notna()).sum())

        d = to_bin(full["D_j"])
        expected_dx = (d * expected_is).astype("Int64")
        observed_dx = to_bin(full[f"D_x_{c}"])
        bad_dx = int(
            (
                expected_dx.notna()
                & observed_dx.notna()
                & (expected_dx != observed_dx)
            ).sum()
        )

        if bad_is == 0:
            rep.pass_("interaction", f"is_{c} correct", observed=0, expected=0)
        else:
            rep.fail_("interaction", f"is_{c} correct", observed=bad_is, expected=0)

        if bad_dx == 0:
            rep.pass_("interaction", f"D_x_{c} correct", observed=0, expected=0)
        else:
            rep.fail_("interaction", f"D_x_{c} correct", observed=bad_dx, expected=0)

    # ================================================================
    # 9. Subset-file consistency
    # ================================================================
    full_key = full[[ID, "cohort"]].drop_duplicates()
    d_key = dmain[[ID, "cohort"]].drop_duplicates()
    a_key = amain[[ID, "cohort"]].drop_duplicates()

    d_merged = d_key.merge(full_key, on=[ID, "cohort"], how="left", indicator=True)
    a_merged = a_key.merge(full_key, on=[ID, "cohort"], how="left", indicator=True)

    d_outside = int((d_merged["_merge"] != "both").sum())
    a_outside = int((a_merged["_merge"] != "both").sum())

    if d_outside == 0:
        rep.pass_("subsets", "D main is subset of full panel", observed=0, expected=0)
    else:
        rep.fail_("subsets", "D main is subset of full panel", observed=d_outside, expected=0)

    if a_outside == 0:
        rep.pass_("subsets", "A indexed-only is subset of full panel", observed=0, expected=0)
    else:
        rep.fail_("subsets", "A indexed-only is subset of full panel", observed=a_outside, expected=0)

    # D-main rows should satisfy GS observed + D known
    bad_dmain = int(
        (
            ~to_bin(dmain["gs_record_observed"]).eq(1)
            | dmain["D_j"].isna()
        ).sum()
    )
    if bad_dmain == 0:
        rep.pass_("subsets", "D main inclusion rule", observed=0, expected=0)
    else:
        rep.fail_("subsets", "D main inclusion rule", observed=bad_dmain, expected=0)

    # A-main rows should satisfy D=1 + A known
    bad_amain = int(
        (
            ~to_bin(amain["D_j"]).eq(1)
            | amain["A_j"].isna()
        ).sum()
    )
    if bad_amain == 0:
        rep.pass_("subsets", "A indexed-only inclusion rule", observed=0, expected=0)
    else:
        rep.fail_("subsets", "A indexed-only inclusion rule", observed=bad_amain, expected=0)

    # ================================================================
    # 10. Plausibility checks / warnings
    # ================================================================
    full_y = safe_num(full["Y_jc"])
    if set(full_y.dropna().unique()).issubset({0, 1}):
        rep.pass_("values", "Y_jc binary", observed=str(sorted(full_y.dropna().unique().tolist())))
    else:
        rep.fail_("values", "Y_jc binary", observed=str(sorted(full_y.dropna().unique().tolist()[:20])))

    dvals = safe_num(target_gs["D_j"])
    if set(dvals.dropna().unique()).issubset({0, 1}):
        rep.pass_("values", "D_j binary", observed=str(sorted(dvals.dropna().unique().tolist())))
    else:
        rep.fail_("values", "D_j binary", observed=str(sorted(dvals.dropna().unique().tolist()[:20])))

    avals = safe_num(target_gs["A_j"])
    if set(avals.dropna().unique()).issubset({0, 1}):
        rep.pass_("values", "A_j binary conditional", observed=str(sorted(avals.dropna().unique().tolist())))
    else:
        rep.fail_("values", "A_j binary conditional", observed=str(sorted(avals.dropna().unique().tolist()[:20])))

    # GS coverage
    gs_cov = float(target_gs["gs_record_observed"].mean())
    if gs_cov >= 0.95:
        rep.pass_("coverage", "GS target coverage >=95%", observed=f"{gs_cov:.2%}", expected=">=95%")
    else:
        rep.warn_("coverage", "GS target coverage >=95%", observed=f"{gs_cov:.2%}", expected=">=95%",
                 detail="Do not code uncollected targets as D=0.")

    # Cohort event counts
    cohort_counts = (
        full.groupby("cohort")
        .agg(
            n_cells=(ID, "size"),
            n_targets=(ID, "nunique"),
            Y1=("Y_jc", "sum"),
            Y_rate=("Y_jc", "mean"),
            citation_events=("eng_cite_count", "sum"),
        )
        .reset_index()
    )

    for _, r in cohort_counts.iterrows():
        if r["n_cells"] > 0:
            rep.pass_(
                "cohort_counts",
                f"{r['cohort']} nonempty",
                observed=f"cells={int(r['n_cells']):,}, Y1={int(r['Y1']):,}, rate={r['Y_rate']:.4%}",
            )
        else:
            rep.fail_("cohort_counts", f"{r['cohort']} nonempty", observed=0, expected=">0")

    # ================================================================
    # 11. Cross-file counts
    # ================================================================
    cross = pd.DataFrame(
        {
            "file": [
                EDGE_FILE,
                SOURCE_FILE,
                GS_FILE,
                FULL_PANEL_FILE,
                D_MAIN_FILE,
                A_MAIN_FILE,
                TARGET_GS_FILE,
            ],
            "rows": [
                len(edges),
                len(source),
                len(gs),
                len(full),
                len(dmain),
                len(amain),
                len(target_gs),
            ],
            "unique_targets": [
                edges[ID].nunique(),
                np.nan,
                gs[ID].nunique(),
                full[ID].nunique(),
                dmain[ID].nunique(),
                amain[ID].nunique(),
                target_gs[ID].nunique(),
            ],
        }
    )

    # ================================================================
    # 12. Schema inventory
    # ================================================================
    schema = []
    schema += schema_rows(paths["edges"], edges, "citation_edges")
    schema += schema_rows(paths["source"], source, "english_source_metadata")
    schema += schema_rows(paths["gs"], gs, "google_scholar_target_metadata")
    schema += schema_rows(paths["full"], full, "study1_full_panel")
    schema += schema_rows(paths["dmain"], dmain, "study1_D_main")
    schema += schema_rows(paths["amain"], amain, "study1_A_indexed")
    schema += schema_rows(paths["target_gs"], target_gs, "study1_target_level")
    schema_df = pd.DataFrame(schema)

    # ================================================================
    # 13. Save reports
    # ================================================================
    report = rep.frame()
    failures = report.loc[report["status"].isin(["FAIL", "WARN"])].copy()

    report.to_csv(out_dir / "validation_report.csv", index=False, encoding="utf-8-sig")
    failures.to_csv(out_dir / "validation_failures.csv", index=False, encoding="utf-8-sig")
    schema_df.to_csv(out_dir / "schema_inventory.csv", index=False, encoding="utf-8-sig")
    cross.to_csv(out_dir / "crossfile_counts.csv", index=False, encoding="utf-8-sig")
    cohort_counts.to_csv(out_dir / "validation_cohort_counts.csv", index=False, encoding="utf-8-sig")

    n_pass = int((report.status == "PASS").sum())
    n_warn = int((report.status == "WARN").sum())
    n_fail = int((report.status == "FAIL").sum())

    summary = f"""
STUDY 1 VALIDATION SUMMARY
==========================

PASS: {n_pass}
WARN: {n_warn}
FAIL: {n_fail}

Overall status:
{"READY" if n_fail == 0 else "NOT READY — inspect FAIL rows before analysis"}

Important interpretation:
- WARN does not automatically invalidate the dataset.
- FAIL means a schema, merge, cohort, outcome, or exposure inconsistency was detected.
- A missing GS record is intentionally kept as missing, not D_j=0.
- A_j is intentionally defined only when D_j=1.
- D_j in the current GS file is index presence / lookup availability from exact-title matching.

Files written:
- validation_report.csv
- validation_failures.csv
- schema_inventory.csv
- crossfile_counts.csv
- validation_cohort_counts.csv
""".strip()

    (out_dir / "validation_summary.txt").write_text(summary, encoding="utf-8")

    print("\n" + "=" * 80)
    print(summary)
    print("=" * 80)

    if n_fail:
        print("\nFAILURES:")
        print(
            report.loc[report.status == "FAIL", ["section", "check", "observed", "expected", "detail"]]
            .to_string(index=False)
        )
    if n_warn:
        print("\nWARNINGS:")
        print(
            report.loc[report.status == "WARN", ["section", "check", "observed", "expected", "detail"]]
            .to_string(index=False)
        )


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--base-dir",
        type=Path,
        default=Path("."),
        help="Folder containing the local Study 1 files.",
    )
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    validate(args.base_dir.expanduser().resolve())
