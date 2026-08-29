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

Research on Korean politics is produced and circulated in distinct Korean- and English-language scholarly spheres, and the scholarship accumulated in the two spheres is neither internationally visible nor cited to the same extent (Rhee 2026; Kim et al. 2025). This paper examines one dimension of this difference: the visibility of publications in scholarly search environments. Because researchers use search environments to construct the body of literature they review, the scholarly existence of a study must be distinguished from whether that study actually appears as a candidate in the search process. We analyze how research on Korean politics that has already been used or identified as important in the Korean-language sphere becomes visible in Google Scholar and generative search, while treating full-text access through links supplied by the search environment as a separate outcome.

Study 1 analyzes 54,789 papers on Korean politics cited by Korean-language political science articles published from 2000 to 2025, examining the relationship between Google Scholar index presence as of 2026 and English-language citation probability across periods. Compared with the baseline period through 2009, the English-language citation-probability gap between papers whose bibliographic records are currently confirmed in Google Scholar and those whose records are not was significantly larger by 0.405 percentage points (pp) in 2010–2014 and 0.696 pp in 2015–2019, but did not widen further in 2020–2024. Among papers with confirmed index presence, full-text access through links currently supplied by Google Scholar was not significantly associated with English-language citation probability. These results describe an association between current Google Scholar index presence and historical English-language citation trajectories, not a causal effect of Google Scholar.

Study 2 audits two web-enabled generative search systems using 50 preselected Korean-language and 50 English-language papers across five Korean-politics topics studied in both scholarly spheres. Under the English-query, general-web baseline, no Korean benchmark paper was recovered in either the observable search trace or the final recommendations, whereas English benchmark recovery was 3.4% and 3.2%, respectively. Combining a Korean query with an instruction to search Korean scholarly databases narrowed the Korean–English gap by 5.6 pp at search and 6.4 pp at recommendation, yet Korean benchmark recovery in final recommendations remained only 3.2%. Only 44.2% of all recommendations provided direct full-text access through the accompanying link, and no significant language gap was found in access.

Together, the studies show that the international visibility of Korean-politics research should be analyzed not only through publication and citation but also through which publications actually appear as reviewable candidates in scholarly search and are selected as final sources. In particular, a large number of Korean-language recommendations in generative search does not necessarily mean that the major scholarship accumulated in the Korean-language sphere is represented to a corresponding degree. We introduce discovery bottleneck as an operational concept for the loss of visibility at observable stages of search or final source selection before a publication receives substantive evaluation.

Keywords: Korean political science; Korean-politics research; scholarly search; Google Scholar; generative search; non-English-language scholarship; international visibility; full-text access; discovery bottleneck

# 1. Introduction

Which research enters scholarly discussion and receives citations in international political science is not determined by content alone. The countries and regions studied in leading political science journals have long been concentrated in North America and Western Europe, while international publishing also exhibits inequalities associated with researchers' geographic and institutional locations (Wilson and Knutsen 2022; Breuning et al. 2018). Language adds another divide. Major international scholarly databases disproportionately cover English-language journals, and publications in other languages tend to be disadvantaged in international citation relative to English-language work (Mongeon and Paul-Hus 2016; Vera-Baceta, Thelwall, and Kousha 2019; Di Bitetti and Ferreras 2017).

Research on Korean politics provides a case in which this linguistic and scholarly segmentation can be observed. Research circulating around KCI and SSCI in Korean political science exhibits different topical and methodological patterns (Rhee 2026), while Korean- and English-language research on Korean politics also forms distinct scholarly spheres in production, circulation, and international citation reach (Kim et al. 2025).[^1] The accumulation of a substantial body of Korean-language scholarship therefore does not by itself imply that it will be discovered and reviewed to the same degree in international scholarly environments.

This paper analyzes that difference through the visibility of publications in scholarly search environments. Researchers construct the literature they review through search in order to understand prior work and position their research questions. A paper's existence as a publication, or its inclusion within the aggregate coverage of a database, is therefore not the same as the paper actually appearing for review in a particular search environment. The distinction in information-retrieval research between database-level coverage and document-level retrievability is relevant for precisely this reason (Azzopardi and Vinay 2008). We apply this distinction to the international visibility of Korean-politics research.

