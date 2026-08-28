---
title: "Discovery Bottleneck: The Visibility of Korean Politics Scholarship across Google Scholar and Generative Search"
author: "Hyowon Kim, Do Won Kim, Won-ho Park"
date: "September 2026"
geometry: margin=0.72in
fontsize: 10pt
linestretch: 1.05
mainfont: Times New Roman
mathfont: STIX Two Math
CJKmainfont: AppleMyungjo
---

# Abstract

Korean political science is produced and circulated across distinct KCI- and SSCI-centered scholarly spheres (Rhee 2026). This paper examines one dimension of that segmentation through visibility in scholarly search and full-text access.

Study 1 analyzes 54,789 papers on Korean politics cited by Korean-language political science articles published in 2000–2025. Relative to the baseline period, the English-language citation-probability gap between papers that are and are not currently retrievable in Google Scholar was significantly larger by 0.405 percentage points in 2010–2014 and 0.696 points in 2015–2019, but did not widen further in 2020–2024. Full-text access through Google Scholar links was not significantly associated with English-language citation probability. These estimates describe an association between current retrievability and historical citation trajectories, not a causal effect of Google Scholar.

Study 2 audits two web-enabled generative search systems using 50 Korean-language and 50 English-language benchmark papers across five topics. Under the English-query, general-web baseline, no Korean benchmark paper was recovered in search or final recommendations, whereas English benchmark recovery was 3.4% and 3.2%, respectively. Combining a Korean query with an instruction to search Korean scholarly databases narrowed the Korean–English gap by 5.6 points at search and 6.4 points at recommendation, yet Korean benchmark recommendation recovery remained only 3.2%. Only 44.2% of all recommendations provided direct full-text access through the accompanying link, with no significant language difference.

Together, the studies show that the international visibility of Korean political science should be analyzed not only through publication and citation but also through the processes by which publications are retrieved and selected as final sources. Unlike the search and recommendation results, full-text access shows no corresponding language gap. The paper defines discovery bottleneck as the failure of a publication to enter the search candidate set or survive final source selection before substantive evaluation.

Keywords: Korean political science; scholarly search; Google Scholar; generative search; non-English-language scholarship; international visibility; full-text access; discovery bottleneck


# 1. Introduction

International political science does not draw evenly on research from all countries, regions, and languages. Across more than a century of publications in eight major political science journals, research has historically concentrated on a limited number of North American and Western European countries, although geographical coverage has broadened over time (Wilson and Knutsen 2022). International publishing in the discipline also remains uneven by researchers' institutional and geographic location (Breuning et al. 2018). More broadly, major bibliographic databases disproportionately cover English-language journals, and non-English publications tend to receive fewer international citations than comparable English-language work (Mongeon and Paul-Hus 2016; Vera-Baceta, Thelwall, and Kousha 2019; Di Bitetti and Ferreras 2017).

Within Korean political science, research published in KCI and SSCI venues differs in topical and methodological patterns (Rhee 2026), while research on Korean politics published and circulated in English tends to achieve broader citation reach and international recognition than research produced in the Korean-language sphere (Kim et al. 2025).[^1]

These patterns raise a specific question for Korean political science. A substantial Korean-language literature exists on topics that are also central to international research on Korea, including democratization, economic development, the Korean War, the North Korean nuclear issue, and the Korean Wave. Yet the existence and domestic use of a publication do not tell us whether it appears in the search environments used to identify scholarly literature.

This paper focuses on that search-mediated form of visibility. It does not compare the substantive quality of Korean- and English-language research, nor does it treat search as the only explanation for international citation inequality. Instead, it asks whether locally used Korean scholarship appears in two different scholarly discovery environments and whether the systems themselves provide a direct route to the paper's full text.

The first environment is Google Scholar, an established scholarly search tool. Google Scholar covers a broader range of document types and languages than selective citation indexes such as Web of Science and Scopus (Chen 2010; Martín-Martín et al. 2018b, 2021). It is also widely used in actual scholarly discovery. In the 2021 Ithaka S+R US Faculty Survey, 29% of faculty reported that they most often began a search for new scholarly literature in Google Scholar, including 36% of social science faculty (Blankstein 2022). Study 1 therefore examines a minimal paper-level condition, namely whether a known Korean-language paper can currently be recovered through an exact-title Google Scholar search. It separately measures whether Google Scholar supplies a link through which the full text can be opened.

The second environment is web-enabled generative search. LLMs are increasingly being tested and used for literature search, although they are not yet as established as conventional academic search engines. A 2025 scoping review of LLM applications in systematic reviews found literature search to be the most frequently studied application, appearing in 15 of 37 included studies, while also concluding that fully established or validated applications remained limited (Lieberum et al. 2025). Recent academic-search systems explicitly combine retrieval with LLM-based selection and synthesis (Ajith et al. 2024; He et al. 2025; Asai et al. 2026). Study 2 therefore observes three user-facing stages where available, asking whether a pre-specified paper appears in an observable search trace, whether it is included in the final recommendation, and whether the URL supplied with that recommendation opens the full text.

The two studies answer different empirical questions. Study 1 uses a large longitudinal citation panel but observes Google Scholar status only in 2026. It therefore tests whether current retrievability marks papers with different historical English-language citation trajectories; it does not reconstruct historical Google Scholar indexing. Study 2 directly manipulates current search conditions but uses a smaller benchmark corpus and observes no later citation outcome. The studies should not be concatenated into a causal chain from Google Scholar to LLM recommendation to citation.

