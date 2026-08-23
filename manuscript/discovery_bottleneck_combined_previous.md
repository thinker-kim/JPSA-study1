---
title: "Discovery Bottleneck"
subtitle: "Infrastructural Barriers to Local Scholarship"
author: "[Author name]"
date: "August 2026"
geometry: margin=0.72in
fontsize: 10pt
linestretch: 1.05
mainfont: STIX Two Text
mathfont: STIX Two Math
link-citations: true
colorlinks: true
linkcolor: "2F5F7F"
urlcolor: "2F5F7F"
---

## Abstract

Research published in local languages occupies a structurally disadvantaged position in international scholarship (Amano, González-Varo, and Sutherland 2016; Di Bitetti and Ferreras 2017; Mongeon and Paul-Hus 2016). This paper isolates one part of that broader inequality: the discovery of Korean political science. Study 1 examines the relationship between Google Scholar visibility and English-language citation trajectories for 54,789 Korean-language papers cited within Korean scholarship. Target-paper fixed-effects estimates show that the citation-probability gap between visible and nonvisible papers increased by 0.405 percentage points in 2010–2014 and 0.696 points in 2015–2019, relative to 2009 or earlier. Study 2 audits two web-enabled large language models with 100 pre-specified papers on five Korean-politics topics. Under an English general-web prompt, the systems recovered no Korean benchmark paper. Korean queries and Korean-database instructions changed the language composition of recommendations substantially, but recommendation recovery remained at or below 3.2% per execution. Of 1,932 recommendation occurrences, 44.2% supplied accessible full text. Across established and emerging search systems, Korean political science remains difficult to discover even when translation is technically available.

**Keywords:** scholarly discovery; Google Scholar; large language models; Korean political science; citation inequality; metadata

## 1. Introduction

Research published in local languages occupies a structurally disadvantaged position in international scholarship (Amano, González-Varo, and Sutherland 2016; Di Bitetti and Ferreras 2017; Mongeon and Paul-Hus 2016). A bibliographic analysis of Korean politics finds a divided citation structure: Korean-language scholarship draws heavily on locally accumulated research, whereas English-language scholarship concentrates recognition within the international literature (Kim 2025). Existing accounts establish the importance of language hierarchy but do not fully explain how scholars encounter candidate literature. A paper absent from a search result or recommendation receives no opportunity to be evaluated, translated, or cited, regardless of its substantive relevance.

This paper calls that constraint the **discovery bottleneck**. It examines the problem in two infrastructures that increasingly organize scholarly discovery. Google Scholar represents established indexed search; web-enabled LLMs represent an emerging interface that retrieves web sources, selects publications, and supplies links in a generated answer.

**Study 1** examines whether Google Scholar visibility is associated with the English-language citation trajectories of Korean political science, and whether that relationship changed as Google Scholar diffused:

> **Google Scholar visibility** $\rightarrow$ **English-language citation**

**Study 2** examines whether web-enabled LLMs recover pre-specified Korean political science papers, carry them into final recommendations, and provide links to accessible full text. It also tests Korean-language queries and explicit Korean-database instructions:

> **Search-trace recovery** $\rightarrow$ **final recommendation** $\rightarrow$ **supplied-link access**

Study 1 provides population-level evidence about Google Scholar visibility and citation over time. Study 2 provides experimental evidence about retrieval, recommendation, and linkage in current generative search. Together, they examine whether successive generations of search infrastructure make locally established Korean political science visible to international users.

The argument does not replace language hierarchy with infrastructure. It identifies discovery as a separate source of inequality. Study 1 finds that the English-language citation gap by Google Scholar visibility widened during the service's diffusion. Study 2 finds that the default LLM search recovered no Korean benchmark paper and that explicit Korean-oriented prompts still left more than 96% of that benchmark absent from each recommendation list. Publication language alone cannot account for these two patterns.

![Integrated evidence across Study 1 and Study 2](combined_analysis/figures/discovery_bottleneck_global_figure.png){width=100%}

## 2. Literature and Argument

### 2.1 Language and international citation

