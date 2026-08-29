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

## 국문초록

본 논문은 한국 정치 연구의 국제적 가시성을 이해하려면 출판과 인용뿐 아니라 어떤 문헌이 학술검색에서 실제 검토 가능한 후보로 나타나는지도 분석해야 한다고 주장한다. 한국 정치 연구는 한국어권과 영어권의 구분된 학술공간에서 생산·유통되며, 두 공간에서 축적된 연구가 국제적으로 발견되고 인용되는 범위도 동일하지 않다(Rhee 2026; Kim et al. 2025). 본 연구는 한국어권에서 이미 사용되거나 주요 문헌으로 확인된 연구가 Google Scholar와 생성형 검색에서 어떻게 가시화되는지를 분석하고, 검색환경이 제공하는 링크를 통한 원문 접근은 별도의 결과로 다룬다.

Study 1은 2000–2025년에 생산된 한국어권 정치학 논문들이 인용한 한국 정치 관련 논문 54,789편을 대상으로 2026년 현재 Google Scholar index presence와 영어권 인용확률의 시기별 관계를 분석한다. 현재 bibliographic record가 확인된 논문과 확인되지 않은 논문의 영어권 인용확률 격차는 2009년까지의 기준기간에 비해 2010–2014년에 0.405퍼센트포인트(pp), 2015–2019년에 0.696pp 유의하게 더 컸으나 2020–2024년에는 추가 확대되지 않았다. 현재 Google Scholar가 제공하는 링크를 통한 원문 접근은 index presence가 확인된 논문들 사이에서 영어권 인용확률과 유의한 관계를 보이지 않았다. 이는 현재 index presence와 과거 영어권 인용궤적의 연관성이며 Google Scholar의 인과효과가 아니다.

Study 2는 한국어권과 영어권에서 모두 연구되어 온 다섯 개의 한국 정치 주제에서 사전에 선정한 한국어 논문 50편과 영어 논문 50편을 기준으로 두 개의 web-enabled generative search system을 감사한다. 영어 질의와 일반 웹검색을 사용한 baseline에서는 한국어 benchmark가 관찰 가능한 검색흔적과 최종 추천에서 모두 회수되지 않은 반면 영어 benchmark는 각각 3.4%와 3.2% 회수되었다. 한국어 질의와 한국 학술 데이터베이스 검색 지시를 함께 적용하면 한국어–영어 격차는 검색에서 5.6pp, 추천에서 6.4pp 축소되었지만 한국어 benchmark의 최종 추천 회수율은 3.2%에 머물렀다. 전체 추천의 44.2%만 제공된 링크를 통해 원문에 직접 접근할 수 있었으며 원문 접근에서는 유의한 언어격차가 확인되지 않았다.

두 연구의 공통된 결론은 검색결과의 언어적 구성과 특정 학술공간의 주요 문헌이 실제로 회수되는 정도를 구분해야 한다는 것이다. 생성형 검색에서 한국어 논문이 많이 제시되어도 한국어권에서 축적된 주요 연구가 그만큼 충실하게 반영되었다고 볼 수는 없다. 본 논문은 문헌이 내용에 대한 실질적 평가를 받기 전에 검색 또는 최종 출처 선택의 관찰 가능한 단계에서 가시성을 잃는 현상을 discovery bottleneck이라는 조작적 개념으로 제시한다.

Keywords: 한국 정치학; 한국 정치 연구; 학술검색; Google Scholar; 생성형 검색; 비영어권 학술문헌; 국제적 가시성; 원문 접근; discovery bottleneck

# 1. 서론

본 논문의 핵심 주장은 한국 정치 연구의 국제적 가시성을 출판과 인용만으로 파악할 수 없다는 것이다. 연구자가 선행연구를 구성하는 검색단계에서 어떤 문헌이 후보로 나타나고 최종 출처로 선택되는지도 별도의 가시성 결과이다. 관련 연구가 검색결과에 나타나지 않으면 연구자는 그 내용을 평가하기 전에 해당 문헌을 검토대상에서 제외하게 될 수 있다.

이 문제는 정치학 지식의 국제적 분포가 이미 지역과 언어에 따라 불균등하다는 점에서 중요하다. 주요 정치학 학술지의 연구대상은 오랫동안 북미와 서유럽에 집중되어 왔고, 국제적 출판에서도 연구자의 지리적·제도적 위치에 따른 불균형이 관찰된다(Wilson and Knutsen 2022; Breuning et al. 2018). 주요 국제 학술 데이터베이스 역시 영어권 학술지를 상대적으로 많이 포괄하며, 비영어로 출판된 연구는 영어 논문보다 국제 인용에서 불리한 경향을 보인다(Mongeon and Paul-Hus 2016; Vera-Baceta, Thelwall, and Kousha 2019; Di Bitetti and Ferreras 2017).

한국 정치 연구는 이러한 분화를 분석하기에 적절한 사례이다. KCI와 SSCI를 중심으로 유통되는 한국 정치학 연구는 주제와 방법론에서 서로 다른 패턴을 보이며(Rhee 2026), 한국 정치에 관한 한국어권과 영어권 연구도 생산, 유통, 국제적 인용 범위에서 구분되는 학술공간을 형성한다(Kim et al. 2025).[^1] 따라서 한국어권에 상당한 연구가 축적되어 있다는 사실만으로 그 연구가 국제적 학술환경에서 같은 정도로 발견되고 검토된다고 가정할 수 없다.

이 논문은 학술적 존재와 검색 가시성을 구분하여 이 문제를 분석한다. 어떤 논문이 출판되어 있거나 데이터베이스의 전체 coverage에 포함되는 것과 특정 검색환경에서 개별 문헌이 실제 검토대상으로 나타나는 것은 동일하지 않다. 정보검색 연구가 database-level coverage와 document-level retrievability를 구분해 온 것도 이 차이 때문이다(Azzopardi and Vinay 2008). 원문 접근도 별도 결과이다. 논문이 검색되더라도 제공된 URL이 paywall, abstract page 또는 broken link로 이어질 수 있고, 반대로 publisher version이 유료여도 repository나 저자 공개본을 이용할 수 있다(Jamali and Nabavi 2015). 본 연구는 일반적인 OA 여부가 아니라 각 검색환경이 실제 제공한 링크가 로그인이나 결제 없이 full text로 연결되는지를 측정한다.