Study 1 analyzes the relationship between English-language citation over time and whether an individual paper's bibliographic record is currently indexed and retrievable in Google Scholar. The analysis includes 54,789 Korean-politics publications cited at least once by Korean-language political science articles produced between 2000 and 2025. Every target paper therefore has a record of actual scholarly use in the Korean-language sphere. Within this common body of literature, we compare how the English-language citation-probability gap between papers with and without confirmed current Google Scholar index presence varies across periods. Because Google Scholar status is observed only in 2026, the analysis does not estimate whether historical Google Scholar indexing caused English-language citation.

Study 2 analyzes whether individual papers appear in generative-search processes and which of them are ultimately presented as sources. Web-enabled generative search retrieves external material but does not return all retrieved items to the user; it selects some as citations or recommendations when constructing an answer (Liu, Zhang, and Liang 2023; He et al. 2025). Whether a pre-specified benchmark paper appears in the provider's disclosed search trace and whether it is included in the final recommendations are therefore distinct outcomes. Study 2 holds constant Korean-politics topics studied in both the Korean- and English-language spheres, varies query language and instructions to search Korean scholarly databases, and compares how major publications in the two languages appear at these two points.

The analysis is not simply concerned with how many Korean-language publications are presented. A high number of Korean-language publications and faithful representation of major scholarship accumulated in Korean political science are different outcomes. Generative search may recommend many Korean-language papers while including few of the Korean studies designated as important before the search. Study 2 therefore distinguishes the Korean-language share of final recommendations from the extent to which pre-specified Korean benchmark papers are actually recovered in search and recommendation.

Full-text access is also analyzed separately from search visibility. Even when a paper is indexed in Google Scholar or recommended by generative search, the supplied URL may lead to a paywall, an abstract page, or a broken link. Conversely, a publisher version may be paywalled while a repository or author-hosted copy remains available (Jamali and Nabavi 2015). We thus do not measure a paper's general open-access (OA) status; instead, we measure whether the link actually supplied by each search environment opens the full text without login or payment.

The two studies do not constitute a single causal sequence from search to full-text access to citation. Study 1 analyzes the relationship between current Google Scholar index presence and historical English-language citation trajectories. Study 2 directly observes how major Korean- and English-language publications differ in current generative search and final source selection. Their designs and temporal scopes differ, but both ask which studies among those that exist and are actually used in the Korean-language sphere appear as reviewable research in search environments used internationally.

We use discovery bottleneck to refer to the loss of visibility in search and final source selection before a publication receives substantive evaluation. The concept does not claim that search technology is the single cause of international citation inequality. It is an operational label for an observable omission in which a publication fails to appear as a candidate in a particular search environment or appears in the search process but is excluded from the sources ultimately presented.

This study makes three contributions. First, it extends the international visibility of Korean-politics research beyond publication and citation to the level of whether individual papers are actually confirmed in scholarly search. Second, within generative search, it distinguishes appearance in the search process from final source selection in order to identify where major Korean-language studies lose visibility. Third, by separating the retrieval and selection of publications from full-text access through the supplied links, it avoids reducing international visibility to a single outcome.

# 2. Prior Research

## 2.1 International visibility in political science and linguistic scholarly spheres

Internationally visible knowledge in political science has been unevenly constituted by research subject, researcher location, and publication language. The subjects covered in major political science journals have historically been concentrated in North America and Western Europe, a geographic imbalance that also bears on the scope over which descriptive and causal claims developed in particular regions are generalized to political science as a whole (Wilson and Knutsen 2022). On the producer side, scholars from the Global South are underrepresented in leading international political science journals, while researchers affiliated with certain institutions are overrepresented (Breuning et al. 2018). The international knowledge structure of political science therefore concerns not only what is studied but also which research enters and circulates within central scholarly spaces.

Publication language and bibliographic infrastructure form another axis of inequality. Web of Science and Scopus disproportionately cover English-language journals relative to the overall population of scholarly journals (Mongeon and Paul-Hus 2016; Vera-Baceta, Thelwall, and Kousha 2019). Even in multilingual publishing environments, non-English articles receive lower citation rates than English-language articles after other publication characteristics are taken into account (Di Bitetti and Ferreras 2017). The scholarly record observable internationally is thus not identical to the totality of research produced across languages, and database coverage and citation visibility may themselves be selectively structured by language.

