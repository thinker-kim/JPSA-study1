#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Study 1 — End-to-end sample + cohort validation
===============================================

Purpose
-------
Independently verify the full Study 1 construction pipeline:

1) Reconstruct the analytic target sample from rq2analticsample.csv
   using the historical Study 1 inclusion rule:
       Korean-source cited target >= 1

2) Compare that reconstructed sample against:
       rq2_analytic_sample_korean_target_journal_or_na.csv   (if present)

3) Compare the analytic sample against:
       panel_with_offset.csv

4) Diagnose every target that is in the analytic sample but absent from
   the panel, including likely exclusion reasons:
       - missing_target_year
       - invalid_target_year
       - target_year_after_2024
       - no_structurally_valid_cohort
       - other_unexplained

5) Verify the final cohort panel construction:
       C1 <= 2009
       C2 2010-2014
       C3 2015-2019
       C4 2020-2024

6) Verify target×cohort structural eligibility and Y_jc consistency.

Inputs expected in --base-dir
-----------------------------
Required:
    rq2analticsample.csv
    panel_with_offset.csv

Strongly recommended:
    rq2_analytic_sample_korean_target_journal_or_na.csv

Optional:
    rq2analticsample_with_google_scholar_metadata.csv
    rq2analticsample_with_kci_metadata_unique.csv

Outputs
-------
study1_sample_validation/
    validation_summary.txt
    validation_report.csv
    sample_counts.csv
    reconstructed_analytic_sample.csv
    analytic_sample_vs_panel.csv
    panel_missing_targets.csv
    panel_extra_targets.csv
    panel_missing_reason_counts.csv
    cohort_validation.csv
    cohort_target_counts.csv
    duplicate_checks.csv
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
ANALYTIC_FILE = "rq2_analytic_sample_korean_target_journal_or_na.csv"
PANEL_FILE = "panel_with_offset.csv"
GS_FILE = "rq2analticsample_with_google_scholar_metadata.csv"
KCI_UNIQUE_FILE = "rq2analticsample_with_kci_metadata_unique.csv"

OUTDIR = "study1_sample_validation"

COHORTS = {
    "C1": (1900, 2009),
    "C2": (2010, 2014),
    "C3": (2015, 2019),
    "C4": (2020, 2024),
}


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


def detect_source_language_column(df: pd.DataFrame) -> Optional[str]:
    candidates = [
        "src_lang",
        "source_lang",
        "source_language",
        "lang_sphere1",
        "_source_language",
        "language_sphere",
    ]
    for c in candidates:
        if c in df.columns:
            return c
    return None


def classify_language(series: pd.Series) -> pd.Series:
    raw = series.astype("string").str.strip().str.lower()
    out = pd.Series("Unknown", index=series.index, dtype="string")
    out.loc[raw.str.contains(r"korean|한국|kor", regex=True, na=False)] = "Korean"
    out.loc[raw.str.contains(r"english|영어|eng", regex=True, na=False)] = "English"
    return out


class Reporter:
    def __init__(self):
        self.rows = []

    def add(self, section, check, status, observed="", expected="", detail=""):
        self.rows.append({
            "section": section,
            "check": check,
            "status": status,
            "observed": observed,
            "expected": expected,
            "detail": detail,
        })

    def passed(self, *args, **kwargs):
        self.add(*args, status="PASS", **kwargs)

    def warn(self, *args, **kwargs):
        self.add(*args, status="WARN", **kwargs)

    def fail(self, *args, **kwargs):
        self.add(*args, status="FAIL", **kwargs)


