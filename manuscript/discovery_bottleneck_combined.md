---
title: "Discovery Bottleneck"
subtitle: "Search Infrastructure and the International Visibility of Korean Political Science"
author: "[Author name]"
date: "August 2026"
geometry: margin=0.72in
fontsize: 10pt
linestretch: 1.05
mainfont: STIX Two Text
mathfont: STIX Two Math
---

## Abstract

Research published outside English is underrepresented in major bibliographic databases and tends to receive fewer citations than comparable English-language publications (Mongeon and Paul-Hus 2016; Amano, González-Varo, and Sutherland 2016; Di Bitetti and Ferreras 2017). This paper examines a distinct part of that inequality: whether Korean political science is retrieved by the systems through which researchers identify publications for possible use.

The paper analyzes two search environments. Study 1 examines 54,789 Korean-language papers that have been cited within Korean-language scholarship and relates their current Google Scholar retrievability to their English-language citation histories. A paper is classified as Google Scholar visible when an exact-title search produces a confirmed bibliographic match. Target-paper fixed-effects estimates show that, relative to citations received in 2009 or earlier, the English-language citation-probability gap between currently visible and nonvisible papers increased by 0.405 percentage points in 2010–2014 and 0.696 percentage points in 2015–2019. The corresponding estimate for 2020–2024 is statistically indistinguishable from zero.

Study 2 audits two web-enabled LLMs using a pre-specified corpus of 100 papers across five topics in Korean politics. Under an English-language general-web condition, neither system recovered a Korean benchmark paper. Korean-language queries and explicit instructions to search KCI, DBpia, or KISS substantially increased the Korean-language share of the recommendation lists, but recovery of the pre-specified Korean benchmark remained no higher than 3.2% per execution. Among 1,932 recommendation occurrences, 44.2% of system-supplied links opened full text without payment or login.

This paper uses the term **discovery bottleneck** to denote failure of a publication to enter the set of documents returned or recommended by a search system before a researcher evaluates its content. The two studies do not estimate a single causal pathway from indexing to citation. They show that Korean political science can be disadvantaged at two empirically separate stages of scholarly discovery: bibliographic retrieval in Google Scholar and paper retrieval and recommendation in web-enabled LLM search.

**Keywords:** scholarly information retrieval; Google Scholar; generative search; Korean political science; citation inequality; bibliographic metadata; retrievability

---

## 1. Introduction

Research published in languages other than English occupies a smaller share of major international bibliographic databases and generally receives fewer international citations than English-language research (Mongeon and Paul-Hus 2016; Amano, González-Varo, and Sutherland 2016; Di Bitetti and Ferreras 2017). Mongeon and Paul-Hus (2016), for example, show that Web of Science and Scopus overrepresent English-language journals relative to the broader population of scholarly journals. Di Bitetti and Ferreras (2017) find higher citation counts for English-language articles even after controlling for journal, publication year, and article length. Research on evidence synthesis further shows that excluding non-English studies can alter the substantive conclusions of a review because the omitted literature is not necessarily a random subset of the available evidence (Konno et al. 2020).

Korean political science provides a case in which this distinction can be examined directly. Korean-language political science contains a substantial literature that is cited within Korean scholarship but only rarely cited by English-language scholarship. Previous bibliographic analysis of Korean politics identifies a linguistically divided citation structure in which Korean-language scholarship relies substantially on locally accumulated work, while English-language scholarship concentrates citation within a different set of publications (Kim 2025).

Publication language is one explanation for this division, but it cannot determine citation unless a potential citer first encounters the paper. An English-language title, English abstract, or machine translation can reduce the linguistic cost of evaluating a Korean-language paper only after that paper has been retrieved. Amano, González-Varo, and Sutherland (2016) make this distinction concrete: among non-English conservation literature they examined, English metadata was often absent, and even papers with English titles were not always retrievable in Google Scholar by those titles.

This paper therefore separates **discovery** from subsequent reading, evaluation, and citation. In information-retrieval research, retrieval systems determine which documents in a collection can be returned in response to queries, and **retrievability** refers to the degree to which a document can be accessed through such a system across possible queries (Azzopardi and Vinay 2008; Manning, Raghavan, and Schütze 2008). Search-engine research likewise shows that search systems do not expose all indexed material equally; indexing and retrieval procedures systematically make some resources more prominent or accessible than others (Introna and Nissenbaum 2000).

This paper uses the term **discovery bottleneck** for a narrower empirical problem: a publication may be relevant and already used within its local scholarly community, yet fail to enter the set of publications returned by the search system through which another researcher identifies candidate literature. **Discovery bottleneck is a term introduced in this paper; it is not presented as an established concept in the information-retrieval literature.** The term names the empirical condition examined here rather than a complete theory of scholarly communication.

The analysis covers two distinct search environments.

**Study 1** examines Google Scholar. It asks whether current Google Scholar retrievability distinguishes Korean political science papers with different English-language citation histories:

> **Google Scholar retrievability** $\rightarrow$ **English-language citation trajectory**

Google Scholar launched in 2004. By 2010, studies of scholarly information seeking documented substantial reliance on Google and Google Scholar for locating research literature, and a 2011 survey found that 75% of 1,141 graduate students surveyed had previously used Google Scholar (Jamali and Asadi 2010; Cothran 2011). Study 1 therefore tests whether the English-language citation gap between papers that are currently retrievable and nonretrievable in Google Scholar changed across citation cohorts before and after Google Scholar became widely used. It does **not** assume that current retrievability measures historical indexing status.

**Study 2** examines current web-enabled LLM search. It measures three outcomes that are directly observable in the audit:

> **search-trace recovery** $\rightarrow$ **final recommendation** $\rightarrow$ **supplied-link access**

