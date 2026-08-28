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

한국 정치학은 KCI와 SSCI를 중심으로 서로 구분되는 학술공간에서 생산·유통된다(Rhee 2026). 본 논문은 이러한 분절이 나타나는 한 측면을 학술검색에서의 가시성과 원문 접근을 통해 분석한다.

Study 1은 2000–2025년 한국어권 정치학 논문들이 인용한 한국 정치 관련 논문 54,789편을 대상으로 현재 Google Scholar 검색가능성과 영어권 인용확률의 시기별 관계를 분석한다. 검색 가능한 논문과 그렇지 않은 논문의 인용확률 격차는 기준기간보다 2010–2014년에 0.405퍼센트포인트(pp), 2015–2019년에 0.696pp 유의하게 더 컸지만 2020–2024년에는 추가 확대되지 않았다. Google Scholar 링크를 통한 원문 접근은 영어권 인용확률과 유의한 관계를 보이지 않았다. 이는 현재 검색가능성과 과거 인용궤적의 연관성이며 Google Scholar의 인과효과를 뜻하지 않는다.

Study 2는 다섯 주제에서 사전 선정한 한국어 논문 50편과 영어 논문 50편을 이용해 두 개의 web-enabled generative search system을 감사한다. 영어 질의·일반 웹검색 baseline에서 한국어 benchmark는 검색과 최종 추천에서 모두 회수되지 않았지만 영어 benchmark recovery는 각각 3.4%와 3.2%였다. 한국어 질의와 한국 학술 데이터베이스 지시를 함께 적용하면 한국어–영어 격차가 검색에서 5.6pp, 추천에서 6.4pp 축소되었지만, 한국어 benchmark의 recommendation recovery는 3.2%에 머물렀다. 전체 추천의 44.2%만 제공된 링크를 통해 원문에 직접 접근할 수 있었으며 유의한 언어격차는 없었다.

두 연구는 한국 정치학의 국제적 가시성을 설명할 때 출판과 인용뿐 아니라 문헌이 검색되고 최종 출처로 선택되는 과정을 별도로 분석할 필요가 있음을 보여준다. 검색·추천에서 나타난 차이와 달리 원문 접근에서는 이에 상응하는 언어격차가 확인되지 않았다. 본 논문은 문헌이 내용 평가 이전에 검색 후보로 진입하지 못하거나 최종 출처로 선택되지 않는 현상을 discovery bottleneck으로 제시한다.

Keywords: 한국 정치학; 학술검색; Google Scholar; 생성형 검색; 비영어권 학술문헌; 국제적 가시성; 원문 접근; discovery bottleneck

# 1. 서론

국제 정치학에서 어떤 연구가 가시화되고 인용되는지는 연구대상뿐 아니라 연구가 생산·유통되는 언어와 학술공간과도 관련된다. 주요 국제 학술 데이터베이스는 영어권 학술지를 상대적으로 많이 포괄하며, 비영어로 출판된 연구는 국제 인용에서도 불리한 경향을 보인다(Mongeon and Paul-Hus 2016; Vera-Baceta, Thelwall, and Kousha 2019; Di Bitetti and Ferreras 2017). 한국 정치학에서도 KCI를 중심으로 한 국내 학술공간과 SSCI를 중심으로 한 국제 학술공간 사이에 연구 주제와 방법론적 차이가 관찰되며(Rhee 2026), 영어로 출판되어 국제 학술공간에서 유통되는 한국 정치 연구는 한국어권에서 생산·유통되는 연구보다 더 넓은 인용 범위와 국제적 인지도를 갖는 경향이 있다(Kim et al. 2025).[^1]

본 논문은 이러한 국제적 가시성의 차이를 학술문헌이 검색환경에서 실제로 가시화되는 과정에서 분석한다. 데이터베이스에 문헌이 존재하는 것과 특정 검색환경에서 개별 논문이 반환되는 것은 동일하지 않다. 정보검색 연구에서는 데이터베이스 전체의 coverage와 개별 문헌이 검색을 통해 반환될 수 있는 retrievability를 구분한다(Azzopardi and Vinay 2008). 따라서 한국어권에서 생산·사용된 연구가 국제적 학술검색에서 어느 정도 가시적인지는 출판과 최종 인용의 차이와 별도로 분석할 수 있다.

이 논문에서 가시성은 검색환경 안에서 문헌이 관찰 가능한 후보로 나타나는 정도를 뜻하며, 두 Study에서 그 조작화는 다르다. Study 1에서는 논문의 식별정보를 알고 있는 상태에서 현재 Google Scholar가 해당 bibliographic record를 반환하는 paper-level known-item retrievability를 측정한다. Study 2에서는 사전에 정한 benchmark paper가 provider가 노출하는 search trace에 나타나는지와 최종 recommendation으로 선택되는지를 각각 측정한다. 따라서 Study 1은 broad topic search에서 처음 논문을 발견할 확률을 측정하지 않으며, Study 2의 observable search trace 역시 시스템 내부의 모든 retrieval 과정을 의미하지 않는다.

원문 접근은 이러한 검색 가시성과 별개의 결과로 다룬다. 논문이 검색되거나 추천되더라도 이용 가능한 full text로 직접 연결되지 않을 수 있고, 반대로 publisher version이 paywall 뒤에 있어도 repository나 저자 공개본이 제시될 수 있다(Jamali and Nabavi 2015). 따라서 본 연구가 측정하는 access는 논문의 일반적인 OA status가 아니라 해당 검색환경이 실제로 제공한 링크가 로그인이나 결제 없이 full text로 이어지는지이다.

이러한 구분을 바탕으로 두 연구를 수행한다. Study 1은 확립된 학술검색 환경인 Google Scholar를 분석한다. 2000–2025년에 생산된 한국어권 정치학 논문들이 인용한 한국 정치 관련 문헌을 출발점으로 하여, 현재 Google Scholar에서 검색 가능한 논문과 그렇지 않은 논문의 영어권 인용확률 격차가 시기에 따라 어떻게 나타나는지를 분석한다. 표본에는 한국어권에서만 인용된 문헌과 영어권에서도 인용된 문헌이 함께 포함되므로, 한국어권에서 이미 학술적으로 사용된 문헌이라는 공통 조건 아래 영어권으로의 인용 범위가 어떻게 달라지는지를 비교할 수 있다.

Study 2는 현재의 web-enabled generative search를 분석한다. 생성형 검색은 외부 문헌을 검색하는 데서 그치지 않고 그중 일부를 최종 citation이나 recommendation으로 선택하여 답변을 구성한다(Liu, Zhang, and Liang 2023; He et al. 2025). 따라서 retrieval과 final source selection은 서로 다른 가시성 단계가 된다. Study 2는 한국어권과 영어권에서 모두 연구되어 온 동일한 한국 정치 주제에 대해 양 언어권의 주요 문헌을 사전에 benchmark로 정하고, 질의 언어와 한국 학술 데이터베이스 검색 지시를 변화시켜 검색과 추천에서의 한국어–영어 recovery gap이 어떻게 달라지는지를 비교한다.

본 논문은 이처럼 문헌이 실질적인 내용 평가 이전에 검색 가능한 후보가 되지 못하거나 검색된 뒤 최종 출처로 선택되지 않는 현상을 discovery bottleneck이라고 부른다. 이는 모든 학술적 발견경로를 포괄하는 일반이론이나 검색 인프라가 국제적 인용격차를 인과적으로 발생시킨다는 주장이 아니다. 본 연구에서 관찰하는 특정 검색환경과 특정 검색단계에서 발생하는 누락을 지칭하기 위한 조작적 개념이다.

