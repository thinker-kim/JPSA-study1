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

This paper argues that the international visibility of Korean-politics research must be analyzed not only through publication and citation but also through which publications actually appear as reviewable candidates in scholarly search. Research on Korean politics is produced and circulated in distinct Korean- and English-language scholarly spheres, and the scholarship accumulated in the two spheres is neither discovered nor cited internationally to the same extent (Rhee 2026; Kim et al. 2025). We analyze how studies already used or identified as important in the Korean-language sphere become visible in Google Scholar and generative search, while treating full-text access through links supplied by the search environment as a separate outcome.

Study 1 analyzes 54,789 Korean-politics papers cited by Korean-language political science articles published from 2000 to 2025, examining the relationship between Google Scholar index presence as of 2026 and English-language citation probability across periods. Compared with the baseline period through 2009, the English-language citation-probability gap between papers whose bibliographic records are currently confirmed and those whose records are not was significantly larger by 0.405 percentage points (pp) in 2010–2014 and 0.696 pp in 2015–2019, but did not widen further in 2020–2024. Among papers with confirmed index presence, full-text access through links currently supplied by Google Scholar was not significantly associated with English-language citation probability. This is an association between current index presence and historical English-language citation trajectories, not a causal effect of Google Scholar.

Study 2 audits two web-enabled generative search systems using 50 preselected Korean-language and 50 English-language papers across five Korean-politics topics studied in both scholarly spheres. Under the English-query, general-web baseline, no Korean benchmark paper was recovered in either the observable search trace or the final recommendations, whereas English benchmark recovery was 3.4% and 3.2%, respectively. Combining a Korean query with an instruction to search Korean scholarly databases narrowed the Korean–English gap by 5.6 pp at search and 6.4 pp at recommendation, yet Korean benchmark recovery in final recommendations remained only 3.2%. Only 44.2% of all recommendations provided direct full-text access through the accompanying link, and no significant language gap was found in access.

The shared conclusion is that the linguistic composition of search results must be distinguished from the recovery of major publications within a particular scholarly sphere. A large number of Korean-language recommendations in generative search does not establish that the major scholarship accumulated in Korean is represented to a corresponding degree. We introduce discovery bottleneck as an operational concept for the loss of visibility at observable stages of search or final source selection before a publication receives substantive evaluation.

Keywords: Korean political science; Korean-politics research; scholarly search; Google Scholar; generative search; non-English-language scholarship; international visibility; full-text access; discovery bottleneck

# 1. Introduction

The central argument of this paper is that the international visibility of Korean-politics research cannot be understood through publication and citation alone. The search stage at which publications become candidates for review and are selected as final sources is a separate visibility outcome. If relevant work does not appear in search results, researchers may exclude it from consideration before they can assess its content.

This problem matters because the international distribution of political science knowledge is already uneven by region and language. The countries and regions studied in leading political science journals have long been concentrated in North America and Western Europe, while international publishing exhibits inequalities associated with researchers' geographic and institutional locations (Wilson and Knutsen 2022; Breuning et al. 2018). Major international scholarly databases also disproportionately cover English-language journals, and non-English publications tend to be disadvantaged in international citation relative to English-language work (Mongeon and Paul-Hus 2016; Vera-Baceta, Thelwall, and Kousha 2019; Di Bitetti and Ferreras 2017).

Research on Korean politics provides a useful case for analyzing this segmentation. Research circulating around KCI and SSCI in Korean political science differs in topical and methodological patterns (Rhee 2026), while Korean- and English-language research on Korean politics also forms distinct scholarly spheres in production, circulation, and international citation reach (Kim et al. 2025).[^1] The accumulation of substantial Korean-language scholarship therefore does not by itself imply that this work will be discovered and reviewed to the same extent in international scholarly environments.

This paper analyzes the problem by separating scholarly existence from search visibility. A paper's existence as a publication or its inclusion in a database's aggregate coverage is not the same as its appearance for review in a particular search environment. Information-retrieval research distinguishes database-level coverage from document-level retrievability for this reason (Azzopardi and Vinay 2008). Full-text access is another outcome. A retrieved paper may lead to a paywall, an abstract page, or a broken link, while a paywalled publisher version may coexist with a repository or author-hosted copy (Jamali and Nabavi 2015). We measure whether the link actually supplied by each environment opens the full text without login or payment, not a paper's general OA status.