The three outcomes are analytically separate. A benchmark paper may appear in an observable search trace but not be included in the generated recommendation. A paper may be recommended but accompanied by a link that does not provide the full text. Study 2 also distinguishes **benchmark recovery**, defined here as recovery of papers fixed before the audit, from **language representation**, defined as the proportion of all recommended items classified as Korean-language. The distinction follows the information-retrieval principle that recall of a pre-specified relevant set is not equivalent to characteristics of the documents a system happens to return (Manning, Raghavan, and Schütze 2008).

The two studies are not treated as consecutive observations of the same papers or as stages in one estimated causal chain. Study 1 provides longitudinal citation evidence for a large set of Korean-language papers but measures Google Scholar visibility only in 2026. Study 2 randomizes search instructions and observes contemporary retrieval behavior directly, but uses a smaller pre-specified benchmark and does not observe later citations. Their common object is more specific: **whether Korean political science that is demonstrably present in the scholarly record becomes visible through two search environments used to identify literature.**

The results identify two distinct forms of unequal discovery. In Study 1, papers currently retrievable in Google Scholar show a larger English-language citation advantage in the 2010–2014 and 2015–2019 cohorts than in the earliest cohort. In Study 2, default English-language LLM search retrieves none of the Korean benchmark papers, and Korean-oriented interventions change the language composition of recommendations far more than they improve recovery of the benchmark itself. These findings do not replace language-based explanations of citation inequality. They identify retrieval as an additional empirical condition that precedes language-based evaluation.

![Overview of the two search environments and principal findings](combined_analysis/figures/discovery_bottleneck_global_figure.png){width=100%}

---

## 2. Literature and Argument

### 2.1 Publication language and international citation

The predominance of English in scholarly communication affects both the production and circulation of research. Amano, González-Varo, and Sutherland (2016) show that a substantial body of scientific literature remains published outside English and that the exclusion of such work limits the evidence available to international research communities. Di Bitetti and Ferreras (2017), analyzing multilingual journals, find that articles published in English receive more citations than articles published in other languages after accounting for journal, year, and article length. These studies establish that publication language is associated with both potential audience size and citation.

Language differences also affect which evidence enters research synthesis. Konno et al. (2020) compare English- and Japanese-language studies used in ecological meta-analyses and find cases in which excluding Japanese-language research changes estimated effect sizes and even their direction. They identify this as a form of **language bias** in evidence synthesis: publications available in different languages can differ systematically in results and study characteristics.

These findings establish a linguistic barrier at the stages of reading, evaluation, publication, and citation. They do not imply that language is the only source of unequal circulation. In particular, the effect of translation, bilingual metadata, or researchers' language competence presupposes that the publication has first been identified as a candidate for reading. The present study isolates that prior retrieval condition.

### 2.2 Bibliographic database coverage

Bibliographic databases define the universe of publications that their users can search. **Database coverage** refers to the set and distribution of records represented in a bibliographic database. Coverage is not uniform across language, country, field, or document type.

Mongeon and Paul-Hus (2016) compare the journals indexed by Web of Science and Scopus with Ulrich's periodical directory and show that both databases disproportionately cover English-language journals and natural and biomedical sciences. This matters not only for bibliometric measurement but also for search: a publication outside a database's indexed record population cannot be retrieved through that database.

Google Scholar differs from selective citation indexes because it uses automated web crawling rather than a fixed journal list. Martín-Martín et al. (2018) find that Google Scholar identifies substantially more citations than Web of Science or Scopus and captures large numbers of non-journal and non-English citing documents. Their comparison found that 19–38% of citations unique to Google Scholar were from non-English documents. Google Scholar therefore provides broader coverage, but broad aggregate coverage does not establish complete article-level retrievability.

The same distinction is visible in newer open bibliographic infrastructure. Céspedes et al. (2025) find substantially greater linguistic diversity in OpenAlex than in Web of Science, but also identify errors and incompleteness in language metadata. Their manually validated estimates suggest that OpenAlex represents multilingual publishing more broadly than Web of Science while still misclassifying some non-English material.

These studies establish **coverage inequality**: the probability that scholarly records enter major bibliographic systems differs across publication environments. Study 1 examines a related but distinct outcome at the paper level. It does not estimate whether a journal or language is covered in aggregate. It asks whether a specific Korean-language paper can currently be retrieved from Google Scholar when its title is known.

### 2.3 Metadata and bibliographic retrievability

A record can only be matched, linked, and retrieved if a system has sufficient bibliographic information to distinguish it from other records. Metadata such as titles, author names, publication dates, persistent identifiers, references, and URLs therefore affect the connection of scholarly records across services. Kemp (2018) describes Crossref metadata as infrastructure used by multiple downstream services for content identification and discoverability and argues that richer, reusable metadata improves the ability of systems to connect research outputs.

Information-retrieval research provides a more precise term for the paper-level issue. **Retrievability** concerns how easily a document can be accessed through the retrieval system across queries (Azzopardi and Vinay 2008). Azzopardi and Vinay's formulation is important here because system coverage and document access are not equivalent: a retrieval system shapes the user's effective view of the collection through the records that queries are capable of surfacing.

Study 1 uses a deliberately minimal operationalization of retrievability. It does not estimate how highly a paper ranks for broad political-science topics. Instead, it asks whether Google Scholar returns a verified bibliographic match when the paper's title is supplied. This is a **known-item retrieval** condition rather than a topical discovery condition. A paper that fails this test is not merely ranked low in a broad search; it is not confirmed even when the query contains the identifying title.

For that reason, throughout Study 1, **Google Scholar visibility** means **verified exact-title retrievability in Google Scholar**, not general prominence, exposure, search ranking, or historical index membership.

### 2.4 Search and recommendation as selection mechanisms