따라서 본 논문의 기여는 한국 정치학의 국제적 가시성을 출판언어와 인용에만 두지 않고, Google Scholar에서의 논문 검색가능성, 생성형 검색의 문헌 회수와 최종 출처 선택, 그리고 제공 링크를 통한 원문 접근을 구분하여 측정하는 데 있다. Study 1은 현재 검색가능성에 따라 과거 영어권 인용궤적이 다르게 나타남을 보여주고, Study 2는 기본 검색조건의 한국어 benchmark deficit이 조건에 따라 달라지지만 언어적 representation의 증가가 높은 benchmark recovery로 이어지지는 않음을 보여준다. 원문 접근은 두 연구의 검색·추천 결과와 동일한 패턴을 보이지 않았다.

# 2. 선행연구

## 2.1 한국 정치학의 국제적 가시성과 학술검색

정치학에서 국제적으로 가시적인 지식은 지역과 언어에 균등하게 분포하지 않는다. 한편으로는 어떤 국가와 지역이 연구대상으로 선택되는가에 편중이 존재한다. 주요 정치학 학술지의 연구대상은 역사적으로 북미와 서유럽에 집중되어 왔으며, 이러한 지리적 편중은 정치학의 기술적·인과적 주장과 이론의 적용범위와 관련된다(Wilson and Knutsen 2022). 국제 정치학의 출판 과정에서도 Global South 연구자의 대표성이 낮고 특정 연구기관 소속 연구자가 과대표되는 패턴이 보고되어 왔다(Breuning et al. 2018).

다른 한편으로는 동일한 국가나 정치현상을 다루더라도 연구가 어느 언어권과 학술공간에서 생산·유통되는가에 따라 국제적 가시성과 인용 범위가 달라질 수 있다. 주요 국제 학술 데이터베이스는 영어권 학술지를 상대적으로 많이 포괄하며(Mongeon and Paul-Hus 2016; Vera-Baceta, Thelwall, and Kousha 2019), 다언어 학술지에서는 다른 출판특성을 고려한 뒤에도 비영어 논문의 인용이 영어 논문보다 낮게 나타난다(Di Bitetti and Ferreras 2017). 따라서 정치학의 국제적 지식구조에는 어떤 지역이 연구되는가뿐 아니라 그 연구가 어느 언어권의 학술공간을 통해 유통되는가라는 차원도 존재한다.

한국 정치학에서도 한국어권과 영어권의 구분된 학술공간이 관찰된다. KCI와 SSCI에 출판된 한국 정치학 연구는 주제와 방법론적 패턴에서 차이를 보이며(Rhee 2026), 영어로 출판되어 국제 학술공간에서 유통되는 한국 정치 연구는 한국어권 연구보다 더 넓은 인용 범위와 국제적 인지도를 확보하는 경향을 보인다(Kim et al. 2025).

본 연구는 이러한 차이를 학술검색에서 어떤 문헌이 가시화되는가라는 차원에서 확장한다. 데이터베이스가 어떤 문헌을 수록하는지는 coverage의 문제인 반면, 개별 문헌이 특정 검색에서 반환되는지는 retrievability의 문제이다(Azzopardi and Vinay 2008). 따라서 학술적 기록에 존재하는 문헌 전체와 특정 검색환경이 실제로 반환하는 문헌은 구분할 필요가 있다.

원문 접근도 검색가능성과 동일하지 않다. 학술문헌의 무료 이용가능성은 주로 OA의 관점에서 분석되어 왔지만, 특정 검색환경이 이용 가능한 원문 version을 식별하여 접근경로로 제시하는지는 별도의 문제이다. Google Scholar는 publisher page뿐 아니라 대학·기관 repository와 연구자 웹사이트 등 다양한 출처의 scholarly content와 여러 version을 색인하고, 이용 가능한 경우 해당 version으로 연결되는 링크를 제공한다(Jamali and Nabavi 2015). 따라서 웹상에 무료 version이 존재하는 것과 검색환경이 그것을 실제 접근경로로 제공하는 것은 구분된다.

이러한 개념적 구분에 따라 Study 1은 Google Scholar의 현재 논문 검색가능성과 영어권 인용의 시기별 관계를 분석하고, Study 2는 생성형 검색에서 benchmark의 검색 회수와 최종 출처 선택을 비교한다. 원문 접근은 두 연구 모두에서 가시성과 구분되는 별도 결과로 분석한다.

## 2.2 Study 1: Google Scholar 검색가능성과 원문 접근

Google Scholar는 한국어를 포함한 비영어권 연구의 국제적 검색 가시성을 분석하기에 적절한 학술검색 환경이다. Web of Science와 Scopus보다 더 넓은 문헌과 인용을 포착하며, 추가적으로 확인되는 자료에는 비영어 문헌과 비학술지 자료가 상당수 포함된다(Chen 2010; Martín-Martín et al. 2018b, 2021). 또한 연구자와 대학원생의 scholarly information seeking에서 지속적으로 사용되어 왔으며, 사회과학에서도 주요 검색도구로 기능한다(Jamali and Asadi 2010; Cothran 2011; Blankstein 2022).

그러나 넓은 database coverage가 모든 개별 논문의 검색가능성을 의미하지는 않는다. 외부 bibliographic record와 비교한 연구에서도 Google Scholar에서 반환되지 않는 문헌이 확인되었으며, 이는 aggregate coverage와 paper-level retrievability가 서로 다른 분석 수준임을 보여준다(Azzopardi and Vinay 2008; Delgado-Quirós et al. 2024).

Study 1은 이 구분을 한국어권 정치학에서 이미 사용된 한국 정치 관련 문헌에 적용한다. 분석대상에는 한국어권에서만 인용된 논문과 영어권에서도 인용된 논문이 함께 포함되므로, 한국어권에서의 학술적 사용이라는 공통 출발점을 가진 문헌 안에서 현재 Google Scholar retrievability와 영어권 인용이 어떤 관계를 보이는지를 비교할 수 있다. 검색 인프라에서의 가시성이 국제적 학술 유통과 관련된다면, 현재 retrievable한 논문과 그렇지 않은 논문의 영어권 인용확률에서도 차이가 나타날 수 있다. 그러나 이는 현재의 Google Scholar 상태가 과거 인용을 발생시켰다는 인과가정이 아니라 현재 검색가능성에 따라 역사적 영어권 인용패턴이 어떻게 구분되는지를 보는 분석적 기대이다.

Google Scholar가 제공하는 full-text route도 별도의 조건이다. Publisher version이 paywall 뒤에 있더라도 repository copy나 author-deposited manuscript가 연결될 수 있고, 반대로 무료 version이 웹에 존재하더라도 Google Scholar가 이를 제시하지 않을 수 있다(Jamali and Nabavi 2015). 기존 연구는 Google Scholar의 database 및 citation coverage와 Google Scholar를 통해 이용할 수 있는 full text의 범위를 주로 분석해 왔다(Chen 2010; Jamali and Nabavi 2015; Martín-Martín et al. 2018a, 2018b, 2021; Delgado-Quirós et al. 2024). 본 연구에서는 이러한 접근경로를 일반적 OA와 구분하여 Google Scholar-mediated full-text access로 측정한다.