Study 1 analyzes the relationship between current Google Scholar index presence and English-language citation across periods. The analysis includes 54,789 Korean-politics publications cited at least once by Korean-language political science articles produced between 2000 and 2025. Holding constant the common condition of actual use in the Korean-language sphere, it compares the English-language citation-probability gap between papers with and without a currently confirmed bibliographic record. Because Google Scholar status is observed only in 2026, the analysis does not estimate whether historical indexing caused English-language citation.

Study 2 distinguishes search from final source selection in generative search. A web-enabled system retrieves external material and selects only some sources as citations or recommendations when composing an answer (Liu, Zhang, and Liang 2023; He et al. 2025). Holding constant Korean-politics topics studied in both language spheres, Study 2 varies query language and instructions to search Korean scholarly databases. It compares whether pre-specified Korean and English benchmarks appear in the disclosed search trace and final recommendations. It also distinguishes the Korean-language share of all recommendations from recovery of the pre-specified Korean benchmark.

The two studies do not form a single causal sequence from search to full-text access to citation. Study 1 shows a relationship between current Google Scholar index presence and historical English-language citation trajectories. Study 2 directly observes retrieval and selection in current generative search. Their shared question is which publications among those that exist and are actually used in the Korean-language sphere appear as reviewable candidates in search environments used internationally.

We use discovery bottleneck to refer to a loss of visibility in search or final source selection before a publication reaches substantive evaluation. The concept does not claim that search technology alone generates international citation inequality. It is an operational label for observable omission within a particular search environment.

The remainder of the paper proceeds as follows. Section 2 connects research on international knowledge inequality to scholarly discovery and identifies the analytical stages that must be distinguished in Google Scholar and generative search. Sections 3 and 4 report the design and results of Studies 1 and 2. Section 5 separates their shared implications from claims that the evidence cannot support. Sections 6 and 7 present the conclusion and limitations.

# 2. Prior Research

## 2.1 International visibility in political science and linguistic scholarly spheres

The starting point of this section is that internationally observable political science is not identical to the full body of research produced across regions and languages. Entry into and circulation within central scholarly spaces have been unevenly structured by research subject, researcher location, and publication language.

On the subject side, major political science journals have historically concentrated on North America and Western Europe. This imbalance bears on the scope over which descriptive and causal claims developed in particular regions are generalized to political science as a whole (Wilson and Knutsen 2022). On the producer side, scholars from the Global South are underrepresented in leading international political science journals, while researchers affiliated with certain institutions are overrepresented (Breuning et al. 2018).

Publication language and bibliographic infrastructure provide another selection mechanism. Web of Science and Scopus disproportionately cover English-language journals relative to the broader journal population (Mongeon and Paul-Hus 2016; Vera-Baceta, Thelwall, and Kousha 2019). Even in multilingual publishing environments, non-English articles receive lower citation rates than English-language articles after other publication characteristics are taken into account (Di Bitetti and Ferreras 2017). Database coverage and citation visibility may therefore be selectively structured by language.

This segmentation also appears in Korean-politics research. Research published in KCI and SSCI venues differs in topical and methodological composition (Rhee 2026), while Korean- and English-language research on Korean politics exhibits different patterns of international recognition and citation reach (Kim et al. 2025). The resulting question is not simply a citation difference by language. It is whether particular studies accumulated in the Korean-language sphere on the same political phenomena become reviewable in international scholarly-information environments.

Existing research documents inequalities in publication, database coverage, and citation, but literature discovery is a separate level of analysis. Information-retrieval research distinguishes database-level coverage from document-level retrievability (Azzopardi and Vinay 2008). We use this distinction as the conceptual basis for the proposition that aggregate coverage cannot determine the search visibility of an individual publication.

## 2.2 Google Scholar coverage, index presence, and full-text access

The key distinction for Google Scholar is that broad aggregate coverage does not guarantee every individual paper's index presence or full-text access. Study 1 separates these three properties and focuses on paper-level index presence among publications actually used in the Korean-language sphere.

Google Scholar captures a wider range of publications and citations than Web of Science and Scopus, including substantial numbers of non-English and non-journal materials (Chen 2010; Martín-Martín et al. 2018b, 2021). This coverage matters for non-English scholarship because research insufficiently captured in selective international citation indexes may nevertheless be found in Google Scholar.

