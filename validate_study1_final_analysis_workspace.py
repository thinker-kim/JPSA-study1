#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Validate final Study 1 analysis files against the intended cohort design.

Base directory example:
    /Users/hyowonkim/hyowonkim/ipsa2study1

Required source files:
    rq2analticsample.csv
    panel_with_offset.csv
    rq2analticsample_with_google_scholar_metadata.csv

Required final files:
    study1_cohort_final/study1_cohort_panel_full.csv
    study1_cohort_final/study1_cohort_panel_D_main.csv
    study1_cohort_final/study1_cohort_panel_A_indexed_only.csv
    study1_cohort_final/study1_target_level_GS.csv

Optional:
    rq2_analytic_sample_korean_target_journal_or_na.csv

Study 1 design checked here:
    Analytic target population:
        unique targets in rq2analticsample.csv
        (= Korean targets cited >=1 time by Korean-source scholarship
           according to the historical Study 1 construction)

    Unit:
        target paper j × cohort c

    Cohorts:
        C1 <= 2009
        C2 2010-2014
        C3 2015-2019
        C4 2020-2024

    Outcome:
        Y_jc = 1 if eng_cite_count > 0

    Main exposure:
        D_j = google_scholar_indexed

    Access:
        A_j = google_scholar_open_fulltext, conditional on D_j=1

    Main interactions:
        D_j × C2/C3/C4

Outputs:
    study1_cohort_final/final_analysis_validation/
        validation_summary.txt
        validation_report.csv
        validation_failures.csv
        sample_flow.csv
        sample_missing_from_panel.csv
        sample_extra_in_panel.csv
        cohort_counts.csv
        cohort_membership_mismatches.csv
        variable_inventory.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import pandas as pd


ID = "paper_uid_after_direct_w"

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


class Report:
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

    def ok(self, section, check, observed="", expected="", detail=""):
        self.add(section, check, "PASS", observed, expected, detail)

    def warn(self, section, check, observed="", expected="", detail=""):
        self.add(section, check, "WARN", observed, expected, detail)

    def fail(self, section, check, observed="", expected="", detail=""):
        self.add(section, check, "FAIL", observed, expected, detail)