Their common object is narrower. It is the paper-level visibility of Korean political science within systems used to identify scholarly literature. In this paper, discovery bottleneck refers to an observable search-mediated loss in which a locally used or pre-specified publication is absent from the retrievable or recommended set, or is presented without a usable full-text route supplied by the system. The term is introduced here as an operational label, not as an established theory of scholarly communication.

The empirical results are similarly bounded. Study 1 finds that current exact-title Google Scholar retrievability is associated with a larger English-language citation gap in the 2010–2014 and 2015–2019 cohorts than in the earliest cohort, but not in 2020–2024. A secondary analysis of full-text access through current Google Scholar links is not statistically associated with cohort-specific citation incidence. Study 2 finds a Korean benchmark deficit under default English-language generative search, but also shows that prompts can radically change the language composition of recommendations without producing high recovery of the pre-specified Korean corpus. Finally, fewer than half of all recommendations provide immediate full-text access through the accompanying link.

These findings refine the problem of international visibility in political science. They do not establish that search infrastructure causes citation inequality. Rather, Study 1 shows that historical citation trajectories differ by current Google Scholar visibility, while Study 2 shows that the default Korean benchmark deficit is conditional on search design and that increased Korean-language representation does not imply high benchmark recovery. Full-text access does not reproduce the search and recommendation gaps. The contribution is therefore to distinguish paper-level visibility, final source selection, language representation, and provided-link access as empirically separate outcomes.


# 2. Literature and Argument

## 2.1 International visibility and scholarly discovery

Political science has long been concerned with the geographic scope of the knowledge on which the discipline builds. Research in leading journals has historically focused disproportionately on North America and Western Europe, with meaningful implications for the scope of descriptive and causal claims made in the field (Wilson and Knutsen 2022). Publication in leading political science outlets is also geographically unequal. Analyses of submissions and publications at the *American Political Science Review* show lower representation of scholars from the Global South and overrepresentation of scholars at prestigious institutions (Breuning et al. 2018).

Language adds another dimension. Web of Science and Scopus overrepresent English-language journals relative to the broader population of scholarly journals (Mongeon and Paul-Hus 2016; Vera-Baceta, Thelwall, and Kousha 2019). Studies of multilingual publishing further find lower citation rates for articles published in languages other than English after accounting for publication characteristics (Di Bitetti and Ferreras 2017). These findings establish that the internationally visible scholarly record differs from the full set of research produced across languages and locations.

This paper examines one part of that difference at the point of literature search. Search systems do not merely measure scholarship after the fact; they are also used to identify candidate literature. Information-retrieval research distinguishes aggregate database coverage from retrievability, the extent to which an individual document can be returned through a retrieval system (Azzopardi and Vinay 2008). The distinction matters here because broad coverage of a language or field does not imply that every individual paper is equally retrievable.

The two studies apply this question to two search environments. Study 1 examines an established academic search engine, Google Scholar. Study 2 examines web-enabled generative search, where retrieval is followed by an additional user-facing selection because the system generates an answer and presents only some sources as recommendations or citations.

A second distinction concerns access. Both Google Scholar and generative-search systems can provide links to the publications they surface. The relevant measure is whether the provided link opens the full text without payment or login. This is not equivalent to a paper's general open-access status. A paper may be freely available elsewhere even when the search environment provides a paywalled, abstract-only, or broken link.

## 2.2 Study 1: Google Scholar visibility and full-text access

Google Scholar is relevant for non-English scholarship because it combines broad coverage with extensive real-world use. Cross-database studies find substantially wider coverage in Google Scholar than in Web of Science or Scopus, including many non-English and non-journal citing documents (Chen 2010; Martín-Martín et al. 2018b, 2021). At the same time, broad aggregate coverage is incomplete at the record level. Using 116,000 Crossref records as an external baseline, Delgado-Quirós et al. (2024) found that 9.8% of sampled publications were not returned by Google Scholar.

Google Scholar is also a major point of entry to scholarly literature. In the 2021 Ithaka S+R survey, 29% of US faculty most often began scholarly discovery in Google Scholar, and the figure was 36% among social scientists (Blankstein 2022). Earlier studies had already documented substantial use of Google and Google Scholar by researchers and graduate students (Jamali and Asadi 2010; Cothran 2011). These data do not imply that every citation results from Google Scholar use; they establish that Google Scholar is a substantively important search environment in which paper-level visibility can be observed.

Google Scholar also links users to available versions of papers. Jamali and Nabavi (2015) found that 61.1% of sampled articles were accessible in full text through Google Scholar. In a much larger sample of 2,269,022 Web of Science documents from 2009 and 2014, Martín-Martín et al. (2018a) found a freely available version displayed in Google Scholar for 54.6% of documents. Those versions came from publishers, repositories, and other web sources. These studies motivate a distinction between being retrievable in Google Scholar and being connected by Google Scholar to a usable full-text version.

Prior research has mainly compared databases or estimated aggregate levels of coverage and online availability. Study 1 instead asks, within a single set of locally used Korean-language political science papers, whether current exact-title Google Scholar retrievability is associated with different histories of English-language citation. It also tests, among currently retrievable papers, whether full-text access through current Google Scholar links provides an additional association with citation incidence.

The temporal limitation is central. The study observes Google Scholar status in 2026, not in each historical citation cohort. Current status may reflect indexing or web availability that changed after some citations occurred. The analysis therefore concerns historical citation trajectories by current search status, not the causal effect of historical Google Scholar indexing or access.

## 2.3 Study 2: generative scholarly search, recommendation, and supplied access

Generative search changes the user-facing organization of scholarly discovery. A web-enabled LLM can retrieve external sources and then produce a synthesized answer that cites or recommends only a subset of what was searched. Research on generative search has therefore evaluated not only whether sources exist, but whether citations support generated claims and whether systems provide complete and verifiable sourcing (Liu, Zhang, and Liang 2023).