External bibliographic comparisons nevertheless identify publications not returned by Google Scholar (Delgado-Quirós et al. 2024). Broad coverage of a language or field and confirmation of an individual paper's bibliographic record are therefore analytically different properties.

Paper-level index presence matters because Google Scholar is widely used in actual scholarly discovery. Studies repeatedly document the use of Google and Google Scholar by researchers and graduate students (Jamali and Asadi 2010; Cothran 2011), and a recent faculty survey identifies Google Scholar as a major starting point for social scientists searching for new literature (Blankstein 2022). This use does not mean that index presence generates citation, but it establishes index presence as an observable property in an environment where literature search takes place.

Full-text access must again be separated from index presence. Google Scholar may link to versions found on publisher sites, in repositories, and elsewhere on the web, and supplies free full-text links for a substantial share of the literature (Jamali and Nabavi 2015; Martín-Martín et al. 2018a). Yet an indexed paper may lead only to a paywall or abstract page, while a free web version may exist without being presented by Google Scholar.

Study 1 consequently does not re-estimate Google Scholar's overall coverage. Within a common set of publications with Korean-language citation records, it compares historical English-language citation patterns between groups with and without confirmed current index presence. Full-text access through the supplied link is analyzed as a secondary outcome.

## 2.3 Generative scholarly search and publication selection

The defining feature of generative search is that final source selection follows retrieval. A web-enabled LLM does not return all retrieved material. It selects some items as citations or recommendations when composing an answer. Whether a publication appears in a disclosed search trace and whether it is ultimately presented as a source must therefore be separated (Liu, Zhang, and Liang 2023).

Recent work on scholarly search increasingly evaluates whether pre-specified publications are actually recovered rather than judging the surface plausibility of a generated list. LitSearch defines target papers independently of the tested system (Ajith et al. 2024), while academic-search agents such as PaSa use query–paper benchmarks (He et al. 2025). This follows the information-retrieval tradition of assessing performance against a predefined relevant set (Manning, Raghavan, and Schütze 2008). Audits of LLM-based scholar recommendation similarly use external benchmarks to measure whether pre-specified scholars or publications are recommended (Espín-Noboa and Méndez 2026). Although LLM-assisted literature search is expanding quickly, it is not yet fully established for rigorous processes such as systematic reviews (Lieberum et al. 2025; Asai et al. 2026).

An external benchmark is particularly important for evaluating non-English scholarship. The presence of many Korean-language papers in a result does not establish adequate representation of major research from the Korean-language sphere. A system may recommend many Korean publications while including few of the particular studies treated as important in Korean political science. The linguistic composition of final recommendations and recovery of a pre-specified Korean benchmark therefore answer different questions.

Search conditions are also analytically important. Generative-search results may differ by source authority, geography, and institutional or commercial source type (Liu, Zhang, and Liang 2023; Li and Sinnamon 2024). When Korean- and English-language publications circulate through different databases and publishing channels, query language and instructions to search Korean scholarly sources may change both the literature retrieved and the sources ultimately presented.

Study 2 operationalizes this argument through three observable outcomes. First, it measures whether a benchmark paper appears in the provider's disclosed search trace. Second, it measures whether the publication appears in the final recommendations. Third, it measures whether the supplied link opens the full text without login or payment. The trace does not reveal the provider's entire internal retrieval process, but these outcomes separate observable search, final selection, and supplied-link access.

# 3. Study 1: Google Scholar Index Presence and English-Language Citation

## 3.1 Data and variables

Study 1 analyzes how the English-language citation-probability gap between Korean-politics publications with and without currently confirmed Google Scholar index presence varies over time, among publications already used in Korean-language political science.

The analysis includes 54,789 Korean-politics publications cited by Korean-language political science articles produced between 2000 and 2025. To enter the sample, a target must have been cited at least once in Korean-language political science during this period. The sample therefore contains both publications cited only in the Korean-language sphere and those cited in both the Korean- and English-language spheres.

English-language citation is constructed as cohort-specific incidence rather than a single cumulative citation count.

* C1: through 2009
* C2: 2010–2014
* C3: 2015–2019
* C4: 2020–2024

C1 is the baseline against which later cohorts are compared; it does not represent a search environment predating Google Scholar. Equal five-year intervals are used from 2010 onward.

A target paper is included only in cohorts in which it had a temporal opportunity to be cited. For target \(j\) and cohort \(c\),