def validate(base: Path) -> None:
    base = base.expanduser().resolve()
    final_dir = base / "study1_cohort_final"
    outdir = final_dir / "final_analysis_validation"
    outdir.mkdir(parents=True, exist_ok=True)

    r = Report()

    paths = {
        "edges": base / "rq2analticsample.csv",
        "panel_source": base / "panel_with_offset.csv",
        "gs": base / "rq2analticsample_with_google_scholar_metadata.csv",
        "saved_sample": base / "rq2_analytic_sample_korean_target_journal_or_na.csv",
        "full": final_dir / "study1_cohort_panel_full.csv",
        "dmain": final_dir / "study1_cohort_panel_D_main.csv",
        "amain": final_dir / "study1_cohort_panel_A_indexed_only.csv",
        "target": final_dir / "study1_target_level_GS.csv",
    }

    required_keys = ["edges", "panel_source", "gs", "full", "dmain", "amain", "target"]

    for key in required_keys:
        p = paths[key]
        if p.exists():
            r.ok("files", f"{p.name} exists", observed=str(p))
        else:
            r.fail("files", f"{p.name} exists", observed="missing")

    if paths["saved_sample"].exists():
        r.ok("files", f"{paths['saved_sample'].name} exists", detail="optional historical sample file found")
    else:
        r.warn("files", f"{paths['saved_sample'].name} exists", observed="missing",
               detail="optional; unique targets in rq2analticsample.csv will be used as the analytic target population")

    if any(not paths[k].exists() for k in required_keys):
        report = pd.DataFrame(r.rows)
        report.to_csv(outdir / "validation_report.csv", index=False, encoding="utf-8-sig")
        raise FileNotFoundError("Required Study 1 files are missing. See validation_report.csv.")

    # ------------------------------------------------------------------
    # Load
    # ------------------------------------------------------------------
    edges = pd.read_csv(
        paths["edges"],
        encoding="utf-8-sig",
        low_memory=False,
        dtype={ID: "string"},
    )
    panel_source = pd.read_csv(
        paths["panel_source"],
        encoding="utf-8-sig",
        low_memory=False,
        dtype={ID: "string", "cohort": "string"},
    )
    gs = pd.read_csv(
        paths["gs"],
        encoding="utf-8-sig",
        low_memory=False,
        dtype={ID: "string"},
    )
    full = pd.read_csv(
        paths["full"],
        encoding="utf-8-sig",
        low_memory=False,
        dtype={ID: "string", "cohort": "string"},
    )
    dmain = pd.read_csv(
        paths["dmain"],
        encoding="utf-8-sig",
        low_memory=False,
        dtype={ID: "string", "cohort": "string"},
    )
    amain = pd.read_csv(
        paths["amain"],
        encoding="utf-8-sig",
        low_memory=False,
        dtype={ID: "string", "cohort": "string"},
    )
    target = pd.read_csv(
        paths["target"],
        encoding="utf-8-sig",
        low_memory=False,
        dtype={ID: "string"},
    )

    for df in [edges, panel_source, gs, full, dmain, amain, target]:
        if ID not in df.columns:
            raise KeyError(f"Required ID variable missing: {ID}")
        df[ID] = norm_id(df[ID])

    # ------------------------------------------------------------------
    # A. Intended analytic target population
    # ------------------------------------------------------------------
    intended_ids = set(edges[ID].dropna().unique())

    saved_sample = None
    if paths["saved_sample"].exists():
        saved_sample = pd.read_csv(
            paths["saved_sample"],
            encoding="utf-8-sig",
            low_memory=False,
            dtype={ID: "string"},
        )
        saved_sample[ID] = norm_id(saved_sample[ID])
        saved_ids = set(saved_sample[ID].dropna().unique())

        if intended_ids == saved_ids:
            r.ok(
                "sample",
                "rq2analticsample target set equals saved analytic-sample target set",
                observed=f"{len(intended_ids):,}",
                expected=f"{len(saved_ids):,}",
            )
        else:
            r.warn(
                "sample",
                "rq2analticsample target set equals saved analytic-sample target set",
                observed=f"edge targets={len(intended_ids):,}; saved targets={len(saved_ids):,}; "
                         f"edge-only={len(intended_ids-saved_ids):,}; saved-only={len(saved_ids-intended_ids):,}",
                expected="identical sets",
            )

    # ------------------------------------------------------------------
    # B. Panel target population
    # ------------------------------------------------------------------
    panel_ids = set(full[ID].dropna().unique())

    missing_from_panel = intended_ids - panel_ids
    extra_in_panel = panel_ids - intended_ids

    if len(extra_in_panel) == 0:
        r.ok("sample", "final full panel contains no targets outside intended sample", observed=0)
    else:
        r.fail("sample", "final full panel contains no targets outside intended sample",
               observed=len(extra_in_panel), expected=0)

    # Reconstruct target publication year from edge file to diagnose exclusions.
    if "ref_year" not in edges.columns:
        r.fail("sample", "rq2analticsample contains ref_year", observed="missing")
        target_year = pd.DataFrame({ID: list(intended_ids), "target_year_reconstructed": np.nan})
    else:
        edges["_ref_year_num"] = num(edges["ref_year"])
        edges.loc[
            ~edges["_ref_year_num"].between(1900, 2026, inclusive="both"),
            "_ref_year_num",
        ] = np.nan

        target_year = (
            edges.groupby(ID)["_ref_year_num"]
            .agg(lambda s: s.mode().iloc[0] if not s.mode().empty else np.nan)
            .rename("target_year_reconstructed")
            .reset_index()
        )

    missing_df = target_year[target_year[ID].isin(missing_from_panel)].copy()

    def reason(row):
        y = row["target_year_reconstructed"]
        if pd.isna(y):
            return "missing_target_year"
        if y > 2024:
            return "target_year_after_2024"
        if y < 1900 or y > 2026:
            return "invalid_target_year"
        expected = [c for c, (_, end) in COHORTS.items() if y <= end]
        if len(expected) == 0:
            return "no_structurally_valid_cohort"
        return "other_unexplained"

    if len(missing_df):
        missing_df["exclusion_reason"] = missing_df.apply(reason, axis=1)
    else:
        missing_df["exclusion_reason"] = pd.Series(dtype="string")

    unexplained = int((missing_df["exclusion_reason"] == "other_unexplained").sum())

    if unexplained == 0:
        r.ok(
            "sample",
            "targets absent from panel have an explained structural reason",
            observed=0,
        )
    else:
        r.fail(
            "sample",
            "targets absent from panel have an explained structural reason",
            observed=unexplained,
            expected=0,
        )

    pd.DataFrame({ID: sorted(extra_in_panel)}).to_csv(
        outdir / "sample_extra_in_panel.csv",
        index=False,
        encoding="utf-8-sig",
    )
    missing_df.to_csv(
        outdir / "sample_missing_from_panel.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # ------------------------------------------------------------------
    # C. Final file schema
    # ------------------------------------------------------------------
    required_final = [
        ID, "cohort", "target_year", "target_topic",
        "partial", "eng_cite_count", "Y_jc",
        "obs_start", "obs_end", "age_jc", "age_bin",
        "cohort_order", "cohort_start", "cohort_end",
        "D_j", "A_j", "gs_record_observed",
        "main_D_sample", "access_A_sample",
        "is_C2", "is_C3", "is_C4",
        "D_x_C2", "D_x_C3", "D_x_C4",
        "A_x_C2", "A_x_C3", "A_x_C4",
    ]

    missing_cols = [c for c in required_final if c not in full.columns]
    if not missing_cols:
        r.ok("schema", "all required final-analysis variables exist", observed=len(required_final))
    else:
        r.fail("schema", "all required final-analysis variables exist",
               observed=str(missing_cols), expected="none missing")

    # User wants cohort-based final data, not offset-based final file.
    forbidden = [c for c in ["N_topic_jc", "ln_offset"] if c in full.columns]
    if not forbidden:
        r.ok("schema", "offset fields excluded from final cohort analysis file", observed="[]")
    else:
        r.fail("schema", "offset fields excluded from final cohort analysis file",
               observed=str(forbidden), expected="[]")

    # ------------------------------------------------------------------
    # D. Panel source -> final core-data preservation
    # ------------------------------------------------------------------
    core_cols = [
        ID, "cohort", "target_year", "target_topic",
        "partial", "eng_cite_count", "Y_jc",
        "obs_start", "obs_end", "age_jc", "age_bin",
    ]

    missing_core_source = [c for c in core_cols if c not in panel_source.columns]
    if missing_core_source:
        r.fail("panel", "panel_with_offset contains all core cohort variables",
               observed=str(missing_core_source), expected="none")
    else:
        a = panel_source[core_cols].sort_values([ID, "cohort"]).reset_index(drop=True)
        b = full[core_cols].sort_values([ID, "cohort"]).reset_index(drop=True)

        if a.shape != b.shape:
            r.fail("panel", "core panel shape preserved",
                   observed=str(b.shape), expected=str(a.shape))
        else:
            mismatch = 0
            for c in core_cols:
                av = a[c].astype("string").fillna("<NA>")
                bv = b[c].astype("string").fillna("<NA>")
                mismatch += int((av != bv).sum())

            if mismatch == 0:
                r.ok("panel", "core cohort/Y fields preserved exactly from panel_with_offset", observed=0)
            else:
                r.fail("panel", "core cohort/Y fields preserved exactly from panel_with_offset",
                       observed=mismatch, expected=0)

    # ------------------------------------------------------------------
    # E. Cohort construction
    # ------------------------------------------------------------------
    if full.duplicated([ID, "cohort"]).sum() == 0:
        r.ok("cohort", "target×cohort key unique", observed=0)
    else:
        r.fail("cohort", "target×cohort key unique",
               observed=int(full.duplicated([ID, "cohort"]).sum()), expected=0)

    observed_cohorts = set(full["cohort"].dropna().astype(str).unique())
    if observed_cohorts == set(COHORTS):
        r.ok("cohort", "exact C1-C4 labels", observed=str(sorted(observed_cohorts)))
    else:
        r.fail("cohort", "exact C1-C4 labels",
               observed=str(sorted(observed_cohorts)),
               expected=str(sorted(COHORTS)))

    full["_target_year"] = num(full["target_year"])
    full["_cohort_start_expected"] = full["cohort"].map({c: s for c, (s, _) in COHORTS.items()})
    full["_cohort_end_expected"] = full["cohort"].map({c: e for c, (_, e) in COHORTS.items()})

    bad_bounds = int(
        (num(full["cohort_start"]) != full["_cohort_start_expected"]).sum()
        + (num(full["cohort_end"]) != full["_cohort_end_expected"]).sum()
    )
    if bad_bounds == 0:
        r.ok("cohort", "cohort boundaries exactly match Study 1 design", observed=0)
    else:
        r.fail("cohort", "cohort boundaries exactly match Study 1 design",
               observed=bad_bounds, expected=0)

    impossible = int((full["_target_year"] > full["_cohort_end_expected"]).sum())
    if impossible == 0:
        r.ok("cohort", "no target appears in a cohort ending before target publication", observed=0)
    else:
        r.fail("cohort", "no target appears in a cohort ending before target publication",
               observed=impossible, expected=0)

    expected_partial = (
        full["_target_year"] >= full["_cohort_start_expected"]
    ).astype("Int64")
    actual_partial = bin01(full["partial"])
    bad_partial = int(
        (
            expected_partial.notna()
            & actual_partial.notna()
            & (expected_partial != actual_partial)
        ).sum()
    )
    if bad_partial == 0:
        r.ok("cohort", "partial flag correct", observed=0)
    else:
        r.fail("cohort", "partial flag correct", observed=bad_partial, expected=0)

    expected_obs_start = np.maximum(
        full["_target_year"],
        full["_cohort_start_expected"],
    )
    bad_obs_start = int(
        (np.abs(expected_obs_start - num(full["obs_start"])) > 1e-9).sum()
    )
    if bad_obs_start == 0:
        r.ok("cohort", "obs_start correct", observed=0)
    else:
        r.fail("cohort", "obs_start correct", observed=bad_obs_start, expected=0)

    expected_order = full["cohort"].map(ORDER).astype("Int64")
    actual_order = num(full["cohort_order"]).astype("Int64")
    bad_order = int(
        (
            expected_order.notna()
            & actual_order.notna()
            & (expected_order != actual_order)
        ).sum()
    )
    if bad_order == 0:
        r.ok("cohort", "cohort_order correct", observed=0)
    else:
        r.fail("cohort", "cohort_order correct", observed=bad_order, expected=0)

    # For each target, expected vs actual cohort membership.
    cohort_membership_rows = []
    target_year_final = full[[ID, "target_year"]].drop_duplicates(ID)

    for _, row in target_year_final.iterrows():
        uid = row[ID]
        y = num(pd.Series([row["target_year"]])).iloc[0]
        actual = sorted(full.loc[full[ID].eq(uid), "cohort"].dropna().astype(str).tolist())
        expected = [] if pd.isna(y) else [
            c for c, (_, end) in COHORTS.items() if y <= end
        ]
        if actual != expected:
            cohort_membership_rows.append({
                ID: uid,
                "target_year": y,
                "expected_cohorts": "|".join(expected),
                "actual_cohorts": "|".join(actual),
            })

    mismatch_df = pd.DataFrame(cohort_membership_rows)
    mismatch_df.to_csv(
        outdir / "cohort_membership_mismatches.csv",
        index=False,
        encoding="utf-8-sig",
    )

    if len(mismatch_df) == 0:
        r.ok("cohort", "every target has exactly the expected cohort cells", observed=0)
    else:
        r.fail("cohort", "every target has exactly the expected cohort cells",
               observed=len(mismatch_df), expected=0)

    # ------------------------------------------------------------------
    # F. Outcome
    # ------------------------------------------------------------------
    expected_y = (num(full["eng_cite_count"]).fillna(0) > 0).astype("Int64")
    actual_y = bin01(full["Y_jc"])
    bad_y = int(
        (
            expected_y.notna()
            & actual_y.notna()
            & (expected_y != actual_y)
        ).sum()
    )
    if bad_y == 0:
        r.ok("outcome", "Y_jc equals 1 when eng_cite_count > 0", observed=0)
    else:
        r.fail("outcome", "Y_jc equals 1 when eng_cite_count > 0",
               observed=bad_y, expected=0)

    # ------------------------------------------------------------------
    # G. GS exposure and access
    # ------------------------------------------------------------------
    if gs[ID].duplicated().sum() == 0:
        r.ok("GS", "GS file is one row per target", observed=0)
    else:
        r.fail("GS", "GS file is one row per target",
               observed=int(gs[ID].duplicated().sum()), expected=0)

    if "google_scholar_indexed" not in gs.columns:
        r.fail("GS", "google_scholar_indexed exists", observed="missing")
    else:
        gs_small = gs[[ID, "google_scholar_indexed"]].copy()
        gs_small["D_expected"] = bin01(gs_small["google_scholar_indexed"])

        if "google_scholar_open_fulltext" in gs.columns:
            gs_small["open_expected"] = bin01(gs["google_scholar_open_fulltext"])
            r.ok("GS", "A_j source is strict google_scholar_open_fulltext",
                 observed="google_scholar_open_fulltext")
        elif "google_scholar_download_verified" in gs.columns:
            gs_small["open_expected"] = bin01(gs["google_scholar_download_verified"])
            r.warn("GS", "A_j source is strict google_scholar_open_fulltext",
                   observed="fallback: google_scholar_download_verified")
        else:
            gs_small["open_expected"] = pd.Series(pd.NA, index=gs_small.index, dtype="Int64")
            r.fail("GS", "verified access variable exists", observed="missing")

        gs_small["A_expected"] = pd.Series(pd.NA, index=gs_small.index, dtype="Int64")
        m = gs_small["D_expected"].eq(1)
        gs_small.loc[m, "A_expected"] = (
            gs_small.loc[m, "open_expected"].fillna(0).astype("Int64")
        )

        check = target[[ID, "D_j", "A_j", "gs_record_observed"]].merge(
            gs_small[[ID, "D_expected", "A_expected"]],
            on=ID,
            how="left",
            validate="one_to_one",
        )

        bad_d = int(
            (
                bin01(check["D_j"]).fillna(-9)
                != check["D_expected"].fillna(-9)
            ).sum()
        )
        bad_a = int(
            (
                bin01(check["A_j"]).fillna(-9)
                != check["A_expected"].fillna(-9)
            ).sum()
        )

        if bad_d == 0:
            r.ok("GS", "D_j exactly reproduces google_scholar_indexed", observed=0)
        else:
            r.fail("GS", "D_j exactly reproduces google_scholar_indexed",
                   observed=bad_d, expected=0)

        if bad_a == 0:
            r.ok("GS", "A_j exactly reproduces strict verified full-text access", observed=0)
        else:
            r.fail("GS", "A_j exactly reproduces strict verified full-text access",
                   observed=bad_a, expected=0)

    # A undefined for D=0
    bad_a_d0 = int(target.loc[bin01(target["D_j"]).eq(0), "A_j"].notna().sum())
    if bad_a_d0 == 0:
        r.ok("GS", "A_j is undefined when D_j=0", observed=0)
    else:
        r.fail("GS", "A_j is undefined when D_j=0",
               observed=bad_a_d0, expected=0)

    # GS coverage
    gs_coverage = float(bin01(target["gs_record_observed"]).mean())
    if gs_coverage == 1.0:
        r.ok("GS", "GS coverage of final panel targets is 100%", observed=f"{gs_coverage:.1%}")
    else:
        r.warn("GS", "GS coverage of final panel targets is 100%",
               observed=f"{gs_coverage:.1%}", expected="100%")

    # ------------------------------------------------------------------
    # H. Interactions
    # ------------------------------------------------------------------
    for c in ["C2", "C3", "C4"]:
        expected_is = full["cohort"].eq(c).astype("Int64")
        actual_is = bin01(full[f"is_{c}"])
        bad_is = int((actual_is != expected_is).sum())

        expected_dx = (bin01(full["D_j"]) * expected_is).astype("Int64")
        actual_dx = bin01(full[f"D_x_{c}"])
        bad_dx = int(
            (actual_dx.fillna(-9) != expected_dx.fillna(-9)).sum()
        )

        expected_ax = (bin01(full["A_j"]) * expected_is).astype("Int64")
        actual_ax = bin01(full[f"A_x_{c}"])
        bad_ax = int(
            (actual_ax.fillna(-9) != expected_ax.fillna(-9)).sum()
        )

        if bad_is == 0:
            r.ok("interaction", f"is_{c} correct", observed=0)
        else:
            r.fail("interaction", f"is_{c} correct", observed=bad_is, expected=0)

        if bad_dx == 0:
            r.ok("interaction", f"D_x_{c} correct", observed=0)
        else:
            r.fail("interaction", f"D_x_{c} correct", observed=bad_dx, expected=0)

        if bad_ax == 0:
            r.ok("interaction", f"A_x_{c} correct", observed=0)
        else:
            r.fail("interaction", f"A_x_{c} correct", observed=bad_ax, expected=0)

    # ------------------------------------------------------------------
    # I. Main-analysis subset correctness
    # ------------------------------------------------------------------
    dmain_keys = set(zip(dmain[ID], dmain["cohort"].astype("string")))
    expected_d = full.loc[
        bin01(full["gs_record_observed"]).eq(1) & full["D_j"].notna(),
        [ID, "cohort"]
    ]
    expected_d_keys = set(zip(expected_d[ID], expected_d["cohort"].astype("string")))

    if dmain_keys == expected_d_keys:
        r.ok("analysis_sample", "D-main file exactly equals intended D-analysis rows",
             observed=f"{len(dmain):,} rows / {dmain[ID].nunique():,} targets")
    else:
        r.fail("analysis_sample", "D-main file exactly equals intended D-analysis rows",
               observed=f"extra={len(dmain_keys-expected_d_keys):,}; missing={len(expected_d_keys-dmain_keys):,}",
               expected="0 / 0")

    amain_keys = set(zip(amain[ID], amain["cohort"].astype("string")))
    expected_a = full.loc[
        bin01(full["gs_record_observed"]).eq(1)
        & bin01(full["D_j"]).eq(1)
        & full["A_j"].notna(),
        [ID, "cohort"]
    ]
    expected_a_keys = set(zip(expected_a[ID], expected_a["cohort"].astype("string")))

    if amain_keys == expected_a_keys:
        r.ok("analysis_sample", "A-indexed file exactly equals intended conditional-access rows",
             observed=f"{len(amain):,} rows / {amain[ID].nunique():,} targets")
    else:
        r.fail("analysis_sample", "A-indexed file exactly equals intended conditional-access rows",
               observed=f"extra={len(amain_keys-expected_a_keys):,}; missing={len(expected_a_keys-amain_keys):,}",
               expected="0 / 0")

    # ------------------------------------------------------------------
    # J. Summaries
    # ------------------------------------------------------------------
    reason_counts = (
        missing_df["exclusion_reason"]
        .value_counts(dropna=False)
        .rename_axis("reason")
        .reset_index(name="n")
        if len(missing_df)
        else pd.DataFrame(columns=["reason", "n"])
    )

    sample_flow = pd.DataFrame({
        "stage": [
            "intended_unique_targets_from_rq2analticsample",
            "saved_analytic_sample_targets",
            "final_panel_unique_targets",
            "targets_missing_from_panel",
            "targets_extra_in_panel",
            "D_main_unique_targets",
            "A_indexed_unique_targets",
        ],
        "n": [
            len(intended_ids),
            saved_sample[ID].nunique() if saved_sample is not None else np.nan,
            full[ID].nunique(),
            len(missing_from_panel),
            len(extra_in_panel),
            dmain[ID].nunique(),
            amain[ID].nunique(),
        ],
    })
    sample_flow.to_csv(outdir / "sample_flow.csv", index=False, encoding="utf-8-sig")

    cohort_counts = (
        full.groupby("cohort")
        .agg(
            n_cells=(ID, "size"),
            n_targets=(ID, "nunique"),
            Y1=("Y_jc", "sum"),
            Y_rate=("Y_jc", "mean"),
            eng_citation_events=("eng_cite_count", "sum"),
            partial_cells=("partial", "sum"),
        )
        .reindex(["C1", "C2", "C3", "C4"])
        .reset_index()
    )
    cohort_counts.to_csv(outdir / "cohort_counts.csv", index=False, encoding="utf-8-sig")

    # Variable inventory
    inventory = []
    for name, df in [
        ("study1_cohort_panel_full.csv", full),
        ("study1_cohort_panel_D_main.csv", dmain),
        ("study1_cohort_panel_A_indexed_only.csv", amain),
        ("study1_target_level_GS.csv", target),
    ]:
        for c in df.columns:
            inventory.append({
                "file": name,
                "variable": c,
                "dtype": str(df[c].dtype),
                "nonmissing": int(df[c].notna().sum()),
                "missing": int(df[c].isna().sum()),
                "n_unique": int(df[c].nunique(dropna=True)),
            })
    pd.DataFrame(inventory).to_csv(
        outdir / "variable_inventory.csv",
        index=False,
        encoding="utf-8-sig",
    )

    report = pd.DataFrame(r.rows)
    report.to_csv(outdir / "validation_report.csv", index=False, encoding="utf-8-sig")
    report.loc[report["status"].isin(["WARN", "FAIL"])].to_csv(
        outdir / "validation_failures.csv",
        index=False,
        encoding="utf-8-sig",
    )

    n_pass = int((report["status"] == "PASS").sum())
    n_warn = int((report["status"] == "WARN").sum())
    n_fail = int((report["status"] == "FAIL").sum())

    summary = f"""STUDY 1 FINAL ANALYSIS DATA VALIDATION

Base directory:
{base}

PASS: {n_pass}
WARN: {n_warn}
FAIL: {n_fail}

OVERALL: {"READY FOR ANALYSIS" if n_fail == 0 else "NOT READY — inspect FAIL rows"}

SAMPLE FLOW
-----------
Intended unique targets from rq2analticsample.csv: {len(intended_ids):,}
Saved analytic sample targets: {saved_sample[ID].nunique() if saved_sample is not None else "not available"}
Final panel unique targets: {full[ID].nunique():,}
Targets missing from final panel: {len(missing_from_panel):,}
Targets extra in final panel: {len(extra_in_panel):,}

Missing-from-panel reasons:
{reason_counts.to_string(index=False) if len(reason_counts) else "None"}

FINAL ANALYSIS FILES
--------------------
D main:
  rows={len(dmain):,}
  targets={dmain[ID].nunique():,}

A indexed-only:
  rows={len(amain):,}
  targets={amain[ID].nunique():,}

COHORT COUNTS
-------------
{cohort_counts.to_string(index=False)}

Interpretation:
- FAIL must be 0 before substantive regression.
- WARN should be inspected, but may reflect an optional missing historical file.
- 'other_unexplained' in sample_missing_from_panel.csv should be 0.
- study1_cohort_panel_D_main.csv is the main D_j × cohort analysis file.
- study1_cohort_panel_A_indexed_only.csv is the conditional A_j × cohort analysis file.
"""

    (outdir / "validation_summary.txt").write_text(summary, encoding="utf-8")

    print("\n" + "=" * 80)
    print(summary)
    print("=" * 80)

    if n_fail:
        print("\nFAILURES")
        print(
            report.loc[
                report["status"].eq("FAIL"),
                ["section", "check", "observed", "expected", "detail"]
            ].to_string(index=False)
        )

    if n_warn:
        print("\nWARNINGS")
        print(
            report.loc[
                report["status"].eq("WARN"),
                ["section", "check", "observed", "expected", "detail"]
            ].to_string(index=False)
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-dir",
        type=Path,
        required=True,
        help="Study 1 workspace directory.",
    )
    args = parser.parse_args()
    validate(args.base_dir)


if __name__ == "__main__":
    main()