This segmentation also appears in Korean-politics research. Korean political science published in KCI and SSCI venues differs in topical and methodological composition (Rhee 2026), while Korean- and English-language research on Korean politics displays different patterns of international recognition and citation reach (Kim et al. 2025). International visibility cannot therefore be reduced to citation differences between otherwise identical papers published in different languages. It also includes the extent to which scholarship accumulated in the Korean-language sphere on the same political phenomena appears in international scholarly-information environments.

Existing research documents inequalities in publication, database coverage, and citation, but the process by which researchers actually discover literature constitutes a separate level of analysis. Because researchers use search to build a candidate body of prior work, the existence of a study or a database's aggregate coverage of a field must be distinguished from whether an individual publication actually appears for review in the search process.

Information-retrieval research conceptualizes this difference as one between database-level coverage and document-level retrievability (Azzopardi and Vinay 2008). Here, the concept does not make retrievability itself the sole outcome. Rather, it supplies the conceptual basis for the proposition that aggregate coverage cannot determine the search visibility of an individual publication. Study 1 applies this distinction to whether the paper's bibliographic record is currently confirmed in Google Scholar, or its Google Scholar index presence.

## 2.2 Google Scholar coverage, index presence, and full-text access

Google Scholar is an important environment in which to examine the international visibility of non-English scholarship. Comparisons with Web of Science and Scopus show that Google Scholar captures a wider range of publications and citations, including substantial numbers of non-English and non-journal materials (Chen 2010; Martín-Martín et al. 2018b, 2021). This broad coverage matters for non-English scholarship because research insufficiently captured in selective international citation indexes may nevertheless be found in Google Scholar.

However, broad coverage of a language or field does not guarantee that every individual paper's bibliographic record can actually be confirmed. Comparisons with external bibliographic records have also identified publications not returned by Google Scholar (Delgado-Quirós et al. 2024). Aggregate Google Scholar coverage and paper-level index presence must therefore be distinguished analytically.

The distinction matters because Google Scholar is widely used for actual scholarly discovery. Studies repeatedly document the use of Google and Google Scholar by researchers and graduate students (Jamali and Asadi 2010; Cothran 2011), and a recent faculty survey identifies Google Scholar as one of the main starting points for social scientists searching for new scholarly literature (Blankstein 2022). Such use does not itself mean that index presence generates subsequent citations, but it clearly establishes index presence as an observable property within an environment where actual literature search takes place.

Research on Google Scholar's provision of full text points to a separate dimension. Google Scholar may link not only to a publisher site but also to versions identified in repositories and elsewhere on the web, and it provides links to free full text for a substantial share of the literature (Jamali and Nabavi 2015; Martín-Martín et al. 2018a). Yet confirming a bibliographic record in Google Scholar and receiving a usable full-text link from Google Scholar are not the same. An indexed paper may lead only to a paywall or abstract page, while a freely available web version may exist without being presented by Google Scholar.

Prior research thus indicates that database coverage, paper-level index presence, and full-text access through the supplied link are distinct properties. Study 1 applies this distinction to Korean-politics publications that have actually been used in Korean-language political science. Rather than re-estimating Google Scholar's overall coverage, it compares historical English-language citation patterns by current Google Scholar index presence within a common set of publications with Korean-language citation records.

## 2.3 Generative scholarly search and publication selection

In generative search, retrieved materials are not all presented directly to the user. A web-enabled LLM searches external materials, selects some as citations or recommendations, and uses them to compose an answer. Research on generative search has therefore treated source inclusion in the final answer, whether citations support the associated claims, and whether supplied sources can be verified as distinct problems rather than examining retrieval alone (Liu, Zhang, and Liang 2023).

Recent work applying LLMs to scholarly search increasingly evaluates whether pre-specified publications are actually recovered, rather than relying on the apparent plausibility of generated lists. LitSearch defines target papers independently of a system run and then evaluates retrieval performance (Ajith et al. 2024); academic-search agents such as PaSa likewise use query–paper benchmarks (He et al. 2025). This approach follows the information-retrieval tradition of evaluating search performance against a predefined relevant set (Manning, Raghavan, and Schütze 2008). A recent audit of LLM-based scholar recommendations similarly uses an external benchmark to measure whether pre-specified scholars or publications are actually recommended (Espín-Noboa and Méndez 2026). At the same time, although research on LLM-assisted literature search is rapidly expanding, its use in rigorous processes such as systematic reviews is not yet fully established (Lieberum et al. 2025; Asai et al. 2026).