Traditional information retrieval and recommender systems solve related but different selection problems. A retrieval system returns documents in response to a query; classical evaluation distinguishes precision and recall with respect to a defined set of relevant documents (Manning, Raghavan, and Schütze 2008). Research-paper recommender systems instead select publications that a system predicts will be useful or relevant to a user. Reviews of the field document a wide range of content-based, collaborative, citation-based, and hybrid approaches to scholarly recommendation (Beel et al. 2016; Kreutz and Schenkel 2022).

Search systems are therefore not neutral conduits between a fixed literature and a user. Introna and Nissenbaum (2000) showed that search engines systematically assign prominence and exclusion through their technical selection processes. Their argument concerned web search rather than contemporary scholarly LLMs, but the relevant informational property is the same: what a user can consider depends in part on what the retrieval interface exposes.

Web-enabled LLMs add a second selection step because they generate an answer after search. A system may search several pages or records but mention only a subset of them in the final response. Scientific retrieval-augmented language models explicitly separate retrieval from answer synthesis; for example, OpenScholar retrieves passages from a large scholarly corpus before using them to construct a citation-supported answer (Asai et al. 2026). This architecture demonstrates why retrieval and generated output should be measured separately rather than treated as a single event.

General-purpose LLMs introduce an additional bibliographic reliability problem. Walters and Wilder (2023) document fabricated and erroneous bibliographic citations in ChatGPT outputs. Fabrication is distinct from omission: a system can fail by inventing a publication, but it can also recommend valid publications while failing to recover papers that were specified in advance as benchmark items. Study 2 measures both retrieval failure and link validity rather than reducing performance to hallucination alone.

### 2.5 Empirical gap

The literatures above identify three established problems.

First, non-English publication is associated with lower international citation and systematic exclusion from some evidence syntheses (Amano, González-Varo, and Sutherland 2016; Di Bitetti and Ferreras 2017; Konno et al. 2020).

Second, bibliographic databases differ systematically in their linguistic and disciplinary coverage (Mongeon and Paul-Hus 2016; Martín-Martín et al. 2018; Céspedes et al. 2025).

Third, information-retrieval and recommender-system research distinguishes document availability from document retrieval and recommendation (Azzopardi and Vinay 2008; Manning, Raghavan, and Schütze 2008; Beel et al. 2016).

What remains unresolved for the present case are two empirical questions.

1. Among Korean-language papers already demonstrated to have been used in Korean scholarship, is current Google Scholar retrievability associated with a different history of English-language citation?

2. When web-enabled LLMs are asked to recommend scholarship on Korean politics, do Korean-language queries and explicit Korean-database instructions recover pre-specified Korean papers, or do they mainly change the language composition of the papers that happen to be recommended?

Study 1 addresses the first question; Study 2 addresses the second.

---

## 3. Study 1: Google Scholar Retrievability and English-Language Citation

### 3.1 Research question and hypotheses

Study 1 asks whether Korean-language political-science papers that are currently retrievable in Google Scholar have different English-language citation histories from papers that are not retrievable.

The first hypothesis concerns an unconditional difference:

**S1-H1: Current retrievability difference.**
Korean-language papers currently retrievable through exact-title Google Scholar search will have a higher observed probability of English-language citation than papers that are not retrievable.

The second hypothesis concerns changes in that difference over citation cohorts:

**S1-H2: Post-launch divergence.**
Relative to the earliest citation cohort, the difference in English-language citation probability between currently retrievable and nonretrievable papers will be larger in cohorts after Google Scholar's introduction and increasing use.

The second hypothesis is intentionally stated as a cohort comparison rather than an effect of historical indexing. Google Scholar was launched in November 2004, and empirical studies by 2010–2011 documented substantial use of Google and Google Scholar in scholarly information seeking (Jamali and Asadi 2010; Cothran 2011). The data do not identify the date at which each target paper entered Google Scholar.

### 3.2 Sample

Study 1 analyzes **54,789 Korean-language target papers** cited at least once by Korean-language scholarship. The analysis therefore does not compare internationally visible Korean research with arbitrary uncited publications. It starts from a set of papers with documented use within Korean scholarship.

The unit of analysis is the **target paper (j) × English-language citing-paper cohort (c)**. The resulting panel contains **179,230 observations**.

This sample definition is important for interpretation. Study 1 asks why Korean research with demonstrated domestic scholarly use has different rates of entry into English-language citation. It does not estimate citation rates for the entire universe of Korean publications.

### 3.3 Citation cohorts

English-language citing papers are grouped according to publication year:

* **C1:** 2009 or earlier
* **C2:** 2010–2014
* **C3:** 2015–2019
* **C4:** 2020–2024

A target paper contributes observations only to cohorts in which citation was temporally possible. A target published in 2017, for example, does not receive C1 or C2 observations.

For target (j) and cohort (c),

$$
Y_{jc}=1
$$

if at least one English-language source paper published in cohort (c) cites target (j), and

$$
Y_{jc}=0
$$

otherwise.

Thus $Y_{jc}$ measures **citation incidence**, not the total number of citations.

### 3.4 Google Scholar retrievability

The exposure variable $D_j$ is constructed through title-based Google Scholar lookup.

$$
D_j=1
$$

when the search produces a bibliographic result that satisfies the study's pre-specified matching criteria, and

$$
D_j=0
$$

when the lookup completes but no candidate satisfies those criteria.

The analytical sample contains:

* **19,436 Google Scholar-retrievable papers**
* **35,353 nonretrievable papers**

The variable is deliberately called **retrievability** or **exact-title visibility** rather than “discoverability” when discussing Study 1. An exact-title query provides the system with information that a researcher conducting a normal topical search would not necessarily possess. Therefore $D_j$ measures a low-threshold bibliographic condition: whether the known paper can be recovered from Google Scholar. It does not measure ranking for topical queries.