영어권 인용을 시기별 cohort로 나누는 이유는 누적 인용만으로는 현재 retrievable한 논문과 그렇지 않은 논문의 격차가 어느 기간에 확대되거나 축소되었는지를 알 수 없기 때문이다. 반면 연도별 citation incidence는 희소하여 지나치게 세분하면 추정이 불안정해질 수 있다. 이에 2010년 이후를 동일한 5년 단위로 나누고 그 이전을 기준기간으로 통합하여 visible–nonvisible gap의 시간적 이질성을 비교한다.

이 cohort는 Google Scholar의 역사적 indexing 상태나 adoption stage를 대리하지 않는다. 각 target paper가 어느 시점부터 Google Scholar에서 검색 가능했는지는 관찰되지 않기 때문이다. 따라서 cohort의 역할은 현재의 retrievability로 구분되는 두 집단 사이의 영어권 인용격차가 서로 다른 citation period에서 어떻게 나타났는지를 비교하는 것에 한정된다.

또한 늦게 출판된 target은 초기 cohort에 기여할 수 없어 cohort별 eligible-target composition이 달라질 수 있다. 이를 점검하기 위해 Google Scholar가 출시된 2004년까지 출판된 target만을 대상으로 동일한 분석을 반복한다. 이 restriction은 과거 Google Scholar 상태를 복원하기 위한 것이 아니라, 네 cohort 모두에 기여할 시간적 기회를 가진 보다 일정한 target set에서 결과가 유지되는지를 확인하기 위한 robustness check이다.

## 2.3 Study 2: 생성형 검색에서의 검색, 추천, 원문 접근

Generative search는 retrieval 이후의 source selection까지 검색환경이 수행한다는 점에서 기존 학술검색과 구분된다. Web-enabled LLM은 외부 자료를 검색한 뒤 검색된 문헌 전체를 그대로 제시하지 않고 그중 일부를 citation이나 recommendation으로 선택하여 답변을 구성한다(Liu, Zhang, and Liang 2023). 따라서 생성형 검색에서의 문헌 가시성은 검색단계에 나타나는 것과 최종 출처로 선택되는 것을 구분하여 분석할 필요가 있다.

Scholarly retrieval을 평가하려면 생성된 결과 자체와 독립적인 비교기준이 필요하다. 정보검색에서는 사전에 정의된 relevant set을 이용하여 retrieval 성능을 평가하며(Manning, Raghavan, and Schütze 2008), 최근의 scholarly-search benchmark도 실행 이전에 target paper를 정한 뒤 해당 문헌의 회수를 측정한다(Ajith et al. 2024; He et al. 2025). 이 구분은 multilingual search에서 특히 중요하다. 한국어 논문이 결과에 많이 포함되는 것과 한국어권에서 사전에 주요 문헌으로 선정된 특정 논문이 실제로 회수되는 것은 동일하지 않다. Study 2는 전자를 language representation, 후자를 benchmark recovery로 구분한다.

질의 언어와 출처 지시는 생성형 검색에서 어떤 학술공간의 문헌이 후보로 들어오는지와 관련된 조건이다. Query와 source instruction은 retrieval과 source selection의 입력이 되며, 탐색되는 출처의 범위와 최종적으로 선택되는 자료를 변화시킬 수 있다(Liu, Zhang, and Liang 2023; He et al. 2025). 한국 정치학처럼 한국어권과 영어권이 서로 다른 학술정보원을 통해 문헌을 유통하는 경우에는 영어 general-web query와 한국어 질의 또는 한국 학술 데이터베이스를 명시한 검색이 서로 다른 scholarly source space를 불러올 수 있다. 따라서 한국어 문헌의 상대적 가시성은 고정된 값이 아니라 검색조건에 따라 달라질 수 있는 결과로 분석할 필요가 있다.

Study 2의 주제는 이 언어권 비교가 가능한 영역으로 제한한다. 한국어권과 영어권 한국 정치학의 연구지형을 비교한 Kim et al. (2025)을 바탕으로, 두 학술공간에서 모두 지속적으로 연구되어 온 한국 정치 주제 가운데 한국 현대정치의 전개를 대체로 시간적 순서로 포괄하도록 한국전쟁, 한국 경제발전, 한국 민주화, 북한 핵문제, 한류의 다섯 주제를 선정하였다. 이는 특정 주제 자체가 한 언어권에 거의 존재하지 않기 때문에 발생하는 차이를 줄이고, 동일한 substantive topic 안에서 양 언어권의 주요 문헌이 어떻게 검색·선택되는지를 비교하기 위한 것이다.

생성형 검색에서 추천 이후의 원문 접근도 별개의 결과이다. 실제 논문이 정확하게 추천되더라도 제공된 URL이 paywall, abstract page 또는 broken link로 연결될 수 있다. 따라서 Study 2는 검색 결과에서의 benchmark recovery, final recommendation recovery, 제공 링크를 통한 full-text access를 분리하여 측정한다. 이 구분을 통해 한국어–영어 격차가 검색에서 발생하는지, 최종 source selection에서 나타나는지, 또는 원문 접근에서도 이어지는지를 살펴본다.

# 3. Study 1: Google Scholar 가시성과 영어권 인용

## 3.1 데이터와 변수

Study 1의 핵심 비교는 한국어권 정치학에서 이미 사용된 한국 정치 관련 문헌 가운데 현재 Google Scholar에서 검색 가능한 논문과 그렇지 않은 논문의 영어권 인용확률이 시기에 따라 어떻게 다른가이다.

분석대상은 2000–2025년에 생산된 한국어권 정치학 논문들이 인용한 한국 정치 관련 논문 54,789편이다. 표본 포함 기준은 해당 기간의 한국어권 정치학 문헌에서 최소 한 번 인용되었다는 것이므로, 한국어권에서만 인용된 논문과 한국어권 및 영어권 양쪽에서 인용된 논문이 함께 포함된다. 따라서 분석은 국내 학술적 사용 여부가 전혀 다른 문헌을 비교하는 것이 아니라, 한국어권에서 사용된 기록을 공유하는 문헌 안에서 영어권 인용 여부와 검색가능성의 관계를 살펴본다.

영어권 인용은 누적 citation count로 합치지 않고 citation cohort별 incidence로 구성한다. 누적 인용만 사용하면 visible–nonvisible gap의 시간적 변화를 확인할 수 없고, 연도별 outcome은 citation event가 희소하여 추정이 불안정할 수 있다. 이에 영어권 citing paper를 다음 네 기간으로 구분한다.

* C1 — 2009년 이하
* C2 — 2010–2014
* C3 — 2015–2019
* C4 — 2020–2024

C1은 이후 cohort와의 비교를 위한 기준기간이며 Google Scholar 도입 이전의 검색환경을 의미하지 않는다. 2010년 이후에는 동일한 5년 구간을 사용하여 기간 길이에 따른 차이를 줄인다.

Target paper는 해당 cohort에서 실제로 인용될 시간적 기회가 있었던 경우에만 포함한다. Target \(j\)와 cohort \(c\)에 대해,

$$
Y_{jc}=1
$$

은 해당 기간의 영어권 source paper가 target을 적어도 한 번 인용한 경우이며, 그렇지 않으면 0이다. 최종 panel은 179,230개의 target-paper × cohort observation으로 구성된다.

주요 exposure \(D_j\)는 2026년 현재 Google Scholar retrievability이다. 가능한 한국어 제목, 영어 제목, reference-title variant를 이용하여 검색하고 사전에 정한 bibliographic matching 기준을 충족하는 record가 확인되면 \(D_j=1\), 검색을 완료했지만 match가 없으면 \(D_j=0\)으로 코딩한다. 표본에는 19,436편의 retrievable paper와 35,353편의 nonretrievable paper가 있다.