Research published outside English is less visible and less cited internationally (Amano, González-Varo, and Sutherland 2016; Di Bitetti and Ferreras 2017). This disparity is consequential: excluding non-English studies can change the evidence available for synthesis and bias substantive conclusions (Konno et al. 2020).

This literature explains how language hierarchy organizes publication, evaluation, audience, and citation. The present argument adds a distinct mechanism: unequal entry into the systems used to identify candidate literature. English titles, English abstracts, and machine translation can assist evaluation only after a publication has been retrieved.

### 2.2 Index coverage and metadata

Bibliometric research documents another source of inequality: databases represent fields, countries, and languages unevenly. Web of Science and Scopus overrepresent English-language and commercially published journals, limiting cross-national and social-science comparisons (Mongeon and Paul-Hus 2016). Google Scholar covers more citations and document types than Web of Science or Scopus, especially outside core journal literature, but broad coverage does not guarantee that every local paper is correctly represented or retrievable (Martín-Martín et al. 2018).

Newer open infrastructures broaden coverage without eliminating metadata problems. OpenAlex represents more multilingual work than selective commercial indexes, but language labels and metadata completeness remain uneven (Céspedes, Kozlowski, and Priego 2025). The practical consequence is that metadata quality is not merely an administrative detail. Titles, publication years, author names, persistent identifiers, abstracts, and reference deposits determine whether records can be connected across Crossref, OpenAlex, search engines, and retrieval-augmented systems (Kemp 2018).

Coverage studies generally describe what a database contains. They rarely test whether index presence is associated with later international citation or observe how a search interface transforms indexed records into user-facing recommendations. Those are the tasks of the two studies below.

### 2.3 LLMs as scholarly-search interfaces

Web-enabled LLMs combine search with synthesis. They do not simply return ranked records; they decide what to search, which sources to use, which papers to name, and which links to supply. Specialized retrieval-augmented systems can improve scientific synthesis when they search a defined scholarly corpus (Asai et al. 2025). General-purpose systems, however, may fabricate or corrupt bibliographic references (Walters and Wilder 2023). Citation validity is only one risk. A system can recommend real papers while failing to retrieve locally central work, or it can produce a list rich in Korean-language titles without recovering the Korean papers that local citation patterns identify as important.

This distinction yields two outcomes. **Benchmark recovery** asks whether specific papers selected before the audit are returned. **Language representation** asks what share of all returned items is Korean-language. A high representation share does not imply high recovery. Study 2 tests both.

## 3. Study 1: Google Scholar Visibility and Citation

### 3.1 Research question and hypotheses

Study 1 asks whether Google Scholar visibility is associated with English-language citation of Korean political science, and whether that relationship changed as Google Scholar became a routine scholarly-search tool.

**S1-H1: Visibility difference.** Google Scholar-visible Korean papers should have a higher probability of English-language citation than nonvisible Korean papers.

**S1-H2: Diffusion-period divergence.** Relative to the earliest citation cohort, the visible–nonvisible citation gap should increase after Google Scholar's diffusion.

### 3.2 Data and measures

Study 1 analyzes 54,789 Korean-language target papers cited at least once by Korean-language scholarship. The sample therefore contains research with demonstrated local use and includes targets with and without English-language citations. The unit is target paper $j$ by source-paper cohort $c$, producing 179,230 observations.

English-language citing papers are grouped by publication year: C1 (2009 or earlier), C2 (2010–2014), C3 (2015–2019), and C4 (2020–2024). A target enters the cohorts in which it could have been cited. The outcome $Y_{jc}$ equals one when target $j$ receives at least one citation from an English-language source paper in cohort $c$.

The exposure $D_j$ indicates whether paper $j$ is found in Google Scholar when searched by its title. A confirmed Google Scholar result is coded $D_j=1$; no confirmed result is coded $D_j=0$. The sample contains 19,436 visible and 35,353 nonvisible papers. This measure captures index presence and bibliographic retrievability. It does not measure topic-search ranking and does not reconstruct the year in which a paper entered Google Scholar.

