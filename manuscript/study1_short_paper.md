---
title: "Visible Before Cited"
subtitle: "Google Scholar Index Presence and English-Language Citation of Korean Political Science"
author: "[Author name]"
date: "August 2026"
geometry: margin=0.72in
fontsize: 10pt
linestretch: 1.05
mainfont: STIX Two Text
mathfont: STIX Two Math
---

## Abstract

Most locally cited Korean political science never enters English-language scholarship. This paper tests whether part of that gap tracks a basic feature of discovery infrastructure: whether a paper can be retrieved in Google Scholar even when its exact title is known. The analysis includes 54,789 Korean-language target papers cited at least once by Korean-language source papers and 179,230 target-paper-by-source-cohort observations. Google Scholar visibility is measured through exact-title lookup. English-language citations are grouped into four source-paper cohorts: 2009 or earlier, 2010–2014, 2015–2019, and 2020–2024. Target-paper fixed-effects models show that the citation-probability gap between visible and nonvisible papers grew by 0.405 percentage points in 2010–2014 and 0.696 points in 2015–2019, relative to the earliest cohort. The same pattern appears among papers published by 2004, for which all four cohorts are observable. No further expansion appears in 2020–2024. Poisson specifications are less precise, so the evidence supports a bounded claim: citation trajectories diverged by current index visibility during Google Scholar’s diffusion, but the divergence did not continue through the latest cohort.

**Keywords:** scholarly visibility; Google Scholar; citation inequality; Korean political science; research infrastructure

## 1. Introduction

Korean political science has accumulated a large body of locally used research, yet very little of it is cited in English-language scholarship. The puzzle is not whether local research exists or matters locally. It is why so little crosses into English-language citation networks.

One possible bottleneck precedes reading and evaluation. A paper that does not appear in a major scholarly index cannot be considered by researchers who rely on that index. This paper examines a minimal form of such visibility: whether a Korean paper can be retrieved in Google Scholar through an exact-title search. Exact-title lookup does not measure topic-search ranking or the probability that an unfamiliar researcher independently discovers the paper. It measures a more basic condition—index presence and bibliographic retrievability. Failure at this low bar indicates that even a researcher who already knows the title may not recover the paper through Google Scholar.

A cross-sectional comparison is not enough. Visible papers may appear in better-known journals, have stronger metadata, or be of higher quality. Those same characteristics can also raise English-language citations. The analysis therefore asks whether citation trajectories changed as Google Scholar became a routine discovery tool. If current visibility only marks fixed paper quality, the visible–nonvisible citation gap need not widen during the period of Google Scholar’s diffusion. If index visibility became more consequential as scholars increasingly searched through Google Scholar, visible papers should gain a relative citation advantage during that period.

The evidence is specific rather than universal. Papers currently visible in Google Scholar have higher raw English-language citation incidence in every cohort. After target-paper and cohort fixed effects, the visible–nonvisible gap increases in 2010–2014 and 2015–2019 relative to the earliest cohort. The increase remains when the sample is restricted to papers published by 2004. It does not persist in 2020–2024. The result therefore supports a diffusion-period divergence, not a monotonic increase through the latest cohort.

This distinction matters for the broader project. The latest cohort is not evidence that discovery barriers have disappeared. Citations take time to accumulate, and the cohort contains only two years after web-enabled generative search began to spread. A separate audit of generative search can test whether newer systems recover papers that older indexes miss. The present study establishes the historical citation pattern without treating the latest cohort as a clean test of AI-era search.

## 2. Data and Measurement

### 2.1 Target population and citation outcome

The target population is Korean-language scholarship that has demonstrated local use: each target paper was cited at least once by a Korean-language source paper. This criterion admits papers with and without English-language citations. It also matches the substantive question, which concerns whether knowledge used in the Korean scholarly community crosses into English-language research.

The analysis contains 54,789 unique targets. For each target $j$, English-language citing papers are grouped by source publication year into four cohorts:

