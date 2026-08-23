#!/usr/bin/env python3
"""Integrated Study 1–2 figure for the Discovery Bottleneck paper."""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "combined_analysis" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
S2 = Path("/Users/hyowonkim/SciSci-LLM-audit/outputs")

LOCAL = "#2F5F7F"; LOCAL_LIGHT = "#8EAABD"; ENGLISH = "#929AA1"
ENGLISH_DARK = "#4F5962"; GRID = "#DDE2E5"; PALE = "#EDF3F6"
INK = "#1D2933"; MUTED = "#64717C"; PAPER = "#FFFFFF"

plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":10.2,
    "axes.titleweight":"bold", "axes.labelcolor":MUTED, "text.color":INK,
    "axes.edgecolor":GRID, "xtick.color":MUTED, "ytick.color":MUTED,
    "figure.facecolor":PAPER, "axes.facecolor":PAPER, "savefig.facecolor":PAPER})

lpm = pd.read_csv(ROOT / "study1_analysis/lpm_target_fe_changes.csv")
s2panel = pd.read_csv(S2 / "study2_paper_execution_panel.csv", encoding="utf-8-sig")
audit = json.loads((S2 / "audit_results_manual.json").read_text(encoding="utf-8"))


def clean(ax, axis="y"):
    ax.grid(axis=axis, color=GRID, lw=.8); ax.set_axisbelow(True)
    ax.spines[["top","right","left"]].set_visible(False)


def ptitle(ax, letter, title, subtitle=None):
    ax.set_title(f"{letter}. {title}", loc="left", fontsize=13.2, color=INK, pad=17)
    if subtitle:
        ax.text(0,1.02,subtitle,transform=ax.transAxes,ha="left",va="bottom",fontsize=8.8,color=MUTED)


def box(ax, xy, wh, text, fc=PAPER, ec=ENGLISH, tc=INK):
    p=FancyBboxPatch(xy,*wh,boxstyle="round,pad=.012,rounding_size=.018",
                     transform=ax.transAxes,facecolor=fc,edgecolor=ec,lw=1)
    ax.add_patch(p); ax.text(xy[0]+wh[0]/2,xy[1]+wh[1]/2,text,transform=ax.transAxes,
                            ha="center",va="center",fontsize=8.8,color=tc,linespacing=1.2)


def pipeline(ax):
    ax.set_axis_off(); ptitle(ax,"A","Two discovery environments","Both studies examine Korean political science")
    ax.text(.02,.73,"STUDY 1 · GOOGLE SCHOLAR",transform=ax.transAxes,fontsize=8.3,
            fontweight="bold",color=LOCAL)
    box(ax,(.02,.46),(.27,.18),"Exact-title\nGS visibility",LOCAL,LOCAL,PAPER)
    ax.annotate("",xy=(.39,.55),xytext=(.29,.55),xycoords=ax.transAxes,
                arrowprops=dict(arrowstyle="->",color=MUTED,lw=1.1))
    box(ax,(.39,.46),(.27,.18),"English-language\ncitation",LOCAL,LOCAL,PAPER)
    ax.text(.02,.31,"STUDY 2 · WEB-ENABLED LLM SEARCH",transform=ax.transAxes,fontsize=8.3,
            fontweight="bold",color=LOCAL)
    labels=["Trace\nrecovery","Final\nrecommendation","Supplied-link\naccess"]
    xs=[.02,.28,.54]
    for i,(label,x) in enumerate(zip(labels,xs)):
        box(ax,(x,.05),(.21,.17),label,PALE,LOCAL_LIGHT,INK)
        if i<2:
            ax.annotate("",xy=(xs[i+1],.135),xytext=(x+.21,.135),xycoords=ax.transAxes,
                        arrowprops=dict(arrowstyle="->",color=MUTED,lw=1.1))


def study1_effect(ax):
    z=lpm.copy(); z["cohort"]=z.term.str.extract(r"(C[234])")
    base=np.arange(3); cohorts=["C2","C3","C4"]
    for model,label,color,off,marker in [
        ("lpm_target_fe","All eligible papers",LOCAL,-.06,"o"),
        ("lpm_pre2005","Published by 2004",ENGLISH_DARK,.06,"s")]:
        q=z[z.model.eq(model)].set_index("cohort").loc[cohorts]
        y=q.change_percentage_points.values; lo=q.conf_low_pp.values; hi=q.conf_high_pp.values
        ax.errorbar(base+off,y,yerr=[y-lo,hi-y],fmt=marker,color=color,ecolor=color,
                    capsize=3,lw=1.4,ms=6,label=label)
    ax.axhline(0,color=ENGLISH,ls="--",lw=1)
    ax.set_xticks(base,cohorts); ax.set_ylim(-.55,1.55)
    ax.set_ylabel("Change in visibility gap (pp)")
    ptitle(ax,"B","Citation trajectories diverge in C2–C3","Study 1: target fixed effects; C1 is the reference")
    ax.legend(frameon=False,fontsize=7.8,loc="upper right"); clean(ax,"y")