Study 1은 현재 Google Scholar index presence와 영어권 인용의 시기별 관계를 분석한다. 분석대상은 2000–2025년에 생산된 한국어권 정치학 논문에서 적어도 한 번 인용된 한국 정치 관련 문헌 54,789편이다. 모든 target paper가 한국어권에서 실제 사용되었다는 공통 조건 아래, 현재 bibliographic record가 확인되는 논문과 확인되지 않는 논문의 영어권 인용확률 격차가 시기에 따라 어떻게 나타나는지를 비교한다. Google Scholar 상태는 2026년에만 관찰되므로 이 분석은 과거 indexing이 영어권 인용을 발생시켰는지를 추정하지 않는다.

Study 2는 생성형 검색에서 검색과 최종 출처 선택을 구분한다. Web-enabled generative search는 외부 자료를 검색한 뒤 일부만 citation이나 recommendation으로 선택하여 답변을 구성한다(Liu, Zhang, and Liang 2023; He et al. 2025). Study 2는 한국어권과 영어권에서 모두 연구되어 온 동일한 한국 정치 주제에 대해 query language와 한국 학술 데이터베이스 검색 지시를 변화시키고, 사전에 정한 한국어와 영어 benchmark가 공개된 search trace와 최종 recommendation에 각각 나타나는지를 비교한다. 또한 전체 추천의 한국어 논문 비율과 사전 지정 한국어 benchmark의 회수율을 구분한다.

두 Study는 검색, 원문 접근, 인용으로 이어지는 하나의 인과과정을 구성하지 않는다. Study 1은 현재 Google Scholar index presence와 과거 영어권 인용궤적의 관계를 보여주고, Study 2는 현재 생성형 검색의 검색 및 선택 결과를 직접 관찰한다. 두 연구가 공유하는 질문은 한국어권에서 존재하고 실제 사용되는 연구 가운데 어떤 문헌이 국제적으로 이용되는 검색환경에서 검토 가능한 후보로 나타나는가이다.

본 논문은 문헌이 실질적 내용 평가에 도달하기 전에 검색 또는 최종 출처 선택에서 가시성을 잃는 현상을 discovery bottleneck이라고 부른다. 이는 검색기술이 국제적 인용격차를 단독으로 발생시킨다는 주장이 아니라 특정 검색환경에서 관찰되는 누락을 지칭하는 조작적 개념이다.

논문의 구성은 다음과 같다. 2절은 국제적 지식 불균형에 관한 연구를 scholarly discovery의 문제와 연결하고, Google Scholar와 생성형 검색에서 구분해야 할 분석단계를 제시한다. 3절과 4절은 각각 Study 1과 Study 2의 설계와 결과를 보고한다. 5절은 두 연구가 공유하는 함의와 서로 결합할 수 없는 증거의 범위를 구분하며, 6절과 7절은 결론과 한계를 제시한다.

# 2. 선행연구

## 2.1 국제 정치학의 가시성과 언어적 학술공간

이 절의 출발점은 국제적으로 관찰되는 정치학 지식이 여러 지역과 언어에서 생산된 연구 전체와 일치하지 않는다는 것이다. 어떤 연구가 중심적 학술공간에 진입하고 유통되는가는 연구대상, 연구자의 위치, 출판언어에 따라 불균등하게 구성되어 왔다.

연구대상 측면에서 주요 정치학 학술지는 역사적으로 북미와 서유럽에 집중되어 왔으며, 이러한 편중은 특정 지역에서 형성된 기술적·인과적 주장이 정치학 전체로 일반화되는 범위와 관련된다(Wilson and Knutsen 2022). 지식 생산자 측면에서도 국제 정치학의 핵심 학술지에는 Global South 연구자의 대표성이 낮고 특정 연구기관 소속 연구자가 과대표되는 경향이 확인된다(Breuning et al. 2018).

출판언어와 bibliographic infrastructure는 또 다른 선택기제이다. Web of Science와 Scopus는 전체 학술지 모집단에 비해 영어권 학술지를 상대적으로 많이 포괄하고(Mongeon and Paul-Hus 2016; Vera-Baceta, Thelwall, and Kousha 2019), 다언어 출판환경에서도 비영어 논문은 다른 출판특성을 고려한 뒤 영어 논문보다 낮은 citation rate를 보인다(Di Bitetti and Ferreras 2017). 따라서 database coverage와 citation visibility 자체가 언어에 따라 선택적으로 구성될 수 있다.

한국 정치 연구에서도 이 분화가 나타난다. KCI와 SSCI에 출판되는 연구는 주제와 방법론적 구성에서 차이를 보이며(Rhee 2026), 한국어권과 영어권의 한국 정치 연구는 국제적 인지도와 인용 범위에서도 서로 다른 패턴을 보인다(Kim et al. 2025). 이 사례가 제기하는 질문은 단순한 언어별 citation difference가 아니다. 동일한 정치현상에 대해 한국어권에서 축적된 구체적인 연구가 국제적 학술정보 환경에서 어느 정도 검토 가능한가라는 질문이다.

기존 연구는 publication, database coverage, citation의 불균형을 보여주지만 연구자가 실제로 문헌을 발견하는 과정은 별도의 분석 수준이다. 정보검색 연구는 데이터베이스 수준의 coverage와 개별 문헌 수준의 retrievability를 구분한다(Azzopardi and Vinay 2008). 본 연구는 이 구분을 aggregate coverage만으로 개별 논문의 검색 가시성을 판단할 수 없다는 개념적 근거로 사용한다.

## 2.2 Google Scholar의 coverage, index presence, 그리고 원문 접근

Google Scholar에 관한 핵심 구분은 넓은 aggregate coverage가 모든 개별 논문의 index presence나 원문 접근을 보장하지 않는다는 것이다. Study 1은 이 세 속성을 구분한 뒤, 한국어권에서 실제 사용된 문헌의 paper-level index presence에 초점을 둔다.