$$
Y_{jc}=1
$$

if at least one English-language source paper cited the target during that period, and 0 otherwise. The final panel contains 179,230 target-paper × cohort observations.

The main variable \(D_j\) indicates Google Scholar index presence as of 2026. We searched plausible Korean and English titles and reference-title variants. If a Google Scholar record satisfying predefined bibliographic matching criteria was confirmed, \(D_j=1\); if the search was completed without finding a verifiable matching record, \(D_j=0\). The sample includes 19,436 papers with \(D_j=1\) and 35,353 with \(D_j=0\).

Because Google Scholar does not publish a complete list of its index, index presence is operationalized as confirmation of a bibliographic record through this study's title-based search and matching procedure. Thus, \(D_j=0\) does not mean that the paper is absolutely absent from every possible Google Scholar search. It means that current index presence could not be confirmed under our search procedure.

The secondary variable, measured for papers with confirmed current Google Scholar records, indicates whether the link supplied by Google Scholar opens the full text without login or payment. It does not measure the paper's general OA status.

## 3.2 Empirical strategy

The main analysis tests whether the English-language citation-probability gap by current Google Scholar index presence differs across citation cohorts. The target-paper fixed-effects linear probability model is

$$
Y_{jc}=\alpha_j+\lambda_c+
\sum_{k=2}^{4}\beta_k
\left(D_j\times1[c=k]\right)
+\gamma AgeBin_{jc}+\epsilon_{jc}.
$$

The target fixed effect α_j absorbs time-invariant target-paper attributes, while the cohort fixed effect λ_c absorbs changes in citation incidence common to all targets in a period. Because \(D_j\) does not vary within a paper, its main effect is absorbed by the target fixed effect.

The key coefficient β_k indicates how much the English-language citation-probability gap between \(D=1\) and \(D=0\) papers in each later cohort differs from the gap in C1. It is not a causal effect of Google Scholar indexing; it is the period-specific difference in the gap between groups defined by current index presence. Standard errors are clustered at the target-paper level.

To assess changes in eligible-target composition across cohorts, we repeat the analysis only for target papers published through 2004. These papers had an opportunity to contribute to all four cohorts, reducing changes in cohort composition caused by the addition of later publications. This restriction does not reconstruct historical Google Scholar indexing status.

Additional robustness analyses use Poisson pseudo-maximum likelihood, citation-count outcomes, and additional journal, topic, and publication-year interactions with cohort.

## 3.3 Results

Papers with confirmed current Google Scholar index presence have higher raw English-language citation incidence than those without it in every cohort.

| Cohort | \(D=1\) | \(D=0\) | Raw difference |
| ------ | ------: | ------: | -------------: |
| C1     |   0.68% |   0.31% |       +0.37 pp |
| C2     |   1.90% |   0.67% |       +1.23 pp |
| C3     |   3.01% |   1.25% |       +1.76 pp |
| C4     |   2.66% |   1.38% |       +1.28 pp |

In the fixed-effects analysis, the gap between the two groups increases by 0.405 pp in C2 relative to C1 (95% CI [0.040, 0.770], \(p=.030\)). In C3, it increases by 0.696 pp (95% CI [0.329, 1.063], \(p<.001\)). The joint test of the C2 and C3 coefficients also yields \(p<.001\).

By contrast, the change in C4 is 0.008 pp (95% CI [−0.337, 0.353], \(p=.965\)), providing no evidence that the gap widened further in 2020–2024 relative to C1.

Restricting the analysis to targets published through 2004 also yields positive gap changes in C2 and C3.

| Change in \(D\) gap from C1 |       Full eligible sample |        Published through 2004 |
| --------------------------- | -------------------------: | ----------------------------: |
| C2                          | +0.405 pp [0.040, 0.770]   | +0.791 pp [0.227, 1.355]      |
| C3                          | +0.696 pp [0.329, 1.063]   | +0.496 pp [0.027, 0.964]      |
| C4                          | +0.008 pp [−0.337, 0.353]  | +0.273 pp [−0.175, 0.721]     |

In the pre-2005 sample, \(p=.006\) for C2 and \(p=.038\) for C3; the joint test for C2–C3 yields \(p=.011\). The C4 estimate is positive but statistically uncertain (\(p=.233\)).

