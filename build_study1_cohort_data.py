#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Study 1 — cohort-based analysis dataset builder
===============================================

This script preserves the Study 1 design as a TARGET × COHORT panel.

MAIN DESIGN
-----------
Population:
    Korean target papers that have been cited at least once by a Korean-source paper.

Unit:
    target paper j × English-source publication cohort c

Cohorts:
    C1: <= 2009   (Google Scholar introduction / early-adoption baseline)
    C2: 2010–2014
    C3: 2015–2019
    C4: 2020–2024

Outcome:
    Y_jc = 1 if target j receives at least one citation from an English-source
           paper published in cohort c; 0 otherwise.

Main exposure:
    D_j = Google Scholar index presence / accepted target match.

Access:
    A_j = verified open-full-text accessibility, defined conditionally for D_j=1.

Main empirical quantity:
    cohort × D_j interaction.
    The key question is whether the citation gap between D_j=1 and D_j=0
    becomes larger in later cohorts relative to C1.

IMPORTANT
---------
This script does NOT define Study 1 by an offset.
It builds the cohort panel first. If an existing opportunity/offset file is
available, you can merge it later as an optional adjustment, but the cohort
structure is the core analysis structure.

Also note:
The current Google Scholar collection code uses exact-title / author-refined
lookup. Therefore D_j is best described as Google Scholar INDEX PRESENCE /
LOOKUP AVAILABILITY, not blinded topic-query discoverability.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


# ============================================================
# File names
# ============================================================

EDGE_FILE = "rq2analticsample.csv"
SOURCE_FILE = "english_source_ids.csv"
GS_FILE = "rq2analticsample_with_google_scholar_metadata.csv"

# Optional target-level sample summary. The script can run without it.
TARGET_SAMPLE_FILE = "rq2_analytic_sample_korean_target_journal_or_na.csv"

OUTPUT_DIRNAME = "study1_cohort_final"

ID = "paper_uid_after_direct_w"
SOURCE_ID = "src_논문"


# ============================================================
# Fixed Study 1 cohort definition
# ============================================================

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


# ============================================================
# Helpers
# ============================================================

def normalize_id(s: pd.Series) -> pd.Series:
    return (
        s.astype("string")
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "<NA>": pd.NA})
    )


def safe_numeric(s: pd.Series) -> pd.Series:
    return pd.to_numeric(
        s.astype("string").str.replace(",", "", regex=False).str.strip(),
        errors="coerce",
    )