LLM-assisted scholarly search is also becoming an explicit research area. A 2025 scoping review of LLM use in systematic reviews identified literature search as the most frequent application among 37 included studies, while emphasizing that validated applications remain limited (Lieberum et al. 2025). Scientific-search benchmarks such as LitSearch define target papers independently of the tested system and evaluate whether retrieval methods recover those papers (Ajith et al. 2024). Agentic systems such as PaSa similarly use query–paper benchmarks to evaluate LLM-based academic search rather than treating a plausible-looking generated list as self-validating (He et al. 2025).

This benchmark logic follows the standard information-retrieval practice of evaluating returned documents against an independently specified relevant set (Manning, Raghavan, and Schütze 2008). It is particularly important for multilingual search. A recommendation list can contain many Korean-language papers without recovering the particular Korean papers fixed before the audit. Language representation and benchmark recovery therefore answer different questions. Representation measures the composition of what the system chooses to show; recovery measures whether a pre-specified evaluation set appears.

Study 2 further distinguishes observable search from final recommendation. A benchmark paper may appear in a provider-exposed search trace but not in the final list shown to the user. Even an accurately recommended paper may be paired with a URL that is paywalled, abstract-only, broken, or otherwise unusable. The audit therefore treats benchmark recovery in search, final recommendation recovery, and full-text access through the provided link as separate outcomes.

Existing generative-search audits have examined citation correctness, source authority, and geographic or commercial source bias (Liu, Zhang, and Liang 2023; Li and Sinnamon 2024). Recent work has also evaluated LLM-based scholar or paper recommendation with external benchmarks (Ajith et al. 2024; He et al. 2025; Espín-Noboa and Méndez 2026). Less is known about how query language and explicit instructions to search local scholarly databases affect recovery of a pre-specified non-English political science corpus. Study 2 addresses that question for Korean politics.


# 3. Study 1: Google Scholar Visibility and English-Language Citation

## 3.1 Data and measures

Study 1 begins with Korean-language political science papers that have demonstrated local scholarly use. Every target paper was cited at least once by a Korean-language source paper. The final sample contains 54,789 unique target papers.

English-language citing papers are grouped into four source-paper cohorts.

- C1 — 2009 or earlier;
- C2 — 2010–2014;
- C3 — 2015–2019; and
- C4 — 2020–2024.

A target contributes only to cohorts in which citation was temporally possible. For target paper $j$ and cohort $c$,

$$
Y_{jc}=1
$$

if the target receives at least one citation from an English-language source paper in that cohort, and zero otherwise. The final panel contains 179,230 target-paper × cohort observations.

The main exposure is current exact-title Google Scholar visibility, $D_j$. Searches use available Korean, English, and reference-title variants. A confirmed bibliographic match is coded $D_j=1$; a completed search with no confirmed match is coded $D_j=0$. The sample contains 19,436 retrievable papers and 35,353 nonretrievable papers.

The term *retrievability* is intentionally narrow. Exact-title lookup is a known-item search. It does not measure whether an unfamiliar researcher would find the paper through a topical query or where the paper ranks for a broad political-science search. It measures whether the known paper can currently be recovered in Google Scholar when identifying title information is supplied.

A secondary measure captures full-text access through Google Scholar links among currently visible papers. It records whether the link supplied through Google Scholar opens the full text. This is conditional on current Google Scholar visibility and does not attempt to classify the paper's general OA status across the web.

## 3.2 Empirical strategy

The principal specification is a target-paper fixed-effects linear probability model.

$$
Y_{jc}=\alpha_j+\lambda_c+\sum_{k=2}^{4}\beta_k
\left(D_j\times 1[c=k]\right)+\gamma AgeBin_{jc}+\epsilon_{jc}.
$$

Target fixed effects $\alpha_j$ absorb all time-invariant target-paper attributes, and cohort fixed effects $\lambda_c$ absorb common cohort shocks. Because $D_j$ is time-invariant, its main effect is absorbed by the target fixed effects. The interaction coefficients $\beta_k$ estimate how the visible–nonvisible citation-probability gap in each later cohort differs from the gap in C1. Standard errors are clustered by target paper.

To address changing eligibility across cohorts, the analysis is repeated among papers published by 2004. Every target in this restricted sample predates Google Scholar and can contribute to all four citation cohorts. Robustness checks use Poisson pseudo-maximum likelihood, citation counts, and alternative journal-, topic-, and publication-year-by-cohort controls.

## 3.3 Results

Currently retrievable papers have higher raw English-language citation incidence in every cohort.

| Cohort | $D=1$ | $D=0$ | Raw difference |
|---|---:|---:|---:|
| C1 | 0.68% | 0.31% | +0.37 pp |
| C2 | 1.90% | 0.67% | +1.23 pp |
| C3 | 3.01% | 1.25% | +1.76 pp |
| C4 | 2.66% | 1.38% | +1.28 pp |

The fixed-effects analysis asks whether that difference changes across cohorts. Relative to C1, the visible–nonvisible gap increases by 0.405 percentage points in C2 (95% CI [0.040, 0.770], $p=.030$) and 0.696 percentage points in C3 (95% CI [0.329, 1.063], $p<.001$). The C2 and C3 coefficients are jointly different from zero ($p<.001$). The C4 change is 0.008 percentage points (95% CI [−0.337, 0.353], $p=.965$), providing no evidence of a further increase in the latest cohort.

The pre-2005 target sample produces the same bounded pattern.