The robustness results are not identical across all specifications. In target-fixed-effects Poisson models, the C2 and C3 changes are positive, but targets with no English-language citations do not identify the conditional model and are therefore excluded. Other Poisson specifications are less precise. In models with journal-by-cohort and publication-year-by-cohort controls, the positive C2 estimate remains, but C3 and C4 are not reproduced as statistically significant. The findings should therefore be interpreted within the scope of the C2–C3 pattern found in the main incidence model and pre-2005 restriction.

Among papers with a confirmed current Google Scholar record, full-text access through the link supplied by Google Scholar is not statistically significantly associated with cohort-specific English-language citation incidence.

## 3.4 Interpretation

The central result of Study 1 is that current Google Scholar index presence separates groups of papers with different historical English-language citation trajectories. The citation-probability gap between the two groups is larger in C2 and C3 than in C1, and the same direction appears among pre-2005 targets. The gap does not widen further in C4, however, and some alternative specifications are less precise. The observed pattern should therefore be interpreted as specific to C2 and C3.

The estimates of 0.405 pp and 0.696 pp are not citation probabilities. They are additional changes in the group gap relative to C1. The results do not indicate an advantage that expands continuously across every period.

Causal interpretation is also limited. Because Google Scholar status is observed only in 2026, current index presence cannot be said to have caused historical citation. A current record may reflect subsequent indexing, web availability, prior scholarly circulation, or other characteristics that changed with these factors. The most limited conclusion supported by Study 1 is that historical English-language citation trajectories differ by current index presence.

# 4. Study 2: Auditing Web-Enabled Generative Search

## 4.1 Benchmark and audit design

Study 2 analyzes the extent to which major Korean- and English-language publications on the same Korean-politics topics are searched and presented as final sources in generative search, and whether the difference changes across search conditions.

The comparison set was fixed as a benchmark before the systems were run rather than defined after viewing the audit results. This makes it possible to distinguish the prevalence of publications in a particular language in the results from the actual search and recommendation of studies preselected as important within each scholarly sphere.

Benchmark topics were selected on the basis of Kim et al. (2025), which compares the research landscapes of Korean- and English-language political science on Korea. We chose five Korean-politics topics studied in both scholarly spheres and organized to cover major developments in modern Korean politics in broadly chronological order:

1. Korean War
2. South Korean economic development
3. South Korean democratization
4. North Korean nuclear issue
5. Korean Wave

Each topic was operationalized using three semantically corresponding Korean and English search terms.

| Topic | Korean terms | English terms |
| ----- | ------------ | ------------- |
| Korean War | 한국전쟁; 한국전쟁 발발; 한국전쟁 기원 | Korean War; Outbreak of the Korean War; Origins of the Korean War |
| South Korean economic development | 한국 경제발전; 한국 발전국가; 한국 수출주도 산업화 | South Korean Economic Development; Korean Developmental State; South Korean Export-Led Industrialization |
| South Korean democratization | 한국 민주화; 한국 민주화운동; 한국 시민사회 | South Korean Democratization; South Korean Democracy Movement; South Korean Civil Society |
| North Korean nuclear issue | 북핵 문제; 북한 핵무기; 대북 확장억제 | North Korean Nuclear Program; North Korean Nuclear Weapons; Extended Deterrence against North Korea |
| Korean Wave | 한류; 케이팝; 한국 영화 | Korean Wave; K-pop; South Korean Cinema |

Each topic contains ten Korean-language and ten English-language papers. Korean benchmark papers were drawn from DBpia and KISS, while English benchmark papers were drawn from Web of Science and Google Scholar. Candidate pools were ranked by citation counts, and the ten papers per topic ranked highly in both respective sources were selected. The final benchmark contains 50 Korean-language and 50 English-language papers, 100 in total, and was fixed before the LLM audit. It is an evaluation set for comparisons across conditions, not a gold standard covering all relevant literature on each topic.

The audit crosses three factors:

* Query language: English / Korean
* Source instruction: general web / explicit KCI, DBpia, and KISS instruction
* System: OpenAI gpt-5.6-sol / Perplexity sonar-pro

Every prompt included all three search terms for the topic and requested ten relevant scholarly publications in a fixed JSON format. Searches were limited to two per search term and six per execution. We conducted 200 stateless executions: 5 topics × 4 prompt conditions × 2 systems × 5 independent repetitions. These produced 1,932 valid recommendation occurrences.