It also measures **current**, not historical, retrievability. A paper coded $D_j=1$ in 2026 may have entered Google Scholar after some of the citations analyzed here occurred.

### 3.5 Estimation

The principal specification is a target-paper fixed-effects linear probability model:

$$
Y_{jc}=\alpha_j+\lambda_c+\sum_{k=2}^{4}\beta_k\left(D_j\times 1[c=k]\right)+\gamma AgeBin_{jc}+\epsilon_{jc}.
$$

Here:

* $\alpha_j$ denotes target-paper fixed effects;
* $\lambda_c$ denotes citation-cohort fixed effects;
* $D_j$ is current Google Scholar retrievability;
* $AgeBin_{jc}$ controls for the target's age in the cohort;
* C1 is the reference cohort.

Because $D_j$ does not vary within a target paper, its main effect is absorbed by $\alpha_j$. The fixed-effects model therefore does **not** estimate whether retrievable papers are intrinsically more cited than nonretrievable papers. That raw difference is reported descriptively for S1-H1.

The interaction coefficient $\beta_k$ instead answers:

> How much larger or smaller is the retrievable–nonretrievable citation-probability difference in cohort (k) than it was in C1?

Standard errors are clustered at the target-paper level.

A second analysis restricts the sample to papers published by **2004**. Every target in this restriction predates the launch of Google Scholar and can contribute to all four citation cohorts. This restriction removes changes in target composition caused by later publications entering only later cohorts. It does not solve the absence of historical indexing dates.

Robustness specifications use:

* Poisson pseudo-maximum likelihood;
* English-language citation counts rather than binary citation incidence;
* journal × cohort fixed effects;
* topic × cohort fixed effects; and
* publication-year × cohort fixed effects.

No opportunity offset is used.

### 3.6 Descriptive results

Currently Google Scholar-retrievable papers have a higher raw English-language citation incidence in every cohort.

| Cohort | (D=1) | (D=0) | Raw difference |
| ------ | ----: | ----: | -------------: |
| C1     | 0.68% | 0.31% |       +0.37 pp |
| C2     | 1.90% | 0.67% |       +1.23 pp |
| C3     | 3.01% | 1.25% |       +1.76 pp |
| C4     | 2.66% | 1.38% |       +1.28 pp |

These descriptive comparisons are consistent with S1-H1. They do not identify the source of the difference because retrievable and nonretrievable papers can differ in journal, publication period, authorship, topic, or other characteristics.

### 3.7 Target-paper fixed-effects results

The fixed-effects results show that the retrievable–nonretrievable citation gap changes across cohorts.

Relative to C1, the gap increases by **0.405 percentage points in C2**:

$$
\beta_2=0.405\text{ pp},
$$

95% CI [0.040, 0.770], $p=.030$.

In C3, the increase relative to C1 is **0.696 percentage points**:

$$
\beta_3=0.696\text{ pp},
$$

95% CI [0.329, 1.063], $p<.001$.

The C2 and C3 coefficients are jointly different from zero:

$$
p<.001.
$$

For C4, the estimated change from C1 is **0.008 percentage points**:

$$
\beta_4=0.008\text{ pp},
$$

95% CI [−0.337, 0.353], $p=.965$.

The results therefore support S1-H2 for C2 and C3, but not for C4. They do not show a monotonic increase in the retrievability gap across all post-2009 cohorts.

### 3.8 Pre-2005 target sample

Restricting the analysis to targets published by 2004 produces the same qualitative boundary.

Relative to C1:

* C2: **+0.791 pp**, 95% CI [0.227, 1.355], $p=.006$
* C3: **+0.496 pp**, 95% CI [0.027, 0.964], $p=.038$
* C4: **+0.273 pp**, 95% CI [−0.175, 0.721], $p=.233$

The joint test for C2 and C3 gives:

$$
p=.011.
$$

| Change in (D) gap from C1 |               Full sample |         Published by 2004 |
| ------------------------- | ------------------------: | ------------------------: |
| C2                        |  +0.405 pp [0.040, 0.770] |  +0.791 pp [0.227, 1.355] |
| C3                        |  +0.696 pp [0.329, 1.063] |  +0.496 pp [0.027, 0.964] |
| C4                        | +0.008 pp [−0.337, 0.353] | +0.273 pp [−0.175, 0.721] |

The pre-2005 restriction matters because cohort composition is fixed: every target is old enough to appear in every citation cohort. The persistence of the C2 and C3 coefficients therefore cannot be attributed solely to later cohorts containing newer target papers.

### 3.9 Robustness and inferential scope

The Poisson results are less stable than the main linear-probability estimates.

Journal × cohort and publication-year × cohort specifications retain positive C2 coefficients, with $p=.086$ and $p=.061$, respectively, but do not reproduce statistically significant C3 or C4 interactions.

A target-fixed-effects Poisson model produces positive C2 and C3 estimates but excludes targets with zero citations in all observed cohorts. It therefore conditions on papers that receive at least one English-language citation and addresses **when citations occur among cited papers**, rather than the broader probability that a target enters English-language citation at all.

The appropriate conclusion is therefore limited:

> Current Google Scholar retrievability distinguishes papers whose English-language citation trajectories diverged in C2 and C3 relative to the earliest cohort.

The results do **not** establish that Google Scholar indexing caused the additional citations. Historical indexing dates are unobserved, current visibility may partly reflect processes that occurred after earlier citations, and several alternative count specifications are less precise.

![Study 1 design, citation incidence, and target-paper fixed-effects estimates](study1_analysis/figures/study1_fig1_design_and_main_results.png){width=100%}

---

## 4. Study 2: Auditing Web-Enabled LLM Search