| Change in $D$ gap from C1 | Full eligible sample | Published by 2004 |
|---|---:|---:|
| C2 | +0.405 pp [0.040, 0.770] | +0.791 pp [0.227, 1.355] |
| C3 | +0.696 pp [0.329, 1.063] | +0.496 pp [0.027, 0.964] |
| C4 | +0.008 pp [−0.337, 0.353] | +0.273 pp [−0.175, 0.721] |

In the pre-2005 sample, C2 is significant at $p=.006$, C3 at $p=.038$, and the joint C2–C3 test at $p=.011$; C4 remains uncertain ($p=.233$).

Robustness checks are less uniform. A target-fixed-effects Poisson model produces positive C2 and C3 changes but conditions on papers receiving at least one English-language citation because all-zero targets do not identify the conditional model. Other Poisson specifications are less precise; journal-by-cohort and publication-year-by-cohort models retain positive C2 estimates but do not reproduce statistically significant C3 or C4 interactions. The central finding should therefore remain tied to the incidence model and the pre-2005 restriction rather than generalized across all functional forms.

The secondary access analysis does not provide an independent confirmation. Among currently visible papers, full-text access through current Google Scholar links is not significantly associated with cohort-specific English-language citation incidence. Because the access variable is conditional on present Google Scholar visibility and is also measured only at the current observation point, the null result does not establish that access is generally irrelevant to scholarly use.

## 3.4 Interpretation

Study 1 supports a limited temporal association. Papers currently retrievable in Google Scholar differ in their historical English-language citation trajectories, with the visible–nonvisible gap expanding in C2 and C3 relative to the earliest cohort. The result survives a sample restriction that holds target composition constant across cohorts, but it does not continue in C4 and is less stable in alternative count models.

The 0.405- and 0.696-point estimates are additional changes in the visible–nonvisible gap relative to C1, not citation-probability levels. The central pattern is therefore concentrated widening in C2 and C3, followed by no detectable additional widening in C4—not a uniformly accelerating advantage across all periods.

The design cannot establish that Google Scholar visibility caused those citation differences. Current visibility may reflect later indexing, later web availability, or processes associated with earlier scholarly circulation. The appropriate conclusion is therefore that current exact-title visibility identifies papers whose English-language citation trajectories diverged during the period in which Google Scholar became widely used, not that historical indexing dates or causal effects have been recovered.


# 4. Study 2: Auditing Web-Enabled Generative Search

## 4.1 Benchmark and audit design

Study 2 evaluates two pre-specified 50-paper corpora covering five topics in Korean politics.

1. the Korean War;
2. South Korean economic development;
3. South Korean democratization;
4. the North Korean nuclear program; and
5. the Korean Wave.

Each topic was operationalized with three translation-equivalent Korean and English keywords. All three topic keywords were embedded in the prompt in the assigned query language so that the substantive scope remained comparable across language conditions.

| Topic | Korean keywords | English keywords |
|---|---|---|
| Korean War | 한국전쟁; 한국전쟁 발발; 한국전쟁 기원 | Korean War; Outbreak of the Korean War; Origins of the Korean War |
| South Korean economic development | 한국 경제발전; 한국 발전국가; 한국 수출주도 산업화 | South Korean Economic Development; Korean Developmental State; South Korean Export-Led Industrialization |
| South Korean democratization | 한국 민주화; 한국 민주화운동; 한국 시민사회 | South Korean Democratization; South Korean Democracy Movement; South Korean Civil Society |
| North Korean nuclear program | 북핵 문제; 북한 핵무기; 대북 확장억제 | North Korean Nuclear Program; North Korean Nuclear Weapons; Extended Deterrence against North Korea |
| Korean Wave | 한류; 케이팝; 한국 영화 | Korean Wave; K-pop; South Korean Cinema |

For each topic, the audit includes ten Korean-language papers selected using DBpia and KISS and ten English-language papers selected using Web of Science and Google Scholar. Candidate pools were ranked by citation count, and the ten highest-ranked overlapping papers were selected for each topic. The resulting 100 papers were fixed before the LLM audit. They form an evaluation set, not an exhaustive definition of all relevant scholarship.

The audit crosses three factors.

- Query language — English / Korean;
- Source instruction — general web / explicit instruction to search KCI, DBpia, or KISS;
- System — OpenAI `gpt-5.6-sol` / Perplexity `sonar-pro`.

Every prompt included the topic's three keywords and requested ten relevant scholarly publications in a fixed JSON schema. Search activity was capped at two searches per keyword and six searches per execution. Five topics × four prompt conditions × two systems × five independent repetitions yield 200 stateless executions. The audit produces 1,932 valid recommendation occurrences.

For benchmark paper $j$ in execution $i$.

- TraceRecovery = 1 when the paper appears in the provider's observable search trace;
- Recommendation = 1 when the paper appears in the final recommendation;
- SuppliedLinkAccess = 1 when the benchmark paper is recommended and the provided URL opens the full text without payment or login.

The benchmark panel contains 4,000 paper × execution observations, comprising 200 executions × 20 topic-relevant benchmark papers. `SuppliedLinkAccess` in this panel is a joint pipeline-survival outcome because the denominator remains all benchmark-paper × execution pairs.

The study separately measures Korean-language representation, defined as the Korean-language share of valid recommendations. This is not a recall measure. Recommendation language is resolved for all 1,932 recommendation occurrences. Search-trace language representation is not compared across systems because provider-level trace observability differs substantially.

Finally, all 927 distinct supplied URLs or no-URL item keys are manually reviewed and classified as accessible full text, abstract only, paywalled, broken link, or hallucinated/unverifiable publication. This coding evaluates the supplied link, not whether another usable copy exists elsewhere.

## 4.2 Baseline recovery