- C1: 2009 or earlier;
- C2: 2010–2014;
- C3: 2015–2019; and
- C4: 2020–2024.

A target enters only cohorts that end on or after its publication year. The outcome $Y_{jc}$ equals one if target $j$ received at least one citation from an English-language source paper in cohort $c$, and zero otherwise. The final panel contains 179,230 target-by-cohort cells. English-language citation is rare: the cohort-specific incidence ranges from 0.39% in C1 to 1.82% in C4.

### 2.2 Google Scholar visibility

The exposure $D_j$ is current exact-title Google Scholar visibility. Searches use available Korean, English, and reference-title variants. A confirmed result is coded $D_j=1$; no confirmed result is coded $D_j=0$. The sample contains 19,436 papers with $D_j=1$ and 35,353 with $D_j=0$.

The measure has a clear boundary. It records visibility at the 2026 collection date, not historical index status in each cohort. The cohort interaction therefore tests whether past citation trajectories differ by current visibility. It does not observe the exact year in which each paper entered Google Scholar.

## 3. Empirical Strategy

The primary model is a target-paper fixed-effects linear probability model:

$$
Y_{jc}=\alpha_j+\lambda_c+\sum_{k=2}^{4}\beta_k
\left(D_j\times 1[c=k]\right)+\gamma AgeBin_{jc}+\epsilon_{jc}.
$$

Target fixed effects $\alpha_j$ absorb every time-invariant paper characteristic, including author, topic, journal, and baseline quality. Cohort fixed effects $\lambda_c$ absorb shocks common to all targets in a source cohort. The coefficients $\beta_k$ measure how much the visible–nonvisible citation-probability gap changes in cohort $k$ relative to C1. Standard errors are clustered by target paper.

The linear probability model is useful here because it retains targets with no English-language citation in any cohort. A target-fixed-effects Poisson model drops such targets and answers a narrower question about citation timing among papers that receive citations. We report that model as a robustness check rather than the primary specification.

Two features complicate the full panel. First, targets published after C1 do not contribute a C1 observation. Second, the composition of eligible papers changes across cohorts. We therefore repeat the primary model among papers published by 2004. Every paper in this restricted sample predates Google Scholar and can be observed in all four cohorts. This is a design-based restriction, not a cut point selected for statistical significance.

Additional checks use Poisson pseudo-maximum likelihood for binary and count outcomes, journal-by-cohort fixed effects, topic-by-cohort fixed effects, and publication-year-by-cohort fixed effects. These models test whether the result depends on functional form or on changing journal, topic, or publication-year composition. No opportunity offset is used.

## 4. Results

### 4.1 Raw citation incidence

Visible papers have higher raw citation incidence in every cohort. In C1, 0.68% of $D=1$ cells and 0.31% of $D=0$ cells contain an English-language citation. The corresponding rates are 1.90% versus 0.67% in C2, 3.01% versus 1.25% in C3, and 2.66% versus 1.38% in C4. The raw relative risk peaks in C2 and declines thereafter. The unadjusted pattern therefore shows a persistent level difference but not a monotonic increase.

### 4.2 Within-paper change during diffusion

Figure 1C presents the primary estimates. In the full eligible sample, the visible–nonvisible gap increases by 0.405 percentage points in C2 relative to C1 (95% CI [0.040, 0.770], $p=.030$). The increase reaches 0.696 points in C3 (95% CI [0.329, 1.063], $p<.001$). The C2 and C3 coefficients are jointly different from zero ($p<.001$). Given the low baseline incidence of English-language citation, these absolute changes are substantively meaningful.

The increase does not continue in C4. Its estimate is 0.008 percentage points (95% CI [−0.337, 0.353], $p=.965$). This is not evidence that current discovery barriers have disappeared. It shows only that the gap did not expand further relative to C1 in the latest citation cohort.