Google Scholar는 Web of Science와 Scopus보다 더 넓은 범위의 문헌과 인용을 포착하며, 추가로 확인되는 자료에는 비영어 문헌과 비학술지 자료도 상당수 포함된다(Chen 2010; Martín-Martín et al. 2018b, 2021). 선택적 국제 citation index에서 충분히 포착되지 않는 연구가 Google Scholar에서는 확인될 수 있다는 점에서 이러한 coverage는 비영어권 문헌의 가시성과 관련된다.

그러나 외부 bibliographic record와 비교한 연구에서도 Google Scholar에서 반환되지 않는 publication이 보고되어 왔다(Delgado-Quirós et al. 2024). 특정 언어나 분야에 대한 broad coverage와 개별 논문의 bibliographic record가 실제로 확인되는지는 따라서 분석적으로 다른 속성이다.

Paper-level index presence가 중요한 이유는 Google Scholar가 실제 scholarly discovery에서 널리 사용되기 때문이다. 연구자와 대학원생의 정보탐색에서 Google과 Google Scholar의 이용이 반복적으로 확인되었고(Jamali and Asadi 2010; Cothran 2011), 최근 faculty survey에서도 사회과학 연구자가 새로운 학술문헌을 찾는 주요 시작점 가운데 하나로 나타난다(Blankstein 2022). 이 이용 자체가 citation을 발생시킨다는 뜻은 아니지만, index presence가 실제 문헌탐색 환경에서 관찰되는 속성임은 분명하다.

원문 접근은 index presence와 다시 구분된다. Google Scholar는 publisher site뿐 아니라 repository와 기타 웹 출처에서 확인되는 version으로 연결할 수 있으며, 상당수 문헌에 무료 full-text link를 제공한다(Jamali and Nabavi 2015; Martín-Martín et al. 2018a). 그럼에도 indexed paper가 paywall이나 abstract page로만 연결될 수 있고, 웹에 무료 version이 존재해도 Google Scholar가 해당 version을 제시하지 않을 수 있다.

이 구분에 따라 Study 1은 Google Scholar 전체의 coverage를 다시 추정하지 않는다. 한국어권 citation record라는 공통 조건을 가진 문헌 안에서 현재 index presence가 확인되는 집단과 확인되지 않는 집단의 역사적 영어권 인용패턴을 비교하고, 제공 링크를 통한 원문 접근은 보조 결과로 분석한다.

## 2.3 생성형 학술검색과 문헌 선택

생성형 검색의 핵심적인 특징은 retrieval 뒤에 final source selection이 추가된다는 것이다. Web-enabled LLM은 검색된 자료 전체를 그대로 반환하지 않고 일부를 citation이나 recommendation으로 선택해 답변을 구성한다. 따라서 어떤 문헌이 공개된 search trace에 나타나는지와 최종 출처로 제시되는지를 분리해야 한다(Liu, Zhang, and Liang 2023).

최근 학술검색 연구는 생성된 목록의 표면적 타당성보다 사전에 정한 문헌이 실제로 회수되는지를 평가한다. LitSearch는 시스템 실행과 독립적으로 target paper를 정의한 뒤 검색성능을 평가하고(Ajith et al. 2024), PaSa와 같은 academic-search agent도 query–paper benchmark를 사용한다(He et al. 2025). 이는 사전에 정의된 relevant set으로 검색성능을 평가하는 정보검색의 전통과 연결된다(Manning, Raghavan, and Schütze 2008). LLM 기반 scholar recommendation audit도 외부 benchmark를 이용해 사전 지정 연구자나 문헌의 추천 여부를 측정한다(Espín-Noboa and Méndez 2026). 다만 LLM 기반 literature search는 빠르게 확산되고 있지만 체계적 문헌고찰과 같은 엄격한 검색과정에서 충분히 확립되지는 않았다(Lieberum et al. 2025; Asai et al. 2026).

외부 benchmark는 비영어권 문헌을 평가할 때 특히 중요하다. 한국어 논문이 결과에 많이 포함되었다는 사실은 한국어권의 주요 연구가 충분히 반영되었다는 증거가 아니다. 검색조건에 따라 한국어 논문이 다수 추천되어도 한국어권에서 주요하게 다뤄진 특정 연구가 거의 포함되지 않을 수 있기 때문이다. 최종 추천의 언어적 구성과 사전 지정 한국어 benchmark의 recovery는 따라서 다른 질문에 답한다.

검색조건도 중요한 분석대상이다. 생성형 검색결과는 source authority, 지리적 위치, 기관 또는 상업적 출처에 따라 달라질 수 있다(Liu, Zhang, and Liang 2023; Li and Sinnamon 2024). 한국어권과 영어권 문헌이 서로 다른 데이터베이스와 출판경로를 통해 유통되는 경우 query language와 한국 학술정보원 검색 지시는 검색되는 문헌과 최종 출처를 바꿀 수 있다.

Study 2는 이 논의를 세 개의 관찰 가능한 결과로 조작화한다. 첫째, benchmark paper가 provider가 공개한 search trace에서 확인되는지를 측정한다. 둘째, 그 문헌이 최종 recommendation에 포함되는지를 측정한다. 셋째, 제공된 링크가 로그인이나 결제 없이 full text로 연결되는지를 측정한다. Search trace는 내부 retrieval 전체가 아니지만, 이 구분을 통해 관찰 가능한 검색, 최종 선택, 원문 접근의 누락을 서로 분리할 수 있다.

# 3. Study 1: Google Scholar Index Presence와 영어권 인용

## 3.1 데이터와 변수

Study 1은 한국어권 정치학에서 이미 사용된 한국 정치 관련 문헌 가운데 현재 Google Scholar index presence가 확인되는 논문과 그렇지 않은 논문의 영어권 인용확률이 시기에 따라 어떻게 다른가를 분석한다.

