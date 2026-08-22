#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Study 1 cohort-panel validator
==============================

Validates the datasets produced by build_study1_cohort_data_final.py.

Checks:
- required files exist
- required variable names exist
- target×cohort key uniqueness
- exact C1–C4 definitions
- structural cohort eligibility
- Y_jc consistency with eng_cite_count
- partial / obs_start / cohort_order consistency
- D_j consistency with google_scholar_indexed
- D_j consistency with google_scholar_match_accepted where available
- A_j consistency with google_scholar_open_fulltext or download_verified
- A_j undefined when D_j=0
- missing GS rows not silently recoded as D_j=0
- D×cohort and A×cohort interactions
- D-main and A-indexed subset rules
- final cohort-analysis files exclude N_topic_jc and ln_offset
- optional target-ID cross-checks against rq2analticsample.csv

Outputs:
  validation_report.csv
  validation_failures.csv
  validation_summary.txt
  schema_inventory.csv
  crossfile_counts.csv
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
ORDER = {"C1": 1, "C2": 2, "C3": 3, "C4": 4}


def norm_id(s):
    return (
        s.astype("string")
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "<NA>": pd.NA})
    )


def num(s):
    return pd.to_numeric(s, errors="coerce")


def bin01(s):
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

    def passed(self, section, check, observed="", expected="", detail=""):
        self.add(section, check, "PASS", observed, expected, detail)

    def warn(self, section, check, observed="", expected="", detail=""):
        self.add(section, check, "WARN", observed, expected, detail)

    def fail(self, section, check, observed="", expected="", detail=""):
        self.add(section, check, "FAIL", observed, expected, detail)