Under the English-language general-web baseline, recovery is low for both corpora but lower for the Korean benchmark.

| Stage | English benchmark | Korean corpus | Korean gap | 95% CI | $p$ |
|---|---:|---:|---:|---:|---:|
| Observable search trace | 3.4% | 0.0% | −3.4 pp | [−6.46, −0.34] | .029 |
| Final recommendation | 3.2% | 0.0% | −3.2 pp | [−5.77, −0.63] | .015 |
| Accessible supplied link | 0.6% | 0.0% | −0.6 pp | [−1.76, 0.56] | .311 |

The first two differences are statistically distinguishable from zero. The provided-link comparison is not, but this reflects a severe floor because almost no benchmark item from either language reaches the final access stage. Across all experimental conditions, none of the pre-specified Korean papers survives through an accessible provided link.

The baseline therefore shows two things simultaneously. First, these systems are not high-recall bibliographic tools for either corpus. Second, within that low-recall environment, the Korean benchmark has an additional deficit under the default English general-web condition.

## 4.3 Effects of query language and Korean-database instruction

Both interventions narrow the Korean–English recovery gap at the observable search stage. A Korean query changes the gap by +3.8 percentage points (95% CI [0.72, 6.88], $p=.016$), and the Korean-database instruction changes it by +4.0 points (95% CI [0.73, 7.27], $p=.017$). At final recommendation, the database instruction changes the gap by +3.2 points (95% CI [0.71, 5.69], $p=.012$); the Korean-query estimate is +2.6 points and less precise ($p=.068$).

The three-way interaction testing departure from additivity is not distinguishable from zero. The more interpretable full combined-condition contrast is larger. Applying both a Korean query and a Korean-database instruction changes the Korean–English gap relative to baseline by +5.6 points at discovery and +6.4 points at recommendation.

Under the combined condition, 2.2% of Korean benchmark papers are recovered in observable traces and 3.2% are included in final recommendations, compared with zero English benchmark recovery in that condition. This is a reversal of the *relative* gap, not high absolute recovery. More than 96% of Korean benchmark-paper opportunities remain unrecovered in a given execution.

## 4.4 Representation is not benchmark recovery

Prompting changes the language composition of final recommendations much more than it changes benchmark recovery.

| Prompt condition | Korean-language share of recommendations |
|---|---:|
| English + general web | 0.0% |
| English + Korean DB instruction | 35.3% |
| Korean + general web | 55.8% |
| Korean + Korean DB instruction | 91.2% |

Among recommendations whose supplied links are accessible, the corresponding Korean-language shares are 0.0%, 26.6%, 57.5%, and 94.9%.

The regression estimates confirm these large compositional shifts. Korean queries increase the Korean-language recommendation share by 55.7 percentage points ($p<.001$), and Korean-database instructions increase it by 35.4 points ($p<.001$). Yet under the combined condition, recommendation recovery of the pre-specified Korean benchmark is only 3.2% per paper-execution opportunity.

The distinction is therefore methodological as well as substantive. A locally oriented reading list is not evidence of high recovery of known local scholarship. The non-benchmark Korean recommendations may be relevant; the audit does not classify them as irrelevant. The point is that language representation and benchmark recovery measure different properties of the output.

## 4.5 What happens at the supplied link?

Across all 1,932 recommendation occurrences.

- 854 (44.2%) provide accessible full text;
- 859 (44.5%) are access-restricted, including 247 abstract-only and 612 paywalled links;
- 219 (11.3%) are invalid or unverifiable, including 176 broken links and 43 coded hallucinated publications.

The occurrence-weighted hallucination rate is therefore 2.2%, distinct from the 9.1% broken-link rate.

| Supplied-link outcome | Overall | Korean-language item | English-language item |
|---|---:|---:|---:|
| Accessible | 44.2% | 46.3% | 42.4% |
| Access restricted | 44.5% | 47.9% | 41.6% |
| Invalid or unverifiable | 11.3% | 5.8% | 16.0% |
| — Broken link | 9.1% | 3.3% | 14.1% |
| — Hallucinated item | 2.2% | 2.6% | 1.9% |

After controlling for prompt condition and system, recommended-item language is not independently associated with full access, access restriction, or invalid/unverifiable status. The raw language differences therefore describe the mix of outputs generated under the experiment rather than an effect of publication language.

System differences are secondary but visible. Conditional on recommended-item language and prompt factors, Perplexity is estimated to be 8.2 percentage points more likely than OpenAI to provide an accessible link ($p=.065$), 15.3 points less likely to provide an access-restricted link ($p<.001$), and 7.2 points more likely to produce an invalid or unverifiable result ($p=.017$). Its coded hallucination probability is 4.0 points higher ($p=.017$), but 39 of Perplexity's 40 hallucination occurrences come from a single English-query/Korean-database cell, so this sparse result should not be generalized beyond the audit.

## 4.6 Interpretation

Study 2 locates a default Korean benchmark deficit at the observable search and recommendation stages. Query-language and database instructions can narrow or reverse the relative gap, but they do not produce high absolute recovery. The same interventions are far more effective at changing the language composition of the list.

Under the combined condition, the relative gap reverses, yet Korean benchmark recovery remains only 2.2% in search and 3.2% in final recommendations. Relative improvement and a substantial absolute discovery bottleneck therefore coexist. Because search traces include only what each provider exposes, trace recovery should not be interpreted as complete observation of internal retrieval.

The link audit identifies a separate downstream limitation because fewer than half of recommendations provide immediate full-text access through the URL the system itself supplies. This result concerns the user pathway created by the system, not the publication's availability elsewhere on the web.


# 5. Combined Discussion

## 5.1 What the two studies jointly show