여기서 retrievability의 범위는 의도적으로 좁다. Exact-title 기반 lookup은 known-item search이므로 broad topic query에서 처음 해당 논문이 발견될 가능성이나 ranking을 측정하지 않는다. 이미 논문을 식별할 수 있는 제목정보가 주어졌을 때 현재 Google Scholar가 해당 bibliographic record를 반환하는지를 측정한다.

보조 변수는 현재 retrievable한 논문에 대한 Google Scholar-mediated full-text access이다. Google Scholar가 제공한 링크가 로그인이나 결제 없이 full text를 여는 경우 accessible로 코딩한다. 이는 인터넷 전체에서의 OA status가 아니라 현재 Google Scholar가 제공하는 접근경로에 조건부인 변수이다.

## 3.2 분석전략

주요 분석은 현재 Google Scholar retrievability에 따른 영어권 인용확률 격차가 citation cohort별로 달라지는지를 검정한다. Target-paper fixed-effects linear probability model은 다음과 같다.

$$
Y_{jc}=\alpha_j+\lambda_c+
\sum_{k=2}^{4}\beta_k
\left(D_j\times1[c=k]\right)
+\gamma AgeBin_{jc}+\epsilon_{jc}.
$$

Target fixed effect \(\alpha_j\)는 시간에 따라 변하지 않는 target-paper attribute를 흡수하고, cohort fixed effect \(\lambda_c\)는 각 기간에 모든 target에 공통적으로 나타나는 citation incidence의 변화를 흡수한다. \(D_j\)는 paper 내에서 변하지 않기 때문에 그 main effect는 target fixed effect에 흡수된다.

따라서 핵심 계수 \(\beta_k\)는 각 후속 cohort의 visible–nonvisible 영어권 인용확률 격차가 C1의 격차와 얼마나 다른지를 나타낸다. 이 계수는 Google Scholar visibility의 causal effect가 아니라 두 집단 사이 gap의 시기별 차이를 의미한다. Standard error는 target paper 수준에서 cluster한다.

Cohort별 eligible-target composition의 변화를 점검하기 위해 2004년까지 출판된 target paper만을 대상으로 같은 분석을 반복한다. 이 논문들은 네 cohort 모두에 기여할 시간적 기회를 가지므로, 후기에 출판된 논문의 추가로 인해 cohort 구성 자체가 바뀌는 문제를 줄일 수 있다.

추가 robustness에서는 Poisson pseudo-maximum likelihood, citation-count outcome, journal·topic·publication-year와 cohort의 추가 control을 사용한다. 이들 분석은 주모형의 결과가 다른 functional form과 통제에서도 어느 정도 유지되는지를 확인하기 위한 것이다.

## 3.3 결과

현재 Google Scholar에서 retrievable한 논문은 모든 cohort에서 nonretrievable paper보다 높은 raw English-language citation incidence를 보인다.

| Cohort | \(D=1\) | \(D=0\) | Raw difference |
| ------ | ------: | ------: | -------------: |
| C1     |   0.68% |   0.31% |       +0.37 pp |
| C2     |   1.90% |   0.67% |       +1.23 pp |
| C3     |   3.01% |   1.25% |       +1.76 pp |
| C4     |   2.66% |   1.38% |       +1.28 pp |

Fixed-effects 분석에서는 C1 대비 visible–nonvisible gap이 C2에서 0.405pp 증가한다(95% CI [0.040, 0.770], \(p=.030\)). C3에서는 0.696pp 증가한다(95% CI [0.329, 1.063], \(p<.001\)). C2와 C3 계수의 joint test 역시 \(p<.001\)이다.

반면 C4의 변화는 0.008pp(95% CI [−0.337, 0.353], \(p=.965\))로, 2020–2024년에 C1 대비 격차가 추가적으로 확대되었다는 근거는 확인되지 않는다.

2004년까지 출판된 target만을 분석해도 C2와 C3의 양의 gap 변화가 나타난다.

| C1 대비 \(D\) gap 변화 |        전체 eligible sample |                2004년까지 출판 |
| ------------------ | ------------------------: | ------------------------: |
| C2                 |  +0.405 pp [0.040, 0.770] |  +0.791 pp [0.227, 1.355] |
| C3                 |  +0.696 pp [0.329, 1.063] |  +0.496 pp [0.027, 0.964] |
| C4                 | +0.008 pp [−0.337, 0.353] | +0.273 pp [−0.175, 0.721] |

Pre-2005 sample에서 C2는 \(p=.006\), C3는 \(p=.038\)이며 C2–C3 joint test는 \(p=.011\)이다. C4는 양의 추정치이지만 통계적으로 불확실하다(\(p=.233\)).

Robustness 결과는 모든 specification에서 동일하지 않다. Target-fixed-effects Poisson에서는 C2와 C3 변화가 양수이지만 영어권 인용이 전혀 없는 target은 conditional model을 식별하지 못하므로 제외된다. 다른 Poisson specification은 더 불정확하며, journal-by-cohort 및 publication-year-by-cohort model에서는 C2의 양의 추정치는 유지되지만 C3와 C4가 통계적으로 유의하게 재현되지는 않는다. 따라서 결과는 main incidence model과 pre-2005 restriction에서 확인된 C2–C3 패턴의 범위에서 해석한다.

현재 Google Scholar에서 visible한 논문들 사이에서는 Google Scholar-mediated full-text access가 cohort별 영어권 citation incidence와 통계적으로 유의한 관계를 보이지 않았다. 이 null result는 access가 일반적으로 중요하지 않다는 의미가 아니라 현재 retrievability에 조건부인 현재 시점의 접근경로가 이 표본의 historical citation pattern을 별도로 구분하지 못했다는 의미이다.

## 3.4 해석

Study 1의 결과는 현재 Google Scholar에서 known-item search로 확인 가능한 논문과 그렇지 않은 논문의 과거 영어권 인용패턴이 동일하지 않음을 보여준다. C1에 비해 visible–nonvisible gap은 C2와 C3에서 확대되며, 네 cohort에 모두 기여할 수 있는 pre-2005 target으로 제한해도 같은 방향의 결과가 나타난다. 그러나 C4에서는 추가적인 확대가 확인되지 않고 일부 대안 specification에서는 결과가 덜 정밀하다.

여기서 0.405pp와 0.696pp는 각 기간의 인용확률 수준 자체가 아니라 C1 대비 visible–nonvisible gap의 추가 변화량이다. 따라서 핵심 결과는 검색 가능한 논문의 인용확률이 모든 시기에 일관되게 더 빠르게 증가했다는 것이 아니라, 격차 확대가 C2와 C3에 집중되고 C4에서는 재현되지 않았다는 것이다.

따라서 이 결과를 Google Scholar가 영어권 인용을 증가시켰다는 증거로 해석할 수 없다. 현재 retrievability는 과거의 circulation, 이후의 web availability, indexing 또는 이들과 함께 변화한 다른 특성과 관련될 수 있다. Study 1이 보여주는 것은 보다 제한적으로 현재 paper-level retrievability가 서로 다른 historical English-language citation trajectory를 가진 논문을 구분한다는 것이다.

# 4. Study 2: Web-Enabled 생성형 검색 감사

## 4.1 Benchmark와 감사 설계