The pre-2005 sample produces the same bounded pattern. The D gap increases by 0.791 points in C2 (95% CI [0.227, 1.355], $p=.006$) and 0.496 points in C3 (95% CI [0.027, 0.964], $p=.038$). The two coefficients are jointly significant ($p=.011$). The C4 estimate remains positive but uncertain: 0.273 points (95% CI [−0.175, 0.721], $p=.233$).

| Change in D gap from C1 | Full eligible sample | Published by 2004 |
|---|---:|---:|
| C2 | +0.405 pp [0.040, 0.770] | +0.791 pp [0.227, 1.355] |
| C3 | +0.696 pp [0.329, 1.063] | +0.496 pp [0.027, 0.964] |
| C4 | +0.008 pp [−0.337, 0.353] | +0.273 pp [−0.175, 0.721] |

![Integrated Study 1 results: cohort design, raw citation incidence, target-fixed-effects estimates, and analysis sample](study1_analysis/figures/study1_global_figure.png){width=100%}

### 4.3 Robustness and scope

The target-fixed-effects Poisson model also yields positive C1-relative changes in C2 and C3, but it uses only 7,191 informative cells because all-zero targets do not identify the conditional model. The result supports a change in citation timing among cited papers, not the full extensive margin.

Other Poisson models are weaker. After journal and age controls, the C2, C3, and C4 interaction estimates are not individually distinguishable from zero. Journal-by-cohort and publication-year-by-cohort models retain a positive C2 coefficient, with $p=.086$ and $p=.061$, respectively, but C3 and C4 are not precise. A citation-count outcome produces the same lack of sustained expansion. These checks prevent a stronger claim that the result is invariant to functional form.

Accessibility does not provide an independent confirmation. Among currently visible papers, open supplied full text is not significantly associated with cohort-specific English citation incidence. The access measure is conditional on Google Scholar visibility and is based on present access, so its null result should not be read as evidence that access never matters.

## 5. Discussion

The results support a limited infrastructure account. Papers currently retrievable in Google Scholar have higher raw English-language citation incidence. More importantly, their relative citation trajectories diverge from those of nonvisible papers in C2 and C3, the period in which Google Scholar became a routine scholarly search tool. The pattern survives a restriction to papers published before Google Scholar existed and a model that removes all fixed paper attributes.

The evidence does not establish a simple causal effect of index presence. Current visibility may partly reflect events that occurred after the relevant citations, including later indexing and later citations that improved metadata or ranking. The design removes fixed paper differences but cannot reconstruct historical index entry. The safest interpretation is temporal alignment: current index visibility marks papers whose English-language citation advantage grew during Google Scholar’s diffusion.

C4 places an important boundary on the claim. The result is not a steady sequence in which the D gap grows in every period. Three explanations remain open. First, C4 citations are right-censored, especially for work published near 2024. Second, Google Scholar’s diffusion effect may have saturated after the visible–nonvisible distinction became established. Third, discovery pathways changed after 2023, but C4 contains too little post-generative-search time—and too much publication lag—to test that explanation. A current audit of web-enabled generative search is better suited to determining whether newer systems recover locally important work or inherit older visibility gaps.

## 6. Conclusion

English-language citation of locally used Korean political science is rare. Exact-title-visible papers fare better in raw comparisons, and their citation-probability advantage grows relative to the earliest cohort in 2010–2014 and 2015–2019. The result appears both in the full eligible panel and among papers published before Google Scholar. It does not extend through 2020–2024, and Poisson estimates are less precise.

The contribution is therefore narrow but clear. Bibliographic visibility and international citation trajectories became more closely aligned during Google Scholar’s diffusion. This does not show that visibility alone causes citation, nor that recent search systems have solved the problem. It shows that metadata and index presence are part of the conditions under which locally used knowledge enters international citation networks.

## Data and Reproducibility

The replication package includes the target-by-cohort analysis panel, target-level Google Scholar coding, model coefficients, cohort-specific contrasts, and figure source files. `analyze_study1.R` reproduces the statistical results, and `plot_study1_paper_figures.py` reproduces all manuscript figures.