The two studies converge on one limited point. Local scholarly use does not guarantee equivalent visibility in the search environments examined here. Study 1 begins with Korean-language papers already cited in Korean scholarship. Study 2 begins with Korean papers fixed before the audit from Korean scholarly databases. In both cases, the analysis asks what happens when these papers meet a search system used to identify literature.

The evidence differs by study. In Google Scholar, current exact-title retrievability partitions a large corpus of locally cited papers into groups with different historical English-language citation trajectories. The gap expands in 2010–2014 and 2015–2019 relative to the earliest cohort, but not in 2020–2024. In generative search, the default English general-web condition produces a directly observed Korean benchmark deficit in contemporary retrieval and recommendation, although overall recovery is low for English papers as well.

As Figure 1 shows, Study 1's widening is concentrated in C2 and C3 and is absent in C4. In Study 2, the baseline Korean deficit reverses under the combined search condition, but absolute recovery remains low; even when Korean-language publications constitute 91.2% of recommendations, Korean benchmark recommendation recovery is only 3.2%.

![Study 1 Google Scholar visibility and Study 2 generative-search results](combined_analysis/figures/discovery_bottleneck_combined_simple.png){width=100%}

Together, these results support a search-mediated visibility interpretation without requiring a single causal mechanism. Search environments can place the same broad category of local scholarship into different observable states. Papers may be retrievable or not; recovered in a trace or not; selected for the final answer or not; linked to accessible full text or not.

## 5.2 Established and emerging discovery environments

The distinction between the two search environments is important. Google Scholar is an established scholarly search tool with documented use among social scientists (Blankstein 2022). Study 1 can therefore relate current paper-level visibility to historical citation trajectories during the period of Google Scholar's diffusion, although it cannot reconstruct historical index status.

Web-enabled LLM search is newer. Existing research shows growing experimentation with LLMs for literature search but also limited validation (Lieberum et al. 2025). Study 2 consequently makes a different claim. It directly audits current behavior under controlled search conditions. It does not infer that LLMs already dominate political-science literature search or that present recommendations have produced later citation outcomes.

This difference prevents a misleading historical narrative. The C4 result in Study 1 should not be interpreted as evidence about generative search. The 2020–2024 cohort contains limited post-LLM time and substantial citation lag. Study 2, rather than C4, provides the direct evidence about current generative-search behavior.

## 5.3 Retrieval, representation, and access are different outcomes

The combined analysis also clarifies three concepts that are often collapsed.

First, retrieval is not representation. Study 2 shows this most clearly. A prompt condition can produce 91.2% Korean-language recommendations while recovering only 3.2% of pre-specified Korean benchmark opportunities. A linguistically localized output does not establish that known local scholarship has been recovered.

Second, retrieval or recommendation is not the same as access through the provided link. Google Scholar can retrieve a paper without providing an open full-text link; a generative-search system can recommend the correct paper but link only to an abstract, a paywall, or a broken page. This paper therefore evaluates the route provided in the search result rather than treating general OA status as equivalent to user-facing access.

Third, the two studies do not show the same relationship between access and the main outcome. In Study 1, present full-text access through Google Scholar links does not independently track cohort-specific English citation incidence among visible papers. In Study 2, access is not a later citation outcome at all; it is a directly observed property of the recommendation pathway. The combined paper therefore does not claim a general access-to-citation effect.

## 5.4 Implications for political science

The political-science implication is narrower than a claim that search technology determines disciplinary knowledge. Existing work already documents geographic and institutional concentration in political science publishing and research coverage (Breuning et al. 2018; Wilson and Knutsen 2022). The present studies identify an additional empirical location where unequal visibility can be observed in the systems through which literature is searched and presented.

Search environments do not determine scholarly value, but they help structure which publications enter the candidate set for evaluation. The political-science significance of discovery bottlenecks therefore lies not in the language composition of an output alone, but in whether concrete publications accumulated in a local scholarly sphere become available for substantive consideration.

For research on a country such as South Korea, this matters because a substantial part of the relevant scholarly record is produced in Korean and circulates through Korean journals and databases. If evaluation of international visibility considers only what appears in major English-language outlets or in a generated reading list, it can miss the distinction between the local literature that exists and the subset that a particular search environment returns.

The Study 2 representation result is especially important for evaluating AI-mediated political knowledge. A response can appear highly localized because most of its references are Korean-language, while still recovering very little of a pre-specified Korean benchmark. Audits of multilingual scholarly search should therefore report recovery against an external local-language benchmark rather than only the language composition of the answer.

## 5.5 Practical and research implications

The empirical results do not test specific infrastructure reforms, so policy implications should remain modest. Two evaluation practices follow directly from the measurement results.

First, scholarly search systems should be assessed against pre-specified local-language corpora when claims concern multilingual or regional coverage. Output composition alone is not sufficient to measure recovery.

Second, evaluations should distinguish bibliographic retrieval from the usability of the supplied link. A correct citation paired with an inaccessible or broken URL creates a different user pathway from a correct citation paired with immediate full text.

Future work can extend both dimensions longitudinally. Repeated Google Scholar observations could identify actual changes in paper-level visibility and supplied links, while repeated LLM audits could determine whether retrieval patterns persist as models, search indexes, and provider interfaces change.


# 6. Conclusion

This paper examines international visibility of Korean political science in two scholarly search environments rather than treating publication language or citation counts as the entire process.