분석대상은 2000–2025년에 생산된 한국어권 정치학 논문들이 인용한 한국 정치 관련 논문 54,789편이다. 표본에 포함되려면 이 기간의 한국어권 정치학 문헌에서 적어도 한 번 인용되어야 한다. 따라서 한국어권에서만 인용된 논문과 한국어권 및 영어권 양쪽에서 인용된 논문이 함께 포함된다.

영어권 인용은 누적 citation count 하나로 합치지 않고 citation cohort별 incidence로 구성한다.

* C1: 2009년까지
* C2: 2010–2014
* C3: 2015–2019
* C4: 2020–2024

C1은 이후 cohort와 비교하기 위한 기준기간이며 Google Scholar 도입 이전의 검색환경을 의미하지 않는다. 2010년 이후에는 동일한 5년 구간을 사용한다.

Target paper는 해당 cohort에서 실제로 인용될 시간적 기회가 있었던 경우에만 포함한다. Target \(j\)와 cohort \(c\)에 대해,

$$
Y_{jc}=1
$$

은 해당 기간의 영어권 source paper가 target을 적어도 한 번 인용한 경우이며, 그렇지 않으면 0이다. 최종 panel은 179,230개의 target-paper × cohort observation으로 구성된다.

주요 변수 \(D_j\)는 2026년 현재 Google Scholar index presence이다. 가능한 한국어 제목, 영어 제목, reference-title variant를 사용해 검색하고 사전에 정한 bibliographic matching 기준을 충족하는 Google Scholar record가 확인되면 \(D_j=1\)로 코딩한다. 검색을 완료했지만 확인 가능한 matching record를 찾지 못하면 \(D_j=0\)으로 코딩한다. 표본에는 \(D_j=1\)인 논문 19,436편과 \(D_j=0\)인 논문 35,353편이 있다.

Google Scholar는 전체 index의 공개 목록을 제공하지 않으므로, 여기서 index presence는 본 연구의 title-based search와 matching 절차를 통해 bibliographic record의 존재가 확인되었는지로 조작화한다. 따라서 \(D_j=0\)은 Google Scholar의 모든 가능한 검색에서 해당 논문이 절대 존재하지 않는다는 뜻이 아니라, 본 연구의 검색절차에서 현재 index presence를 확인하지 못했다는 의미이다.

보조 변수는 현재 Google Scholar record가 확인된 논문에 대해 Google Scholar가 제공한 링크가 로그인이나 결제 없이 full text로 연결되는지이다. 이는 논문의 일반적인 OA 여부를 측정하지 않는다.

## 3.2 분석전략

주요 분석은 현재 Google Scholar index presence에 따른 영어권 인용확률 격차가 citation cohort별로 달라지는지를 검정한다. Target-paper fixed-effects linear probability model은 다음과 같다.

$$
Y_{jc}=\alpha_j+\lambda_c+
\sum_{k=2}^{4}\beta_k
\left(D_j\times1[c=k]\right)
+\gamma AgeBin_{jc}+\epsilon_{jc}.
$$

Target fixed effect α_j는 시간에 따라 변하지 않는 target-paper attribute를 흡수하고, cohort fixed effect λ_c는 각 기간에 모든 target에 공통적으로 나타나는 citation incidence의 변화를 흡수한다. \(D_j\)는 paper 내에서 변하지 않으므로 main effect는 target fixed effect에 흡수된다.

핵심 계수 β_k는 각 후속 cohort에서 \(D=1\)과 \(D=0\) 논문의 영어권 인용확률 격차가 C1의 격차와 얼마나 다른지를 나타낸다. 이는 Google Scholar indexing의 causal effect가 아니라 현재 index presence에 따라 구분되는 두 집단 사이 gap의 시기별 차이를 나타낸다. Standard error는 target paper 수준에서 cluster한다.

Cohort별 eligible-target composition의 변화를 점검하기 위해 2004년까지 출판된 target paper만을 대상으로 동일한 분석을 반복한다. 이 논문들은 네 cohort 모두에 기여할 시간적 기회를 가지므로 후기에 출판된 논문의 추가로 인해 cohort 구성이 바뀌는 문제를 줄일 수 있다. 이 restriction은 과거 Google Scholar indexing 상태를 복원하기 위한 것이 아니다.

추가 robustness에서는 Poisson pseudo-maximum likelihood, citation-count outcome, journal·topic·publication-year와 cohort의 추가 control을 사용한다.

## 3.3 결과

현재 Google Scholar index presence가 확인된 논문은 모든 cohort에서 그렇지 않은 논문보다 높은 raw English-language citation incidence를 보인다.

| Cohort | \(D=1\) | \(D=0\) | Raw difference |
| ------ | ------: | ------: | -------------: |
| C1     |   0.68% |   0.31% |       +0.37 pp |
| C2     |   1.90% |   0.67% |       +1.23 pp |
| C3     |   3.01% |   1.25% |       +1.76 pp |
| C4     |   2.66% |   1.38% |       +1.28 pp |

Fixed-effects 분석에서 C1 대비 두 집단의 격차는 C2에서 0.405pp 증가한다(95% CI [0.040, 0.770], \(p=.030\)). C3에서는 0.696pp 증가한다(95% CI [0.329, 1.063], \(p<.001\)). C2와 C3 계수의 joint test 역시 \(p<.001\)이다.

반면 C4의 변화는 0.008pp(95% CI [−0.337, 0.353], \(p=.965\))로, 2020–2024년에 C1 대비 격차가 추가적으로 확대되었다는 근거는 확인되지 않는다.

2004년까지 출판된 target만을 분석해도 C2와 C3에서 양의 gap 변화가 나타난다.

| C1 대비 \(D\) gap 변화 |        전체 eligible sample |                2004년까지 출판 |
| ------------------ | ------------------------: | ------------------------: |
| C2                 |  +0.405 pp [0.040, 0.770] |  +0.791 pp [0.227, 1.355] |
| C3                 |  +0.696 pp [0.329, 1.063] |  +0.496 pp [0.027, 0.964] |
| C4                 | +0.008 pp [−0.337, 0.353] | +0.273 pp [−0.175, 0.721] |

