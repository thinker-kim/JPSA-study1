STUDY 1 COHORT DATA

Main file:
  study1_cohort_panel_D_main.csv

Unit:
  target paper j × cohort c

Cohorts:
  C1 <= 2009
  C2 2010-2014
  C3 2015-2019
  C4 2020-2024

Outcome:
  Y_jc

Exposure:
  D_j = google_scholar_indexed

Access:
  A_j = google_scholar_open_fulltext, conditional on D_j=1

Main interactions:
  D_x_C2, D_x_C3, D_x_C4

Access interactions:
  A_x_C2, A_x_C3, A_x_C4

Important:
  N_topic_jc and ln_offset are intentionally excluded from these final
  cohort-analysis datasets.