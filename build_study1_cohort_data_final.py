#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Study 1 cohort-panel builder
============================

Local input files expected in --base-dir:
1) panel_with_offset.csv
2) rq2analticsample_with_google_scholar_metadata.csv

Optional cross-check inputs:
3) rq2analticsample.csv
4) rq2analticsample_with_kci_metadata_unique.csv

Core Study 1 structure:
- Unit: target paper j × cohort c
- C1: <= 2009
- C2: 2010–2014
- C3: 2015–2019
- C4: 2020–2024
- Outcome: Y_jc
- Main exposure: D_j = google_scholar_indexed
- Access: A_j = google_scholar_open_fulltext, defined only when D_j=1
- Main estimand: D_j × cohort

IMPORTANT:
panel_with_offset.csv is used only because it already contains the correctly
constructed target×cohort panel and Y_jc. The final analysis datasets created
here intentionally EXCLUDE N_topic_jc and ln_offset.
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
ORDER = {"C1": 1, "C2": 2, "C3": 3, "C4": 4}


def norm_id(s: pd.Series) -> pd.Series:
    return (
        s.astype("string")
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "<NA>": pd.NA})
    )


def num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(
        s.astype("string").str.replace(",", "", regex=False).str.strip(),
        errors="coerce",
    )


def bin01(s: pd.Series) -> pd.Series:
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


def first_existing(columns, candidates) -> Optional[str]:
    cols = set(columns)
    for c in candidates:
        if c in cols:
            return c
    return None