### 4.1 Research questions

Study 2 examines current scholarly search behavior rather than historical citation.

It asks four specific questions.

1. Under a default English-language general-web prompt, how often do web-enabled LLMs recover a pre-specified Korean benchmark relative to an English-language benchmark?

2. Does using Korean rather than English in the query improve Korean benchmark recovery?

3. Does explicitly instructing the system to search Korean scholarly databases improve Korean benchmark recovery?

4. When a publication is recommended, does the URL supplied by the system provide accessible full text?

### 4.2 Hypotheses

**S2-H1: Default benchmark-recovery gap.**
Under the English-language general-web condition, Korean benchmark papers will be recovered less frequently than English benchmark papers.

**S2-H2: Retrieval intervention.**
Korean-language queries and explicit Korean-database instructions will increase Korean benchmark recovery relative to the English general-web condition.

**S2-H3: Representation–recovery distinction.**
The interventions will increase the Korean-language share of recommendations by more than they increase recovery of the pre-specified Korean benchmark.

**S2-H4: Recommendation–access distinction.**
A recommended publication will not necessarily be accompanied by a link that provides full text without login or payment.

### 4.3 Benchmark corpora

The audit uses two pre-specified 50-paper corpora covering five topics in Korean politics:

1. Korean War
2. South Korean economic development
3. South Korean democratization
4. North Korean nuclear program
5. Korean Wave

For each topic, the benchmark contains:

* ten Korean-language papers selected using DBpia and KISS; and
* ten English-language papers selected using Web of Science and Google Scholar.

The 100 benchmark papers were fixed **before** the LLM audit. This is essential because benchmark recovery requires a denominator that is independent of what the systems subsequently return.

The benchmark is not claimed to contain every relevant paper on the five topics. It is an evaluation set of publications selected before treatment assignment.

### 4.4 Factorial audit design

The experiment crosses three factors:

**Query language**

* English
* Korean

**Source instruction**

* general web
* explicit instruction to search KCI, DBpia, or KISS

**System**

* OpenAI `gpt-5.6-sol`
* Perplexity `sonar-pro`

The design therefore contains four prompt conditions within each system:

1. English + general web
2. English + Korean-database instruction
3. Korean + general web
4. Korean + Korean-database instruction

With five topics, two systems, four prompt conditions, and five independent repetitions:

$$
5\times2\times4\times5=200
$$

stateless executions are observed.

Each execution requests ten scholarly publications in a fixed JSON format.

The 200 executions produce **1,932 valid recommendation occurrences**.

### 4.5 Benchmark recovery

Information-retrieval research conventionally defines recall relative to a set of relevant documents known in advance (Manning, Raghavan, and Schütze 2008). Study 2 uses a related but deliberately narrower measure that this paper calls **benchmark recovery**. The term refers only to whether the pre-specified audit papers are observed; it does not claim that papers outside the benchmark are irrelevant.

For benchmark paper (j) in execution (i):

### TraceRecovery

$$
TraceRecovery_{ij}=1
$$

when benchmark paper (j) appears in the provider's observable search trace.

### Recommendation

$$
Recommendation_{ij}=1
$$

when benchmark paper (j) appears in the final recommendation returned to the user.

### SuppliedLinkAccess

$$
SuppliedLinkAccess_{ij}=1
$$

when benchmark paper (j):

1. appears in the final recommendation, and
2. is accompanied by a system-supplied URL that opens full text without payment or login.

Because the denominator remains all topic-relevant benchmark-paper × execution observations, `SuppliedLinkAccess` is a **joint recovery-and-link-access measure**. It should not be interpreted as the probability of access conditional on recommendation.

Matching uses:

* normalized titles;
* English-title aliases;
* DOI;
* canonical URLs;
* DBpia identifiers; and
* KCI identifiers.

With 200 executions and 20 topic-relevant benchmark papers per execution, the resulting benchmark panel contains:

$$
200\times20=4,000
$$

observations.

### 4.6 Language representation

Benchmark recovery is distinct from the linguistic composition of a system's recommendations.

This paper uses **language representation** as an operational label for:

$$
\frac{\text{number of recommended items classified as Korean-language}}
{\text{all valid recommended items}}.
$$

It is not an information-retrieval recall metric.

Recommendation language is resolved for all 1,932 valid recommendation occurrences.

Search-trace language shares are not compared across systems because provider-level trace observability differs. Using incomplete traces to compare language composition would confound system behavior with differences in what each provider exposes to the audit.

### 4.7 Supplied-link review

All **927 distinct supplied URLs or no-URL item keys** are manually reviewed.

Each item is assigned to one of five categories:

* accessible full text;
* abstract only;
* paywalled;
* broken link;
* hallucinated or unverifiable publication.

For summary analysis:

* **access restricted** = abstract-only + paywalled;
* **invalid or unverifiable** = broken + hallucinated.

This classification evaluates the URL supplied by the LLM. It does not claim that a publication classified as restricted or broken is unavailable from every other location on the web.

### 4.8 Statistical analysis

Benchmark-recovery models use a linear probability specification containing:

* Korean-benchmark indicator;
* Korean-query indicator;
* Korean-database-instruction indicator;
* interactions among these variables; and
* system indicator.

The interaction terms estimate whether changing the query language or source instruction changes the Korean–English benchmark recovery gap.

Standard errors are multiway clustered by benchmark paper and execution.

Language-representation models use execution-level Korean-language recommendation shares as the dependent variable. Predictors are:

* Korean query;
* Korean-database instruction;
* their interaction; and
* system.

HC3 standard errors are used.

Recommendation-link models use item-level link outcomes and include:

* recommended-item language;
* prompt condition; and
* system,

with clustering by unique supplied-link/item key and execution.