## 4.2 Measurement and analysis

We distinguish three outcomes for benchmark paper \(j\) and execution \(i\):

* TraceRecovery: whether the benchmark paper is confirmed in the search trace exposed externally by the provider
* Recommendation: whether the benchmark paper is included in the final recommendations
* SuppliedLinkAccess: whether the benchmark paper is recommended and the supplied URL opens the full text without login or payment

The first two variables answer different questions. TraceRecovery measures whether a benchmark appears in the observable search trace, while Recommendation measures whether that publication is ultimately included among the sources presented to the user. Because the trace is observed only to the extent disclosed by the provider, it does not represent the system's entire internal retrieval process.

The benchmark panel contains 4,000 paper × execution observations. Each of the 200 executions is matched to the ten Korean and ten English benchmark papers for the corresponding topic. The denominator for SuppliedLinkAccess is all benchmark-paper × execution pairs, so it is not the access rate conditional on recommendation. It captures cases in which search, recommendation, and access all succeed.

We use the English-query, general-web condition as the baseline, estimate the difference between Korean and English benchmark papers, and assess how query language and source instruction alter that difference. We also calculate a direct contrast between the combined condition and the baseline.

Separately, we measure the share of Korean-language publications among all recommendations. This is distinct from benchmark recovery because Korean-language papers outside the benchmark also count toward the language share.

Finally, we reviewed 927 distinct supplied URLs or no-URL item keys, classifying them as accessible full text, abstract only, paywalled, broken links, or hallucinated/unverifiable publications. This assessment concerns only the URL supplied by the system; it does not investigate whether a free copy exists elsewhere on the web.

## 4.3 Results

Under the English-query, general-web baseline, recovery was low for both benchmarks, with an additional deficit for Korean-language papers.

| Stage | English benchmark | Korean benchmark | Korean–English gap | 95% CI | \(p\) |
| ----- | ----------------: | ---------------: | -----------------: | -----: | ----: |
| Observable search trace | 3.4% | 0.0% | −3.4 pp | [−6.46, −0.34] | .029 |
| Final recommendation | 3.2% | 0.0% | −3.2 pp | [−5.77, −0.63] | .015 |
| Accessible supplied link | 0.6% | 0.0% | −0.6 pp | [−1.76, 0.56] | .311 |

The Korean–English differences in the search trace and final recommendations are statistically significant. The difference in full-text access through the supplied link is not significant, although benchmark papers rarely reach this final stage at all.

A Korean-language query changes the Korean–English gap at the search-trace stage by +3.8 pp (95% CI [0.72, 6.88], \(p=.016\)), while the Korean-database instruction changes it by +4.0 pp (95% CI [0.73, 7.27], \(p=.017\)). At final recommendation, the database instruction changes the gap by +3.2 pp (95% CI [0.71, 5.69], \(p=.012\)). The Korean-query estimate is +2.6 pp in the same direction but has \(p=.068\).

A direct comparison of the combined condition with the baseline shows that the Korean–English gap changes by +5.6 pp in the search trace and +6.4 pp in final recommendation. Under the combined condition, Korean benchmark recovery is 2.2% in the search trace and 3.2% in the final recommendations. The direction of the relative gap reverses, but absolute recovery remains low.

Search conditions change the language composition of final recommendations much more than benchmark recovery.

| Prompt condition | Korean-language share of recommendations |
| ---------------- | ----------------------------------------: |
| English + general web | 0.0% |
| English + Korean DB instruction | 35.3% |
| Korean + general web | 55.8% |
| Korean + Korean DB instruction | 91.2% |

A Korean-language query increases the Korean-language share of recommendations by 55.7 pp (\(p<.001\)), while a Korean-database instruction increases it by 35.4 pp (\(p<.001\)). Yet even under the combined condition, recommendation recovery for the preselected Korean benchmark is only 3.2%.

Thus, recommending many Korean-language publications is not the same as including at high rates the particular studies that have been important in the Korean-language sphere. This does not mean that Korean-language recommendations outside the benchmark are inappropriate; the two measures answer different questions.

Outcomes for the links supplied with all 1,932 recommendation occurrences are:

* 854 (44.2%): full text accessible
* 859 (44.5%): access restricted

  * 247 abstract only
  * 612 paywalled
* 219 (11.3%): invalid or unverifiable

  * 176 broken links
  * 43 coded hallucinated publications