This approach is particularly important when analyzing non-English scholarship. A generated list with many Korean-language papers demonstrates that a large amount of Korean-language material was presented, but does not by itself show that major scholarship accumulated in the Korean-language sphere was adequately represented. Depending on the search condition, a system may recommend many Korean-language publications yet include almost none of the particular studies treated as important in Korean political science. An analysis of Korean-language visibility in generative search must therefore distinguish the linguistic composition of final recommendations from whether pre-identified major Korean-language studies are actually searched and selected.

The sources ultimately selected by generative search are also not fixed. Prior research reports that generative-search results can differ with source authority, geography, and institutional or commercial source type (Liu, Zhang, and Liang 2023; Li and Sinnamon 2024). In Korean-politics research, where Korean- and English-language publications circulate through different databases and publishing channels, query language and instructions about which scholarly information sources to search may change both the literature retrieved and the sources ultimately presented.

Study 2 therefore distinguishes two points. First, it asks whether a benchmark paper appears in the provider's externally disclosed search trace. Second, it asks whether the paper is included in the final recommendations. Providers do not disclose their entire internal retrieval process, so the search trace cannot be equated with that full process. Nevertheless, separating the two outcomes permits a distinction between an item that never appears in the observable search trace and one that appears there but is not ultimately presented as a source.

Study 2 applies this distinction to Korean-politics topics studied in both scholarly spheres. By varying query language and explicit instructions to search Korean scholarly databases, it analyzes the conditions under which major publications pre-identified in the Korean-language sphere actually appear in search traces and final recommendations. Full-text access through the supplied link is measured as an outcome separate from search and source selection.

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

Study 1 shows that historical English-language citation patterns differ between papers grouped by current Google Scholar index presence. Relative to C1, the citation-probability gap between the two groups widens in C2 and C3, and the same directional result appears when the sample is restricted to pre-2005 targets that could contribute to all four cohorts. The gap does not widen further in C4, however, and some alternative specifications produce less precise results.

The estimates of 0.405 pp and 0.696 pp do not represent citation probability itself. They indicate how much the citation-probability gap between the two groups increased relative to C1. The results should therefore not be interpreted as a continuously expanding advantage across all periods.

Nor can we conclude that current index presence caused historical English-language citation. The existence of a current Google Scholar record may reflect subsequent indexing, web availability, prior scholarly circulation, or other characteristics that changed alongside these factors. The most limited interpretation is that historical English-language citation trajectories differ by current Google Scholar index presence.

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

In Study 2, the Korean benchmark deficit under the English general-web baseline appears in both the search trace and the final recommendations. Korean-language queries and Korean-database instructions narrow or reverse this relative difference, but absolute Korean benchmark recovery remains low.

In the combined condition, 91.2% of final recommendations are Korean-language publications, while recommendation recovery for the pre-specified Korean benchmark is only 3.2%. A result set that appears linguistically Korean-centered therefore does not establish that major research in the Korean-language sphere has been adequately included.

Separating the search trace from final recommendation also makes it possible to distinguish some forms of omission. A benchmark paper absent from the disclosed search trace has a different observable outcome from one that appears in the trace but is not included in the final recommendations. Because providers do not disclose their entire internal retrieval process, however, this should not be interpreted as a complete observation of the internal retrieval mechanism.

Full-text access through supplied links is another issue. Fewer than half of all recommendations led directly to the full text, but this outcome did not exhibit the same statistically significant Korean–English difference found in search and recommendation.

# 5. Discussion

## 5.1 Synthesis of the main findings

The common finding across the two studies is that research that exists and is actually used in the Korean-language sphere does not automatically become equally visible in other search environments. The form in which visibility is observed and the temporal character of the evidence nevertheless differ across the studies.

Study 1 begins with publications already cited in Korean-language political science. Among them, the English-language citation-probability gap between papers with and without confirmed Google Scholar index presence as of 2026 varies across periods. The gap is larger in 2010–2014 and 2015–2019 than in the baseline period, but does not widen further in 2020–2024. This is an association between current Google Scholar index presence and historical citation trajectories; it does not directly reveal the historical search environment.