### 3.3 Research design and estimation

The primary model is a target-paper fixed-effects linear probability model:

$$
Y_{jc}=\alpha_j+\lambda_c+\sum_{k=2}^{4}\beta_k
\left(D_j\times 1[c=k]\right)+\gamma AgeBin_{jc}+\epsilon_{jc}.
$$

Target effects $\alpha_j$ remove time-invariant differences in author, topic, journal, status, and baseline quality. Cohort effects $\lambda_c$ remove common changes in English-language citation. Each $\beta_k$ is the change in the visible–nonvisible citation-probability gap relative to C1. Standard errors are clustered by target.

We also analyze papers published by 2004. Every paper in that sample predates Google Scholar and is observable in all four cohorts. Robustness specifications use Poisson pseudo-maximum likelihood, citation counts, and topic-by-cohort, journal-by-cohort, or publication-year-by-cohort fixed effects. No opportunity offset is used.

### 3.4 Results

Raw citation incidence favors visible papers in every cohort. The $D=1$ and $D=0$ rates are 0.68% and 0.31% in C1, 1.90% and 0.67% in C2, 3.01% and 1.25% in C3, and 2.66% and 1.38% in C4. This supports S1-H1 descriptively, although the raw gap can reflect paper composition.

The within-paper results support S1-H2 during C2 and C3. Relative to C1, the D gap increases by 0.405 percentage points in C2 (95% CI [0.040, 0.770], $p=.030$) and 0.696 points in C3 (95% CI [0.329, 1.063], $p<.001$). The two coefficients are jointly different from zero ($p<.001$). In C4, the change is 0.008 points (95% CI [−0.337, 0.353], $p=.965$).

The pre-2005 sample gives the same bounded result. The D gap increases by 0.791 points in C2 (95% CI [0.227, 1.355], $p=.006$) and 0.496 points in C3 (95% CI [0.027, 0.964], $p=.038$). The joint test gives $p=.011$. The C4 estimate is positive but uncertain: 0.273 points (95% CI [−0.175, 0.721], $p=.233$).

| Change in D gap from C1 | Full sample | Published by 2004 |
|---|---:|---:|
| C2 | +0.405 pp [0.040, 0.770] | +0.791 pp [0.227, 1.355] |
| C3 | +0.696 pp [0.329, 1.063] | +0.496 pp [0.027, 0.964] |
| C4 | +0.008 pp [−0.337, 0.353] | +0.273 pp [−0.175, 0.721] |

Poisson estimates are less precise. Journal-by-cohort and publication-year-by-cohort specifications retain a positive C2 estimate with $p=.086$ and $p=.061$, respectively, but do not reproduce significant C3 or C4 interactions. A target-fixed-effects Poisson model produces positive C2 and C3 changes but excludes all-zero targets and therefore addresses citation timing among cited papers. The evidence supports a diffusion-period divergence, not a result invariant to every functional form.

![Study 1 design, raw citation incidence, and target-fixed-effects estimates](study1_analysis/figures/study1_fig1_design_and_main_results.png){width=100%}

## 4. Study 2: Auditing Web-Enabled LLM Search

### 4.1 Research questions and hypotheses

Study 2 asks three questions about web-enabled LLM search for Korean political science: whether a default English general-web prompt recovers a pre-specified Korean benchmark; whether query language and Korean-database instructions change recovery; and whether recommended items are reachable through the links that systems supply.

**S2-H1: Default recovery gap.** Under the English general-web prompt, the systems should recover Korean benchmark papers less often than the English benchmark.

**S2-H2: Retrieval intervention.** Korean queries and Korean-database instructions should improve Korean benchmark recovery relative to the English general-web baseline.

**S2-H3: Representation–recovery distinction.** The interventions should increase the Korean-language share of recommendations more than they increase recovery of the pre-specified Korean benchmark.

**S2-H4: Recommendation–access distinction.** Recommendation should not guarantee that the supplied link provides full text.

### 4.2 Benchmark corpora and factorial design