| Outcome of supplied link | Overall | Korean papers | English papers |
| ------------------------ | ------: | ------------: | -------------: |
| Accessible | 44.2% | 46.3% | 42.4% |
| Access restricted | 44.5% | 47.9% | 41.6% |
| Invalid or unverifiable | 11.3% | 5.8% | 16.0% |
| Broken link | 9.1% | 3.3% | 14.1% |
| Hallucinated item | 2.2% | 2.6% | 1.9% |

After controlling for prompt condition and system, recommended-item language is not significantly associated with full access, access restriction, or invalid/unverifiable outcomes independently. The raw differences in the table should therefore not be interpreted as effects of publication language itself.

## 4.4 Interpretation

The central result of Study 2 is that search conditions alter the relative visibility of the Korean benchmark without producing high absolute recovery of major publications. The Korean deficit under the English general-web baseline appears in both the search trace and the final recommendations. Korean queries and Korean-database instructions narrow or reverse that difference, but Korean benchmark recovery under the combined condition remains only 2.2% in the search trace and 3.2% in final recommendations.

This result demonstrates why language representation must be separated from benchmark recovery. Although 91.2% of final recommendations under the combined condition are Korean-language publications, recommendation recovery for the pre-specified Korean benchmark is 3.2%. A Korean-centered result set does not by itself establish adequate inclusion of major research from the Korean-language sphere.

Separating the search trace from final recommendation also locates observable points of omission. The disclosed trace does not reveal the provider's entire internal retrieval process, so it cannot support a complete account of internal mechanisms. Full-text access through supplied links is another outcome. Fewer than half of all recommendations lead directly to full text, but this stage does not exhibit the same statistically significant Korean–English difference found in search and recommendation.

# 5. Discussion

## 5.1 Synthesis of the main findings

The central claim supported by the two studies is that search visibility constitutes an independent stage in the international circulation of knowledge. Research already used or identified as important in the Korean-language sphere does not automatically become a reviewable candidate in other search environments.

Each study provides different evidence for this claim. Study 1 shows that historical English-language citation trajectories differ by current Google Scholar index presence, but it does not directly observe the historical search environment. Study 2 directly compares current benchmark retrieval and selection in generative search, but it does not observe later citation. The two results therefore cannot be joined into a single causal mechanism. Their shared implication is that becoming a search candidate and being presented as a final source are outcomes distinct from publication and citation.

Study 2 particularly shows that linguistic representation cannot substitute for scholarly recovery. The Korean-language share changes substantially across prompts, while absolute recovery of the pre-specified Korean benchmark remains low. This does not make Korean recommendations outside the benchmark inappropriate. It means that the language of a result list and the degree to which major publications from a scholarly sphere are represented answer different questions.

Full-text access must be separated for the same reason. In Study 1, full-text links currently supplied by Google Scholar have no statistically significant additional relationship with English-language citation incidence. In Study 2, fewer than half of recommendations lead to full text through the supplied link, but no significant language gap appears. Search, final source selection, supplied-link access, and later citation cannot be collapsed into a single indicator.

## 5.2 Implications for political science and future research

The political-science implication is not that knowledge inequality begins with search technology, but that it can also be observed at the search stage. Existing research documents inequalities in research subjects, researcher location, publication language, database coverage, and international citation (Breuning et al. 2018; Wilson and Knutsen 2022; Mongeon and Paul-Hus 2016). This study adds the question of which particular publications become available for review when researchers construct a body of prior literature.

This stage operates before researchers evaluate scholarly content and value. If relevant work does not appear in search results or is excluded from final sources, researchers may never have an opportunity to assess it. Discovery bottleneck refers to this pre-evaluation loss of visibility. In Study 1, it concerns failure to confirm a Google Scholar bibliographic record under the search protocol. In Study 2, it concerns failure to confirm a benchmark in the observable search trace or final recommendations. The concept does not assume a single internal algorithmic cause.

The problem is particularly important when local-language and English-language scholarship coexist on the same political phenomena. If international knowledge of Korean politics is inferred solely from English-language journals, international citation indexes, or reading lists generated by search systems, the difference between the scholarly record accumulated in Korean and the subset appearing in search results may be missed. Evaluations of international visibility should therefore measure not only linguistic diversity in a result set but also paper-level recovery of pre-identified major publications.