### 4.9 Default English general-web condition

Under the English-language general-web condition, neither system recovers a Korean benchmark paper at any measured stage.

Korean benchmark recovery is:

* trace: **0.0%**
* recommendation: **0.0%**
* supplied-link access: **0.0%**

English benchmark recovery is also low, but nonzero:

* trace: **3.4%**
* recommendation: **3.2%**
* supplied-link access: **0.6%**

The corresponding Korean–English differences are:

* trace: **−3.4 pp**, $p=.029$
* recommendation: **−3.2 pp**, $p=.015$
* supplied-link access: **−0.6 pp**, $p=.311$

The supplied-link comparison has a floor problem because almost no benchmark item from either language reaches that outcome.

These results support S2-H1 for trace recovery and recommendation.

They also show that the problem is not exclusively Korean-language retrieval: even the English benchmark has low absolute recovery. The language comparison concerns the **additional deficit** for the Korean benchmark under the default condition.

### 4.10 Korean-language and Korean-database interventions

The interventions improve Korean benchmark recovery relative to the English benchmark.

The Korean-language query reduces the Korean–English trace-recovery gap by **3.8 percentage points**:

$$
p=.016.
$$

The Korean-database instruction reduces the gap by:

* **4.0 pp** for trace recovery, $p=.017$;
* **3.2 pp** for recommendation, $p=.012$.

When both interventions are applied, the Korean–English gap relative to baseline changes by:

* **5.6 pp** for trace recovery;
* **6.4 pp** for recommendation.

Under the combined Korean-query + Korean-database condition:

* **2.2%** of Korean benchmark papers are recovered in the trace;
* **3.2%** are included in recommendations.

The English benchmark recovery rate in that condition is zero.

This is a reversal of the **relative** Korean–English difference, not evidence of high Korean recall. At a 3.2% recommendation rate, more than **96% of benchmark-paper opportunities remain unrecovered in a given execution.**

S2-H2 is therefore supported in relative terms, while absolute benchmark recovery remains low.

### 4.11 Representation versus benchmark recovery

The effect of the interventions is much larger when the outcome is the language composition of the recommendations.

The Korean-language share of recommendation occurrences is:

| Prompt condition                | Korean-language share |
| ------------------------------- | --------------------: |
| English + general web           |                  0.0% |
| English + Korean DB instruction |                 35.3% |
| Korean + general web            |                 55.8% |
| Korean + Korean DB instruction  |             **91.2%** |

Among items with accessible supplied links, the corresponding Korean-language shares are:

* 0.0%
* 26.6%
* 57.5%
* 94.9%

The contrast with benchmark recovery is large. Under the combined condition, **91.2% of recommended items are Korean-language, but only 3.2% of the pre-specified Korean benchmark-paper opportunities are recovered.**

This result supports S2-H3.

The inference is specific:

> A high Korean-language share is not evidence that the system has recovered the Korean papers fixed in advance as the evaluation benchmark.

It does not imply that non-benchmark Korean papers are irrelevant. It shows that **linguistic composition and benchmark recall are different evaluation quantities**.

### 4.12 Recommendation versus supplied-link access

Across all **1,932 recommendation occurrences**:

* **854 (44.2%)** provide accessible full text;
* **859 (44.5%)** are access restricted;
* **219 (11.3%)** are invalid or unverifiable.

The restricted category consists of:

* 247 abstract-only items;
* 612 paywalled items.

The invalid or unverifiable category consists of:

* 176 broken links;
* 43 hallucinated items.

Thus:

* broken link: **9.1%**
* hallucinated item: **2.2%**

| Supplied-link outcome   | Overall | Korean-language item | English-language item |
| ----------------------- | ------: | -------------------: | --------------------: |
| Accessible              |   44.2% |                46.3% |                 42.4% |
| Access restricted       |   44.5% |                47.9% |                 41.6% |
| Invalid or unverifiable |   11.3% |                 5.8% |                 16.0% |
| — Broken link           |    9.1% |                 3.3% |                 14.1% |
| — Hallucinated item     |    2.2% |                 2.6% |                  1.9% |

Because only 44.2% of recommendation occurrences are accompanied by accessible full text, S2-H4 is supported.

After prompt condition and system are controlled, recommended-item language is not independently associated with whether the supplied link is accessible, restricted, or invalid. The raw Korean–English differences in the table therefore should not be interpreted as an effect of publication language on link access.

![Study 2 design, benchmark recovery, representation, and supplied-link outcomes](/Users/hyowonkim/SciSci-LLM-audit/outputs/figures/study2_global_figure.png){width=100%}

---

## 5. What the Two Studies Establish

Study 1 and Study 2 measure different outcomes and should not be concatenated into an unobserved sequence from Google Scholar indexing to LLM recommendation to citation.

Study 1 establishes a relationship between:

> **current exact-title Google Scholar retrievability**
> and
> **historical English-language citation trajectories**

for Korean-language papers already cited within Korean scholarship.

Study 2 establishes experimental differences in:

> **benchmark retrieval, final recommendation, and supplied-link access**

under alternative prompt conditions in two current web-enabled LLM systems.

The common finding is therefore narrower than a claim that one mechanism links all stages.

### First, bibliographic presence does not imply equal retrieval.

Bibliographic databases differ in their coverage of language and publication venues (Mongeon and Paul-Hus 2016; Martín-Martín et al. 2018; Céspedes et al. 2025), and Study 1 shows a consequential paper-level division within Korean scholarship: papers that can currently be verified through exact-title Google Scholar search have different English-language citation histories from those that cannot.

### Second, language representation does not measure benchmark recovery.

Study 2's strongest contrast is numerical:

$$
91.2%\text{ Korean-language recommendations}
$$

versus

$$
3.2%\text{ Korean benchmark recommendation recovery}.
$$

