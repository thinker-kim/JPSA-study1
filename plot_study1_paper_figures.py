#!/usr/bin/env python3
"""Create Study 1 manuscript figures in the visual style of Study 2."""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch
from PIL import Image

ROOT = Path(__file__).resolve().parent
ANALYSIS = ROOT / "study1_analysis"
FIGURES = ANALYSIS / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

LOCAL = "#2F5F7F"
LOCAL_LIGHT = "#8EAABD"
ENGLISH = "#929AA1"
ENGLISH_DARK = "#4F5962"
RESTRICTED = "#CED3D7"
GRID = "#DDE2E5"
PALE = "#EDF3F6"
INK = "#1D2933"
MUTED = "#64717C"
PAPER = "#FFFFFF"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10.2,
    "axes.titleweight": "bold", "axes.labelcolor": MUTED,
    "text.color": INK, "axes.edgecolor": GRID,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "figure.facecolor": PAPER, "axes.facecolor": PAPER,
    "savefig.facecolor": PAPER,
})

desc = pd.read_csv(ANALYSIS / "descriptive_by_cohort_D.csv")
lpm = pd.read_csv(ANALYSIS / "lpm_target_fe_changes.csv")
coef = pd.read_csv(ANALYSIS / "model_coefficients.csv")
def clean_axis(ax, grid_axis="x"):
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)


def panel_title(ax, letter, title, subtitle=None):
    ax.set_title(f"{letter}. {title}", loc="left", fontsize=13.2, color=INK, pad=17)
    if subtitle:
        ax.text(0, 1.02, subtitle, transform=ax.transAxes, ha="left", va="bottom",
                fontsize=8.9, color=MUTED)


def save_figure(fig, name):
    for extension in ("png", "svg"):
        path = FIGURES / f"{name}.{extension}"
        fig.savefig(path, dpi=260 if extension == "png" else None,
                    bbox_inches="tight", facecolor=PAPER)
        if extension == "png":
            with Image.open(path) as rendered:
                if rendered.mode != "RGB":
                    rendered.convert("RGB").save(path, optimize=True)
    plt.close(fig)


def rounded_box(ax, xy, width, height, text, facecolor, edgecolor,
                fontsize=9.2, textcolor=INK):
    patch = FancyBboxPatch(xy, width, height,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        facecolor=facecolor, edgecolor=edgecolor, linewidth=1.0,
        transform=ax.transAxes)
    ax.add_patch(patch)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text,
            ha="center", va="center", fontsize=fontsize, color=textcolor,
            transform=ax.transAxes, linespacing=1.25)