Study 2 uses two pre-specified 50-paper corpora on five topics in Korean politics: the Korean War, South Korean economic development, South Korean democratization, the North Korean nuclear program, and the Korean Wave. Each topic includes ten Korean-language papers selected using DBpia and KISS and ten English-language benchmark papers selected using Web of Science and Google Scholar. Selection preceded the audit.

The experiment crosses query language (English or Korean), source instruction (general web or an explicit instruction to search KCI, DBpia, or KISS), and system (OpenAI `gpt-5.6-sol` or Perplexity `sonar-pro`). Five topics, four prompt conditions, two systems, and five repetitions produce 200 stateless executions. Each execution requests ten scholarly publications in a fixed JSON format. The systems return 1,932 valid recommendation occurrences.

### 4.3 Outcomes

For corpus paper $j$ in execution $i$, **TraceRecovery** equals one if the paper appears in the observable search trace. **Recommendation** equals one if it appears in the final answer. **SuppliedLinkAccess** equals one if it is recommended and the supplied link opens full text without payment or login. The denominator remains all topic-relevant corpus-paper-by-execution pairs, so supplied-link access is a joint recovery-and-access outcome.

Matching uses normalized titles, English-title aliases, DOIs, canonical URLs, DBpia identifiers, and KCI identifiers. The benchmark panel contains 4,000 observations: 200 executions × 20 topic-relevant corpus papers.

Language representation is measured separately as the Korean-language share of all returned items. Recommendation language is resolved for all 1,932 valid items. Discovery-trace language is not used for cross-system representation comparisons because trace completeness differs by provider.

All 927 distinct supplied links or no-URL item keys were manually reviewed. Each was classified as accessible, abstract-only, paywalled, broken, or hallucinated. The primary link summary groups abstract-only and paywalled items as access restricted and broken or hallucinated items as invalid or unverifiable.

### 4.4 Statistical analysis

Recovery outcomes are estimated with linear probability models containing Korean-corpus status, Korean query, Korean-database instruction, their interactions, and a system indicator. Standard errors are clustered by paper and execution. Representation models use execution-level Korean-language shares, the two interventions, their interaction, and a system indicator with HC3 standard errors. Recommendation-level link models include item language, prompt condition, and system, with clustering by supplied-link/item key and execution.

### 4.5 Default recovery

Under the English general-web baseline, the systems recovered no Korean benchmark paper at any measured stage. English benchmark recovery was also low but nonzero: 3.4% in the trace, 3.2% in recommendations, and 0.6% through an accessible supplied link. The baseline Korean gaps were −3.4 percentage points for trace recovery ($p=.029$), −3.2 points for recommendation ($p=.015$), and −0.6 points for supplied-link access ($p=.311$). The last comparison has a floor problem: almost no benchmark paper from either corpus survived through access.

These results support S2-H1. The default system does not behave as a high-recall bibliographic database for either corpus, but the Korean benchmark begins at a further disadvantage: zero observed recovery.

### 4.6 Intervention effects and representation

Consistent with S2-H2, Korean queries and Korean-database instructions improve relative recovery. The Korean query narrows the Korean–English gap by 3.8 points at trace recovery ($p=.016$). The database instruction narrows it by 4.0 points at trace recovery ($p=.017$) and 3.2 points at recommendation ($p=.012$). Applying both interventions narrows the gap by 5.6 points at trace recovery and 6.4 points at recommendation relative to baseline.

The combined condition reverses the descriptive gap: 2.2% of Korean benchmark papers are recovered in the trace and 3.2% are recommended, compared with zero English benchmark papers. The reversal is relative, not absolute. More than 96% of the Korean benchmark is still absent from any given recommendation list.

Consistent with S2-H3, representation changes much more. The Korean-language share of recommendations is 0.0% under the English general-web baseline, 35.3% with the database instruction alone, 55.8% with the Korean query alone, and 91.2% with both. The corresponding accessible-link shares are 0.0%, 26.6%, 57.5%, and 94.9%. Intervention can therefore produce a list that looks local without recovering most of the locally central benchmark.

### 4.7 Supplied-link outcomes