Study 2는 동일한 한국 정치 주제를 다루는 한국어권과 영어권의 주요 문헌이 생성형 검색에서 어느 정도 검색되고 최종 출처로 선택되는지, 그리고 그 격차가 검색조건에 따라 달라지는지를 분석한다.

비교대상은 audit 결과를 본 뒤 사후적으로 정의하지 않고 시스템 실행 전에 benchmark로 고정한다. 이를 통해 결과목록에 특정 언어의 논문이 많이 등장하는지와, 각 언어권에서 사전에 주요 문헌으로 선정된 논문이 실제로 회수되는지를 구분할 수 있다.

Benchmark topic은 한국어권과 영어권 한국 정치학의 연구지형을 비교한 Kim et al. (2025)을 바탕으로 선정한다. 두 학술공간에서 모두 지속적으로 연구되어 온 한국 정치 주제 중 한국 현대정치의 전개를 대체로 시간적 순서에 따라 포괄하도록 다음 다섯 주제를 구성하였다.

1. 한국전쟁
2. 한국 경제발전
3. 한국 민주화
4. 북한 핵문제
5. 한류

주제를 양 언어권에서 공통적으로 연구된 영역으로 제한한 이유는 특정 주제 자체의 연구축적이 한쪽에 거의 없기 때문에 발생하는 차이를 언어별 검색가시성의 차이와 혼동하지 않기 위해서이다. 따라서 비교의 초점은 동일한 substantive topic 안에서 각 언어권의 주요 문헌이 생성형 검색에 얼마나 진입하고 선택되는가에 있다.

각 주제는 의미가 대응하는 한국어·영어 주제어 세 개로 조작화하였다. 실행 시 해당 주제의 세 주제어를 질의 언어에 맞추어 prompt에 모두 제공했으며, 두 언어 조건에서 개념적 범위가 달라지지 않도록 번역대응어를 사용하였다.

| 주제 | 한국어 주제어 | 영어 주제어 |
|---|---|---|
| 한국전쟁 | 한국전쟁; 한국전쟁 발발; 한국전쟁 기원 | Korean War; Outbreak of the Korean War; Origins of the Korean War |
| 한국 경제발전 | 한국 경제발전; 한국 발전국가; 한국 수출주도 산업화 | South Korean Economic Development; Korean Developmental State; South Korean Export-Led Industrialization |
| 한국 민주화 | 한국 민주화; 한국 민주화운동; 한국 시민사회 | South Korean Democratization; South Korean Democracy Movement; South Korean Civil Society |
| 북한 핵문제 | 북핵 문제; 북한 핵무기; 대북 확장억제 | North Korean Nuclear Program; North Korean Nuclear Weapons; Extended Deterrence against North Korea |
| 한류 | 한류; 케이팝; 한국 영화 | Korean Wave; K-pop; South Korean Cinema |

각 주제에는 한국어 논문 10편과 영어 논문 10편을 포함한다. 한국어 benchmark는 DBpia와 KISS, 영어 benchmark는 Web of Science와 Google Scholar를 이용해 구성한다. Candidate pool을 citation count에 따라 정렬한 뒤 두 source에서 공통적으로 상위에 위치하는 논문을 기준으로 주제별 10편을 선정하였다. 최종 benchmark는 한국어 50편과 영어 50편, 총 100편이며 LLM audit 전에 고정하였다. 이는 각 주제의 전체 relevant literature를 포괄하는 gold standard가 아니라 조건 간 상대적 recovery를 비교하기 위한 evaluation set이다.

Audit은 다음 세 요인을 교차한다.

* Query language — 영어 / 한국어
* Source instruction — general web / KCI·DBpia·KISS 명시
* System — OpenAI `gpt-5.6-sol` / Perplexity `sonar-pro`

Query language와 source instruction은 단순한 문구상의 차이가 아니라 retrieval에 입력되는 검색조건으로 사용한다. 한국어 질의나 한국 학술 데이터베이스의 명시가 한국어 benchmark의 상대적 recovery를 변화시킨다면, 해당 문헌의 가시성이 단일한 고정값이라기보다 검색이 구성되는 조건에 따라 달라질 수 있음을 의미한다.

모든 prompt는 해당 주제의 세 주제어를 포함하고 관련 학술문헌 10편을 고정된 JSON 형식으로 요청하였다. 검색횟수는 주제어당 최대 2회, execution당 최대 6회로 제한하였다. 5개 주제 × 4개 prompt condition × 2개 system × 5회 독립 repetition으로 200개의 stateless execution을 수행하며, 최종적으로 1,932개의 valid recommendation occurrence가 생성되었다.

## 4.2 측정과 분석

Benchmark paper \(j\)와 execution \(i\)에 대해 세 결과를 구분한다.

* TraceRecovery — provider가 외부에 노출하는 observable search trace에 benchmark paper가 나타나는지
* Recommendation — benchmark paper가 final recommendation에 포함되는지
* SuppliedLinkAccess — benchmark가 추천되고 제공된 URL이 로그인이나 결제 없이 full text를 제공하는지

앞의 두 지표가 Study 2에서의 검색 가시성을 구성한다. TraceRecovery는 관찰 가능한 검색단계에 진입했는지를, Recommendation은 그 문헌이 최종 source selection을 통과했는지를 측정한다. SuppliedLinkAccess는 이와 구분되는 후속 접근결과이다.

Benchmark panel은 4,000개의 paper × execution observation으로 구성된다. 200개의 execution 각각에 해당 topic의 한국어 benchmark 10편과 영어 benchmark 10편을 대응시킨다. `SuppliedLinkAccess`의 denominator는 모든 benchmark-paper × execution pair이므로 이는 추천된 논문에 조건부인 access rate가 아니라 검색, 추천, 접근을 함께 통과했는지를 나타내는 joint pipeline-survival outcome이다.

영어 general-web condition을 baseline으로 한국어와 영어 benchmark의 recovery gap을 추정하고, query language와 source instruction이 이 격차를 어떻게 변화시키는지를 분석한다. 두 intervention을 동시에 적용한 combined condition과 baseline의 전체 contrast도 별도로 산출한다.

이와 별도로 전체 recommendation 가운데 한국어 논문이 차지하는 비율을 Korean-language representation으로 측정한다. 이는 benchmark recovery가 아니다. Benchmark에 포함되지 않은 한국어 논문도 representation에는 포함되기 때문에, 결과목록의 언어구성과 사전에 정한 주요 문헌의 회수는 서로 다른 결과이다.

마지막으로 927개의 distinct supplied URL 또는 no-URL item key를 검토하여 accessible full text, abstract only, paywalled, broken link, hallucinated/unverifiable publication으로 분류한다. 여기서 access는 웹 전체에서 해당 논문의 다른 무료 copy를 찾는 것이 아니라 실제 제공된 URL의 상태를 측정한다.

## 4.3 결과

영어 질의와 일반 웹검색을 사용한 baseline에서는 두 benchmark 모두 recovery가 낮았으며 한국어 benchmark가 추가적인 deficit을 보였다.

| 단계                       | 영어 benchmark | 한국어 benchmark | 한국어–영어 격차 |         95% CI | \(p\) |
| ------------------------ | -----------: | ------------: | --------: | -------------: | ----: |
| Observable search trace  |         3.4% |          0.0% |   −3.4 pp | [−6.46, −0.34] |  .029 |
| Final recommendation     |         3.2% |          0.0% |   −3.2 pp | [−5.77, −0.63] |  .015 |
| Accessible supplied link |         0.6% |          0.0% |   −0.6 pp |  [−1.76, 0.56] |  .311 |