def plot_design(ax, letter="A"):
    ax.set_axis_off()
    panel_title(ax, letter, "Cohort design", "Current exact-title GS visibility × source-paper cohort")
    ax.text(0.50, 0.90, "54,789 locally cited Korean target papers",
            transform=ax.transAxes, ha="center", color=MUTED, fontsize=9.2)
    rounded_box(ax, (0.04, 0.60), 0.19, 0.16, "C1\n≤2009", PAPER, ENGLISH)
    rounded_box(ax, (0.28, 0.60), 0.19, 0.16, "C2\n2010–2014", PALE, LOCAL_LIGHT)
    rounded_box(ax, (0.52, 0.60), 0.19, 0.16, "C3\n2015–2019", PALE, LOCAL_LIGHT)
    rounded_box(ax, (0.76, 0.60), 0.19, 0.16, "C4\n2020–2024", PALE, LOCAL_LIGHT)
    ax.annotate("", xy=(0.92, 0.53), xytext=(0.08, 0.53), xycoords=ax.transAxes,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
    rounded_box(ax, (0.10, 0.23), 0.34, 0.17, "D = 1\nExact-title match in GS", LOCAL, LOCAL,
                textcolor=PAPER)
    rounded_box(ax, (0.56, 0.23), 0.34, 0.17, "D = 0\nNot found", PAPER, ENGLISH)
    ax.text(0.50, 0.08, "Outcome: any English-source citation in each cohort",
            transform=ax.transAxes, ha="center", fontsize=8.8, color=INK,
            bbox={"boxstyle": "round,pad=0.35", "facecolor": PALE, "edgecolor": "none"})


def plot_raw_rates(ax, letter="B"):
    cohorts = ["C1", "C2", "C3", "C4"]
    x = np.arange(4)
    for d, label, color, marker in [(0, "D = 0", ENGLISH_DARK, "s"),
                                     (1, "D = 1", LOCAL, "o")]:
        z = desc.loc[desc.D_j.eq(d)].set_index("cohort").loc[cohorts]
        rates = 100 * z.y_rate.to_numpy()
        ax.plot(x, rates, marker=marker, color=color, lw=1.8, ms=6.5, label=label)
        for xx, yy in zip(x, rates):
            ax.text(xx, yy + 0.10, f"{yy:.2f}", ha="center", fontsize=7.8, color=color)
    panel_title(ax, letter, "Raw citation rates favor GS-visible papers",
                "Share receiving any English-source citation within each cohort")
    ax.set_xticks(x, cohorts)
    ax.set_ylabel("Citation incidence (%)")
    ax.set_ylim(0, 3.5)
    ax.legend(frameon=False, loc="upper left", ncol=2, fontsize=8.2)
    clean_axis(ax, "y")


def plot_primary(ax, letter="C", show_legend=True):
    z = lpm.copy()
    z["cohort"] = z.term.str.extract(r"(C[234])")
    cohorts = ["C2", "C3", "C4"]
    base = np.arange(3)
    specs = [("lpm_target_fe", "All eligible papers", LOCAL, -0.07, "o"),
             ("lpm_pre2005", "Published by 2004", ENGLISH_DARK, 0.07, "s")]
    for model, label, color, offset, marker in specs:
        q = z.loc[z.model.eq(model)].set_index("cohort").loc[cohorts]
        y = q.change_percentage_points.to_numpy()
        lo = q.conf_low_pp.to_numpy(); hi = q.conf_high_pp.to_numpy()
        ax.errorbar(base + offset, y, yerr=[y-lo, hi-y], fmt=marker,
                    color=color, ecolor=color, capsize=3, ms=6, lw=1.5, label=label)
    ax.axhline(0, color=ENGLISH, ls="--", lw=1)
    panel_title(ax, letter, "The D gap grows in C2 and C3",
                "Target fixed effects; change from C1 in percentage points")
    ax.set_xticks(base, cohorts)
    ax.set_ylabel("Change in D gap (pp)")
    ax.set_ylim(-0.55, 1.55)
    if show_legend:
        ax.legend(frameon=False, fontsize=8.0, loc="upper right")
    clean_axis(ax, "y")


def plot_sample_composition(ax, letter="D"):
    vals = [19436, 35353]
    y = np.arange(2)
    colors = [LOCAL, ENGLISH_DARK]
    ax.barh(y, vals, color=colors, height=0.48)
    for yy, vv in zip(y, vals):
        ax.text(vv + 700, yy, f"{vv:,}", va="center", fontsize=8.5)
    ax.set_yticks(y, ["D = 1", "D = 0"])
    ax.invert_yaxis()
    ax.set_xlim(0, 40000)
    ax.set_xlabel("Target papers in the analysis")
    panel_title(ax, letter, "The analysis compares 54,789 targets",
                "19,436 GS-visible and 35,353 nonvisible papers")
    clean_axis(ax, "x")


def plot_robustness(ax, letter="A"):
    models = [
        ("main", "Journal + age PPML"),
        ("topic_cohort_fe", "Topic × cohort PPML"),
        ("journal_cohort_fe", "Journal × cohort PPML"),
        ("pubyear_cohort_fe", "Year × cohort PPML"),
        ("citation_count", "Citation-count PPML"),
        ("pre2005_targets", "Pre-2005 PPML"),
    ]
    terms = ["cohort::C2:D_j", "cohort::C3:D_j", "cohort::C4:D_j"]
    ybase = np.arange(len(models))[::-1]
    colors = [LOCAL_LIGHT, LOCAL, ENGLISH_DARK]
    markers = ["o", "s", "^"]
    offsets = [0.16, 0, -0.16]
    for term, color, marker, off in zip(terms, colors, markers, offsets):
        rows = []
        for model, _ in models:
            r = coef.loc[coef.model.eq(model) & coef.term.eq(term)].iloc[0]
            rows.append(r)
        est = np.array([r.estimate for r in rows])
        se = np.array([r.std_error for r in rows])
        ax.errorbar(est, ybase + off, xerr=1.96*se, fmt=marker, color=color,
                    ecolor=color, capsize=2.5, ms=5.5, lw=1.2)
    ax.axvline(0, color=ENGLISH, ls="--", lw=1)
    ax.set_yticks(ybase, [label for _, label in models])
    ax.set_xlabel("Change in log relative risk from C1 (95% CI)")
    panel_title(ax, letter, "PPML estimates are less precise",
                "Positive values indicate a wider D gap than in C1")
    handles = [Line2D([0],[0],marker=m,color="none",markerfacecolor=c,
                      markeredgecolor=c,label=t.split("::")[1])
               for t,c,m in zip(terms,colors,markers)]
    ax.legend(handles=handles, frameon=False, ncol=3, fontsize=8, loc="lower right")
    clean_axis(ax, "x")


def plot_sample_flow(ax, letter="A"):
    ax.set_axis_off()
    panel_title(ax, letter, "Analysis structure", "Target papers are observed across eligible source cohorts")
    boxes = [(0.24, "Analysis targets\n54,789", LOCAL, LOCAL),
             (0.60, "Target × cohort panel\n179,230 cells", PAPER, LOCAL)]
    for x, text, fc, ec in boxes:
        rounded_box(ax, (x, 0.50), 0.18, 0.22, text, fc, ec,
                    textcolor=PAPER if fc == LOCAL else INK)
    for x1, x2 in [(0.42,0.60)]:
        ax.annotate("", xy=(x2,0.61), xytext=(x1,0.61), xycoords=ax.transAxes,
                    arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))