Pre-2005 sample에서 C2는 \(p=.006\), C3는 \(p=.038\)이며 C2–C3 joint test는 \(p=.011\)이다. C4는 양의 추정치이지만 통계적으로 불확실하다(\(p=.233\)).

Robustness 결과는 모든 specification에서 동일하지 않다. Target-fixed-effects Poisson에서는 C2와 C3의 변화가 양수이지만 영어권 인용이 전혀 없는 target은 conditional model을 식별하지 못하므로 제외된다. 다른 Poisson specification은 더 불정확하며, journal-by-cohort 및 publication-year-by-cohort model에서는 C2의 양의 추정치는 유지되지만 C3와 C4가 통계적으로 유의하게 재현되지는 않는다. 따라서 결과는 main incidence model과 pre-2005 restriction에서 확인된 C2–C3 패턴의 범위에서 해석한다.

현재 Google Scholar record가 확인된 논문들 사이에서는 Google Scholar가 제공한 링크를 통한 full-text access가 cohort별 영어권 citation incidence와 통계적으로 유의한 관계를 보이지 않았다.

## 3.4 해석

Study 1의 핵심 결과는 현재 Google Scholar index presence가 서로 다른 과거 영어권 인용궤적을 가진 논문집단을 구분한다는 것이다. 두 집단의 인용확률 격차는 C1보다 C2와 C3에서 컸고 pre-2005 target에서도 같은 방향이 나타났다. 그러나 C4에서는 추가 확대가 확인되지 않았으며 일부 대안 specification에서는 추정이 덜 정밀했다. 따라서 관찰된 패턴은 C2와 C3에 한정해 해석해야 한다.

0.405pp와 0.696pp는 각 기간의 인용확률이 아니라 C1 대비 집단 간 격차의 추가 변화량이다. 이 결과는 모든 시기에 걸쳐 지속적으로 확대되는 advantage를 의미하지 않는다.

인과 해석도 제한된다. Google Scholar 상태는 2026년에만 관찰되므로 현재 index presence가 과거 인용을 발생시켰다고 결론내릴 수 없다. 현재 record의 존재는 이후의 indexing, web availability, 이전 scholarly circulation 또는 함께 변화한 다른 특성을 반영할 수 있다. Study 1이 지지하는 가장 제한적인 결론은 현재 index presence에 따라 historical English-language citation trajectory가 다르게 나타난다는 것이다.

# 4. Study 2: Web-Enabled 생성형 검색 감사

## 4.1 Benchmark와 감사 설계

Study 2는 동일한 한국 정치 주제를 다루는 한국어권과 영어권의 주요 문헌이 생성형 검색에서 어느 정도 검색되고 최종 출처로 제시되는지, 그리고 그 차이가 검색조건에 따라 달라지는지를 분석한다.

비교대상은 audit 결과를 본 뒤 사후적으로 정하지 않고 시스템 실행 전에 benchmark로 고정한다. 이를 통해 특정 언어의 논문이 결과에 많이 등장하는 것과, 각 언어권에서 사전에 주요 문헌으로 선정한 연구가 실제로 검색·추천되는 것을 구분한다.

Benchmark topic은 한국어권과 영어권 한국 정치학의 연구지형을 비교한 Kim et al. (2025)을 바탕으로 선정하였다. 두 학술공간에서 모두 연구되어 온 한국 정치 주제 가운데 한국 현대정치의 주요 전개를 대체로 시간적 순서로 포괄하도록 다음 다섯 주제를 구성하였다.

1. 한국전쟁
2. 한국 경제발전
3. 한국 민주화
4. 북한 핵문제
5. 한류

각 주제는 의미가 대응하는 한국어·영어 주제어 세 개로 조작화하였다.

| 주제      | 한국어 주제어                       | 영어 주제어                                                                                                   |
| ------- | ----------------------------- | -------------------------------------------------------------------------------------------------------- |
| 한국전쟁    | 한국전쟁; 한국전쟁 발발; 한국전쟁 기원        | Korean War; Outbreak of the Korean War; Origins of the Korean War                                        |
| 한국 경제발전 | 한국 경제발전; 한국 발전국가; 한국 수출주도 산업화 | South Korean Economic Development; Korean Developmental State; South Korean Export-Led Industrialization |
| 한국 민주화  | 한국 민주화; 한국 민주화운동; 한국 시민사회     | South Korean Democratization; South Korean Democracy Movement; South Korean Civil Society                |
| 북한 핵문제  | 북핵 문제; 북한 핵무기; 대북 확장억제        | North Korean Nuclear Program; North Korean Nuclear Weapons; Extended Deterrence against North Korea      |
| 한류      | 한류; 케이팝; 한국 영화                | Korean Wave; K-pop; South Korean Cinema                                                                  |

각 주제에는 한국어 논문 10편과 영어 논문 10편을 포함한다. 한국어 benchmark는 DBpia와 KISS, 영어 benchmark는 Web of Science와 Google Scholar를 이용해 구성한다. Candidate pool을 citation count에 따라 정렬한 뒤 두 source에서 공통적으로 상위에 위치하는 논문을 기준으로 주제별 10편을 선정하였다. 최종 benchmark는 한국어 50편과 영어 50편, 총 100편이며 LLM audit 전에 고정하였다. 이는 각 주제의 모든 relevant literature를 포괄하는 gold standard가 아니라 조건 간 비교를 위한 evaluation set이다.

Audit은 다음 세 요인을 교차한다.

* Query language: 영어 / 한국어
* Source instruction: general web / KCI·DBpia·KISS 명시
* System: OpenAI `gpt-5.6-sol` / Perplexity `sonar-pro`

모든 prompt는 해당 주제의 세 주제어를 포함하고 관련 학술문헌 10편을 고정된 JSON 형식으로 요청하였다. 검색횟수는 주제어당 최대 2회, execution당 최대 6회로 제한하였다. 5개 주제 × 4개 prompt condition × 2개 system × 5회 독립 repetition으로 200개의 stateless execution을 수행하였으며, 최종적으로 1,932개의 valid recommendation occurrence가 생성되었다.

## 4.2 측정과 분석

Benchmark paper \(j\)와 execution \(i\)에 대해 세 결과를 구분한다.