Study 1 shows that among 54,789 Korean-language papers already used in Korean scholarship, current exact-title Google Scholar visibility is associated with different historical English-language citation trajectories. Relative to 2009 or earlier, the visible–nonvisible citation gap increases in 2010–2014 and 2015–2019, including among papers published before Google Scholar, but does not expand further in 2020–2024. The evidence is not fully stable across count specifications, and present full-text access through Google Scholar links does not independently reproduce the citation pattern. The result is therefore an association between current retrievability and historical citation trajectories, not a causal estimate of Google Scholar indexing or access.

Study 2 directly audits contemporary web-enabled generative search. Under the English general-web baseline, the Korean benchmark is absent from both observable search traces and final recommendations, while English benchmark recovery is low but nonzero. Korean queries and explicit Korean-database instructions narrow the relative recovery gap, yet absolute recovery remains very low. These interventions change representation much more strongly. The combined condition produces 91.2% Korean-language recommendations while recovering only 3.2% of Korean benchmark opportunities. Among all recommendations, only 44.2% of provided links open full text directly; 44.5% are access-restricted and 11.3% are broken or unverifiable.

The combined inference is deliberately limited. The studies do not show that a single discovery mechanism causes international citation inequality. They show that locally used Korean political science is unevenly represented at observable points in scholarly search, including bibliographic retrievability, final source selection, and provided-link access. Those distinctions matter for how international visibility is measured. A paper can exist without being retrieved; a recommendation list can look locally representative without recovering known local work; and a correct recommendation can still provide an unusable route to the text.

For political science, this locates part of the international-visibility problem in the practical environments through which scholars now encounter literature—an established academic search engine and an emerging generative-search interface—without reducing the broader problem of disciplinary inequality to technology alone.


# 7. Limitations

Study 1 has a fundamental temporal limitation. Google Scholar retrievability and full-text access through its links are observed in 2026. The analysis does not observe the year in which each paper entered Google Scholar or when a full-text link first became available. Current visibility may also be endogenous to prior circulation. Papers with greater scholarly use may subsequently become easier to index or find. Target fixed effects remove stable paper differences but do not establish temporal precedence.

The Google Scholar measure is also subject to bibliographic matching error. Searches used Korean and English titles and reference-title variants, but misspelled metadata, title variation, duplicate records, or incomplete indexing could still produce false negatives or incorrect matches. The indicator therefore records current visibility under this study's search and matching protocol, not complete Google Scholar coverage.

Study 1 is also model-dependent. The main incidence model and the pre-2005 restriction show C2–C3 divergence, but several Poisson specifications are less precise. The result should therefore not be described as invariant across outcomes or functional forms. The current full-text access analysis is additionally conditional on Google Scholar visibility and yields no statistically significant association with cohort-specific citation incidence.

Study 2 covers two systems, five topics, one collection period, and 100 pre-specified papers. Its benchmark is an evaluation set, not an exhaustive definition of relevant literature. Recovery events are sparse, especially at the accessible-link stage. Provider-level trace observability differs, so language representation in observable search traces cannot be compared symmetrically across systems.

Benchmark construction also favors papers that rank highly by citation count and overlap across two bibliographic sources. This creates a stable evaluation set of comparatively visible publications, but may underrepresent recent, low-cited, or specialized work. The reported recovery rates are therefore recall against the pre-specified benchmark, not recall for Korean political science as a whole.

The Study 2 link audit evaluates the URL supplied by the system. An abstract-only, paywalled, or broken link does not establish that the paper is unavailable elsewhere. Hallucination events are also sparse and unevenly distributed across experimental cells, limiting generalization of system-level differences.

Finally, neither study observes what researchers do after encountering a paper. Reading, substantive relevance, perceived quality, language competence, citation norms, collaboration networks, and publication venue can all influence later use and citation. The evidence concerns search-mediated visibility and access, not the full process by which political-science knowledge travels internationally.


[^1]: An earlier version of Kim et al. (2025) was presented at the 28th IPSA World Congress of Political Science (Seoul, July 12–16, 2025). The revised manuscript is under review at *Humanities and Social Sciences Communications* following a revise-and-resubmit decision.

# References

Ajith, Anirudh, Mengzhou Xia, Alexis Chevalier, Tanya Goyal, Danqi Chen, and Tianyu Gao. 2024. “LitSearch: A Retrieval Benchmark for Scientific Literature Search.” In *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing*, 15068–15083. https://doi.org/10.18653/v1/2024.emnlp-main.840.

Asai, Akari, Jacqueline He, Rulin Shao, et al. 2026. “Synthesizing Scientific Literature with Retrieval-Augmented Language Models.” *Nature* 650: 857–863. https://doi.org/10.1038/s41586-025-10072-4.

Azzopardi, Leif, and Vishwa Vinay. 2008. “Retrievability: An Evaluation Measure for Higher Order Information Access Tasks.” In *Proceedings of the 17th ACM Conference on Information and Knowledge Management*, 561–570. https://doi.org/10.1145/1458082.1458157.

Blankstein, Melissa. 2022. *Ithaka S+R US Faculty Survey 2021*. Ithaka S+R. https://doi.org/10.18665/sr.316896.

Breuning, Marijke, Ayal Feinberg, Benjamin Isaak Gross, Melissa Martinez, Ramesh Sharma, and John Ishiyama. 2018. “How International Is Political Science? Patterns of Submission and Publication in the American Political Science Review.” *PS: Political Science & Politics* 51(4): 789–798. https://doi.org/10.1017/S1049096518000963.

Chen, Xiaotian. 2010. “Google Scholar’s Dramatic Coverage Improvement Five Years after Debut.” *Serials Review* 36(4): 221–226. https://doi.org/10.1016/j.serrev.2010.08.002.

Cothran, Tanya. 2011. “Google Scholar Acceptance and Use among Graduate Students: A Quantitative Study.” *Library & Information Science Research* 33(4): 293–301. https://doi.org/10.1016/j.lisr.2011.02.001.

