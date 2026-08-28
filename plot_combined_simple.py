#!/usr/bin/env python3
"""Simple integrated figure for the combined Study 1 and Study 2 manuscript."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "combined_analysis" / "figures"
S2 = Path("/Users/hyowonkim/SciSci-LLM-audit/outputs")

BLUE = "#2F6687"
GRAY = "#65717A"
LIGHT = "#DCE4E8"
INK = "#1F2A33"
GRID = "#DDE3E7"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titleweight": "bold",
        "axes.labelcolor": GRAY,
        "text.color": INK,
        "xtick.color": GRAY,
        "ytick.color": GRAY,
        "axes.edgecolor": GRID,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    }
)


def clean(ax, axis="y"):
    ax.grid(axis=axis, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)


def panel_title(ax, letter, title):
    ax.set_title(f"{letter}. {title}", loc="left", fontsize=12, pad=12)


# Study 1 estimates
lpm = pd.read_csv(ROOT / "study1_analysis" / "lpm_target_fe_changes.csv")
cohorts = ["C2", "C3", "C4"]
x = np.arange(3)

# Study 2 recovery
panel = pd.read_csv(S2 / "study2_paper_execution_panel.csv", encoding="utf-8-sig")
baseline = panel[(panel.KoreanQuery == 0) & (panel.KoreanDB == 0)]
combined = panel[(panel.KoreanQuery == 1) & (panel.KoreanDB == 1)]

labels = ["EN + Web\nSearch", "EN + Web\nRecommend", "KO + DB\nSearch", "KO + DB\nRecommend"]
korean = [
    100 * baseline.loc[baseline.corpus.eq("korean_gold"), "Discovered"].mean(),
    100 * baseline.loc[baseline.corpus.eq("korean_gold"), "Recommended"].mean(),
    100 * combined.loc[combined.corpus.eq("korean_gold"), "Discovered"].mean(),
    100 * combined.loc[combined.corpus.eq("korean_gold"), "Recommended"].mean(),
]
english = [
    100 * baseline.loc[baseline.corpus.eq("english_benchmark"), "Discovered"].mean(),
    100 * baseline.loc[baseline.corpus.eq("english_benchmark"), "Recommended"].mean(),
    100 * combined.loc[combined.corpus.eq("english_benchmark"), "Discovered"].mean(),
    100 * combined.loc[combined.corpus.eq("english_benchmark"), "Recommended"].mean(),
]

# Study 2 language representation
audit = json.loads((S2 / "audit_results_manual.json").read_text(encoding="utf-8"))
rows = []
for execution in audit:
    meta = execution["representation_metadata"]["recommended"]
    rows.append(
        {
            "KoreanQuery": int(execution["language"] == "ko"),
            "KoreanDB": int(execution["source_instruction"] == "korean_db"),
            "share": meta["share"],
        }
    )
rep = pd.DataFrame(rows).groupby(["KoreanQuery", "KoreanDB"]).share.mean() * 100
conditions = [
    (0, 0, "English · web"),
    (0, 1, "English · Korean DB"),
    (1, 0, "Korean · web"),
    (1, 1, "Korean · Korean DB"),
]
shares = [rep.loc[(q, db)] for q, db, _ in conditions]
korean_benchmark_rec = []
for q, db, _ in conditions:
    subset = panel[
        (panel.KoreanQuery == q)
        & (panel.KoreanDB == db)
        & panel.corpus.eq("korean_gold")
    ]
    korean_benchmark_rec.append(100 * subset.Recommended.mean())


fig, axes = plt.subplots(1, 3, figsize=(15.2, 5.1), gridspec_kw={"width_ratios": [1.05, 1.2, 1.15]})

# A. Study 1
ax = axes[0]
for model, name, color, offset, marker in [
    ("lpm_target_fe", "All papers", BLUE, -0.06, "o"),
    ("lpm_pre2005", "Published by 2004", GRAY, 0.06, "s"),
]:
    z = lpm[lpm.model.eq(model)].copy()
    z["cohort"] = z.term.str.extract(r"(C[234])")
    z = z.set_index("cohort").loc[cohorts]
    estimate = z.change_percentage_points.to_numpy()
    low = z.conf_low_pp.to_numpy()
    high = z.conf_high_pp.to_numpy()
    ax.errorbar(
        x + offset,
        estimate,
        yerr=[estimate - low, high - estimate],
        fmt=marker,
        color=color,
        capsize=3,
        linewidth=1.4,
        markersize=6,
        label=name,
    )
    if model == "lpm_target_fe":
        for xx, value in zip(x + offset, estimate):
            ax.text(xx + 0.03, value + 0.07, f"{value:.3f}",
                    fontsize=7.7, color=BLUE)
ax.axhline(0, color="#9AA5AC", linestyle="--", linewidth=1)
ax.set_xticks(x, cohorts)
ax.set_ylim(-0.55, 1.55)
ax.set_ylabel("Change from C1 (percentage points)")
ax.legend(frameon=False, fontsize=8, loc="upper right")
panel_title(ax, "A", "Study 1 · Gap widens in C2–C3, not C4")
clean(ax)

# B. Study 2 recovery
ax = axes[1]
bx = np.arange(4)
width = 0.34
bars_k = ax.bar(bx - width / 2, korean, width, color=BLUE, label="Korean benchmark")
bars_e = ax.bar(bx + width / 2, english, width, color=GRAY, label="English benchmark")
for bars in (bars_k, bars_e):
    for bar in bars:
        value = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.10, f"{value:.1f}", ha="center", va="bottom", fontsize=8)
ax.set_xticks(bx, labels)
ax.tick_params(axis="x", labelsize=8.4)
ax.set_ylim(0, 4.05)
ax.set_ylabel("Benchmark recovery (%)")
ax.legend(frameon=False, fontsize=8, loc="upper center")
panel_title(ax, "B", "Study 2 · Gap shifts; recovery stays low")
clean(ax)

# C. Study 2 representation
ax = axes[2]
cy = np.arange(4)[::-1]
ax.barh(cy, shares, color=BLUE, height=0.48, label="Korean-language share")
ax.scatter(korean_benchmark_rec, cy, color=INK, marker="s", s=34,
           label="Korean benchmark recovery", zorder=3)
for value, yy in zip(shares, cy):
    ax.text(value + 1.5, yy, f"{value:.1f}", va="center", fontsize=8.5, color=BLUE)
for value, yy in zip(korean_benchmark_rec, cy):
    ax.text(value + 1.5, yy - 0.20, f"{value:.1f}", va="center", fontsize=7.8, color=INK)
ax.set_yticks(cy, [label for _, _, label in conditions])
ax.set_xlim(0, 102)
ax.set_xlabel("Share or recovery (%)")
ax.legend(frameon=False, fontsize=7.7, loc="upper right")
panel_title(ax, "C", "Study 2 · Representation is not recovery")
clean(ax, "x")

fig.suptitle(
    "Figure 1. Visibility across Google Scholar and generative search",
    x=0.06,
    y=1.02,
    ha="left",
    fontsize=17,
    fontweight="bold",
)
fig.text(
    0.06,
    0.955,
    "Study 1 compares citation gaps by current Google Scholar visibility; Study 2 audits benchmark recovery, language representation, and full-text access.",
    fontsize=9.6,
    color=GRAY,
)
fig.text(
    0.06,
    0.015,
    "Combined vs baseline gap change: +5.6 pp at search; +6.4 pp at recommendation",
    ha="left",
    fontsize=8.6,
    color=GRAY,
)
fig.text(
    0.99,
    0.015,
    "Provided-link full-text access: 44.2% overall; no significant Korean–English gap",
    ha="right",
    fontsize=8.6,
    color=GRAY,
)
fig.tight_layout(rect=[0.03, 0.055, 0.99, 0.91], w_pad=2.4)

OUT.mkdir(parents=True, exist_ok=True)
for ext in ("png", "svg"):
    fig.savefig(
        OUT / f"discovery_bottleneck_combined_simple.{ext}",
        dpi=260,
        bbox_inches="tight",
        facecolor="white",
        transparent=False,
    )

# Flatten the PNG to RGB so PDF converters and viewers cannot render an alpha
# channel as a black background.
png_path = OUT / "discovery_bottleneck_combined_simple.png"
with Image.open(png_path) as png:
    png.convert("RGB").save(png_path)
plt.close(fig)

print(OUT / "discovery_bottleneck_combined_simple.png")