* TraceRecovery: provider가 외부에 노출하는 search trace에서 benchmark paper가 확인되는지
* Recommendation: benchmark paper가 최종 recommendation에 포함되는지
* SuppliedLinkAccess: benchmark paper가 추천되고 제공된 URL이 로그인이나 결제 없이 full text로 연결되는지

앞의 두 변수는 서로 다른 질문에 답한다. `TraceRecovery`는 benchmark가 관찰 가능한 검색흔적에 나타나는지를 측정하고, `Recommendation`은 그 문헌이 최종적으로 사용자에게 제시되는 출처에 포함되는지를 측정한다. Search trace는 provider가 공개한 범위만 관찰하므로 시스템 내부의 전체 retrieval process를 의미하지 않는다.

Benchmark panel은 4,000개의 paper × execution observation으로 구성된다. 200개의 execution 각각에 해당 topic의 한국어 benchmark 10편과 영어 benchmark 10편을 대응시킨다. `SuppliedLinkAccess`의 denominator는 모든 benchmark-paper × execution pair이므로 추천된 논문에 조건부인 access rate가 아니라 검색, 추천, 접근까지 모두 성공한 경우를 나타낸다.

영어 general-web condition을 baseline으로 한국어와 영어 benchmark의 차이를 추정하고, query language와 source instruction이 그 차이를 어떻게 변화시키는지를 분석한다. 두 조건을 동시에 적용한 combined condition과 baseline의 contrast도 별도로 계산한다.

이와 별도로 전체 recommendation에서 한국어 논문이 차지하는 비율을 측정한다. 이 값은 benchmark 회수율과 다르다. Benchmark에 포함되지 않은 한국어 논문도 한국어 논문 비율에는 포함되기 때문이다.

마지막으로 927개의 distinct supplied URL 또는 no-URL item key를 검토하여 accessible full text, abstract only, paywalled, broken link, hallucinated/unverifiable publication으로 분류한다. 이 평가는 시스템이 제공한 URL의 상태만을 대상으로 하며, 다른 웹 위치에 무료 copy가 존재하는지는 조사하지 않는다.

## 4.3 결과

영어 질의와 일반 웹검색을 사용한 baseline에서는 두 benchmark 모두 회수율이 낮았으며, 한국어 benchmark에서 추가적인 deficit이 나타났다.

| 단계                       | 영어 benchmark | 한국어 benchmark | 한국어–영어 격차 |         95% CI | \(p\) |
| ------------------------ | -----------: | ------------: | --------: | -------------: | ----: |
| Observable search trace  |         3.4% |          0.0% |   −3.4 pp | [−6.46, −0.34] |  .029 |
| Final recommendation     |         3.2% |          0.0% |   −3.2 pp | [−5.77, −0.63] |  .015 |
| Accessible supplied link |         0.6% |          0.0% |   −0.6 pp |  [−1.76, 0.56] |  .311 |

검색흔적과 최종 추천에서의 한국어–영어 차이는 통계적으로 유의하다. 제공된 링크를 통한 원문 접근의 차이는 유의하지 않지만, benchmark가 마지막 단계까지 도달하는 경우 자체가 매우 적다는 점을 함께 고려해야 한다.

한국어 query는 검색흔적 단계의 Korean–English gap을 +3.8pp 변화시키고(95% CI [0.72, 6.88], \(p=.016\)), Korean-database instruction은 +4.0pp 변화시킨다(95% CI [0.73, 7.27], \(p=.017\)). 최종 recommendation에서는 database instruction이 gap을 +3.2pp 변화시킨다(95% CI [0.71, 5.69], \(p=.012\)). Korean-query estimate는 +2.6pp로 같은 방향이지만 \(p=.068\)이다.

두 조건을 함께 적용한 combined condition과 baseline을 직접 비교하면 Korean–English gap은 검색흔적에서 +5.6pp, 최종 추천에서 +6.4pp 변화한다. Combined condition에서 한국어 benchmark의 검색흔적 회수율은 2.2%, 최종 추천 회수율은 3.2%이다. 상대적인 격차의 방향은 바뀌지만 절대적인 회수율은 낮다.

검색조건은 benchmark 회수율보다 최종 추천의 언어구성을 훨씬 크게 변화시킨다.

| Prompt condition                | Recommendation의 한국어 논문 비율 |
| ------------------------------- | ------------------------: |
| English + general web           |                      0.0% |
| English + Korean DB instruction |                     35.3% |
| Korean + general web            |                     55.8% |
| Korean + Korean DB instruction  |                 91.2% |

한국어 query는 recommendation의 한국어 논문 비율을 55.7pp 증가시키고(\(p<.001\)), Korean-database instruction은 35.4pp 증가시킨다(\(p<.001\)). 그러나 combined condition에서도 사전에 선정한 한국어 benchmark의 recommendation recovery는 3.2%에 그친다.

따라서 한국어 논문이 많이 추천되는 것과 한국어권에서 주요하게 축적된 특정 연구가 실제로 높은 비율로 포함되는 것은 동일하지 않다. Benchmark 밖의 한국어 추천이 부적절하다는 의미가 아니라, 두 지표가 다른 질문에 답한다는 의미이다.

전체 1,932개의 recommendation occurrence 가운데 제공된 링크의 결과는 다음과 같다.

* 854개(44.2%): full text 접근 가능
* 859개(44.5%): 접근 제한

  * abstract-only 247개
  * paywall 612개
* 219개(11.3%): invalid 또는 unverifiable

  * broken link 176개
  * coded hallucinated publication 43개

| 제공된 링크의 결과              |    전체 | 한국어 논문 | 영어 논문 |
| ----------------------- | ----: | -----: | ----: |
| Accessible              | 44.2% |  46.3% | 42.4% |
| Access restricted       | 44.5% |  47.9% | 41.6% |
| Invalid or unverifiable | 11.3% |   5.8% | 16.0% |
| Broken link             |  9.1% |   3.3% | 14.1% |
| Hallucinated item       |  2.2% |   2.6% |  1.9% |