Study 2 directly observes current generative search. Under the English general-web baseline, Korean benchmark papers appear less often than English benchmark papers in both the disclosed search trace and final recommendations, and the difference changes with Korean-language queries and instructions to search Korean scholarly databases. The extent to which major Korean-language publications appear in generative search can therefore vary with search conditions.

The two studies cannot be combined as a single causal mechanism. Study 1 demonstrates the relationship between current Google Scholar index presence and past English-language citation patterns, while Study 2 directly compares retrieval and final source selection under current generative-search conditions. Their more limited joint implication is that the process by which scholarly publications appear as reviewable studies in search environments is itself a distinct object of analysis in international visibility.

Study 2 particularly demonstrates that the linguistic composition of a final list and the actual representation of major scholarship from the Korean-language sphere can diverge. In the combined condition, 91.2% of recommendations are Korean-language publications, yet recommendation recovery for the pre-specified Korean benchmark is 3.2%. Seeing a large amount of Korean-language material and adequately including major scholarship accumulated in Korean are therefore different claims.

Full-text access is also not the same outcome as search and recommendation. In Study 1, full-text links currently supplied by Google Scholar have no statistically significant additional relationship with English-language citation incidence. In Study 2, fewer than half of all recommendations lead to full text through the supplied link, but no significant Korean–English difference is found. Whether a publication is found in search, presented as a final source, readable through the supplied link, and later cited must therefore be interpreted as distinct outcomes.

## 5.2 Implications for political science and future research

The political-science implication is not that search technology alone determines international knowledge inequality. Existing research already shows that the subjects, publishing, database coverage, and international citations of political science are unevenly constituted by region and language (Breuning et al. 2018; Wilson and Knutsen 2022; Mongeon and Paul-Hus 2016). In Korean-politics research, the Korean- and English-language spheres also differ in topics, methodology, and international recognition (Rhee 2026; Kim et al. 2025).

This study adds that differences in visibility can also be observed in the search processes researchers use to identify prior literature. A paper actually cited in the Korean-language sphere is not necessarily confirmed in current Google Scholar, and even when generative search presents many Korean-language papers, it does not necessarily include the particular studies treated as important in Korean-language scholarship to the same degree.

Search environments do not determine the scholarly value of publications themselves, but they intervene in the process that structures which publications researchers may review. When relevant work does not appear in search results, a researcher may be unable to consider it before evaluating its content or value. In this sense, discovery bottleneck is a problem of visibility that occurs before the evaluation of scholarly quality.

The issue is particularly important where substantial local-language and English-language literatures coexist on the same political phenomena. If international knowledge of Korean politics is inferred solely from English-language journals, international citation indexes, or reading lists produced by generative search, the difference between the scholarly record accumulated in Korean and the subset that actually appears in a given search environment may be missed.

Studies 1 and 2 constrain and observe this difference in distinct ways. Study 1 begins with the common condition of actual citation in Korean-language scholarship and compares current retrievability and English-language citation patterns within that set. Study 2 holds substantive topics studied in both language spheres constant and compares whether major publications preselected from each sphere appear in the search trace and final recommendations.

The paper's concept of discovery bottleneck does not refer to a single internal algorithmic cause. In Study 1, it concerns failure to confirm a Google Scholar bibliographic record under the study's search protocol. In Study 2, it concerns failure to confirm a benchmark paper in the observable search trace or to include it in the final recommendations. It labels the condition in which a publication loses visibility in an observable search or selection process before substantive evaluation.

Future research should observe these conditions directly over time. Repeated measurement of the same publications' Google Scholar index presence and supplied links could document indexing changes that Study 1 cannot observe. Reapplying the same benchmark and search conditions in generative search could show how the visibility of particular Korean-language studies changes as models and search environments evolve.

# 6. Conclusion

The international visibility of Korean-politics research is not fully captured by which studies are published and ultimately cited. In the actual process of identifying prior literature, there is an additional question: which publications exist in a search environment, appear in search results, and are ultimately presented as sources for review.

Study 1 compares current Google Scholar index presence and historical English-language citation patterns for 54,789 Korean-politics publications cited by Korean-language political science articles produced from 2000 to 2025. The English-language citation-probability gap between papers with and without confirmed current Google Scholar records is significantly larger in 2010–2014 and 2015–2019 than in the baseline period, but does not widen further in 2020–2024. Full-text links currently supplied by Google Scholar have no separate statistically significant relationship with English-language citation incidence. The result is a limited association between current index presence and historical citation trajectories, not a historical causal effect of Google Scholar.