Of 1,932 recommendation occurrences, 854 (44.2%) provide full text through the supplied link. Another 859 (44.5%) are restricted: 247 are abstract-only and 612 are paywalled. The remaining 219 (11.3%) are invalid or unverifiable, comprising 176 broken links and 43 coded hallucinated items. Broken links (9.1%) are more common than hallucinated papers (2.2%).

| Supplied-link outcome | Overall | Korean-language item | English-language item |
|---|---:|---:|---:|
| Accessible | 44.2% | 46.3% | 42.4% |
| Access restricted | 44.5% | 47.9% | 41.6% |
| Invalid or unverifiable | 11.3% | 5.8% | 16.0% |
| — Broken link | 9.1% | 3.3% | 14.1% |
| — Hallucinated item | 2.2% | 2.6% | 1.9% |

The fact that only 44.2% of recommendation occurrences provide full text through the supplied link supports S2-H4. After adjustment for prompt condition and system, item language is not independently associated with full access, restriction, or invalid status. The descriptive language difference reflects the mix of items generated under different conditions, not a causal effect of Korean publication language.

![Study 2 design, benchmark recovery, representation, and supplied-link outcomes](/Users/hyowonkim/SciSci-LLM-audit/outputs/figures/study2_global_figure.png){width=100%}

## 5. What the Two Studies Show Together

Study 1 and Study 2 examine the same substantive problem in separate discovery environments. Study 1 shows that current Google Scholar visibility marks Korean political science papers whose English-language citation advantage grew during the period when Google Scholar became a standard search tool. Study 2 shows that current LLM search often fails to retrieve and recommend pre-specified Korean political science papers, even after direct intervention.

The studies also clarify what the claim is not. The evidence does not show that Korean language is unimportant. It does not show that Google Scholar visibility alone causes citation. It does not show that a Korean-language prompt solves benchmark recovery. Instead, each study identifies a distinct infrastructural constraint that language-only accounts miss.

Study 1 identifies the divide between Google Scholar visibility and English-language citation. Study 2 identifies two further problems within generative search. **Representation is not recovery**: a recommendation list can be 91.2% Korean-language while recovering only 3.2% of the pre-specified Korean benchmark. **Recommendation is not access**: fewer than half of supplied links open full text, and some links are broken or point to unverifiable items.

C4 in Study 1 does not contradict Study 2. The C4 interaction says that the visibility gap did not expand further relative to C1; it does not show that discovery barriers disappeared. C4 combines 2020–2024 citations, contains only a short period after web-enabled generative search began to diffuse, and is subject to publication and citation lags. Study 2 directly observes current search and finds that existing visibility problems remain in the LLM setting.

## 6. Implications

The findings change the policy target. Requiring local scholars to publish full papers in English treats international visibility as an author-level language problem and can weaken the local scholarly sphere. The results point to interventions that preserve local-language publication while improving machine-readable presence:

1. deposit complete bilingual metadata, including Korean and English titles, abstracts, author identifiers, publication years, and references;
2. improve DOI and persistent-identifier coverage;
3. transmit records from KCI, DBpia, and KISS into Crossref, OpenAlex, and other reusable indexes;
4. expose stable full-text or landing-page links that search systems can verify; and
5. evaluate search tools with pre-specified local benchmarks, not only the language mix of their outputs.

These interventions target the points at which papers disappear without requiring the local literature itself to become English-only.

## 7. Limitations

Study 1 measures Google Scholar visibility in 2026 and cannot reconstruct historical index entry. Its fixed-effects design removes time-invariant paper differences but not every time-varying process that could affect both visibility and citation. The main linear probability result is stronger than several Poisson robustness specifications, so the evidence should be stated as a diffusion-period alignment rather than a definitive causal effect.

Study 2 covers two systems, five topics, and one collection period. Recovery events are sparse, and trace observability differs by provider. The pre-specified corpora are locally and internationally prominent benchmarks, not exhaustive definitions of relevance. Link review evaluates the URL supplied by the system, not whether the paper can be found elsewhere.