A recommendation list can therefore be overwhelmingly Korean-language without reproducing the set of Korean publications fixed before the audit.

### Third, recommendation does not imply full-text access through the supplied link.

Only **44.2%** of recommendation occurrences are linked by the system to accessible full text.

This distinction matters because recommendation and access are different system outputs. The experiment evaluates the URL chosen by the system, not all possible locations from which the publication could potentially be obtained.

### Fourth, the C4 result in Study 1 should not be interpreted as evidence about generative search.

The C4 interaction is statistically indistinguishable from zero. This means that the retrievable–nonretrievable citation gap does not increase further relative to C1 in the 2020–2024 citation cohort.

It does not establish that discovery inequality disappeared after 2020, and it cannot identify an effect of generative search. Most of C4 predates widespread web-enabled LLM search, and publications in the later years of that cohort have had less time to accumulate citations.

Study 2 is the direct evidence about current generative search; C4 is not.

---

## 6. Implications

The results identify different intervention targets for different search environments.

For bibliographic search, the relevant problem is **record-level retrievability**. Existing metadata research shows that titles, identifiers, publication dates, references, and stable links are reused across scholarly discovery services (Kemp 2018), while recent work on OpenAlex demonstrates that expanding database coverage does not by itself eliminate metadata errors for multilingual publications (Céspedes et al. 2025).

For LLM search, the relevant evaluation problem is **retrieval performance**, not simply whether the output contains Korean-language text or Korean-language publications. Standard information-retrieval evaluation uses a pre-specified relevant set to distinguish recall from other properties of returned results (Manning, Raghavan, and Schütze 2008). The Study 2 result demonstrates why that distinction is necessary for multilingual scholarly search.

The empirical results do not estimate the causal effect of specific metadata reforms. The following interventions should therefore be treated as implications of the observed failure points combined with existing metadata and information-retrieval research, not as treatments tested in this paper:

1. deposit both Korean and English titles and abstracts where available;
2. provide accurate publication years and author metadata;
3. increase DOI or other persistent-identifier coverage;
4. expose bibliographic records through reusable services such as Crossref and OpenAlex;
5. provide stable publication landing pages and full-text links;
6. evaluate scholarly search systems against pre-specified local-language benchmarks rather than reporting only the language composition of outputs.

These interventions differ from a policy of requiring full-text publication in English. Their target is the **machine-readable bibliographic record and the retrieval system**, not the language in which the substantive research must be written.

---

## 7. Limitations

Study 1 has a temporal identification limitation.

$D_j$ measures Google Scholar retrievability in 2026. The analysis does not observe when each target first became retrievable. Consequently, the target fixed effects eliminate time-invariant differences among papers but cannot establish that Google Scholar visibility preceded the citation changes measured in C2 and C3.

Current retrievability may also be partly endogenous to earlier scholarly circulation. Papers that accumulated citations may subsequently have acquired better metadata, more web copies, or stronger linkage into systems indexed by Google Scholar.

For these reasons, the Study 1 result should be described as a **cohort-specific association between current retrievability and historical citation trajectories**, not a causal estimate of Google Scholar indexing.

The fixed-effects linear probability result is also stronger than several Poisson robustness results. The conclusion should therefore preserve the observed model dependence: the C2–C3 divergence is present in the main incidence model and the pre-2005 restriction but is not statistically reproduced in every count-model specification.

Study 2 has a different set of limitations.

The audit includes:

* two systems;
* five topics;
* one collection period;
* 100 pre-specified benchmark papers.

The benchmark is an evaluation set, not an exhaustive definition of all relevant scholarship on each topic.

Trace observability also differs across providers. This is why trace-language composition is not compared across systems.

Recommendation events for benchmark papers are sparse, which limits precision, particularly at the supplied-link-access stage.

Finally, the manual link audit evaluates the **system-supplied URL**. A broken, paywalled, or abstract-only supplied link does not establish that the publication is unavailable elsewhere.

Neither study observes what researchers do after encountering a paper. Reading, topical relevance, perceived quality, citation norms, and publication language can all affect the transition from discovery to citation. The empirical contribution is limited to demonstrating inequalities that occur **before or at the point of retrieval and recommendation**.

---

## 8. Conclusion

Research published in Korean can be used within Korean political science yet remain weakly represented in the search processes through which English-language scholars identify literature.

Study 1 analyzes 54,789 such papers and finds that current exact-title Google Scholar retrievability is associated with different English-language citation trajectories. Relative to the earliest citation cohort, the retrievable–nonretrievable citation gap increases in 2010–2014 and 2015–2019, but not in 2020–2024. Because historical Google Scholar indexing dates are unavailable, these estimates identify temporal alignment rather than a causal indexing effect.

Study 2 directly audits current search behavior. Under the English general-web condition, neither tested system recovers a Korean benchmark paper. Korean-language queries and Korean-database instructions improve relative benchmark recovery, but the highest recommendation recovery remains 3.2% per execution. At the same time, those interventions can raise the Korean-language share of recommendation occurrences to 91.2%. The two outcomes therefore cannot be treated as substitutes. A list can contain predominantly Korean-language scholarship while still omitting almost all of the pre-specified Korean benchmark.

Recommendation also does not imply access through the system's own link: only 44.2% of recommendation occurrences are linked to accessible full text.

This paper uses **discovery bottleneck** to name these empirically observed failures of retrieval before substantive evaluation. The concept does not replace established explanations based on English-language dominance. It specifies an additional condition: **a publication cannot be read, translated, evaluated, or cited through a search system unless that system first returns it to the user.**

For Korean political science, both an established scholarly search engine and current web-enabled LLM search exhibit measurable failures at that prior stage.

---

## References