Future research should track this visibility over time. Repeatedly measuring Google Scholar index presence and supplied links for the same papers would document indexing changes that Study 1 cannot reconstruct. Repeating the same benchmarks and conditions in generative search would show how retrieval and recommendation of particular Korean studies change with models, search indexes, and ranking procedures. Research linking discovery to user clicks, full-text reading, relevance assessment, and actual citation would identify the stages that follow search.

# 6. Conclusion

This paper has argued that discovery between knowledge production and citation must be analyzed as a separate stage in the international visibility of Korean-politics research. The core question is which particular studies among those that exist and are used in the Korean-language sphere become reviewable candidates and final sources in search environments.

Study 1 shows different historical English-language citation trajectories for papers with and without confirmed current Google Scholar index presence. The relationship appears in C2 and C3 but does not widen further in C4, and it cannot be interpreted as a historical causal effect of Google Scholar. Study 2 directly observes a Korean benchmark deficit under the English general-web baseline. Korean queries and Korean-database instructions change the relative gap but do not resolve low absolute recovery. In particular, a high Korean-language recommendation share coexists with low Korean benchmark recovery.

The conclusion supported by these findings is limited but clear. Whether a publication is retrieved, selected as a final source, readable through the supplied link, and later cited are distinct outcomes. Discovery bottleneck names the loss of visibility in a particular search environment before substantive evaluation. In fields with parallel Korean- and English-language bodies of scholarship, analyses must consider not only what research is produced and cited but also which studies actually appear in the search process.

# 7. Limitations

The limitations fall into three categories: temporal identification, measurement, and generalizability. Study 1 observes only current Google Scholar status and therefore cannot identify a historical causal effect. Study 2 measures behavior for a limited set of systems and topics at one collection period. Neither study observes user behavior after search.

First, Google Scholar index presence in Study 1 is observed only in 2026. We do not know when each target first entered Google Scholar, when it became retrievable, or what full-text links were supplied at earlier times. Current index presence may itself result from prior scholarly circulation. Widely cited or more visible publications may subsequently have become more likely to be confirmed in Google Scholar, and target fixed effects cannot eliminate this temporal ordering or time-varying process.

Second, the measurement of Google Scholar index presence may contain bibliographic matching error. Although we used Korean and English titles and reference-title variants, metadata errors, title variation, duplicate records, or incomplete indexing may have caused us to miss or incorrectly match a record. Because Google Scholar does not publish a complete index list, (D=0) means that index presence was not confirmed under this study's search and matching protocol, not absolute absence from Google Scholar.

Third, the strength of the Study 1 result varies across specifications. The main incidence model and pre-2005 restriction show widening gaps in C2 and C3, but some Poisson and additional-control specifications are more uncertain. We cannot generalize that the same pattern appears across all outcomes and functional forms.

Fourth, Study 2 is limited to two systems, five Korean-politics topics, one collection period, and 100 benchmark papers. The five topics were selected to compare areas studied in both language spheres, but they are not a probability sample of all Korean-politics research. A benchmark based on citation counts and papers jointly ranked highly in two sources may also underrepresent recent, low-citation, or specialized research.

Fifth, generative-search environments change continuously. The underlying model, search index, ranking procedure, or provider interface may change under the same model name. The search traces disclosed by providers also do not reveal the complete internal retrieval process, and observability differs across providers. Failure to find a benchmark in the trace does not establish that the system never considered it internally.

Sixth, the full-text access results face both a floor and a limited measurement scope. Benchmark retrieval and recommendation are themselves rare, leaving few observations at the access stage. The absence of a significant access gap is not affirmative evidence of equal accessibility across languages. The link audit evaluates only the URLs supplied by the systems and does not capture free copies elsewhere. Hallucination events are also few and concentrated in particular experimental cells.

Finally, neither study observes user behavior after search. Clicking results, reading full text, evaluating substantive relevance, language proficiency, perceived quality, citation norms, collaboration networks, and publication venues may all shape later use and citation. The evidence is limited to which publications become visible and are presented in search environments, and whether their full text can be accessed through supplied links.

[^1]: An early version of Kim et al. (2025) was presented at the 28th IPSA World Congress of Political Science in Seoul, July 12–16, 2025. A revised manuscript is currently under re-review following a revise-and-resubmit decision at *Humanities and Social Sciences Communications*.

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