Neither study observes the full decision process between reading and citation. Author judgment, topic fit, journal norms, and language still matter. The contribution is to show that many papers face unequal opportunity before those factors can operate.

## 8. Conclusion

Local scholarship can be abundant, locally cited, and partially available in English metadata while remaining absent from international search pathways. Study 1 finds that Google Scholar visibility and English-language citation trajectories became more closely aligned during Google Scholar’s diffusion. Study 2 finds that current LLM search recovers almost none of a pre-specified Korean benchmark by default and only a small share after direct intervention. Prompting changes language representation far more than benchmark recovery, and recommendation does not ensure access.

The resulting inequality is not only linguistic. It is also infrastructural. In Study 1, the relevant divide is whether Korean political science can be retrieved in Google Scholar and how that divide corresponds to English-language citation. In Study 2, the relevant divides occur within LLM search: recovery, recommendation, and supplied-link access. Improving international circulation therefore requires interventions tailored to each environment—better bibliographic visibility for indexed search and benchmarked retrieval with stable linkage for LLM search—not only translation or English-language publication.

## Data and Reproducibility

The Study 1 replication files include the target-by-cohort panel, target-level Google Scholar coding, coefficient tables, and figure scripts. `analyze_study1.R` reproduces the statistical results. The Study 2 package includes the execution outcomes, benchmark-recovery panel, recommendation-accessibility panel, coefficient table, manual link review, and analysis scripts. `plot_combined_discovery_figure.py` reproduces the integrated figure.

## References

Amano, Tatsuya, Juan P. González-Varo, and William J. Sutherland. 2016. “Languages Are Still a Major Barrier to Global Science.” *PLOS Biology* 14(12): e2000933. https://doi.org/10.1371/journal.pbio.2000933.

Asai, Akari, et al. 2025. “Synthesizing Scientific Literature with Retrieval-Augmented Language Models.” *Nature*. https://doi.org/10.1038/s41586-025-10072-4.

Céspedes, Lucía, Diego Kozlowski, and Ernesto Priego. 2025. “Evaluating the Linguistic Coverage of OpenAlex: An Assessment of Metadata Accuracy and Completeness.” *Journal of the Association for Information Science and Technology* 76: 884–895. https://doi.org/10.1002/asi.24979.

Di Bitetti, Mario S., and Julián A. Ferreras. 2017. “Publish (in English) or Perish: The Effect on Citation Rate of Using Languages Other than English in Scientific Publications.” *Ambio* 46: 121–127. https://doi.org/10.1007/s13280-016-0820-7.

Kemp, Jennifer. 2018. “Metadata and Discoverability: A Use Case Overview.” *Information Services & Use* 38(3): 131–141. https://doi.org/10.3233/ISU-180004.

Kim, Hyowon. 2025. *Two Spheres of Korean Politics: Knowledge Production and Dissemination across Linguistic Divides*. Ann Arbor, MI: Inter-university Consortium for Political and Social Research. https://doi.org/10.3886/E240683V1.

Konno, Katsuya, et al. 2020. “Ignoring Non-English-Language Studies May Bias Ecological Meta-Analyses.” *Ecology and Evolution* 10(13): 6373–6384. https://doi.org/10.1002/ece3.6368.

Martín-Martín, Alberto, Enrique Orduna-Malea, Mike Thelwall, and Emilio Delgado López-Cózar. 2018. “Google Scholar, Web of Science, and Scopus: A Systematic Comparison of Citations in 252 Subject Categories.” *Journal of Informetrics* 12(4): 1160–1177. https://doi.org/10.1016/j.joi.2018.09.002.

Mongeon, Philippe, and Adèle Paul-Hus. 2016. “The Journal Coverage of Web of Science and Scopus: A Comparative Analysis.” *Scientometrics* 106: 213–228. https://doi.org/10.1007/s11192-015-1765-5.

Walters, William H., and Esther I. Wilder. 2023. “Fabrication and Errors in the Bibliographic Citations Generated by ChatGPT.” *Scientific Reports* 13: 14045. https://doi.org/10.1038/s41598-023-41032-5.