Observable search trace와 final recommendation에서는 통계적으로 유의한 한국어–영어 gap이 확인된다. Accessible supplied link의 차이는 유의하지 않지만, benchmark가 마지막 단계까지 도달하는 경우 자체가 매우 적기 때문에 floor와 함께 해석해야 한다.

한국어 query는 observable search 단계의 Korean–English gap을 +3.8pp 변화시키고(95% CI [0.72, 6.88], \(p=.016\)), Korean-database instruction은 +4.0pp 변화시킨다(95% CI [0.73, 7.27], \(p=.017\)). Final recommendation에서는 database instruction이 gap을 +3.2pp 변화시킨다(95% CI [0.71, 5.69], \(p=.012\)). Korean-query estimate는 +2.6pp로 같은 방향이지만 \(p=.068\)로 더 불확실하다.

두 조건을 함께 적용한 combined condition과 baseline을 직접 비교하면 Korean–English gap은 observable search에서 +5.6pp, recommendation에서 +6.4pp 변화한다. Combined condition에서 한국어 benchmark의 observable-trace recovery는 2.2%, recommendation recovery는 3.2%이다. 이는 relative gap의 reversal이지만 높은 절대 recovery를 의미하지 않는다. 한국어 benchmark-paper opportunity의 96% 이상이 여전히 최종 추천에 포함되지 않는다.

검색조건은 benchmark recovery보다 recommendation의 언어적 구성을 훨씬 크게 바꾼다.

| Prompt condition                | Recommendation의 한국어 논문 비율 |
| ------------------------------- | ------------------------: |
| English + general web           |                      0.0% |
| English + Korean DB instruction |                     35.3% |
| Korean + general web            |                     55.8% |
| Korean + Korean DB instruction  |                 91.2% |

한국어 query는 recommendation의 Korean-language share를 55.7pp 증가시키고(\(p<.001\)), Korean-database instruction은 35.4pp 증가시킨다(\(p<.001\)). 그러나 combined condition에서도 사전에 선정한 한국어 benchmark의 recommendation recovery는 3.2%에 그친다.

따라서 추천결과가 한국어 중심으로 구성된다는 것과 한국어권의 사전 지정 주요 문헌이 높은 비율로 회수된다는 것은 동일하지 않다. 이는 benchmark 밖의 한국어 논문이 부적절하다는 뜻이 아니라 language representation과 benchmark recovery가 서로 다른 속성을 측정한다는 의미이다.

전체 1,932개의 recommendation occurrence 가운데 제공된 링크의 결과는 다음과 같다.

* 854개(44.2%) — full text 접근 가능
* 859개(44.5%) — 접근 제한

  * abstract-only 247개
  * paywall 612개
* 219개(11.3%) — invalid 또는 unverifiable

  * broken link 176개
  * coded hallucinated publication 43개

| 제공된 링크의 결과              |    전체 | 한국어 논문 | 영어 논문 |
| ----------------------- | ----: | -----: | ----: |
| Accessible              | 44.2% |  46.3% | 42.4% |
| Access restricted       | 44.5% |  47.9% | 41.6% |
| Invalid or unverifiable | 11.3% |   5.8% | 16.0% |
| — Broken link           |  9.1% |   3.3% | 14.1% |
| — Hallucinated item     |  2.2% |   2.6% |  1.9% |

Prompt condition과 system을 통제하면 recommended-item language는 full access, access restriction 또는 invalid/unverifiable outcome과 독립적으로 유의한 관계를 보이지 않는다. 따라서 raw language difference를 publication language 자체의 효과로 해석하지 않는다.

## 4.4 해석

Study 2에서 한국어–영어 가시성 격차는 검색과 최종 source selection에서 직접 관찰된다. 영어 general-web baseline에서는 한국어 benchmark가 observable search trace와 recommendation에서 모두 회수되지 않았으며, 한국어 질의와 한국 학술 데이터베이스 지시는 상대적 gap을 줄였다. 그러나 이러한 조건 변화가 높은 절대 recovery로 이어지지는 않았다.

두 조건을 함께 적용한 경우에는 gap의 방향이 반전되지만, 이는 한국어 benchmark가 충분히 회수되었다는 의미가 아니다. 검색 회수율 2.2%와 추천 회수율 3.2%는 상대적 격차의 개선과 절대적 discovery bottleneck이 동시에 존재할 수 있음을 보여준다. 또한 search trace는 provider가 공개한 범위만 관찰하므로 내부 retrieval 전체로 해석하지 않는다.

또한 한국어 representation의 큰 변화와 benchmark recovery의 낮은 수준이 동시에 나타났다. 따라서 생성형 검색에서 한국어 문헌이 많이 제시되는 것만으로 한국어권의 주요 학술기록이 충분히 가시화되었다고 볼 수 없다.

추천 이후의 full-text access는 별도의 제약을 보여준다. 전체 recommendation 가운데 절반 미만만 제공된 URL을 통해 바로 원문으로 연결되었으나, 이 단계에서는 검색과 추천에서 나타난 것과 같은 유의한 한국어–영어 격차가 확인되지 않았다.

# 5. 종합 논의

## 5.1 주요 발견의 종합

두 Study가 공통으로 보여주는 것은 한국어권에서 학술적으로 사용되거나 주요하게 다뤄진 문헌이 다른 검색환경에서 자동적으로 동일한 가시성을 갖는 것은 아니라는 점이다. 다만 두 연구에서 가시성이 의미하는 바와 증거의 성격은 구분해야 한다.

Study 1의 분석대상은 2000–2025년에 생산된 한국어권 정치학 논문들이 인용한 한국 정치 관련 문헌이다. 이 문헌들 가운데 현재 Google Scholar의 known-item search에서 확인되는 논문과 그렇지 않은 논문의 영어권 인용확률 격차는 시기에 따라 다르게 나타났다. 특히 기준기간보다 2010–2014년과 2015–2019년에 격차가 확대되었지만, 2020–2024년에는 추가 확대가 확인되지 않았다. 여기서 가시성은 broad discovery가 아니라 현재 bibliographic retrievability를 의미하며, 영어권 citation은 그와 비교되는 별도의 historical outcome이다.

Study 2에서는 가시성을 현재의 생성형 검색과정에서 직접 관찰한다. 영어 general-web baseline에서 한국어 benchmark의 observable search-trace recovery와 final recommendation recovery가 영어 benchmark보다 낮았고, 그 격차는 한국어 질의와 한국 학술 데이터베이스 지시에 따라 변화하였다. 따라서 Study 2의 가시성은 사전에 정의한 문헌이 검색과 최종 source selection을 통과하는가를 의미한다.

Figure 1에서 보듯이, Study 1의 격차 확대는 C2와 C3에 집중되고 C4에서는 확인되지 않는다. Study 2에서는 baseline의 한국어 deficit이 검색조건에 따라 반전되지만 절대 recovery는 낮으며, combined condition에서 한국어 추천 비율은 91.2%까지 증가해도 한국어 benchmark recommendation recovery는 3.2%에 머문다.

![Study 1의 Google Scholar 가시성과 Study 2의 생성형 검색 결과](combined_analysis/figures/discovery_bottleneck_combined_simple.png){width=100%}

이 차이 때문에 두 결과를 하나의 인과 메커니즘으로 결합해서는 안 된다. Study 1은 현재의 paper-level retrievability와 historical English-language citation pattern 사이의 association을 보여주며, Study 2는 현재 조건에서 나타나는 retrieval 및 recommendation difference를 실험적으로 비교한다. 두 연구가 공유하는 것은 검색환경이 문헌을 후보로 포함하고 선택하는 과정 자체가 관찰 가능한 차이를 만든다는 것이다.