Prompt condition과 system을 통제하면 recommended-item language는 full access, access restriction 또는 invalid/unverifiable outcome과 독립적으로 유의한 관계를 보이지 않는다. 따라서 표의 raw difference를 publication language 자체의 효과로 해석하지 않는다.

## 4.4 해석

Study 2의 핵심 결과는 검색조건이 한국어 benchmark의 상대적 가시성을 바꾸지만 주요 문헌의 절대 회수율을 충분히 높이지는 못한다는 것이다. 영어 general-web baseline의 한국어 deficit은 검색흔적과 최종 추천에서 모두 나타났다. 한국어 query와 한국 학술 데이터베이스 지시는 이 차이를 줄이거나 반전시켰지만 combined condition에서도 한국어 benchmark 회수율은 검색흔적 2.2%, 최종 추천 3.2%에 그쳤다.

이 결과는 language representation과 benchmark recovery를 구분해야 함을 보여준다. Combined condition에서 최종 추천의 91.2%가 한국어 논문이어도 사전 지정 한국어 benchmark의 recommendation recovery는 3.2%였다. 검색결과가 한국어 중심으로 보인다는 사실만으로 한국어권의 주요 연구가 충분히 포함되었다고 판단할 수 없다.

Search trace와 final recommendation의 구분은 누락이 관찰되는 지점도 보여준다. 다만 공개된 trace는 provider의 내부 retrieval 전체가 아니므로 내부 mechanism을 완전히 관찰한 것으로 해석할 수 없다. 제공 링크를 통한 원문 접근도 별도 결과이다. 전체 추천의 절반 미만만 바로 full text로 연결되었지만 검색과 추천에서 나타난 것과 같은 유의한 한국어–영어 차이는 확인되지 않았다.

# 5. 논의

## 5.1 주요 발견의 종합

두 연구가 지지하는 중심 주장은 문헌의 검색 가시성이 국제적 지식 유통의 독립적인 분석단계라는 것이다. 한국어권에서 이미 사용되거나 주요 문헌으로 확인된 연구도 다른 검색환경에서 자동적으로 검토 가능한 후보가 되지는 않았다.

각 Study가 이 주장에 제공하는 증거는 다르다. Study 1은 현재 Google Scholar index presence에 따라 과거 영어권 인용궤적이 다르게 나타남을 보여주지만 과거 검색환경을 직접 관찰하지 않는다. Study 2는 현재 생성형 검색에서 benchmark의 검색과 선택을 직접 비교하지만 이후의 인용을 관찰하지 않는다. 따라서 두 결과를 하나의 인과 메커니즘으로 연결할 수는 없다. 두 연구의 공통된 함의는 검색환경에서 어떤 문헌이 후보가 되고 최종 출처로 제시되는가가 출판 및 인용과 구분되는 결과라는 점이다.

Study 2는 특히 언어적 representation이 scholarly recovery를 대신할 수 없음을 보여준다. 한국어 논문의 비율은 prompt에 따라 크게 변했지만 사전 지정 한국어 benchmark의 절대 회수율은 낮았다. 이는 benchmark 밖의 한국어 추천이 부적절하다는 뜻이 아니라, 결과목록의 언어와 특정 학술공간의 주요 문헌이 반영된 정도가 서로 다른 질문이라는 뜻이다.

원문 접근도 같은 이유로 분리해야 한다. Study 1에서 현재 Google Scholar가 제공한 full-text link는 영어권 citation incidence와 유의한 별도 관계를 보이지 않았다. Study 2에서는 전체 추천의 절반 미만이 제공 링크를 통해 full text로 연결되었지만 유의한 언어격차는 나타나지 않았다. 검색, 최종 출처 선택, 제공 링크를 통한 접근, 이후의 인용은 하나의 지표로 합칠 수 없는 결과이다.

## 5.2 정치학적 함의와 후속연구

본 연구의 정치학적 함의는 지식 불평등이 검색기술에서 시작된다는 것이 아니라 검색단계에서도 관찰된다는 것이다. 기존 연구가 연구대상, 연구자의 위치, 출판언어, database coverage와 국제 인용의 불균형을 보여주었다면(Breuning et al. 2018; Wilson and Knutsen 2022; Mongeon and Paul-Hus 2016), 본 연구는 연구자가 선행연구를 구성하는 과정에서 어떤 구체적인 문헌이 검토대상으로 나타나는지를 추가한다.

이 단계는 문헌의 내용과 가치를 평가하기 전에 작동한다. 관련 문헌이 검색결과에 나타나지 않거나 최종 출처에서 제외되면 연구자는 그 문헌을 평가할 기회 자체를 갖지 못할 수 있다. Discovery bottleneck은 바로 이 평가 이전의 가시성 손실을 지칭한다. Study 1에서는 search protocol으로 Google Scholar bibliographic record를 확인하지 못한 상태를, Study 2에서는 benchmark가 관찰 가능한 search trace나 final recommendation에서 확인되지 않은 상태를 가리킨다. 이 개념은 하나의 내부 알고리즘적 원인을 가정하지 않는다.

이 문제는 현지어와 영어의 연구가 동일한 정치현상에 대해 병존할 때 특히 중요하다. 한국 정치에 관한 국제적 지식을 영어권 학술지, 국제 citation index 또는 생성형 검색의 reading list만으로 파악하면 한국어권에 축적된 scholarly record와 실제 검색결과에 나타나는 subset의 차이를 놓칠 수 있다. 따라서 국제적 가시성을 평가할 때 결과목록의 언어적 다양성뿐 아니라 사전에 확인된 주요 문헌의 paper-level recovery도 함께 측정할 필요가 있다.

후속연구는 이 가시성을 시간에 따라 직접 추적해야 한다. Google Scholar에서 동일한 문헌의 index presence와 제공 링크를 반복 측정하면 Study 1이 복원할 수 없는 indexing 변화를 기록할 수 있다. 생성형 검색에서도 동일한 benchmark와 조건을 반복 적용하면 모델, search index, ranking procedure의 변화에 따라 특정 한국어 연구의 검색과 추천이 어떻게 달라지는지 분석할 수 있다. 이용자의 클릭, 원문 열람, relevance 평가와 실제 인용까지 연결한 연구는 discovery 이후의 단계를 추가로 규명할 수 있다.

