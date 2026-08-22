#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Study 1 cohort panel builder — local-files version
==================================================

This version uses ONLY files that are actually present in the user's
/Users/hyowonkim/Downloads folder:

Required:
    panel_with_offset.csv
    rq2analticsample_with_google_scholar_metadata.csv

Optional cross-check:
    rq2analticsample.csv
    rq2analticsample_with_kci_metadata_unique.csv

IMPORTANT:
- The cohort panel is the core Study 1 structure.
- N_topic_jc and ln_offset are NOT used in the final analysis dataset here.
- panel_with_offset.csv is used only as the already-built target×cohort source
  for cohort, Y_jc, citation count, target year, partial exposure, age, and topic.
"""

from __future__ import annotations
import argparse
from pathlib import Path
from typing import Optional
import numpy as np
import pandas as pd

ID = "paper_uid_after_direct_w"

PANEL_FILE = "panel_with_offset.csv"
GS_FILE = "rq2analticsample_with_google_scholar_metadata.csv"
EDGE_FILE = "rq2analticsample.csv"
KCI_UNIQUE_FILE = "rq2analticsample_with_kci_metadata_unique.csv"

OUTDIR = "study1_cohort_final"

COHORTS = {
    "C1": (1900, 2009),
    "C2": (2010, 2014),
    "C3": (2015, 2019),
    "C4": (2020, 2024),
}
COHORT_ORDER = {"C1": 1, "C2": 2, "C3": 3, "C4": 4}


def norm_id(s):
    return (
        s.astype("string").str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "<NA>": pd.NA})
    )


def to_bin(s):
    if pd.api.types.is_bool_dtype(s):
        return s.astype("Int64")
    n = pd.to_numeric(s, errors="coerce")
    vals = set(n.dropna().unique())
    if vals and vals.issubset({0, 1}):
        return n.astype("Int64")
    x = s.astype("string").str.strip().str.lower()
    out = pd.Series(pd.NA, index=s.index, dtype="Int64")
    out.loc[x.isin({"1","true","t","yes","y"})] = 1
    out.loc[x.isin({"0","false","f","no","n"})] = 0
    return out


def num(s):
    return pd.to_numeric(
        s.astype("string").str.replace(",", "", regex=False).str.strip(),
        errors="coerce"
    )


def first_existing(cols, candidates) -> Optional[str]:
    cols = set(cols)
    for c in candidates:
        if c in cols:
            return c
    return None


def build(base_dir: Path):
    panel_path = base_dir / PANEL_FILE
    gs_path = base_dir / GS_FILE
    edge_path = base_dir / EDGE_FILE
    kci_path = base_dir / KCI_UNIQUE_FILE
    outdir = base_dir / OUTDIR
    outdir.mkdir(parents=True, exist_ok=True)

    for p in [panel_path, gs_path]:
        if not p.exists():
            raise FileNotFoundError(f"Required file not found: {p}")

    print("="*80)
    print("STUDY 1 COHORT PANEL — BUILD")
    print("="*80)

    # ------------------------------------------------------------
    # 1. panel
    # ------------------------------------------------------------
    panel = pd.read_csv(
        panel_path,
        encoding="utf-8-sig",
        low_memory=False,
        dtype={ID:"string", "cohort":"string"},
    )

    required = [
        ID, "cohort", "target_year", "target_topic",
        "partial", "eng_cite_count", "Y_jc",
        "obs_start", "obs_end", "age_jc", "age_bin"
    ]
    missing = [c for c in required if c not in panel.columns]
    if missing:
        raise KeyError(f"{PANEL_FILE} missing required columns: {missing}")

    panel[ID] = norm_id(panel[ID])
    panel["target_year"] = num(panel["target_year"])
    panel["eng_cite_count"] = num(panel["eng_cite_count"]).fillna(0).astype("int64")
    panel["Y_jc"] = to_bin(panel["Y_jc"])
    panel["partial"] = to_bin(panel["partial"])
    panel["age_jc"] = num(panel["age_jc"])
    panel["obs_start"] = num(panel["obs_start"])
    panel["obs_end"] = num(panel["obs_end"])

    # We deliberately drop offset fields from the analysis dataset.
    keep_panel = required.copy()
    panel = panel[keep_panel].copy()

    if panel.duplicated([ID, "cohort"]).any():
        raise ValueError("panel has duplicated target×cohort cells")

    observed_cohorts = set(panel["cohort"].dropna().astype(str).unique())
    if observed_cohorts != set(COHORTS):
        raise ValueError(
            f"Unexpected cohort labels: {sorted(observed_cohorts)}; "
            f"expected {sorted(COHORTS)}"
        )

    panel["cohort_order"] = panel["cohort"].map(COHORT_ORDER).astype("Int64")

    # Explicit boundary fields reconstructed from the Study 1 design.
    panel["cohort_start"] = panel["cohort"].map({k:v[0] for k,v in COHORTS.items()})
    panel["cohort_end"]   = panel["cohort"].map({k:v[1] for k,v in COHORTS.items()})

    # ------------------------------------------------------------
    # 2. Google Scholar target file
    # ------------------------------------------------------------
    gs_header = pd.read_csv(gs_path, nrows=0, encoding="utf-8-sig").columns.tolist()

    wanted = [
        ID,
        "google_scholar_indexed",
        "google_scholar_match_status",
        "google_scholar_match_accepted",
        "google_scholar_match_confidence",
        "google_scholar_match_score",
        "google_scholar_title_score",
        "google_scholar_author_score",
        "google_scholar_journal_score",
        "google_scholar_year_match",
        "google_scholar_query",
        "google_scholar_query_source",
        "google_scholar_result_position",
        "google_scholar_global_result_position",
        "google_scholar_fulltext_link_provided",
        "google_scholar_oa_link_provided",
        "google_scholar_restricted_link_provided",
        "google_scholar_open_fulltext",
        "google_scholar_fulltext_access",
        "google_scholar_access_verified",
        "google_scholar_download_verified",
        "google_scholar_access_block_reason",
        "google_scholar_access_verification_error",
        "google_scholar_citation_count",
        "google_scholar_year",
        "google_scholar_source",
        "google_scholar_primary_domain",
        "kci_journal_name",
        "kci_pub_year",
        "kci_title_original",
        "kci_title_english",
        "ref_title",
        "ref_author",
        "ref_publisher_or_journal",
        "ref_year",
    ]
    usecols = [c for c in wanted if c in gs_header]
    if ID not in usecols:
        raise KeyError(f"{GS_FILE} missing {ID}")

    gs = pd.read_csv(
        gs_path,
        usecols=usecols,
        encoding="utf-8-sig",
        low_memory=False,
        dtype={ID:"string"},
    )
    gs[ID] = norm_id(gs[ID])
    gs = gs.dropna(subset=[ID]).copy()

    if gs[ID].duplicated().any():
        raise ValueError(
            f"{GS_FILE} must be one row per target; "
            f"duplicated IDs={gs.loc[gs[ID].duplicated(False), ID].nunique():,}"
        )

    if "google_scholar_indexed" not in gs.columns:
        raise KeyError("google_scholar_indexed is missing from GS file")

    gs["D_j"] = to_bin(gs["google_scholar_indexed"])

    # A_j: verified open full text, conditional on D=1.
    if "google_scholar_open_fulltext" in gs.columns:
        open_raw = to_bin(gs["google_scholar_open_fulltext"])
    elif "google_scholar_download_verified" in gs.columns:
        open_raw = to_bin(gs["google_scholar_download_verified"])
    else:
        raise KeyError(
            "Neither google_scholar_open_fulltext nor "
            "google_scholar_download_verified exists."
        )

    gs["A_j"] = pd.Series(pd.NA, index=gs.index, dtype="Int64")
    m = gs["D_j"].eq(1)
    gs.loc[m, "A_j"] = open_raw.loc[m].fillna(0).astype("Int64")

    journal_source = first_existing(
        gs.columns, ["kci_journal_name", "ref_publisher_or_journal"]
    )
    if journal_source:
        gs["journal_fe"] = (
            gs[journal_source].astype("string").str.strip()
            .replace({"":pd.NA, "nan":pd.NA, "None":pd.NA})
        )
    else:
        gs["journal_fe"] = pd.Series(pd.NA, index=gs.index, dtype="string")

    if "google_scholar_citation_count" in gs.columns:
        gs["gs_citation_count"] = num(gs["google_scholar_citation_count"])
        gs["log1p_gs_citation_count"] = np.log1p(
            gs["gs_citation_count"].clip(lower=0)
        )

    # ------------------------------------------------------------
    # 3. Target-level master and merge
    # ------------------------------------------------------------
    panel_targets = panel[[ID, "target_year", "target_topic"]].drop_duplicates(ID)
    gs_ids = set(gs[ID].dropna())
    panel_targets["gs_record_observed"] = panel_targets[ID].isin(gs_ids).astype("Int64")

    target_master = panel_targets.merge(
        gs,
        on=ID,
        how="left",
        validate="one_to_one",
        suffixes=("", "_gs"),
    )

    # Optional raw/KCI membership checks only.
    if edge_path.exists():
        edge_ids = pd.read_csv(
            edge_path,
            usecols=[ID],
            encoding="utf-8-sig",
            dtype={ID:"string"},
        )
        edge_ids[ID] = norm_id(edge_ids[ID])
        edge_set = set(edge_ids[ID].dropna())
        target_master["present_in_rq2analticsample"] = (
            target_master[ID].isin(edge_set).astype("Int64")
        )

    if kci_path.exists():
        kci_ids = pd.read_csv(
            kci_path,
            usecols=[ID],
            encoding="utf-8-sig",
            dtype={ID:"string"},
        )
        kci_ids[ID] = norm_id(kci_ids[ID])
        kci_set = set(kci_ids[ID].dropna())
        target_master["present_in_kci_unique"] = (
            target_master[ID].isin(kci_set).astype("Int64")
        )

    merge_cols = [
        c for c in target_master.columns
        if c not in {"target_year", "target_topic"}
    ]

    final = panel.merge(
        target_master[merge_cols],
        on=ID,
        how="left",
        validate="many_to_one",
    )

    # ------------------------------------------------------------
    # 4. Study 1 cohort interactions
    # ------------------------------------------------------------
    for c in ["C2", "C3", "C4"]:
        final[f"is_{c}"] = final["cohort"].eq(c).astype("Int64")
        final[f"D_x_{c}"] = (final["D_j"] * final[f"is_{c}"]).astype("Int64")
        final[f"A_x_{c}"] = (final["A_j"] * final[f"is_{c}"]).astype("Int64")

    final["main_D_sample"] = (
        final["gs_record_observed"].eq(1) & final["D_j"].notna()
    ).astype("Int64")

    final["access_A_sample"] = (
        final["gs_record_observed"].eq(1)
        & final["D_j"].eq(1)
        & final["A_j"].notna()
    ).astype("Int64")

    # ------------------------------------------------------------
    # 5. Outputs
    # ------------------------------------------------------------
    full_path = outdir / "study1_cohort_panel_full.csv"
    d_path = outdir / "study1_cohort_panel_D_main.csv"
    a_path = outdir / "study1_cohort_panel_A_indexed_only.csv"
    t_path = outdir / "study1_target_level_GS.csv"

    final.to_csv(full_path, index=False, encoding="utf-8-sig")
    final.loc[final["main_D_sample"].eq(1)].to_csv(
        d_path, index=False, encoding="utf-8-sig"
    )
    final.loc[final["access_A_sample"].eq(1)].to_csv(
        a_path, index=False, encoding="utf-8-sig"
    )
    target_master.to_csv(t_path, index=False, encoding="utf-8-sig")

    cohort_summary = (
        final.groupby("cohort")
        .agg(
            n_cells=(ID,"size"),
            n_targets=(ID,"nunique"),
            Y1=("Y_jc","sum"),
            Y_rate=("Y_jc","mean"),
            eng_citation_events=("eng_cite_count","sum"),
            partial_cells=("partial","sum"),
        )
        .reindex(["C1","C2","C3","C4"])
        .reset_index()
    )
    cohort_summary.to_csv(
        outdir / "cohort_summary.csv", index=False, encoding="utf-8-sig"
    )

    diagnostics = pd.DataFrame({
        "metric":[
            "panel_rows",
            "panel_unique_targets",
            "GS_unique_targets",
            "panel_targets_with_GS_record",
            "GS_coverage_rate",
            "D_main_rows",
            "D_main_targets",
            "A_indexed_rows",
            "A_indexed_targets",
        ],
        "value":[
            len(final),
            final[ID].nunique(),
            gs[ID].nunique(),
            target_master["gs_record_observed"].sum(),
            target_master["gs_record_observed"].mean(),
            int(final["main_D_sample"].sum()),
            final.loc[final["main_D_sample"].eq(1), ID].nunique(),
            int(final["access_A_sample"].sum()),
            final.loc[final["access_A_sample"].eq(1), ID].nunique(),
        ]
    })
    diagnostics.to_csv(
        outdir / "build_diagnostics.csv", index=False, encoding="utf-8-sig"
    )

    print("\nCreated:")
    for p in [full_path, d_path, a_path, t_path]:
        print(" ", p)
    print("\nDiagnostics:")
    print(diagnostics.to_string(index=False))
    print("\nNOTE: N_topic_jc and ln_offset were intentionally NOT included.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base-dir", type=Path, required=True)
    args = p.parse_args()
    build(args.base_dir.expanduser().resolve())


if __name__ == "__main__":
    main()