# Figure 1: design and core result
fig, axes = plt.subplots(1, 3, figsize=(17.8, 5.7), gridspec_kw={"width_ratios": [1.05, 1, 1]})
fig.suptitle("Figure 1. Google Scholar visibility and English-language citation trajectories",
             x=0.055, ha="left", fontsize=18, fontweight="bold", color=INK)
plot_design(axes[0], "A"); plot_raw_rates(axes[1], "B"); plot_primary(axes[2], "C")
fig.subplots_adjust(top=0.80, wspace=0.30)
fig.text(0.055, 0.01, "Note: D is current exact-title Google Scholar visibility. Primary estimates use target and cohort fixed effects with target-clustered standard errors.", fontsize=8.2, color=MUTED)
save_figure(fig, "study1_fig1_design_and_main_results")

# Figure 2: robustness
fig, ax = plt.subplots(figsize=(12.8, 6.7))
fig.suptitle("Figure 2. Robustness of cohort-specific changes in the visibility gap",
             x=0.055, ha="left", fontsize=18, fontweight="bold", color=INK)
plot_robustness(ax, "A")
fig.subplots_adjust(top=0.80, left=0.23)
fig.text(0.055, 0.015, "Note: These are interaction coefficients relative to C1, not cohort-specific levels. The target-FE linear probability models are reported in Figure 1C.", fontsize=8.2, color=MUTED)
save_figure(fig, "study1_fig2_robustness")

# Figure 3: analysis sample
fig, axes = plt.subplots(1, 2, figsize=(14.5, 5.6), gridspec_kw={"width_ratios": [1.55, 1]})
fig.suptitle("Figure 3. Study 1 analysis sample",
             x=0.055, ha="left", fontsize=18, fontweight="bold", color=INK)
plot_sample_flow(axes[0], "A"); plot_sample_composition(axes[1], "B")
fig.subplots_adjust(top=0.78, wspace=0.30)
fig.text(0.055, 0.01, "Note: The unit is target paper × eligible source-paper cohort.", fontsize=8.2, color=MUTED)
save_figure(fig, "study1_fig3_analysis_structure")

# Global figure
fig = plt.figure(figsize=(15.5, 11.2))
gs = fig.add_gridspec(2, 2, left=0.07, right=0.97, top=0.88, bottom=0.08,
                      wspace=0.34, hspace=0.42)
axes = [fig.add_subplot(gs[i, j]) for i in range(2) for j in range(2)]
fig.suptitle("Figure 1. The GS visibility gap grows during diffusion, not through the latest cohort",
             x=0.07, y=0.965, ha="left", fontsize=19, fontweight="bold", color=INK)
fig.text(0.07, 0.925, "Design, raw incidence, within-paper estimates, and analysis structure",
         fontsize=10.5, color=MUTED)
plot_design(axes[0], "A"); plot_raw_rates(axes[1], "B"); plot_primary(axes[2], "C"); plot_sample_composition(axes[3], "D")
fig.text(0.07, 0.02, "Exact-title-visible papers have higher raw citation incidence. Within-paper estimates show a larger D gap in C2–C3 but no further expansion in C4.", fontsize=9.0, color=INK,
         bbox={"boxstyle":"round,pad=0.55", "facecolor":PALE, "edgecolor":GRID})
save_figure(fig, "study1_global_figure")

print(f"Figures written to {FIGURES}")