def validate(base_dir: Path) -> None:
    base_dir = base_dir.expanduser().resolve()
    outdir = base_dir / OUTDIR
    outdir.mkdir(parents=True, exist_ok=True)
    rep = Reporter()

    paths = {
        "panel_source": base_dir / "panel_with_offset.csv",
        "gs_source": base_dir / "rq2analticsample_with_google_scholar_metadata.csv",
        "edges": base_dir / "rq2analticsample.csv",
        "full": outdir / "study1_cohort_panel_full.csv",
        "dmain": outdir / "study1_cohort_panel_D_main.csv",
        "amain": outdir / "study1_cohort_panel_A_indexed_only.csv",
        "target": outdir / "study1_target_level_GS.csv",
    }

    required = ["panel_source", "gs_source", "full", "dmain", "amain", "target"]
    for key in required:
        p = paths[key]
        if p.exists():
            rep.passed("files", f"{p.name} exists")
        else:
            rep.fail("files", f"{p.name} exists", observed="missing")

    if any(not paths[k].exists() for k in required):
        report = pd.DataFrame(rep.rows)
        report.to_csv(
            outdir / "validation_report.csv",
            index=False,
            encoding="utf-8-sig",
        )
        raise FileNotFoundError("Required files missing. See validation_report.csv")

    src = pd.read_csv(
        paths["panel_source"],
        encoding="utf-8-sig",
        low_memory=False,
        dtype={ID: "string", "cohort": "string"},
    )
    gs = pd.read_csv(
        paths["gs_source"],
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

    for df in [src, gs, full, dmain, amain, target]:
        df[ID] = norm_id(df[ID])

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------
    required_full = [
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

    missing = [c for c in required_full if c not in full.columns]
    if missing:
        rep.fail("schema", "full panel required variables", observed=str(missing), expected="none")
    else:
        rep.passed("schema", "full panel required variables", observed=len(required_full))

    forbidden = [c for c in ["N_topic_jc", "ln_offset"] if c in full.columns]
    if forbidden:
        rep.fail(
            "schema",
            "offset variables excluded from final analysis panel",
            observed=str(forbidden),
            expected="[]",
        )
    else:
        rep.passed(
            "schema",
            "offset variables excluded from final analysis panel",
            observed="[]",
        )

    # ------------------------------------------------------------------
    # Key uniqueness
    # ------------------------------------------------------------------
    dup = int(full.duplicated([ID, "cohort"]).sum())
    if dup == 0:
        rep.passed("keys", "target×cohort unique", observed=0)
    else:
        rep.fail("keys", "target×cohort unique", observed=dup, expected=0)

    tg_dup = int(target[ID].duplicated().sum())
    if tg_dup == 0:
        rep.passed("keys", "target-level file unique by target", observed=0)
    else:
        rep.fail("keys", "target-level file unique by target", observed=tg_dup, expected=0)

    # ------------------------------------------------------------------
    # Cohort definitions
    # ------------------------------------------------------------------
    obs_coh = set(full["cohort"].dropna().astype(str).unique())
    if obs_coh == set(COHORTS):
        rep.passed("cohort", "cohort labels", observed=str(sorted(obs_coh)))
    else:
        rep.fail(
            "cohort",
            "cohort labels",
            observed=str(sorted(obs_coh)),
            expected=str(sorted(COHORTS)),
        )

    bad_bounds = 0
    for c, (start, end) in COHORTS.items():
        x = full.loc[full["cohort"].eq(c)]
        bad_bounds += int((num(x["cohort_start"]) != start).sum())
        bad_bounds += int((num(x["cohort_end"]) != end).sum())

    if bad_bounds == 0:
        rep.passed("cohort", "C1-C4 boundaries", observed=0)
    else:
        rep.fail("cohort", "C1-C4 boundaries", observed=bad_bounds, expected=0)

    impossible = int(
        (num(full["target_year"]) > num(full["cohort_end"])).sum()
    )
    if impossible == 0:
        rep.passed("cohort", "no structurally impossible cells", observed=0)
    else:
        rep.fail(
            "cohort",
            "no structurally impossible cells",
            observed=impossible,
            expected=0,
        )

    expected_order = full["cohort"].map(ORDER).astype("Int64")
    observed_order = num(full["cohort_order"]).astype("Int64")
    bad_order = int(
        (
            expected_order.notna()
            & observed_order.notna()
            & (expected_order != observed_order)
        ).sum()
    )
    if bad_order == 0:
        rep.passed("cohort", "cohort_order correct", observed=0)
    else:
        rep.fail("cohort", "cohort_order correct", observed=bad_order, expected=0)

    expected_partial = (
        num(full["target_year"]) >= num(full["cohort_start"])
    ).astype("Int64")
    observed_partial = bin01(full["partial"])
    bad_partial = int(
        (
            expected_partial.notna()
            & observed_partial.notna()
            & (expected_partial != observed_partial)
        ).sum()
    )
    if bad_partial == 0:
        rep.passed("cohort", "partial flag correct", observed=0)
    else:
        rep.fail("cohort", "partial flag correct", observed=bad_partial, expected=0)

    expected_obs_start = np.maximum(
        num(full["target_year"]),
        num(full["cohort_start"]),
    )
    bad_obs_start = int(
        (np.abs(expected_obs_start - num(full["obs_start"])) > 1e-9).sum()
    )
    if bad_obs_start == 0:
        rep.passed("cohort", "obs_start correct", observed=0)
    else:
        rep.fail("cohort", "obs_start correct", observed=bad_obs_start, expected=0)

    # obs_end may reflect data max year rather than nominal C4 end, so warn only.
    bad_obs_end = int(
        (num(full["obs_end"]) > num(full["cohort_end"])).sum()
    )
    if bad_obs_end == 0:
        rep.passed("cohort", "obs_end does not exceed cohort end", observed=0)
    else:
        rep.fail(
            "cohort",
            "obs_end does not exceed cohort end",
            observed=bad_obs_end,
            expected=0,
        )

    # ------------------------------------------------------------------
    # Outcome consistency
    # ------------------------------------------------------------------
    expected_y = (num(full["eng_cite_count"]).fillna(0) > 0).astype("Int64")
    observed_y = bin01(full["Y_jc"])
    bad_y = int(
        (
            expected_y.notna()
            & observed_y.notna()
            & (expected_y != observed_y)
        ).sum()
    )
    if bad_y == 0:
        rep.passed("outcome", "Y_jc == 1[eng_cite_count>0]", observed=0)
    else:
        rep.fail(
            "outcome",
            "Y_jc == 1[eng_cite_count>0]",
            observed=bad_y,
            expected=0,
        )

    # Compare core panel fields back to panel_with_offset.csv
    core = [
        ID, "cohort", "target_year", "target_topic",
        "partial", "eng_cite_count", "Y_jc",
        "obs_start", "obs_end", "age_jc", "age_bin",
    ]
    src_core = src[core].sort_values([ID, "cohort"]).reset_index(drop=True)
    full_core = full[core].sort_values([ID, "cohort"]).reset_index(drop=True)

    if src_core.shape != full_core.shape:
        rep.fail(
            "panel",
            "core panel shape preserved",
            observed=str(full_core.shape),
            expected=str(src_core.shape),
        )
    else:
        mismatch = 0
        for c in core:
            a = src_core[c].astype("string").fillna("<NA>")
            b = full_core[c].astype("string").fillna("<NA>")
            mismatch += int((a != b).sum())
        if mismatch == 0:
            rep.passed("panel", "core cohort/Y fields preserved exactly", observed=0)
        else:
            rep.fail(
                "panel",
                "core cohort/Y fields preserved exactly",
                observed=mismatch,
                expected=0,
            )

    # ------------------------------------------------------------------
    # GS D_j / A_j
    # ------------------------------------------------------------------
    if "google_scholar_indexed" not in gs.columns:
        rep.fail("GS", "google_scholar_indexed exists", observed="missing")
    else:
        gs_check = gs[[ID, "google_scholar_indexed"]].copy()
        gs_check["D_expected"] = bin01(gs_check["google_scholar_indexed"])

        if "google_scholar_open_fulltext" in gs.columns:
            open_raw = bin01(gs["google_scholar_open_fulltext"])
            rep.passed(
                "GS",
                "A_j source variable",
                observed="google_scholar_open_fulltext",
            )
        elif "google_scholar_download_verified" in gs.columns:
            open_raw = bin01(gs["google_scholar_download_verified"])
            rep.warn(
                "GS",
                "A_j source variable",
                observed="google_scholar_download_verified",
                detail="google_scholar_open_fulltext absent; fallback used.",
            )
        else:
            open_raw = pd.Series(pd.NA, index=gs.index, dtype="Int64")
            rep.fail("GS", "A_j source variable", observed="missing")

        gs_check["A_expected"] = pd.Series(
            pd.NA, index=gs_check.index, dtype="Int64"
        )
        d1 = gs_check["D_expected"].eq(1)
        gs_check.loc[d1, "A_expected"] = (
            open_raw.loc[d1].fillna(0).astype("Int64")
        )

        if "google_scholar_match_accepted" in gs.columns:
            accepted = bin01(gs["google_scholar_match_accepted"])
            bad_internal = int(
                (
                    accepted.notna()
                    & gs_check["D_expected"].notna()
                    & (accepted != gs_check["D_expected"])
                ).sum()
            )
            if bad_internal == 0:
                rep.passed(
                    "GS",
                    "google_scholar_indexed matches match_accepted",
                    observed=0,
                )
            else:
                rep.fail(
                    "GS",
                    "google_scholar_indexed matches match_accepted",
                    observed=bad_internal,
                    expected=0,
                )

        chk = target[[ID, "D_j", "A_j", "gs_record_observed"]].merge(
            gs_check[[ID, "D_expected", "A_expected"]],
            on=ID,
            how="left",
            validate="one_to_one",
        )

        d_mismatch = int(
            (
                bin01(chk["D_j"]).fillna(-9)
                != chk["D_expected"].fillna(-9)
            ).sum()
        )
        a_mismatch = int(
            (
                bin01(chk["A_j"]).fillna(-9)
                != chk["A_expected"].fillna(-9)
            ).sum()
        )

        if d_mismatch == 0:
            rep.passed("GS", "D_j matches GS source exactly", observed=0)
        else:
            rep.fail(
                "GS",
                "D_j matches GS source exactly",
                observed=d_mismatch,
                expected=0,
            )

        if a_mismatch == 0:
            rep.passed("GS", "A_j matches verified full text exactly", observed=0)
        else:
            rep.fail(
                "GS",
                "A_j matches verified full text exactly",
                observed=a_mismatch,
                expected=0,
            )

    # Missing GS rows must remain missing D_j
    missing_gs = bin01(target["gs_record_observed"]).eq(0)
    bad_missing_d = int(target.loc[missing_gs, "D_j"].notna().sum())
    if bad_missing_d == 0:
        rep.passed("missingness", "missing GS rows keep D_j=NA", observed=0)
    else:
        rep.fail(
            "missingness",
            "missing GS rows keep D_j=NA",
            observed=bad_missing_d,
            expected=0,
        )

    # A_j only defined among D_j=1
    bad_a_d0 = int(
        target.loc[bin01(target["D_j"]).eq(0), "A_j"].notna().sum()
    )
    if bad_a_d0 == 0:
        rep.passed("missingness", "A_j undefined when D_j=0", observed=0)
    else:
        rep.fail(
            "missingness",
            "A_j undefined when D_j=0",
            observed=bad_a_d0,
            expected=0,
        )

    # ------------------------------------------------------------------
    # Interactions
    # ------------------------------------------------------------------
    for c in ["C2", "C3", "C4"]:
        expected_is = full["cohort"].eq(c).astype("Int64")
        observed_is = bin01(full[f"is_{c}"])
        bad_is = int(
            (
                observed_is.notna()
                & (observed_is != expected_is)
            ).sum()
        )

        expected_dx = (bin01(full["D_j"]) * expected_is).astype("Int64")
        observed_dx = bin01(full[f"D_x_{c}"])
        bad_dx = int(
            (
                observed_dx.fillna(-9)
                != expected_dx.fillna(-9)
            ).sum()
        )

        expected_ax = (bin01(full["A_j"]) * expected_is).astype("Int64")
        observed_ax = bin01(full[f"A_x_{c}"])
        bad_ax = int(
            (
                observed_ax.fillna(-9)
                != expected_ax.fillna(-9)
            ).sum()
        )

        if bad_is == 0:
            rep.passed("interaction", f"is_{c} correct", observed=0)
        else:
            rep.fail(
                "interaction",
                f"is_{c} correct",
                observed=bad_is,
                expected=0,
            )

        if bad_dx == 0:
            rep.passed("interaction", f"D_x_{c} correct", observed=0)
        else:
            rep.fail(
                "interaction",
                f"D_x_{c} correct",
                observed=bad_dx,
                expected=0,
            )

        if bad_ax == 0:
            rep.passed("interaction", f"A_x_{c} correct", observed=0)
        else:
            rep.fail(
                "interaction",
                f"A_x_{c} correct",
                observed=bad_ax,
                expected=0,
            )

    # ------------------------------------------------------------------
    # Subset rules
    # ------------------------------------------------------------------
    bad_dmain = int(
        (
            ~bin01(dmain["gs_record_observed"]).eq(1)
            | dmain["D_j"].isna()
        ).sum()
    )
    if bad_dmain == 0:
        rep.passed("subset", "D-main inclusion rule", observed=0)
    else:
        rep.fail(
            "subset",
            "D-main inclusion rule",
            observed=bad_dmain,
            expected=0,
        )

    bad_amain = int(
        (
            ~bin01(amain["D_j"]).eq(1)
            | amain["A_j"].isna()
        ).sum()
    )
    if bad_amain == 0:
        rep.passed("subset", "A-indexed inclusion rule", observed=0)
    else:
        rep.fail(
            "subset",
            "A-indexed inclusion rule",
            observed=bad_amain,
            expected=0,
        )

    # ------------------------------------------------------------------
    # Optional source-ID cross-check
    # ------------------------------------------------------------------
    if paths["edges"].exists():
        edge_ids = pd.read_csv(
            paths["edges"],
            usecols=[ID],
            dtype={ID: "string"},
            encoding="utf-8-sig",
        )
        edge_ids[ID] = norm_id(edge_ids[ID])
        edge_set = set(edge_ids[ID].dropna())
        panel_set = set(target[ID].dropna())
        missing_from_edges = len(panel_set - edge_set)
        if missing_from_edges == 0:
            rep.passed(
                "crossfile",
                "all panel targets appear in rq2analticsample.csv",
                observed=0,
            )
        else:
            rep.warn(
                "crossfile",
                "all panel targets appear in rq2analticsample.csv",
                observed=missing_from_edges,
                expected=0,
            )

    # ------------------------------------------------------------------
    # Save diagnostics
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

    schema_rows = []
    for name, df in [
        ("panel_with_offset.csv", src),
        ("rq2analticsample_with_google_scholar_metadata.csv", gs),
        ("study1_cohort_panel_full.csv", full),
        ("study1_cohort_panel_D_main.csv", dmain),
        ("study1_cohort_panel_A_indexed_only.csv", amain),
        ("study1_target_level_GS.csv", target),
    ]:
        for c in df.columns:
            schema_rows.append(
                {
                    "file": name,
                    "column": c,
                    "dtype": str(df[c].dtype),
                    "non_null": int(df[c].notna().sum()),
                    "null": int(df[c].isna().sum()),
                    "n_unique": int(df[c].nunique(dropna=True)),
                }
            )

    pd.DataFrame(schema_rows).to_csv(
        outdir / "schema_inventory.csv",
        index=False,
        encoding="utf-8-sig",
    )

    counts = pd.DataFrame(
        {
            "file": [
                "panel_with_offset.csv",
                "rq2analticsample_with_google_scholar_metadata.csv",
                "study1_cohort_panel_full.csv",
                "study1_cohort_panel_D_main.csv",
                "study1_cohort_panel_A_indexed_only.csv",
                "study1_target_level_GS.csv",
            ],
            "rows": [
                len(src), len(gs), len(full), len(dmain), len(amain), len(target)
            ],
            "unique_targets": [
                src[ID].nunique(),
                gs[ID].nunique(),
                full[ID].nunique(),
                dmain[ID].nunique(),
                amain[ID].nunique(),
                target[ID].nunique(),
            ],
        }
    )
    counts.to_csv(
        outdir / "crossfile_counts.csv",
        index=False,
        encoding="utf-8-sig",
    )

    n_pass = int((report["status"] == "PASS").sum())
    n_warn = int((report["status"] == "WARN").sum())
    n_fail = int((report["status"] == "FAIL").sum())

    summary = f"""STUDY 1 VALIDATION SUMMARY

PASS: {n_pass}
WARN: {n_warn}
FAIL: {n_fail}

OVERALL: {"READY" if n_fail == 0 else "NOT READY"}

Main analysis file:
  study1_cohort_panel_D_main.csv

Access analysis file:
  study1_cohort_panel_A_indexed_only.csv

Important:
- C1–C4 cohort structure is preserved.
- D_j is taken from google_scholar_indexed.
- A_j is strict verified open full text, conditional on D_j=1.
- Missing GS collection rows are not recoded as D_j=0.
- N_topic_jc and ln_offset are intentionally excluded from final analysis files.
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
    p = argparse.ArgumentParser()
    p.add_argument("--base-dir", type=Path, required=True)
    args = p.parse_args()
    validate(args.base_dir)


if __name__ == "__main__":
    main()