def to_binary(s: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(s):
        return s.astype("Int64")

    numeric = pd.to_numeric(s, errors="coerce")
    vals = set(numeric.dropna().unique())
    if vals and vals.issubset({0, 1}):
        return numeric.astype("Int64")

    x = s.astype("string").str.strip().str.lower()
    out = pd.Series(pd.NA, index=s.index, dtype="Int64")
    out.loc[x.isin({"1", "true", "t", "yes", "y"})] = 1
    out.loc[x.isin({"0", "false", "f", "no", "n"})] = 0
    return out


def find_col(columns, candidates) -> Optional[str]:
    cols = set(columns)
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


def require_unique(df: pd.DataFrame, col: str, label: str) -> None:
    dup = df[col].duplicated(keep=False)
    if dup.any():
        raise ValueError(
            f"{label}: {col} is not unique. "
            f"Duplicated rows={dup.sum():,}, IDs={df.loc[dup, col].nunique():,}"
        )


# ============================================================
# Main
# ============================================================

def build(base_dir: Path) -> None:
    edge_path = base_dir / EDGE_FILE
    source_path = base_dir / SOURCE_FILE
    gs_path = base_dir / GS_FILE
    target_sample_path = base_dir / TARGET_SAMPLE_FILE

    out_dir = base_dir / OUTPUT_DIRNAME
    out_dir.mkdir(parents=True, exist_ok=True)

    for p in [edge_path, source_path, gs_path]:
        if not p.exists():
            raise FileNotFoundError(f"Required file not found: {p}")

    print("=" * 80)
    print("STUDY 1 — COHORT DATA BUILDER")
    print("=" * 80)

    # --------------------------------------------------------
    # 1. Load citation edges
    # --------------------------------------------------------
    print("\n[1] Loading citation edges")

    edges = pd.read_csv(
        edge_path,
        encoding="utf-8-sig",
        low_memory=False,
        dtype={ID: "string", SOURCE_ID: "string"},
    )

    required_edge = [ID, SOURCE_ID, "ref_year"]
    missing = [c for c in required_edge if c not in edges.columns]
    if missing:
        raise KeyError(f"{EDGE_FILE} missing columns: {missing}")

    edges[ID] = normalize_id(edges[ID])
    edges[SOURCE_ID] = normalize_id(edges[SOURCE_ID])
    edges = edges.dropna(subset=[ID, SOURCE_ID]).copy()

    # rq2analticsample.csv is expected to already be the Korean target,
    # journal/NA-filtered analytic citation-edge file.
    if "Language_written_ref" in edges.columns:
        lang = edges["Language_written_ref"].astype("string").str.strip().str.lower()
        non_korean = (~lang.eq("korean")) & lang.notna()
        if non_korean.any():
            raise ValueError(
                f"{EDGE_FILE} contains {non_korean.sum():,} non-Korean target rows. "
                "This is inconsistent with the Study 1 analytic edge frame."
            )

    print(f"Edges: {len(edges):,}")
    print(f"Unique target IDs in edge frame: {edges[ID].nunique():,}")

    # --------------------------------------------------------
    # 2. Load English-source metadata
    # --------------------------------------------------------
    print("\n[2] Loading English-source metadata")

    source_header = pd.read_csv(source_path, nrows=0, encoding="utf-8-sig").columns.tolist()

    source_id_col = find_col(
        source_header,
        ["논문 ID", SOURCE_ID, "paper_id", "source_paper_id"],
    )
    source_year_col = find_col(
        source_header,
        ["발행연도", "publication_year", "pub_year", "year"],
    )

    if source_id_col is None or source_year_col is None:
        raise KeyError(
            f"{SOURCE_FILE} must contain a source-paper ID and publication year.\n"
            f"Detected ID={source_id_col}, year={source_year_col}"
        )

    source = pd.read_csv(
        source_path,
        usecols=[source_id_col, source_year_col],
        encoding="utf-8-sig",
        low_memory=False,
        dtype={source_id_col: "string"},
    ).rename(
        columns={
            source_id_col: SOURCE_ID,
            source_year_col: "src_year",
        }
    )

    source[SOURCE_ID] = normalize_id(source[SOURCE_ID])
    source["src_year"] = safe_numeric(source["src_year"])
    source = source.dropna(subset=[SOURCE_ID]).copy()

    # source metadata should be one row per source paper
    source = (
        source.sort_values(SOURCE_ID)
        .drop_duplicates(SOURCE_ID, keep="first")
        .copy()
    )

    source.loc[
        ~source["src_year"].between(1900, 2026, inclusive="both"),
        "src_year",
    ] = np.nan

    print(f"English-source metadata rows: {len(source):,}")
    print(f"Source year missing: {source['src_year'].isna().sum():,}")

    # --------------------------------------------------------
    # 3. Define target population
    # --------------------------------------------------------
    print("\n[3] Defining Study 1 target population")

    # By construction, the target frame is ALL unique Korean targets in
    # rq2analticsample.csv, including targets never cited by English sources.
    target_ids = pd.DataFrame({ID: pd.Index(edges[ID].unique(), dtype="string")})

    # Target publication year: mode of ref_year across citation-edge appearances.
    edges["target_year_raw"] = safe_numeric(edges["ref_year"])
    edges.loc[
        ~edges["target_year_raw"].between(1900, 2026, inclusive="both"),
        "target_year_raw",
    ] = np.nan

    target_year = (
        edges.groupby(ID)["target_year_raw"]
        .agg(lambda s: s.mode().iloc[0] if not s.mode().empty else np.nan)
        .rename("target_year")
        .reset_index()
    )

    targets = target_ids.merge(target_year, on=ID, how="left", validate="one_to_one")

    print(f"Study 1 target population: {len(targets):,}")
    print(f"Target year missing: {targets['target_year'].isna().sum():,}")

    # --------------------------------------------------------
    # 4. Identify English-source citation events
    # --------------------------------------------------------
    print("\n[4] Identifying English-source citation events")

    english_edges = edges.merge(
        source,
        on=SOURCE_ID,
        how="inner",
        validate="many_to_one",
    )

    english_edges["cohort"] = english_edges["src_year"].apply(cohort_from_year)

    # Remove source years outside the four Study 1 cohort windows.
    english_edges_in_cohort = english_edges.dropna(subset=["cohort"]).copy()

    # Check temporal anomalies: source paper predating cited target.
    target_year_lookup = targets[[ID, "target_year"]]
    temporal_check = english_edges_in_cohort.merge(
        target_year_lookup,
        on=ID,
        how="left",
        validate="many_to_one",
    )
    temporal_check["source_before_target"] = (
        temporal_check["src_year"] < temporal_check["target_year"]
    )

    print(f"English citation edges with valid cohort: {len(english_edges_in_cohort):,}")
    print(
        "Targets ever cited by English sources: "
        f"{english_edges_in_cohort[ID].nunique():,}"
    )
    print(
        "Source-year < target-year anomalies: "
        f"{temporal_check['source_before_target'].sum():,}"
    )

    # --------------------------------------------------------
    # 5. Build target × cohort panel
    # --------------------------------------------------------
    print("\n[5] Building target × cohort panel")

    # Only targets with known publication year can be assigned valid
    # structurally observable cohort cells.
    base = targets.dropna(subset=["target_year"]).copy()

    panel = base.merge(COHORTS, how="cross")

    # Structural-zero rule:
    # if target was published after cohort end, that target-cohort cell did not exist.
    panel = panel[
        panel["target_year"] <= panel["cohort_end"]
    ].copy()

    # Partial cohort:
    # target enters during the cohort rather than being observable for the whole window.
    panel["partial"] = (
        panel["target_year"] >= panel["cohort_start"]
    ).astype("Int64")

    panel["obs_start"] = np.maximum(
        panel["target_year"],
        panel["cohort_start"],
    )
    panel["obs_end"] = panel["cohort_end"]

    # Binary cohort-specific outcome
    yjc = (
        english_edges_in_cohort
        .groupby([ID, "cohort"])
        .size()
        .rename("eng_cite_count")
        .reset_index()
    )

    panel = panel.merge(
        yjc,
        on=[ID, "cohort"],
        how="left",
        validate="one_to_one",
    )

    panel["eng_cite_count"] = (
        panel["eng_cite_count"]
        .fillna(0)
        .astype("int64")
    )

    panel["Y_jc"] = (
        panel["eng_cite_count"] > 0
    ).astype("Int64")

    panel["cohort_order"] = (
        panel["cohort"].map(COHORT_ORDER).astype("Int64")
    )

    # Citation-age control exactly attached to target × cohort cell
    panel["age_jc"] = (
        ((panel["obs_start"] + panel["obs_end"]) / 2)
        - panel["target_year"]
    ).clip(lower=0)

    panel["age_bin"] = pd.cut(
        panel["age_jc"],
        bins=[-0.1, 2, 5, 10, np.inf],
        labels=["0-2", "3-5", "6-10", "11+"],
    )

    print(f"Panel rows: {len(panel):,}")
    print(f"Panel targets: {panel[ID].nunique():,}")

    cohort_summary = (
        panel.groupby("cohort")
        .agg(
            n_cells=(ID, "size"),
            n_targets=(ID, "nunique"),
            n_Y1=("Y_jc", "sum"),
            Y_rate=("Y_jc", "mean"),
            English_citation_events=("eng_cite_count", "sum"),
            partial_cells=("partial", "sum"),
        )
        .reindex(COHORTS["cohort"])
        .reset_index()
    )

    print("\nCohort summary")
    print(cohort_summary.to_string(index=False))

    # --------------------------------------------------------
    # 6. Load GS target-level variables
    # --------------------------------------------------------
    print("\n[6] Loading Google Scholar variables")

    gs_header = pd.read_csv(
        gs_path,
        nrows=0,
        encoding="utf-8-sig",
    ).columns.tolist()

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
        "ref_publisher_or_journal",
        "ref_title",
        "ref_author",
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
        dtype={ID: "string"},
    )

    gs[ID] = normalize_id(gs[ID])
    gs = gs.dropna(subset=[ID]).copy()
    require_unique(gs, ID, "Google Scholar target file")

    # --------------------------------------------------------
    # 7. Construct Study 1 D_j / A_j
    # --------------------------------------------------------
    print("\n[7] Constructing D_j and A_j")

    if "google_scholar_indexed" not in gs.columns:
        raise KeyError(
            "Google Scholar output lacks google_scholar_indexed."
        )

    gs["D_j"] = to_binary(gs["google_scholar_indexed"])

    # Access is conditional on D=1.
    if "google_scholar_open_fulltext" in gs.columns:
        raw_open = to_binary(gs["google_scholar_open_fulltext"])
    elif "google_scholar_download_verified" in gs.columns:
        raw_open = to_binary(gs["google_scholar_download_verified"])
    else:
        raise KeyError(
            "Google Scholar output lacks both "
            "google_scholar_open_fulltext and google_scholar_download_verified."
        )

    gs["A_j"] = pd.Series(pd.NA, index=gs.index, dtype="Int64")
    gs.loc[gs["D_j"].eq(1), "A_j"] = (
        raw_open.loc[gs["D_j"].eq(1)]
        .fillna(0)
        .astype("Int64")
    )

    if "google_scholar_fulltext_link_provided" in gs.columns:
        gs["fulltext_link_provided"] = to_binary(
            gs["google_scholar_fulltext_link_provided"]
        )

    # Journal FE
    journal_source = find_col(
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

    # GS citation quality proxy: robustness only
    if "google_scholar_citation_count" in gs.columns:
        gs["gs_citation_count"] = safe_numeric(
            gs["google_scholar_citation_count"]
        )
        gs["log1p_gs_citation_count"] = np.log1p(
            gs["gs_citation_count"].clip(lower=0)
        )

    # --------------------------------------------------------
    # 8. Merge GS variables onto target × cohort panel
    # --------------------------------------------------------
    print("\n[8] Merging target-level GS variables onto cohort panel")

    gs_ids = pd.Index(gs[ID].dropna().unique())
    panel_ids = pd.Index(panel[ID].dropna().unique())

    covered = int(panel_ids.isin(gs_ids).sum())
    coverage = covered / len(panel_ids)

    print(
        f"Panel targets with GS record: {covered:,}/{len(panel_ids):,} "
        f"({coverage:.2%})"
    )

    # Build a panel-population target master first so missing collection rows
    # remain distinguishable from D_j=0.
    target_master = (
        panel[[ID, "target_year"]]
        .drop_duplicates(ID)
        .merge(
            gs,
            on=ID,
            how="left",
            validate="one_to_one",
            indicator="_gs_merge",
        )
    )

    target_master["gs_record_observed"] = (
        target_master["_gs_merge"].eq("both").astype("Int64")
    )

    # Optional target-sample citation summary
    if target_sample_path.exists():
        target_header = pd.read_csv(
            target_sample_path,
            nrows=0,
            encoding="utf-8-sig",
        ).columns.tolist()

        extra_candidates = [
            ID,
            "Y",
            "total_citation_count",
            "korean_source_citation_count",
            "english_source_citation_count",
            "total_source_paper_count",
            "korean_source_paper_count",
            "english_source_paper_count",
            "sample_status",
            "sample_version",
        ]

        extra_cols = [c for c in extra_candidates if c in target_header]

        extra = pd.read_csv(
            target_sample_path,
            usecols=extra_cols,
            encoding="utf-8-sig",
            low_memory=False,
            dtype={ID: "string"},
        )
        extra[ID] = normalize_id(extra[ID])
        extra = extra.dropna(subset=[ID])
        require_unique(extra, ID, "Target-level analytic sample")

        target_master = target_master.merge(
            extra,
            on=ID,
            how="left",
            validate="one_to_one",
            suffixes=("", "_sample"),
        )

    # Do not duplicate target_year on panel merge
    target_merge_cols = [
        c for c in target_master.columns
        if c not in {"target_year", "_gs_merge"}
    ]

    final = panel.merge(
        target_master[target_merge_cols],
        on=ID,
        how="left",
        validate="many_to_one",
    )

    if len(final) != len(panel):
        raise RuntimeError("Merge unexpectedly changed panel row count.")

    # Main sample indicator: GS collection status actually observed.
    final["main_D_sample"] = (
        final["gs_record_observed"].eq(1)
        & final["D_j"].notna()
    ).astype("Int64")

    # Conditional access sample
    final["access_A_sample"] = (
        final["gs_record_observed"].eq(1)
        & final["D_j"].eq(1)
        & final["A_j"].notna()
    ).astype("Int64")

    # --------------------------------------------------------
    # 9. Explicit D × cohort variables
    # --------------------------------------------------------
    print("\n[9] Creating explicit cohort interaction variables")

    # Reference cohort is C1.
    # These make the intended Study 1 estimand transparent even before regression.
    for c in ["C2", "C3", "C4"]:
        final[f"is_{c}"] = final["cohort"].eq(c).astype("Int64")
        final[f"D_x_{c}"] = (
            final["D_j"] * final[f"is_{c}"]
        ).astype("Int64")

    # Optional access interactions, used only among D=1.
    for c in ["C2", "C3", "C4"]:
        final[f"A_x_{c}"] = (
            final["A_j"] * final[f"is_{c}"]
        ).astype("Int64")

    # --------------------------------------------------------
    # 10. Save exact Study 1 datasets
    # --------------------------------------------------------
    print("\n[10] Saving final datasets")

    # Full cohort panel — preserve all target-cohort cells.
    final.to_csv(
        out_dir / "study1_cohort_panel_full.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Main D_j analysis sample
    main_D = final.loc[
        final["main_D_sample"].eq(1)
    ].copy()

    main_D.to_csv(
        out_dir / "study1_cohort_panel_D_main.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Conditional A_j sample among indexed targets
    access_A = final.loc[
        final["access_A_sample"].eq(1)
    ].copy()

    access_A.to_csv(
        out_dir / "study1_cohort_panel_A_indexed_only.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Target-level dataset for descriptive statistics / GS coverage
    target_master.to_csv(
        out_dir / "study1_target_level_GS.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Diagnostics
    cohort_summary.to_csv(
        out_dir / "cohort_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    D_summary = (
        target_master["D_j"]
        .value_counts(dropna=False)
        .rename_axis("D_j")
        .reset_index(name="n_targets")
    )
    D_summary["share"] = D_summary["n_targets"] / D_summary["n_targets"].sum()
    D_summary.to_csv(
        out_dir / "D_j_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    A_summary = (
        target_master.loc[
            target_master["D_j"].eq(1),
            "A_j",
        ]
        .value_counts(dropna=False)
        .rename_axis("A_j")
        .reset_index(name="n_targets")
    )
    if len(A_summary):
        A_summary["share_among_D1"] = (
            A_summary["n_targets"] / A_summary["n_targets"].sum()
        )
    A_summary.to_csv(
        out_dir / "A_j_summary_among_D1.csv",
        index=False,
        encoding="utf-8-sig",
    )

    merge_summary = pd.DataFrame(
        {
            "metric": [
                "edge_rows",
                "target_population_unique",
                "targets_with_year",
                "panel_rows",
                "panel_unique_targets",
                "gs_unique_targets_in_file",
                "panel_targets_with_GS_record",
                "GS_coverage_rate",
                "D_main_panel_rows",
                "D_main_unique_targets",
                "A_indexed_panel_rows",
                "A_indexed_unique_targets",
                "source_before_target_anomaly_edges",
            ],
            "value": [
                len(edges),
                len(targets),
                targets["target_year"].notna().sum(),
                len(panel),
                panel[ID].nunique(),
                len(gs),
                covered,
                coverage,
                len(main_D),
                main_D[ID].nunique(),
                len(access_A),
                access_A[ID].nunique(),
                int(temporal_check["source_before_target"].sum()),
            ],
        }
    )

    merge_summary.to_csv(
        out_dir / "build_diagnostics.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Temporal anomalies for manual review
    temporal_check.loc[
        temporal_check["source_before_target"]
    ].to_csv(
        out_dir / "temporal_anomalies_source_before_target.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # --------------------------------------------------------
    # 11. README
    # --------------------------------------------------------
    readme = f"""
STUDY 1 — COHORT PANEL

Core design
===========
Unit: target paper j × cohort c

Cohorts:
C1 <= 2009     baseline / GS introduction-early adoption
C2 2010-2014
C3 2015-2019
C4 2020-2024

Outcome:
Y_jc = 1 if target j is cited by >=1 English-source paper in cohort c.

Main exposure:
D_j = Google Scholar index presence / accepted target match.

Main estimand:
The key coefficients are the D_j × cohort interactions.
C1 is the reference cohort.

Interpretation:
D_x_C2, D_x_C3, D_x_C4 measure how the D=1 vs D=0 English-citation
gap differs from the C1 gap in each later cohort.

Access:
A_j is defined only among D_j=1 papers.
A_x_C2, A_x_C3, A_x_C4 can be used in the indexed-only access analysis.

Files
=====
study1_cohort_panel_full.csv
    all structurally observable target × cohort cells.

study1_cohort_panel_D_main.csv
    main D_j analysis panel; GS collection record observed and D_j known.

study1_cohort_panel_A_indexed_only.csv
    indexed targets only; use for conditional A_j analysis.

study1_target_level_GS.csv
    one row per panel target.

cohort_summary.csv
D_j_summary.csv
A_j_summary_among_D1.csv
build_diagnostics.csv
temporal_anomalies_source_before_target.csv

Important missingness rule
==========================
A target absent from the Google Scholar result file is NOT D_j=0.
It remains missing and is excluded from the D_j estimation sample.

Important operationalization note
=================================
The current Google Scholar collection script uses exact-title /
author-refined lookup. Therefore D_j is Google Scholar INDEX PRESENCE /
LOOKUP AVAILABILITY. It is not blinded topic-query discoverability.

No offset is used to define or construct this cohort panel.
If you later decide to include an opportunity adjustment, merge it as
a separate model covariate/offset after this panel is built; do not
replace the cohort structure with it.
""".strip()

    (out_dir / "README_STUDY1.txt").write_text(readme, encoding="utf-8")

    print("\n" + "=" * 80)
    print("DONE")
    print("=" * 80)
    print(merge_summary.to_string(index=False))
    print("\nOutputs:")
    for f in sorted(out_dir.iterdir()):
        print(" ", f.name)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path("."),
        help="Directory containing the local Study 1 CSV files.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    build(args.base_dir.expanduser().resolve())