Delgado-Quirós, Lorena, Isidro F. Aguillo, Alberto Martín-Martín, Emilio Delgado López-Cózar, Enrique Orduña-Malea, and José Luis Ortega. 2024. “Why Are These Publications Missing? Uncovering the Reasons behind the Exclusion of Documents in Free-Access Scholarly Databases.” *Journal of the Association for Information Science and Technology* 75(1): 43–58. https://doi.org/10.1002/asi.24839.

Di Bitetti, Mario S., and Julián A. Ferreras. 2017. “Publish (in English) or Perish: The Effect on Citation Rate of Using Languages Other than English in Scientific Publications.” *Ambio* 46(1): 121–127. https://doi.org/10.1007/s13280-016-0820-7.

Espín-Noboa, Lisette, and Gonzalo G. Méndez. 2026. “Whose Name Comes Up? II: Benchmarking and Intervention-Based Auditing of LLM-Based Scholar Recommendation.” In *Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining*. https://doi.org/10.1145/3770855.3817543.

He, Yichen, Guanhua Huang, Peiyuan Feng, Yuan Lin, Yuchen Zhang, Hang Li, and Weinan E. 2025. “PaSa: An LLM Agent for Comprehensive Academic Paper Search.” In *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics*, 11663–11679. https://doi.org/10.18653/v1/2025.acl-long.572.

Jamali, Hamid R., and Saeid Asadi. 2010. “Google and the Scholar: The Role of Google in Scientists’ Information-Seeking Behaviour.” *Online Information Review* 34(2): 282–294. https://doi.org/10.1108/14684521011036990.

Jamali, Hamid R., and Majid Nabavi. 2015. “Open Access and Sources of Full-Text Articles in Google Scholar in Different Subject Fields.” *Scientometrics* 105(3): 1635–1651. https://doi.org/10.1007/s11192-015-1642-2.

Kim, Do Won, Hyowon Kim, and Won-ho Park. 2025. “Two Spheres of Korean Politics: Knowledge Production and Dissemination across Linguistic Divides.” Revised manuscript under review at *Humanities and Social Sciences Communications*.

Li, Alice, and Luanne Sinnamon. 2024. “Generative AI Search Engines as Arbiters of Public Knowledge: An Audit of Bias and Authority.” *Proceedings of the Association for Information Science and Technology* 61(1): 205–217. https://doi.org/10.1002/pra2.1021.

Lieberum, Judith-Lisa, Markus Töws, Maria-Inti Metzendorf, Felix Heilmeyer, Waldemar Siemens, Christian Haverkamp, Daniel Böhringer, Joerg J. Meerpohl, and Angelika Eisele-Metzger. 2025. “Large Language Models for Conducting Systematic Reviews: On the Rise, but Not Yet Ready for Use—A Scoping Review.” *Journal of Clinical Epidemiology* 181: 111746. https://doi.org/10.1016/j.jclinepi.2025.111746.

Liu, Nelson F., Tianyi Zhang, and Percy Liang. 2023. “Evaluating Verifiability in Generative Search Engines.” In *Findings of the Association for Computational Linguistics: EMNLP 2023*, 7001–7025. https://doi.org/10.18653/v1/2023.findings-emnlp.467.

Manning, Christopher D., Prabhakar Raghavan, and Hinrich Schütze. 2008. *Introduction to Information Retrieval*. Cambridge: Cambridge University Press.

Martín-Martín, Alberto, Rodrigo Costas, Thed N. van Leeuwen, and Emilio Delgado López-Cózar. 2018a. “Evidence of Open Access of Scientific Publications in Google Scholar: A Large-Scale Analysis.” *Journal of Informetrics* 12(3): 819–841. https://doi.org/10.1016/j.joi.2018.06.012.

Martín-Martín, Alberto, Enrique Orduna-Malea, Mike Thelwall, and Emilio Delgado López-Cózar. 2018b. “Google Scholar, Web of Science, and Scopus: A Systematic Comparison of Citations in 252 Subject Categories.” *Journal of Informetrics* 12(4): 1160–1177. https://doi.org/10.1016/j.joi.2018.09.002.

Martín-Martín, Alberto, Mike Thelwall, Enrique Orduña-Malea, and Emilio Delgado López-Cózar. 2021. “Google Scholar, Microsoft Academic, Scopus, Dimensions, Web of Science, and OpenCitations’ COCI: A Multidisciplinary Comparison of Coverage via Citations.” *Scientometrics* 126(1): 871–906. https://doi.org/10.1007/s11192-020-03690-4.

Mongeon, Philippe, and Adèle Paul-Hus. 2016. “The Journal Coverage of Web of Science and Scopus: A Comparative Analysis.” *Scientometrics* 106: 213–228. https://doi.org/10.1007/s11192-015-1765-5.

Rhee, Inbok. 2026. “한국 정치학 연구의 현황과 특성: 2015–2024 [The State of Political Science Research in South Korea: 2015–2024].” *Korean Political Science Review* 60(1): 5–91. https://doi.org/10.18854/kpsr.2026.60.1.001.

Vera-Baceta, Miguel-Angel, Michael Thelwall, and Kayvan Kousha. 2019. “Web of Science and Scopus Language Coverage.” *Scientometrics* 121(3): 1803–1813. https://doi.org/10.1007/s11192-019-03264-z.

Wilson, Matthew Charles, and Carl Henrik Knutsen. 2022. “Geographical Coverage in Political Science Research.” *Perspectives on Politics* 20(3): 1024–1039. https://doi.org/10.1017/S1537592720002509.