Study 2의 결과는 특히 language representation과 scholarly recovery의 차이를 명확하게 보여준다. Combined condition에서는 추천의 91.2%가 한국어 논문이지만 사전에 선정한 한국어 benchmark의 recommendation recovery는 3.2%이다. 따라서 결과목록이 언어적으로 local해 보이는 것과 특정 local scholarly record가 실제로 가시화되는 것은 다른 문제이다.

원문 접근 역시 가시성과 동일하지 않다. Study 1에서는 현재 Google Scholar-mediated access가 영어권 인용과 별도의 유의한 관계를 보이지 않았으며, Study 2에서도 추천된 문헌의 절반 미만만 제공된 링크로 직접 원문에 접근할 수 있었지만 한국어와 영어 사이의 유의한 access gap은 나타나지 않았다. 본 연구의 결과는 따라서 `retrieval → access → citation`이라는 단일한 연쇄효과를 지지하지 않는다. 검색가능성, source selection, access through provided links는 서로 구분되는 결과이다.

두 Study의 시간적 범위도 다르다. Google Scholar는 오랫동안 학술검색에 사용되어 온 환경인 반면(Jamali and Asadi 2010; Cothran 2011; Blankstein 2022), web-enabled generative search는 훨씬 최근의 환경이다. Study 1의 citation cohort를 생성형 검색의 등장과 연결해서는 안 되며, 현재 생성형 검색에서의 직접적인 근거는 Study 2에서 나온다.

## 5.2 정치학적 함의와 후속연구

본 연구의 정치학적 함의는 검색기술이 국제적 지식 불평등을 단독으로 결정한다는 데 있지 않다. 기존 연구는 정치학의 연구대상, 출판, 데이터베이스 coverage, 국제 인용이 지역과 언어에 따라 불균등하게 구성되어 있음을 이미 보여왔다(Breuning et al. 2018; Wilson and Knutsen 2022; Mongeon and Paul-Hus 2016). 한국 정치학에서도 KCI와 SSCI를 중심으로 연구 주제와 방법론이 다른 학술공간이 병존한다(Rhee 2026).

본 연구가 추가하는 것은 문헌이 검색 가능한 후보가 되고 최종 출처로 선택되는 과정도 국제적 가시성의 한 차원으로 측정할 수 있다는 점이다. 한국어권에서 이미 인용된 문헌이라도 현재 국제적으로 이용되는 학술검색 환경에서 모두 동일하게 검색되는 것은 아니며, 생성형 검색이 다수의 한국어 논문을 제시하더라도 한국어권의 사전 지정 주요 문헌이 같은 정도로 회수되는 것도 아니다.

이 관점에서 검색환경은 문헌의 학술적 가치를 직접 결정한다기보다 어떤 문헌이 평가받을 후보집합에 들어오는가를 구조화한다. Discovery bottleneck의 정치학적 의미는 검색결과의 언어적 외형보다, 현지 학술공간에서 축적된 구체적 문헌이 실제 평가대상으로 제시되는지를 묻는 데 있다.

이 문제는 동일한 정치현상에 대해 현지어와 영어의 학술문헌이 병존하는 경우에 특히 중요하다. 한국 정치에 관한 국제적 지식을 영어권 학술지나 국제 citation index 또는 생성된 reading list만으로 파악하면, 한국어권에 축적된 문헌과 실제로 외부 검색환경에서 가시화되는 subset 사이의 차이를 놓칠 수 있다.

Study 1과 Study 2는 이 차이를 서로 다른 방식으로 통제한다. Study 1은 한국어권에서 실제로 인용된 문헌이라는 공통 출발점을 두고 그 내부에서 현재 retrievability와 영어권 citation pattern을 비교한다. Study 2는 양 언어권에서 모두 연구되어 온 substantive topic을 고정한 뒤, 각 언어권에서 사전에 선정한 주요 문헌의 recovery를 비교한다. 따라서 두 연구 모두 단순히 “한국어 논문이 적다”는 진술보다 동일한 비교범위 안에서 어떤 구체적인 문헌이 검색과 선택을 통과하는가에 초점을 둔다.

이러한 관점에서 본 논문의 discovery bottleneck은 문헌이 관련성이나 학술적 가치에 대한 실질적 평가를 받기 전에 검색과 선택의 관찰 가능한 단계에서 후보집합에 들어오지 못하거나 최종 출처로 남지 못하는 현상을 가리킨다. Study 1에서는 현재 known-item lookup에서도 bibliographic record가 반환되지 않는 상태가 가장 좁은 형태의 bottleneck이고, Study 2에서는 benchmark가 observable search trace 또는 final recommendation에 진입하지 못하는 상태가 이에 해당한다. 두 경우 모두 다른 경로를 통한 발견 가능성을 부정하는 개념은 아니다.

후속연구에서는 이러한 검색상태를 longitudinal하게 관찰할 필요가 있다. Google Scholar에서 동일한 문헌의 retrievability와 status of provided links를 반복 측정하면 현재 Study 1에서 관찰할 수 없는 indexing 및 접근경로의 변화를 직접 기록할 수 있다. 생성형 검색에서도 동일 benchmark와 조건을 반복 적용하면 현재 관찰된 recovery pattern이 시간이 지나면서 어떻게 변화하는지를 확인할 수 있다. 이러한 자료는 현재 검색상태와 과거 scholarly circulation 사이의 시간적 간극을 줄이고 discovery bottleneck의 형성과 변화를 보다 직접적으로 분석할 수 있게 한다.

# 6. 결론

한국 정치학의 국제적 가시성은 어떤 연구가 출판되고 최종적으로 인용되는가만으로 완전히 포착되지 않는다. 그 사이에는 문헌이 특정 검색환경에서 검색 가능한 후보로 나타나는지, 최종 출처로 선택되는지, 그리고 원문으로 연결되는지라는 서로 구분되는 단계가 존재한다.

Study 1은 2000–2025년에 생산된 한국어권 정치학 논문들이 인용한 한국 정치 관련 논문 54,789편을 대상으로 현재 Google Scholar의 paper-level retrievability와 과거 영어권 인용패턴을 비교하였다. 현재 검색 가능한 논문과 그렇지 않은 논문의 영어권 인용확률 격차는 기준기간보다 2010–2014년과 2015–2019년에 유의하게 더 컸으나 2020–2024년에는 추가적인 확대가 확인되지 않았다. 현재 Google Scholar가 제공하는 full-text route는 영어권 citation incidence와 별도의 유의한 관계를 보이지 않았다. 이는 Google Scholar의 역사적 인과효과가 아니라 현재 known-item retrievability에 따라 historical citation trajectory가 다르게 나타난다는 제한적인 association이다.

Study 2에서는 양 언어권에서 모두 연구되어 온 동일한 한국 정치 주제를 기준으로 한국어와 영어 benchmark를 사전에 구성하여 현재의 생성형 검색을 감사하였다. 영어 general-web baseline에서는 한국어 benchmark가 검색과 final recommendation에서 영어 benchmark보다 유의하게 덜 회수되었다. 한국어 질의와 한국 학술 데이터베이스 지시는 이 상대적 격차를 줄였지만 절대적인 한국어 benchmark recovery는 낮게 유지되었다. 특히 combined condition에서 recommendation의 91.2%가 한국어 논문이어도 사전 지정 한국어 benchmark의 recommendation recovery는 3.2%였다. 따라서 한국어 문헌이 많이 보이는 것과 한국어권의 주요 문헌이 실제로 회수되는 것은 동일하지 않았다.