def build(base_dir: Path) -> None:
    base_dir = base_dir.expanduser().resolve()
    panel_path = base_dir / PANEL_FILE
    gs_path = base_dir / GS_FILE
    edge_path = base_dir / EDGE_FILE
    kci_unique_path = base_dir / KCI_UNIQUE_FILE

    outdir = base_dir / OUTDIR
    outdir.mkdir(parents=True, exist_ok=True)

    for p in (panel_path, gs_path):
        if not p.exists():
            raise FileNotFoundError(f"Required file not found: {p}")

    print("=" * 80)
    print("STUDY 1 — BUILD COHORT ANALYSIS DATA")
    print("=" * 80)

    # ------------------------------------------------------------------
    # 1) Load existing target × cohort panel
    # ------------------------------------------------------------------
    panel = pd.read_csv(
        panel_path,
        encoding="utf-8-sig",
        low_memory=False,
        dtype={ID: "string", "cohort": "string"},
    )

    required_panel = [
        ID, "cohort", "target_year", "target_topic",
        "partial", "eng_cite_count", "Y_jc",
        "obs_start", "obs_end", "age_jc", "age_bin",
    ]
    missing = [c for c in required_panel if c not in panel.columns]
    if missing:
        raise KeyError(f"{PANEL_FILE} missing columns: {missing}")

    panel = panel[required_panel].copy()
    panel[ID] = norm_id(panel[ID])
    panel["target_year"] = num(panel["target_year"])
    panel["eng_cite_count"] = num(panel["eng_cite_count"]).fillna(0).astype("int64")
    panel["Y_jc"] = bin01(panel["Y_jc"])
    panel["partial"] = bin01(panel["partial"])
    panel["obs_start"] = num(panel["obs_start"])
    panel["obs_end"] = num(panel["obs_end"])
    panel["age_jc"] = num(panel["age_jc"])

    if panel[ID].isna().any():
        raise ValueError("panel contains missing target IDs")

    if panel.duplicated([ID, "cohort"]).any():
        raise ValueError("panel contains duplicated target×cohort cells")

    observed = set(panel["cohort"].dropna().astype(str).unique())
    if observed != set(COHORTS):
        raise ValueError(
            f"Unexpected cohort labels: {sorted(observed)}; "
            f"expected {sorted(COHORTS)}"
        )

    panel["cohort_order"] = panel["cohort"].map(ORDER).astype("Int64")
    panel["cohort_start"] = panel["cohort"].map({k: v[0] for k, v in COHORTS.items()})
    panel["cohort_end"] = panel["cohort"].map({k: v[1] for k, v in COHORTS.items()})

    # ------------------------------------------------------------------
    # 2) Load target-level Google Scholar metadata
    # ------------------------------------------------------------------
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
        "google_scholar_download_link_found",
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
    if "google_scholar_indexed" not in usecols:
        raise KeyError(f"{GS_FILE} missing google_scholar_indexed")

    gs = pd.read_csv(
        gs_path,
        usecols=usecols,
        encoding="utf-8-sig",
        low_memory=False,
        dtype={ID: "string"},
    )
    gs[ID] = norm_id(gs[ID])
    gs = gs.dropna(subset=[ID]).copy()

    if gs[ID].duplicated().any():
        ndup = gs.loc[gs[ID].duplicated(False), ID].nunique()
        raise ValueError(f"{GS_FILE} has duplicated target IDs: {ndup:,}")

    # D_j: exact-title Scholar lookup result.
    # Review cases count as not found; technical/search-input failures are
    # missing because no valid lookup result was obtained.
    gs["D_j"] = bin01(gs["google_scholar_indexed"])
    if "google_scholar_match_status" in gs.columns:
        match_status = (
            gs["google_scholar_match_status"]
            .astype("string")
            .str.strip()
            .str.lower()
        )
        gs.loc[match_status.eq("review"), "D_j"] = 0
        error_statuses = {
            "api_error",
            "processing_error",
            "missing_search_title",
        }
        gs.loc[match_status.isin(error_statuses), "D_j"] = pd.NA

    # Cross-check accepted-match field if present
    if "google_scholar_match_accepted" in gs.columns:
        gs["match_accepted_01"] = bin01(gs["google_scholar_match_accepted"])

    # A_j: strict verified open full text, conditional on D_j=1
    if "google_scholar_open_fulltext" in gs.columns:
        open_raw = bin01(gs["google_scholar_open_fulltext"])
    elif "google_scholar_download_verified" in gs.columns:
        open_raw = bin01(gs["google_scholar_download_verified"])
    else:
        raise KeyError(
            f"{GS_FILE} has neither google_scholar_open_fulltext "
            f"nor google_scholar_download_verified"
        )

    gs["A_j"] = pd.Series(pd.NA, index=gs.index, dtype="Int64")
    d1 = gs["D_j"].eq(1)
    gs.loc[d1, "A_j"] = open_raw.loc[d1].fillna(0).astype("Int64")

    if "google_scholar_fulltext_link_provided" in gs.columns:
        gs["fulltext_link_provided"] = bin01(
            gs["google_scholar_fulltext_link_provided"]
        )

    journal_source = first_existing(
        gs.columns,
        ["kci_journal_name", "ref_publisher_or_journal"],
    )
    if journal_source:
        gs["journal_fe"] = (
            gs[journal_source]
            .astype("string")
            .str.strip()
            .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
        )
    else:
        gs["journal_fe"] = pd.Series(pd.NA, index=gs.index, dtype="string")

    if "google_scholar_citation_count" in gs.columns:
        gs["gs_citation_count"] = num(gs["google_scholar_citation_count"])
        gs["log1p_gs_citation_count"] = np.log1p(
            gs["gs_citation_count"].clip(lower=0)
        )

    # ------------------------------------------------------------------
    # 3) Target-level master
    # ------------------------------------------------------------------
    target_master = (
        panel[[ID, "target_year", "target_topic"]]
        .drop_duplicates(ID)
        .copy()
    )

    gs_ids = set(gs[ID].dropna())
    target_master["gs_record_observed"] = (
        target_master[ID].isin(gs_ids).astype("Int64")
    )

    target_master = target_master.merge(
        gs,
        on=ID,
        how="left",
        validate="one_to_one",
        suffixes=("", "_gs"),
    )

    # Optional source-membership checks
    if edge_path.exists():
        edge_ids = pd.read_csv(
            edge_path,
            usecols=[ID],
            dtype={ID: "string"},
            encoding="utf-8-sig",
        )
        edge_ids[ID] = norm_id(edge_ids[ID])
        edge_set = set(edge_ids[ID].dropna())
        target_master["present_in_rq2analticsample"] = (
            target_master[ID].isin(edge_set).astype("Int64")
        )

    if kci_unique_path.exists():
        kci_ids = pd.read_csv(
            kci_unique_path,
            usecols=[ID],
            dtype={ID: "string"},
            encoding="utf-8-sig",
        )
        kci_ids[ID] = norm_id(kci_ids[ID])
        kci_set = set(kci_ids[ID].dropna())
        target_master["present_in_kci_unique"] = (
            target_master[ID].isin(kci_set).astype("Int64")
        )

    # ------------------------------------------------------------------
    # 4) Merge target-level GS variables to cohort panel
    # ------------------------------------------------------------------
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

    # Explicit Study 1 cohort interactions, C1 reference
    for c in ["C2", "C3", "C4"]:
        final[f"is_{c}"] = final["cohort"].eq(c).astype("Int64")
        final[f"D_x_{c}"] = (final["D_j"] * final[f"is_{c}"]).astype("Int64")
        final[f"A_x_{c}"] = (final["A_j"] * final[f"is_{c}"]).astype("Int64")

    final["main_D_sample"] = (
        final["gs_record_observed"].eq(1)
        & final["D_j"].notna()
    ).astype("Int64")

    final["access_A_sample"] = (
        final["gs_record_observed"].eq(1)
        & final["D_j"].eq(1)
        & final["A_j"].notna()
    ).astype("Int64")

    # ------------------------------------------------------------------
    # 5) Save
    # ------------------------------------------------------------------
    full_file = outdir / "study1_cohort_panel_full.csv"
    d_file = outdir / "study1_cohort_panel_D_main.csv"
    a_file = outdir / "study1_cohort_panel_A_indexed_only.csv"
    target_file = outdir / "study1_target_level_GS.csv"

    final.to_csv(full_file, index=False, encoding="utf-8-sig")
    final.loc[final["main_D_sample"].eq(1)].to_csv(
        d_file, index=False, encoding="utf-8-sig"
    )
    final.loc[final["access_A_sample"].eq(1)].to_csv(
        a_file, index=False, encoding="utf-8-sig"
    )
    target_master.to_csv(target_file, index=False, encoding="utf-8-sig")

    cohort_summary = (
        final.groupby("cohort")
        .agg(
            n_cells=(ID, "size"),
            n_targets=(ID, "nunique"),
            n_Y1=("Y_jc", "sum"),
            Y_rate=("Y_jc", "mean"),
            eng_citation_events=("eng_cite_count", "sum"),
            partial_cells=("partial", "sum"),
        )
        .reindex(["C1", "C2", "C3", "C4"])
        .reset_index()
    )
    cohort_summary.to_csv(
        outdir / "cohort_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    d_summary = (
        target_master["D_j"]
        .value_counts(dropna=False)
        .rename_axis("D_j")
        .reset_index(name="n_targets")
    )
    d_summary["share"] = d_summary["n_targets"] / d_summary["n_targets"].sum()
    d_summary.to_csv(
        outdir / "D_j_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    a_summary = (
        target_master.loc[target_master["D_j"].eq(1), "A_j"]
        .value_counts(dropna=False)
        .rename_axis("A_j")
        .reset_index(name="n_targets")
    )
    if len(a_summary):
        a_summary["share_among_D1"] = (
            a_summary["n_targets"] / a_summary["n_targets"].sum()
        )
    a_summary.to_csv(
        outdir / "A_j_summary_among_D1.csv",
        index=False,
        encoding="utf-8-sig",
    )

    diagnostics = pd.DataFrame(
        {
            "metric": [
                "panel_rows",
                "panel_unique_targets",
                "gs_unique_targets",
                "panel_targets_with_gs_record",
                "gs_coverage_rate",
                "D_main_rows",
                "D_main_unique_targets",
                "A_indexed_rows",
                "A_indexed_unique_targets",
            ],
            "value": [
                len(final),
                final[ID].nunique(),
                gs[ID].nunique(),
                int(target_master["gs_record_observed"].sum()),
                float(target_master["gs_record_observed"].mean()),
                int(final["main_D_sample"].sum()),
                final.loc[final["main_D_sample"].eq(1), ID].nunique(),
                int(final["access_A_sample"].sum()),
                final.loc[final["access_A_sample"].eq(1), ID].nunique(),
            ],
        }
    )
    diagnostics.to_csv(
        outdir / "build_diagnostics.csv",
        index=False,
        encoding="utf-8-sig",
    )

    readme = """
STUDY 1 COHORT DATA

Main file:
  study1_cohort_panel_D_main.csv

Unit:
  target paper j × cohort c

Cohorts:
  C1 <= 2009
  C2 2010-2014
  C3 2015-2019
  C4 2020-2024

Outcome:
  Y_jc

Exposure:
  D_j = google_scholar_indexed

Access:
  A_j = google_scholar_open_fulltext, conditional on D_j=1

Main interactions:
  D_x_C2, D_x_C3, D_x_C4

Access interactions:
  A_x_C2, A_x_C3, A_x_C4

Important:
  N_topic_jc and ln_offset are intentionally excluded from these final
  cohort-analysis datasets.
""".strip()

    (outdir / "README_STUDY1.txt").write_text(readme, encoding="utf-8")

    print("\nCreated:")
    for p in [full_file, d_file, a_file, target_file]:
        print(" ", p)
    print("\nDiagnostics:")
    print(diagnostics.to_string(index=False))
    print("\nCohort summary:")
    print(cohort_summary.to_string(index=False))
    print("\nNOTE: N_topic_jc and ln_offset were intentionally excluded.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base-dir", type=Path, required=True)
    args = p.parse_args()
    build(args.base_dir)


if __name__ == "__main__":
    main()