def recovery(ax):
    base=s2panel[(s2panel.KoreanQuery==0)&(s2panel.KoreanDB==0)]
    both=s2panel[(s2panel.KoreanQuery==1)&(s2panel.KoreanDB==1)]
    stages=[("Discovered","Trace recovery","o"),("Recommended","Recommendation","s"),
            ("Accessible","Supplied-link access","^")]
    y=np.arange(3)[::-1]
    for frame,off,label in [(base,-.10,"English baseline"),(both,.10,"Both interventions")]:
        for corpus,color,filled in [("korean_gold",LOCAL,True),("english_benchmark",ENGLISH_DARK,False)]:
            vals=[]
            for col,_,_ in stages:
                vals.append(100*frame.loc[frame.corpus.eq(corpus),col].mean())
            marker="o" if filled else "s"
            ax.scatter(vals,y+off,marker=marker,s=42,facecolor=color if filled else PAPER,
                       edgecolor=color,lw=1.4,zorder=3,
                       label=f"{label}: {'Korean' if filled else 'English'}")
    ax.set_yticks(y,[s[1] for s in stages]); ax.set_xlim(-.15,3.7)
    ax.set_xlabel("Target papers recovered (%)")
    ptitle(ax,"C","Interventions reverse the gap but not low recall","Study 2: pre-specified Korean and English corpora")
    handles=[Line2D([0],[0],marker="o",color="none",markerfacecolor=LOCAL,
                    markeredgecolor=LOCAL,label="Korean corpus"),
             Line2D([0],[0],marker="s",color="none",markerfacecolor=PAPER,
                    markeredgecolor=ENGLISH_DARK,label="English benchmark")]
    ax.legend(handles=handles,frameon=False,fontsize=7.8,loc="lower right"); clean(ax,"x")


def representation(ax):
    rows=[]
    for e in audit:
        md=e["representation_metadata"]["recommended"]
        rows.append({"KoreanQuery":int(e["language"]=="ko"),
                     "KoreanDB":int(e["source_instruction"]=="korean_db"),
                     "share":md["share"]})
    rep=pd.DataFrame(rows).groupby(["KoreanQuery","KoreanDB"]).share.mean()*100
    conditions=[(0,0,"English · web"),(0,1,"English · Korean DB"),
                (1,0,"Korean · web"),(1,1,"Korean · Korean DB")]
    vals=[rep.loc[(q,d)] for q,d,_ in conditions]
    korean_recovery=[]
    for q,d,_ in conditions:
        f=s2panel[(s2panel.KoreanQuery==q)&(s2panel.KoreanDB==d)&
                  (s2panel.corpus=="korean_gold")]
        korean_recovery.append(100*f.Recommended.mean())
    y=np.arange(4)[::-1]
    ax.scatter(vals,y,marker="o",s=48,color=LOCAL,label="Korean-language share")
    for xx,yy,v in zip(vals,y,vals):
        ax.text(xx+1.4,yy,f"{v:.1f}",va="center",fontsize=7.7,color=LOCAL)
    ax.set_yticks(y,[x[2] for x in conditions]); ax.set_xlim(-1,101)
    ax.set_xlabel("Korean-language recommendations (%)")
    ptitle(ax,"D","Representation changes more than recovery",
           "Korean benchmark recommendation remains 0.0–3.2% across conditions")
    clean(ax,"x")


fig=plt.figure(figsize=(15.5,11.2))
gs=fig.add_gridspec(2,2,left=.07,right=.97,top=.88,bottom=.08,wspace=.36,hspace=.43)
axes=[fig.add_subplot(gs[i,j]) for i in range(2) for j in range(2)]
fig.suptitle("Figure 1. Discovering Korean political science across two search environments",
             x=.07,y=.965,ha="left",fontsize=19,fontweight="bold",color=INK)
fig.text(.07,.925,"Study 1 links Google Scholar visibility to citation; Study 2 audits recovery, recommendation, and supplied-link access.",
         fontsize=10.4,color=MUTED)
pipeline(axes[0]); study1_effect(axes[1]); recovery(axes[2]); representation(axes[3])
fig.text(.07,.02,"Across two studies of Korean political science, Google Scholar visibility corresponds to citation trajectories, while LLM interventions alter language composition but recover few pre-specified local papers.",
         fontsize=8.9,color=INK,bbox={"boxstyle":"round,pad=.55","facecolor":PALE,"edgecolor":GRID})

for ext in ("png","svg"):
    path=OUT/f"discovery_bottleneck_global_figure.{ext}"
    fig.savefig(path,dpi=260 if ext=="png" else None,bbox_inches="tight",facecolor=PAPER)
    if ext=="png":
        with Image.open(path) as im:
            if im.mode!="RGB": im.convert("RGB").save(path,optimize=True)
plt.close(fig)
print(OUT)