# 6. 결론

본 논문은 한국 정치 연구의 국제적 가시성을 이해하려면 생산과 인용 사이에 있는 discovery를 별도의 단계로 분석해야 한다고 주장했다. 핵심 질문은 한국어권에서 존재하고 사용되는 연구 가운데 어떤 구체적인 문헌이 검색환경에서 검토 가능한 후보로 나타나고 최종 출처로 제시되는가이다.

Study 1은 현재 Google Scholar index presence가 확인되는 논문과 확인되지 않는 논문의 과거 영어권 인용궤적이 다르게 나타남을 보여주었다. 이 관계는 C2와 C3에서 확인되었지만 C4에서 추가 확대되지 않았으며 Google Scholar의 역사적 인과효과로 해석할 수 없다. Study 2는 영어 general-web baseline에서 한국어 benchmark deficit을 직접 관찰했고, 한국어 질의와 한국 학술 데이터베이스 지시가 상대적 격차를 바꾸지만 낮은 절대 회수율을 해결하지는 못함을 보여주었다. 특히 높은 한국어 recommendation share와 낮은 한국어 benchmark recovery가 동시에 나타났다.

이 결과가 지지하는 결론은 제한적이지만 분명하다. 문헌이 검색되는지, 최종 출처로 선택되는지, 제공 링크를 통해 읽을 수 있는지, 이후 인용되는지는 서로 다른 결과이다. Discovery bottleneck은 이 가운데 실질적 내용 평가 이전에 특정 검색환경에서 문헌의 가시성이 사라지는 상태를 지칭한다. 한국어권과 영어권에 병렬적인 연구축적이 존재하는 분야에서는 무엇이 출판되고 인용되는가뿐 아니라 어떤 연구가 실제 검색과정에 나타나는가를 함께 분석해야 한다.

# 7. 한계

본 연구의 한계는 시간적 식별, 측정, 일반화의 세 범주로 나뉜다. Study 1은 현재의 Google Scholar 상태만 관찰하므로 역사적 인과효과를 식별할 수 없고, Study 2는 제한된 시스템과 topic에서 특정 수집시점의 behavior를 측정한다. 두 연구 모두 검색 이후 이용자의 행동은 관찰하지 않는다.

첫째, Study 1의 Google Scholar index presence는 2026년에만 관찰된다. 각 target이 언제 처음 포함되었고 과거 어느 시점부터 검색되었는지, 당시 어떤 full-text link가 제공되었는지는 알 수 없다. 현재 index presence 자체가 이전 scholarly circulation의 결과일 수도 있다. 널리 인용되거나 웹에 더 많이 노출된 논문이 이후 Google Scholar에서 확인될 가능성이 높아졌을 수 있으며, target fixed effects는 이러한 temporal ordering이나 time-varying process를 제거하지 못한다.

둘째, Google Scholar index presence에는 bibliographic matching error가 있을 수 있다. 한국어·영어 제목과 reference-title variant를 사용했지만 metadata 오류, 제목 변형, 중복 record 또는 불완전한 indexing 때문에 실제 record를 놓치거나 잘못 연결했을 가능성이 있다. Google Scholar가 전체 index 목록을 공개하지 않으므로 (D=0)은 절대적 부재가 아니라 본 연구의 search and matching protocol에서 index presence를 확인하지 못했다는 의미이다.

셋째, Study 1 결과의 강도는 specification에 따라 달라진다. Main incidence model과 pre-2005 restriction에서는 C2와 C3의 gap 확대가 나타나지만 일부 Poisson 및 추가-control specification에서는 결과가 더 불확실하다. 모든 outcome과 functional form에서 동일한 패턴이 확인되었다고 일반화할 수 없다.

넷째, Study 2는 두 개의 시스템, 다섯 개의 한국 정치 주제, 한 번의 collection period와 100편의 benchmark에 한정된다. 다섯 주제는 양 언어권에서 모두 연구된 영역을 비교하기 위해 선정했지만 한국 정치 연구 전체의 확률표본은 아니다. Citation count와 두 출처의 공통 상위문헌에 의존한 benchmark도 최근 연구, 저인용 연구, 전문적 하위주제를 충분히 대표하지 못할 수 있다.

다섯째, 생성형 검색환경은 지속적으로 변한다. 동일한 model name 아래에서도 underlying model, search index, ranking procedure 또는 provider interface가 달라질 수 있다. 또한 provider가 공개하는 search trace는 내부 retrieval 전체를 보여주지 않으며 provider별 observability도 다르다. Benchmark가 trace에서 발견되지 않았다고 해서 내부적으로 한 번도 고려되지 않았다고 단정할 수 없다.

여섯째, 원문 접근 결과에는 floor와 측정범위의 제약이 있다. Benchmark의 검색과 recommendation 자체가 낮아 access 단계의 관측치가 희소하다. 유의한 access gap이 없다는 결과를 두 언어 문헌의 접근성이 같다는 적극적 증거로 해석해서는 안 된다. Link audit도 시스템이 실제 제공한 URL만 평가하므로 다른 웹 위치의 무료 copy는 반영하지 않는다. Hallucination event 역시 적고 일부 experimental cell에 집중되어 있다.

마지막으로 두 Study 모두 검색 이후의 이용자 행동을 관찰하지 않는다. 검색결과의 클릭, 원문 열람, substantive relevance 평가, 언어능력, perceived quality, citation norm, collaboration network와 publication venue는 후속 이용과 인용에 영향을 줄 수 있다. 본 연구의 증거는 검색환경에서 어떤 문헌이 가시화되고 제시되는지, 그리고 제공된 링크로 원문에 접근할 수 있는지에 한정된다.

[^1]: Kim et al. (2025)의 초기 버전은 제28차 IPSA 세계정치학대회(서울, 2025년 7월 12–16일)에서 발표되었다. 수정본은 *Humanities and Social Sciences Communications*의 revise-and-resubmit 결정을 거쳐 현재 재심사 중이다.

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