def validate(base_dir: Path) -> None:
    base_dir = base_dir.expanduser().resolve()
    outdir = base_dir / OUTDIR
    outdir.mkdir(parents=True, exist_ok=True)

    rep = Reporter()

    edge_path = base_dir / EDGE_FILE
    analytic_path = base_dir / ANALYTIC_FILE
    panel_path = base_dir / PANEL_FILE
    gs_path = base_dir / GS_FILE
    kci_path = base_dir / KCI_UNIQUE_FILE

    for p, required in [
        (edge_path, True),
        (panel_path, True),
        (analytic_path, False),
        (gs_path, False),
        (kci_path, False),
    ]:
        if p.exists():
            rep.passed("files", f"{p.name} exists")
        elif required:
            rep.fail("files", f"{p.name} exists", observed="missing")
        else:
            rep.warn("files", f"{p.name} exists", observed="missing", detail="optional")

    if not edge_path.exists() or not panel_path.exists():
        report = pd.DataFrame(rep.rows)
        report.to_csv(outdir / "validation_report.csv", index=False, encoding="utf-8-sig")
        raise FileNotFoundError("Required files missing. See validation_report.csv")

    # ------------------------------------------------------------------
    # 1. Load raw edge file
    # ------------------------------------------------------------------
    edges = pd.read_csv(
        edge_path,
        encoding="utf-8-sig",
        low_memory=False,
        dtype={ID: "string", SOURCE_ID: "string"},
    )

    if ID not in edges.columns:
        raise KeyError(f"{EDGE_FILE} missing {ID}")

    edges[ID] = norm_id(edges[ID])
    edges = edges.dropna(subset=[ID]).copy()

    # Reconstruct target year from ref_year, same historical logic.
    if "ref_year" not in edges.columns:
        raise KeyError(f"{EDGE_FILE} missing ref_year")

    edges["ref_year_num"] = safe_num(edges["ref_year"])
    edges.loc[
        ~edges["ref_year_num"].between(1900, 2026, inclusive="both"),
        "ref_year_num",
    ] = np.nan

    target_year = (
        edges.groupby(ID)["ref_year_num"]
        .agg(lambda s: s.mode().iloc[0] if not s.mode().empty else np.nan)
        .rename("target_year_reconstructed")
        .reset_index()
    )

    # ------------------------------------------------------------------
    # 2. Reconstruct analytic sample
    # ------------------------------------------------------------------
    # Best case: rq2analticsample.csv already represents the Study 1 analytic
    # target frame ("한국어권 소스에 인용된 한국어 타겟").
    #
    # Historical code explicitly says:
    #   target list = unique targets in rq2analticsample.csv
    #
    # So the primary reconstruction is the unique target set in this file.
    reconstructed = (
        edges[[ID]]
        .drop_duplicates()
        .merge(target_year, on=ID, how="left", validate="one_to_one")
    )
    reconstructed["in_reconstructed_analytic_sample"] = 1

    reconstructed.to_csv(
        outdir / "reconstructed_analytic_sample.csv",
        index=False,
        encoding="utf-8-sig",
    )

    n_reconstructed = len(reconstructed)
    rep.passed(
        "sample",
        "reconstructed analytic sample from rq2analticsample.csv",
        observed=n_reconstructed,
        detail="unique target IDs in rq2analticsample.csv",
    )

    # ------------------------------------------------------------------
    # 3. Compare to historical saved analytic sample if present
    # ------------------------------------------------------------------
    analytic = None
    if analytic_path.exists():
        analytic = pd.read_csv(
            analytic_path,
            encoding="utf-8-sig",
            low_memory=False,
            dtype={ID: "string"},
        )
        if ID not in analytic.columns:
            rep.fail("sample", f"{ANALYTIC_FILE} contains {ID}", observed="missing")
        else:
            analytic[ID] = norm_id(analytic[ID])
            analytic = analytic.dropna(subset=[ID]).copy()

            dup = int(analytic[ID].duplicated().sum())
            if dup == 0:
                rep.passed("sample", "saved analytic sample unique by target", observed=0)
            else:
                rep.fail("sample", "saved analytic sample unique by target", observed=dup, expected=0)

            analytic_ids = set(analytic[ID])
            reconstructed_ids = set(reconstructed[ID])

            missing_from_saved = reconstructed_ids - analytic_ids
            extra_in_saved = analytic_ids - reconstructed_ids

            if not missing_from_saved and not extra_in_saved:
                rep.passed(
                    "sample",
                    "reconstructed sample equals saved analytic sample",
                    observed=f"N={len(analytic_ids):,}",
                )
            else:
                rep.warn(
                    "sample",
                    "reconstructed sample equals saved analytic sample",
                    observed=f"reconstructed-only={len(missing_from_saved):,}, saved-only={len(extra_in_saved):,}",
                    expected="0 / 0",
                    detail="Inspect sample-set differences.",
                )

            pd.DataFrame({ID: sorted(missing_from_saved)}).to_csv(
                outdir / "reconstructed_not_in_saved_analytic.csv",
                index=False,
                encoding="utf-8-sig",
            )
            pd.DataFrame({ID: sorted(extra_in_saved)}).to_csv(
                outdir / "saved_analytic_not_in_reconstructed.csv",
                index=False,
                encoding="utf-8-sig",
            )

    # ------------------------------------------------------------------
    # 4. Load panel and compare sample coverage
    # ------------------------------------------------------------------
    panel = pd.read_csv(
        panel_path,
        encoding="utf-8-sig",
        low_memory=False,
        dtype={ID: "string", "cohort": "string"},
    )

    required_panel = [
        ID, "cohort", "target_year",
        "partial", "eng_cite_count", "Y_jc",
        "obs_start", "obs_end", "age_jc",
    ]
    missing = [c for c in required_panel if c not in panel.columns]
    if missing:
        raise KeyError(f"{PANEL_FILE} missing columns: {missing}")

    panel[ID] = norm_id(panel[ID])
    panel["target_year"] = safe_num(panel["target_year"])
    panel["obs_start"] = safe_num(panel["obs_start"])
    panel["obs_end"] = safe_num(panel["obs_end"])
    panel["eng_cite_count"] = safe_num(panel["eng_cite_count"])
    panel["Y_jc"] = safe_num(panel["Y_jc"])
    panel["partial"] = safe_num(panel["partial"])

    panel_ids = set(panel[ID].dropna())
    reconstructed_ids = set(reconstructed[ID])

    missing_from_panel = reconstructed_ids - panel_ids
    extra_in_panel = panel_ids - reconstructed_ids

    comparison = reconstructed[[ID, "target_year_reconstructed"]].copy()
    comparison["in_panel"] = comparison[ID].isin(panel_ids).astype(int)
    comparison.to_csv(
        outdir / "analytic_sample_vs_panel.csv",
        index=False,
        encoding="utf-8-sig",
    )

    pd.DataFrame({ID: sorted(extra_in_panel)}).to_csv(
        outdir / "panel_extra_targets.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # ------------------------------------------------------------------
    # 5. Diagnose why analytic targets are absent from panel
    # ------------------------------------------------------------------
    missing_df = reconstructed[
        reconstructed[ID].isin(missing_from_panel)
    ].copy()

    def exclusion_reason(row):
        y = row["target_year_reconstructed"]

        if pd.isna(y):
            return "missing_target_year"

        if y < 1900 or y > 2026:
            return "invalid_target_year"

        if y > 2024:
            return "target_year_after_2024"

        valid_cells = sum(
            int(y <= end)
            for _, end in COHORTS.values()
        )
        if valid_cells == 0:
            return "no_structurally_valid_cohort"

        return "other_unexplained"

    if len(missing_df):
        missing_df["exclusion_reason"] = missing_df.apply(exclusion_reason, axis=1)
    else:
        missing_df["exclusion_reason"] = pd.Series(dtype="string")

    missing_df.to_csv(
        outdir / "panel_missing_targets.csv",
        index=False,
        encoding="utf-8-sig",
    )

    reason_counts = (
        missing_df["exclusion_reason"]
        .value_counts(dropna=False)
        .rename_axis("exclusion_reason")
        .reset_index(name="n_targets")
    )
    reason_counts.to_csv(
        outdir / "panel_missing_reason_counts.csv",
        index=False,
        encoding="utf-8-sig",
    )

    unexplained_n = int(
        (missing_df["exclusion_reason"] == "other_unexplained").sum()
    ) if len(missing_df) else 0

    if len(extra_in_panel) == 0:
        rep.passed("sample", "panel has no extra targets outside analytic sample", observed=0)
    else:
        rep.fail(
            "sample",
            "panel has no extra targets outside analytic sample",
            observed=len(extra_in_panel),
            expected=0,
        )

    if unexplained_n == 0:
        rep.passed(
            "sample",
            "all analytic-sample targets missing from panel have explained reason",
            observed=0,
        )
    else:
        rep.fail(
            "sample",
            "all analytic-sample targets missing from panel have explained reason",
            observed=unexplained_n,
            expected=0,
        )

    # ------------------------------------------------------------------
    # 6. Cohort structure checks
    # ------------------------------------------------------------------
    dup_cells = int(panel.duplicated([ID, "cohort"]).sum())
    if dup_cells == 0:
        rep.passed("cohort", "target×cohort cells unique", observed=0)
    else:
        rep.fail("cohort", "target×cohort cells unique", observed=dup_cells, expected=0)

    observed_cohorts = set(panel["cohort"].dropna().astype(str).unique())
    if observed_cohorts == set(COHORTS):
        rep.passed(
            "cohort",
            "cohort labels",
            observed=str(sorted(observed_cohorts)),
        )
    else:
        rep.fail(
            "cohort",
            "cohort labels",
            observed=str(sorted(observed_cohorts)),
            expected=str(sorted(COHORTS)),
        )

    # Expected cohort membership from target year
    target_panel_year = (
        panel[[ID, "target_year"]]
        .drop_duplicates(ID)
        .copy()
    )

    cohort_validation_rows = []

    for _, r in target_panel_year.iterrows():
        uid = r[ID]
        y = r["target_year"]

        actual = sorted(
            panel.loc[panel[ID].eq(uid), "cohort"].dropna().astype(str).tolist()
        )

        if pd.isna(y):
            expected = []
        else:
            expected = [
                c for c, (_, end) in COHORTS.items()
                if y <= end
            ]

        cohort_validation_rows.append({
            ID: uid,
            "target_year": y,
            "expected_cohorts": "|".join(expected),
            "actual_cohorts": "|".join(actual),
            "matches": int(expected == actual),
        })

    cohort_validation = pd.DataFrame(cohort_validation_rows)
    cohort_validation.to_csv(
        outdir / "cohort_validation.csv",
        index=False,
        encoding="utf-8-sig",
    )

    cohort_mismatch = int((cohort_validation["matches"] == 0).sum())

    if cohort_mismatch == 0:
        rep.passed(
            "cohort",
            "every target has exactly the expected cohort cells",
            observed=0,
        )
    else:
        rep.fail(
            "cohort",
            "every target has exactly the expected cohort cells",
            observed=cohort_mismatch,
            expected=0,
        )

    # Structural impossibility
    cohort_end_map = {c: end for c, (_, end) in COHORTS.items()}
    panel["expected_cohort_end"] = panel["cohort"].map(cohort_end_map)

    impossible = int(
        (panel["target_year"] > panel["expected_cohort_end"]).sum()
    )
    if impossible == 0:
        rep.passed("cohort", "no target appears before publication", observed=0)
    else:
        rep.fail(
            "cohort",
            "no target appears before publication",
            observed=impossible,
            expected=0,
        )

    # partial
    cohort_start_map = {c: start for c, (start, _) in COHORTS.items()}
    panel["expected_cohort_start"] = panel["cohort"].map(cohort_start_map)

    expected_partial = (
        panel["target_year"] >= panel["expected_cohort_start"]
    ).astype(int)

    partial_mismatch = int(
        (expected_partial != panel["partial"].fillna(-999)).sum()
    )

    if partial_mismatch == 0:
        rep.passed("cohort", "partial flag correct", observed=0)
    else:
        rep.fail(
            "cohort",
            "partial flag correct",
            observed=partial_mismatch,
            expected=0,
        )

    # obs_start
    expected_obs_start = np.maximum(
        panel["target_year"],
        panel["expected_cohort_start"],
    )

    obs_start_mismatch = int(
        (np.abs(expected_obs_start - panel["obs_start"]) > 1e-9).sum()
    )

    if obs_start_mismatch == 0:
        rep.passed("cohort", "obs_start correct", observed=0)
    else:
        rep.fail(
            "cohort",
            "obs_start correct",
            observed=obs_start_mismatch,
            expected=0,
        )

    # Y_jc
    expected_y = (panel["eng_cite_count"].fillna(0) > 0).astype(int)
    y_mismatch = int(
        (expected_y != panel["Y_jc"].fillna(-999)).sum()
    )

    if y_mismatch == 0:
        rep.passed("outcome", "Y_jc == 1[eng_cite_count>0]", observed=0)
    else:
        rep.fail(
            "outcome",
            "Y_jc == 1[eng_cite_count>0]",
            observed=y_mismatch,
            expected=0,
        )

    # ------------------------------------------------------------------
    # 7. Target counts by cohort
    # ------------------------------------------------------------------
    cohort_counts = (
        panel.groupby("cohort")
        .agg(
            n_cells=(ID, "size"),
            n_targets=(ID, "nunique"),
            n_Y1=("Y_jc", "sum"),
            Y_rate=("Y_jc", "mean"),
            eng_citation_events=("eng_cite_count", "sum"),
            n_partial=("partial", "sum"),
        )
        .reindex(["C1", "C2", "C3", "C4"])
        .reset_index()
    )
    cohort_counts.to_csv(
        outdir / "cohort_target_counts.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # ------------------------------------------------------------------
    # 8. Duplicate checks
    # ------------------------------------------------------------------
    dup_rows = [
        {
            "file": EDGE_FILE,
            "key": ID,
            "duplicate_rows": int(edges[ID].duplicated().sum()),
            "duplicate_ids": int(edges.loc[edges[ID].duplicated(False), ID].nunique()),
            "note": "Expected: citation-edge file naturally repeats target IDs.",
        },
        {
            "file": PANEL_FILE,
            "key": f"{ID}+cohort",
            "duplicate_rows": int(panel.duplicated([ID, "cohort"]).sum()),
            "duplicate_ids": int(panel.loc[panel.duplicated([ID, "cohort"], False), ID].nunique()),
            "note": "Expected: zero duplicate target×cohort cells.",
        },
    ]

    if analytic is not None:
        dup_rows.append({
            "file": ANALYTIC_FILE,
            "key": ID,
            "duplicate_rows": int(analytic[ID].duplicated().sum()),
            "duplicate_ids": int(analytic.loc[analytic[ID].duplicated(False), ID].nunique()),
            "note": "Expected: zero.",
        })

    pd.DataFrame(dup_rows).to_csv(
        outdir / "duplicate_checks.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # ------------------------------------------------------------------
    # 9. Sample counts
    # ------------------------------------------------------------------
    sample_counts = pd.DataFrame({
        "metric": [
            "unique_targets_in_rq2analticsample",
            "saved_analytic_sample_targets",
            "panel_unique_targets",
            "analytic_targets_missing_from_panel",
            "panel_extra_targets",
            "missing_target_year",
            "target_year_after_2024",
            "no_structurally_valid_cohort",
            "other_unexplained",
        ],
        "value": [
            n_reconstructed,
            len(analytic) if analytic is not None else np.nan,
            panel[ID].nunique(),
            len(missing_from_panel),
            len(extra_in_panel),
            int((missing_df["exclusion_reason"] == "missing_target_year").sum()) if len(missing_df) else 0,
            int((missing_df["exclusion_reason"] == "target_year_after_2024").sum()) if len(missing_df) else 0,
            int((missing_df["exclusion_reason"] == "no_structurally_valid_cohort").sum()) if len(missing_df) else 0,
            int((missing_df["exclusion_reason"] == "other_unexplained").sum()) if len(missing_df) else 0,
        ],
    })
    sample_counts.to_csv(
        outdir / "sample_counts.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # ------------------------------------------------------------------
    # 10. Final report
    # ------------------------------------------------------------------
    report = pd.DataFrame(rep.rows)
    report.to_csv(
        outdir / "validation_report.csv",
        index=False,
        encoding="utf-8-sig",
    )

    report.loc[report["status"].isin(["FAIL", "WARN"])].to_csv(
        outdir / "validation_failures.csv",
        index=False,
        encoding="utf-8-sig",
    )

    n_pass = int((report["status"] == "PASS").sum())
    n_warn = int((report["status"] == "WARN").sum())
    n_fail = int((report["status"] == "FAIL").sum())

    summary = f"""STUDY 1 SAMPLE + COHORT VALIDATION

PASS: {n_pass}
WARN: {n_warn}
FAIL: {n_fail}

OVERALL:
{"READY" if n_fail == 0 else "NOT READY"}

Key counts:
- reconstructed analytic sample from rq2analticsample.csv: {n_reconstructed:,}
- saved analytic sample: {len(analytic) if analytic is not None else 'NA'}
- panel unique targets: {panel[ID].nunique():,}
- analytic targets missing from panel: {len(missing_from_panel):,}
- panel extra targets: {len(extra_in_panel):,}

Missing-from-panel reasons:
{reason_counts.to_string(index=False) if len(reason_counts) else 'None'}

Interpretation:
- 'other_unexplained' should ideally be 0.
- panel_extra_targets should ideally be 0.
- cohort_validation mismatches should be 0.
"""

    (outdir / "validation_summary.txt").write_text(
        summary,
        encoding="utf-8",
    )

    print("\n" + "=" * 80)
    print(summary)
    print("=" * 80)

    if n_fail:
        print("\nFAILURES:")
        print(
            report.loc[
                report["status"].eq("FAIL"),
                ["section", "check", "observed", "expected", "detail"],
            ].to_string(index=False)
        )

    if n_warn:
        print("\nWARNINGS:")
        print(
            report.loc[
                report["status"].eq("WARN"),
                ["section", "check", "observed", "expected", "detail"],
            ].to_string(index=False)
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-dir",
        type=Path,
        required=True,
        help="Folder containing local Study 1 files.",
    )
    args = parser.parse_args()
    validate(args.base_dir)


if __name__ == "__main__":
    main()