두 Study 모두 원문 접근에서는 검색 및 추천에서 나타난 차이에 상응하는 유의한 언어격차를 확인하지 못했다. 따라서 본 연구는 retrieval, source selection, access를 하나의 연속적인 효과로 간주하지 않는다. 각 단계는 별도로 측정해야 하는 결과이다.

이 논문에서 discovery bottleneck은 바로 이러한 구분을 포착하기 위한 조작적 개념이다. 문헌은 학술적으로 존재하고 한 학술공간에서 이미 이용되고 있어도 특정 검색환경에서 후보로 나타나지 않을 수 있으며, 검색단계에 진입하더라도 최종 출처로 선택되지 않을 수 있다. 이 개념은 검색기술이 국제적 지식 불평등을 단독으로 발생시킨다는 주장이 아니다. 한국 정치학처럼 한국어권과 영어권에 병렬적인 연구축적이 존재하는 경우, 어떤 문헌이 생산되고 인용되는가와 함께 어떤 문헌이 실제 검색환경에서 가시화되는가를 별도의 국제적 가시성의 차원으로 분석할 필요가 있다는 주장이다.

이 점에서 본 연구는 국제적 가시성을 최종 인용의 결과만으로 보지 않고, 문헌이 평가대상이 되기 전의 검색단계까지 분석범위를 확장한다. 한국어권에서 축적된 지식과 특정 검색환경이 실제로 보여주는 지식 사이의 차이를 측정하는 것은, 국제 정치학에서 어떤 연구가 실질적으로 발견 가능한 scholarly record가 되는지를 이해하기 위한 추가적인 분석축을 제공한다.

# 7. 한계

Study 1의 가장 중요한 한계는 2026년에 관찰한 Google Scholar 환경과 과거 영어권 인용이 발생할 당시의 검색환경이 동일하지 않다는 점이다. 각 target이 언제 Google Scholar에 처음 포함되었는지, 어느 시점부터 현재와 같은 제목으로 검색 가능했는지, 또는 당시 어떤 full-text link가 제공되었는지는 알 수 없다. 과거 연구자들이 실제로 Google Scholar를 통해 해당 문헌을 발견했는지도 관찰하지 않는다. 연구자들은 Web of Science, 도서관 데이터베이스, 참고문헌 추적, 학술지 browsing, 동료 추천 등 다양한 경로를 사용할 수 있었으므로 현재 retrievability를 과거의 실제 discovery opportunity와 동일시할 수 없다.

Citation cohort는 이 문제를 해결하기 위한 historical indexing proxy가 아니다. 그 목적은 현재 retrievability에 따른 영어권 인용격차가 서로 다른 기간에 어떻게 나타났는지를 비교하는 데 있다. Pre-2005 restriction 역시 historical search environment를 복원하지 않는다. 이 분석은 늦게 출판된 target이 초기 cohort에 기여하지 못해 발생하는 eligible-target composition의 변화를 줄이고, 네 기간 모두에서 비교 가능한 보다 일정한 target set에서도 결과가 나타나는지를 점검하기 위한 것이다.

현재 Google Scholar retrievability 자체가 이전 scholarly circulation과 관련되어 있을 가능성도 남는다. 널리 인용되거나 웹에 더 많이 노출된 논문이 이후 Google Scholar에서 검색되기 쉬워졌을 수 있다. Target fixed effects는 시간불변의 paper characteristic을 흡수하지만 이러한 temporal ordering이나 time-varying process를 제거하지 못한다. 따라서 Study 1의 결과는 현재 retrievability와 historical citation trajectory의 association으로 제한하여 해석한다.

Study 1의 검색가능성에는 bibliographic matching error의 가능성도 있다. 한국어·영어 제목과 reference-title variant를 사용했지만 metadata의 오기, 제목 변형, 중복 record 또는 불완전한 indexing 때문에 실제 존재하는 record를 놓치거나 잘못 연결했을 수 있다. 따라서 (D_j)는 Google Scholar 전체 coverage의 완전한 측정이 아니라 본 연구의 검색·매칭 절차에서 확인된 현재 상태이다.

Study 1의 결과는 specification에 따라서도 강도가 달라진다. Main incidence model과 pre-2005 restriction에서는 C2와 C3의 gap 확대가 나타나지만 일부 Poisson 및 추가-control specification에서는 결과가 더 불확실하다. 따라서 모든 outcome과 functional form에서 동일한 패턴이 확인되었다고 일반화할 수 없다. 현재 full-text access 분석 역시 Google Scholar visibility에 조건부이며 영어권 citation incidence와 유의한 관계를 보이지 않았다.

Study 2는 두 개의 시스템, 다섯 개의 한국 정치 주제, 한 번의 collection period, 100편의 사전 지정 benchmark에 한정된다. 다섯 주제는 양 언어권에서 모두 연구되어 온 영역을 비교하기 위해 선정되었지만 한국 정치학 전체를 대표하는 확률표본은 아니다. Benchmark 역시 각 주제의 모든 relevant literature를 포괄하지 않으므로 낮은 benchmark recovery가 benchmark 밖의 recommendation이 관련성 없음을 의미하지 않는다.

Benchmark 선정이 citation count와 두 출처의 공통 상위문헌에 의존한다는 점도 범위를 제한한다. 이 절차는 각 언어권에서 이미 비교적 가시적인 문헌을 중심으로 안정적인 evaluation set을 만들지만, 최근 연구·저인용 연구·전문 주제의 문헌을 충분히 대표하지 못할 수 있다. 따라서 recovery는 한국 정치학 전체에 대한 recall이 아니라 사전에 정한 benchmark에 대한 회수율이다.

생성형 검색환경은 지속적으로 변한다. 동일한 model name 아래에서도 underlying model, search index, ranking procedure 또는 provider interface가 달라질 수 있으므로 Study 2는 수집시점의 behavior를 측정한다. 또한 provider가 외부에 노출하는 trace의 범위가 다르기 때문에 observable search trace를 시스템 내부의 전체 retrieval process와 동일시할 수 없다.

Accessible-link outcome은 특히 baseline에서 희소하다. Retrieval과 recommendation 자체가 낮기 때문에 access 단계에는 강한 floor가 존재한다. 따라서 한국어와 영어 사이에 유의한 access gap이 발견되지 않았다는 결과를 두 언어 문헌의 접근성이 동일하다는 증거로 해석해서는 안 된다.

Link audit은 시스템이 실제 제공한 URL만 평가한다. Paywall, abstract-only page 또는 broken link로 분류된 논문이 인터넷의 다른 위치에서도 이용 불가능하다는 의미는 아니다. Hallucination event 역시 적고 특정 experimental cell에 집중되어 있어 system-level 특성으로 일반화하기 어렵다.

마지막으로 두 Study 모두 문헌이 가시화된 이후 연구자가 실제로 무엇을 하는지는 관찰하지 않는다. 검색결과의 클릭, 원문의 열람, substantive relevance 평가, 언어능력, perceived quality, citation norm, collaboration network 및 publication venue 등은 후속 이용과 인용에 영향을 줄 수 있다. 따라서 본 논문의 증거는 전체적인 지식순환 과정이 아니라 검색환경에서의 paper-level visibility, source selection, 그리고 access through provided links에 한정된다.

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