Study 2 uses pre-specified Korean- and English-language benchmarks on Korean-politics topics studied in both language spheres to audit current generative search. Under the English general-web baseline, Korean benchmark papers are recovered significantly less often than English benchmark papers in the search trace and final recommendations. Korean-language queries and Korean-database instructions narrow the relative gap, but absolute Korean benchmark recovery remains low. In particular, even when 91.2% of recommendations in the combined condition are Korean-language publications, recommendation recovery for the pre-specified Korean benchmark is only 3.2%. A large number of Korean-language recommendations is therefore not the same as adequate representation of major research from the Korean-language sphere.

Neither study identifies a significant language gap in supplied-link access corresponding to the differences found in search and recommendation. This result shows why publication retrieval, final source selection, full-text access, and later scholarly use should not be treated as a single outcome.

In this paper, discovery bottleneck refers to a phenomenon in which a publication loses visibility in a particular search environment before reaching substantive evaluation, even though it exists and has already been used in one scholarly sphere. This is not a claim that search technology alone produces international knowledge inequality. Rather, for a field such as Korean politics, where parallel bodies of Korean- and English-language scholarship exist, the argument is that we must analyze not only what research is produced and cited but also which particular studies actually appear as reviewable publications in the search process.

# 7. Limitations

The most important limitation of Study 1 is that Google Scholar index presence is observed only in 2026. We do not know when each target first entered Google Scholar, when it became retrievable, or what full-text links were supplied at earlier times. Current Google Scholar status therefore cannot be equated with the historical search environment.

Current index presence may itself be a result of prior scholarly circulation. Widely cited or more visible publications may subsequently have become more likely to be confirmed in Google Scholar. Target fixed effects control for time-invariant paper characteristics but cannot eliminate this temporal ordering or time-varying processes.

The measurement of Google Scholar index presence may also contain bibliographic matching error. Although we used Korean and English titles and reference-title variants, metadata errors, title variation, duplicate records, or incomplete indexing may have caused us to miss an existing record or match one incorrectly. Because Google Scholar does not publish a complete index list, \(D=0\) means that index presence was not confirmed under this study's search and matching protocol, not absolute absence from Google Scholar.

The strength of the Study 1 result also varies across specifications. The main incidence model and pre-2005 restriction show widening gaps in C2 and C3, but some Poisson and additional-control specifications are more uncertain. We therefore cannot generalize that the same pattern appears across all outcomes and functional forms.

Study 2 is limited to two systems, five Korean-politics topics, one collection period, and 100 pre-specified benchmark papers. The five topics were selected to compare areas studied in both language spheres, but they are not a probability sample representative of all Korean-politics research. The benchmark also does not cover all relevant literature on each topic.

Reliance on citation counts and publications commonly ranked highly across two sources also limits the benchmark. The procedure produces a stable evaluation set of relatively established scholarship in each language sphere, but may underrepresent recent, low-citation, or specialized subtopic research.

Generative-search environments change continuously. The underlying model, search index, ranking procedure, or provider interface may change under the same model name, so Study 2 measures behavior at the time of data collection.

The search traces externally disclosed by providers do not reveal the full internal retrieval process. Failure to find a benchmark paper in the trace therefore does not establish that the system never considered it internally. Trace observability also differs across providers, so we do not compare the linguistic composition of search traces symmetrically across systems.

Full-text access is especially sparse at the benchmark level. Search and recommendation are themselves uncommon, creating a floor at the access stage. The absence of a significant Korean–English access gap should therefore not be interpreted as affirmative evidence that publications in the two languages are equally accessible.

The link audit evaluates only the URLs actually supplied by the systems. A paper classified as paywalled, abstract only, or associated with a broken link may still be available elsewhere online. Hallucination events are also few and concentrated in particular experimental cells, limiting generalization to the system level.

Finally, neither study observes what researchers do after a publication is retrieved or recommended. Clicking search results, reading full text, evaluating substantive relevance, language proficiency, perceived quality, citation norms, collaboration networks, and publication venues may all shape later use and citation. The evidence is therefore limited to which publications become visible and are presented in search environments, and whether their full text can be accessed through supplied links, rather than the entire process of knowledge circulation.

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