Amano, Tatsuya, Juan P. González-Varo, and William J. Sutherland. 2016. “Languages Are Still a Major Barrier to Global Science.” *PLOS Biology* 14(12): e2000933. [https://doi.org/10.1371/journal.pbio.2000933](https://doi.org/10.1371/journal.pbio.2000933).

Asai, Akari, Jacqueline He, Rulin Shao, et al. **2026**. “Synthesizing Scientific Literature with Retrieval-Augmented Language Models.” *Nature* 650: 857–863. [https://doi.org/10.1038/s41586-025-10072-4](https://doi.org/10.1038/s41586-025-10072-4).

Azzopardi, Leif, and Vishwa Vinay. 2008. “Retrievability: An Evaluation Measure for Higher Order Information Access Tasks.” In *Proceedings of the 17th ACM Conference on Information and Knowledge Management*, 561–570. [https://doi.org/10.1145/1458082.1458157](https://doi.org/10.1145/1458082.1458157).

Beel, Joeran, Bela Gipp, Stefan Langer, and Corinna Breitinger. 2016. “Research-Paper Recommender Systems: A Literature Survey.” *International Journal on Digital Libraries* 17(4): 305–338. [https://doi.org/10.1007/s00799-015-0156-0](https://doi.org/10.1007/s00799-015-0156-0).

Bowker, Geoffrey C., and Susan Leigh Star. 1999. *Sorting Things Out: Classification and Its Consequences*. Cambridge, MA: MIT Press.

Céspedes, Lucía, Diego Kozlowski, Carolina Pradier, et al. 2025. “Evaluating the Linguistic Coverage of OpenAlex: An Assessment of Metadata Accuracy and Completeness.” *Journal of the Association for Information Science and Technology* 76(6): 884–895. [https://doi.org/10.1002/asi.24979](https://doi.org/10.1002/asi.24979).

Cothran, Tanya. 2011. “Google Scholar Acceptance and Use among Graduate Students: A Quantitative Study.” *Library & Information Science Research* 33(4): 293–301. [https://doi.org/10.1016/j.lisr.2011.02.001](https://doi.org/10.1016/j.lisr.2011.02.001).

Di Bitetti, Mario S., and Julián A. Ferreras. 2017. “Publish (in English) or Perish: The Effect on Citation Rate of Using Languages Other than English in Scientific Publications.” *Ambio* 46(1): 121–127. [https://doi.org/10.1007/s13280-016-0820-7](https://doi.org/10.1007/s13280-016-0820-7).

Introna, Lucas D., and Helen Nissenbaum. 2000. “Shaping the Web: Why the Politics of Search Engines Matters.” *The Information Society* 16(3): 169–185. [https://doi.org/10.1080/01972240050133634](https://doi.org/10.1080/01972240050133634).

Jamali, Hamid R., and Saeid Asadi. 2010. “Google and the Scholar: The Role of Google in Scientists' Information-Seeking Behaviour.” *Online Information Review* 34(2): 282–294. [https://doi.org/10.1108/14684521011036990](https://doi.org/10.1108/14684521011036990).

Kemp, Jennifer. 2018. “Metadata and Discoverability: A Use Case Overview.” *Information Services & Use* 38(1–2): 131–141. [https://doi.org/10.3233/ISU-180004](https://doi.org/10.3233/ISU-180004).

Kim, Hyowon. 2025. *Two Spheres of Korean Politics: Knowledge Production and Dissemination across Linguistic Divides*. Ann Arbor, MI: Inter-university Consortium for Political and Social Research. [https://doi.org/10.3886/E240683V1](https://doi.org/10.3886/E240683V1).

Konno, Ko, Munemitsu Akasaka, Chieko Koshida, Naoki Katayama, Noriyuki Osada, Rebecca Spake, and Tatsuya Amano. 2020. “Ignoring Non-English-Language Studies May Bias Ecological Meta-Analyses.” *Ecology and Evolution* 10(13): 6373–6384. [https://doi.org/10.1002/ece3.6368](https://doi.org/10.1002/ece3.6368).

Kreutz, Christin Katharina, and Ralf Schenkel. 2022. “Scientific Paper Recommendation Systems: A Literature Review of Recent Publications.” *International Journal on Digital Libraries* 23: 335–369.

Manning, Christopher D., Prabhakar Raghavan, and Hinrich Schütze. 2008. *Introduction to Information Retrieval*. Cambridge: Cambridge University Press.

Martín-Martín, Alberto, Enrique Orduna-Malea, Mike Thelwall, and Emilio Delgado López-Cózar. 2018. “Google Scholar, Web of Science, and Scopus: A Systematic Comparison of Citations in 252 Subject Categories.” *Journal of Informetrics* 12(4): 1160–1177. [https://doi.org/10.1016/j.joi.2018.09.002](https://doi.org/10.1016/j.joi.2018.09.002).

Mongeon, Philippe, and Adèle Paul-Hus. 2016. “The Journal Coverage of Web of Science and Scopus: A Comparative Analysis.” *Scientometrics* 106: 213–228. [https://doi.org/10.1007/s11192-015-1765-5](https://doi.org/10.1007/s11192-015-1765-5).

Star, Susan Leigh, and Karen Ruhleder. 1996. “Steps Toward an Ecology of Infrastructure: Design and Access for Large Information Spaces.” *Information Systems Research* 7(1): 111–134. [https://doi.org/10.1287/isre.7.1.111](https://doi.org/10.1287/isre.7.1.111).

Walters, William H., and Esther I. Wilder. 2023. “Fabrication and Errors in the Bibliographic Citations Generated by ChatGPT.” *Scientific Reports* 13: 14045. [https://doi.org/10.1038/s41598-023-41032-5](https://doi.org/10.1038/s41598-023-41032-5).
