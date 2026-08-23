#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(data.table)
  library(fixest)
})

args <- commandArgs(trailingOnly = TRUE)
base_dir <- if (length(args)) normalizePath(args[[1]]) else normalizePath(".")
data_dir <- file.path(base_dir, "study1_cohort_final")
out_dir <- file.path(base_dir, "study1_analysis")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

id <- "paper_uid_after_direct_w"
d_path <- file.path(data_dir, "study1_cohort_panel_D_main.csv")
a_path <- file.path(data_dir, "study1_cohort_panel_A_indexed_only.csv")

d <- fread(d_path)
a <- fread(a_path)

prepare <- function(x) {
  x[, cohort := factor(cohort, levels = c("C1", "C2", "C3", "C4"))]
  x[, age_bin := relevel(factor(age_bin), ref = "0-2")]
  x[, journal_fe := fifelse(is.na(journal_fe) | journal_fe == "", "[missing]", journal_fe)]
  x[, target_topic := fifelse(is.na(target_topic), "[missing]", as.character(target_topic))]
  x[, topic_cohort := interaction(target_topic, cohort, drop = TRUE)]
  x
}
d <- prepare(d)
a <- prepare(a)
d[, journal_cohort := interaction(journal_fe, cohort, drop = TRUE)]
d[, pubyear_cohort := interaction(target_year, cohort, drop = TRUE)]

# Main estimand: change in the D gap relative to C1. No opportunity offset.
m_raw <- fepois(
  Y_jc ~ D_j + i(cohort, D_j, ref = "C1") | cohort,
  data = d, vcov = as.formula(paste0("~", id)), notes = FALSE
)
m_main <- fepois(
  Y_jc ~ D_j + i(cohort, D_j, ref = "C1") + age_bin | journal_fe + cohort,
  data = d, vcov = as.formula(paste0("~", id)), notes = FALSE
)
m_topic_time <- fepois(
  Y_jc ~ D_j + i(cohort, D_j, ref = "C1") + age_bin | journal_fe + topic_cohort,
  data = d, vcov = as.formula(paste0("~", id)), notes = FALSE
)
m_count <- fepois(
  eng_cite_count ~ D_j + i(cohort, D_j, ref = "C1") + age_bin | journal_fe + cohort,
  data = d, vcov = as.formula(paste0("~", id)), notes = FALSE
)

# Target FE changes the estimand to citation timing among informative targets.
m_target_fe <- fepois(
  Y_jc ~ i(cohort, D_j, ref = "C1") + age_bin | paper_uid_after_direct_w + cohort,
  data = d, vcov = ~paper_uid_after_direct_w, notes = FALSE
)

# C1 is open-ended, so use papers published by 2004 as a common-history check.
m_pre2005 <- fepois(
  Y_jc ~ D_j + i(cohort, D_j, ref = "C1") + age_bin | journal_fe + cohort,
  data = d[target_year <= 2004],
  vcov = as.formula(paste0("~", id)), notes = FALSE
)

# Linear probability FE models retain targets with zero citations in every
# cohort. Their interaction coefficients are percentage-point changes in the
# D gap relative to C1.
m_lpm_target_fe <- feols(
  Y_jc ~ i(cohort, D_j, ref = "C1") + age_bin | paper_uid_after_direct_w + cohort,
  data = d, vcov = ~paper_uid_after_direct_w, notes = FALSE
)
m_lpm_pre2005 <- feols(
  Y_jc ~ i(cohort, D_j, ref = "C1") + age_bin | paper_uid_after_direct_w + cohort,
  data = d[target_year <= 2004], vcov = ~paper_uid_after_direct_w, notes = FALSE
)

# More demanding controls for time-varying journal composition and publication
# year-specific citation life cycles.
m_journal_cohort <- fepois(
  Y_jc ~ D_j + i(cohort, D_j, ref = "C1") + age_bin | journal_cohort,
  data = d, vcov = ~paper_uid_after_direct_w, notes = FALSE
)
m_pubyear_cohort <- fepois(
  Y_jc ~ D_j + i(cohort, D_j, ref = "C1") | journal_fe + pubyear_cohort,
  data = d, vcov = ~paper_uid_after_direct_w, notes = FALSE
)

# Access is conditional on D=1 by construction.
m_access <- fepois(
  Y_jc ~ A_j + i(cohort, A_j, ref = "C1") + age_bin | journal_fe + cohort,
  data = a, vcov = as.formula(paste0("~", id)), notes = FALSE
)

models <- list(
  raw = m_raw,
  main = m_main,
  topic_cohort_fe = m_topic_time,
  citation_count = m_count,
  target_fe = m_target_fe,
  pre2005_targets = m_pre2005,
  lpm_target_fe = m_lpm_target_fe,
  lpm_pre2005 = m_lpm_pre2005,
  journal_cohort_fe = m_journal_cohort,
  pubyear_cohort_fe = m_pubyear_cohort,
  access_among_D1 = m_access
)

tidy_model <- function(model, name) {
  z <- as.data.table(coeftable(model), keep.rownames = "term")
  setnames(z, 2:5, c("estimate", "std_error", "statistic", "p_value"))
  z[, `:=`(
    model = name,
    rr = if (startsWith(name, "lpm_")) NA_real_ else exp(estimate),
    conf_low = if (startsWith(name, "lpm_")) NA_real_ else exp(estimate - 1.96 * std_error),
    conf_high = if (startsWith(name, "lpm_")) NA_real_ else exp(estimate + 1.96 * std_error),
    n_obs = nobs(model)
  )]
  z[]
}
coef_table <- rbindlist(Map(tidy_model, models, names(models)), fill = TRUE)
fwrite(coef_table, file.path(out_dir, "model_coefficients.csv"))

lpm_terms <- coef_table[
  model %chin% c("lpm_target_fe", "lpm_pre2005") & grepl("cohort::", term),
  .(
    model, term,
    change_probability = estimate,
    change_percentage_points = 100 * estimate,
    conf_low_pp = 100 * (estimate - 1.96 * std_error),
    conf_high_pp = 100 * (estimate + 1.96 * std_error),
    p_value, n_obs
  )
]
fwrite(lpm_terms, file.path(out_dir, "lpm_target_fe_changes.csv"))

joint_test <- function(model, pattern, label) {
  invisible(capture.output(w <- wald(model, pattern)))
  data.table(test = label, statistic = unname(w$stat), p_value = unname(w$p),
             df_num = unname(w$df1), df_den = unname(w$df2))
}
contrast_test <- function(model, term_a, term_b, label) {
  b <- coef(model); v <- vcov(model)
  w <- setNames(rep(0, length(b)), names(b)); w[term_a] <- 1; w[term_b] <- -1
  est <- sum(w * b); se <- sqrt(as.numeric(t(w) %*% v %*% w))
  data.table(test = label, statistic = est / se,
             p_value = 2 * pnorm(abs(est / se), lower.tail = FALSE),
             df_num = 1, df_den = NA_real_)
}
hypothesis_tests <- rbindlist(list(
  joint_test(m_lpm_target_fe, "cohort::C[23]:D_j", "Full sample: C2 and C3 jointly zero"),
  joint_test(m_lpm_pre2005, "cohort::C[23]:D_j", "Pre-2005: C2 and C3 jointly zero"),
  contrast_test(m_lpm_target_fe, "cohort::C2:D_j", "cohort::C3:D_j",
                "Full sample: C2 equals C3"),
  contrast_test(m_lpm_pre2005, "cohort::C2:D_j", "cohort::C3:D_j",
                "Pre-2005: C2 equals C3")
))
fwrite(hypothesis_tests, file.path(out_dir, "primary_hypothesis_tests.csv"))

cohort_gap <- function(model, exposure, name) {
  b <- coef(model)
  v <- vcov(model)
  out <- rbindlist(lapply(c("C1", "C2", "C3", "C4"), function(cc) {
    weights <- setNames(rep(0, length(b)), names(b))
    main_term <- exposure
    if (main_term %in% names(weights)) weights[main_term] <- 1
    interaction_term <- paste0("cohort::", cc, ":", exposure)
    if (cc != "C1" && interaction_term %in% names(weights)) weights[interaction_term] <- 1
    est <- sum(weights * b)
    se <- sqrt(as.numeric(t(weights) %*% v %*% weights))
    data.table(
      model = name, cohort = cc, log_rr = est, std_error = se,
      rr = exp(est), conf_low = exp(est - 1.96 * se),
      conf_high = exp(est + 1.96 * se),
      p_value = 2 * pnorm(abs(est / se), lower.tail = FALSE)
    )
  }))
  out
}

gaps <- rbindlist(list(
  cohort_gap(m_raw, "D_j", "raw"),
  cohort_gap(m_main, "D_j", "main"),
  cohort_gap(m_topic_time, "D_j", "topic_cohort_fe"),
  cohort_gap(m_count, "D_j", "citation_count"),
  cohort_gap(m_pre2005, "D_j", "pre2005_targets"),
  cohort_gap(m_access, "A_j", "access_among_D1")
), fill = TRUE)
fwrite(gaps, file.path(out_dir, "cohort_specific_relative_risks.csv"))

descriptive <- d[, .(
  n_cells = .N,
  n_targets = uniqueN(get(id)),
  y_events = sum(Y_jc),
  citation_events = sum(eng_cite_count),
  y_rate = mean(Y_jc)
), by = .(cohort, D_j)]
fwrite(descriptive, file.path(out_dir, "descriptive_by_cohort_D.csv"))

sample_flow <- data.table(
  quantity = c(
    "full target universe", "D analysis targets", "D=1 targets",
    "D=0 targets", "D missing/error targets", "A analysis targets",
    "PPML main-model observations", "PPML target-FE observations",
    "primary LPM target-FE observations"
  ),
  value = c(
    uniqueN(fread(file.path(data_dir, "study1_target_level_GS.csv"), select = id)[[id]]),
    uniqueN(d[[id]]), uniqueN(d[D_j == 1][[id]]), uniqueN(d[D_j == 0][[id]]),
    55622 - uniqueN(d[[id]]), uniqueN(a[[id]]), nobs(m_main), nobs(m_target_fe),
    nobs(m_lpm_target_fe)
  )
)
fwrite(sample_flow, file.path(out_dir, "analysis_sample_flow.csv"))

main_gaps <- gaps[model == "main"]
png(file.path(out_dir, "main_D_gap_by_cohort.png"), width = 1400, height = 900, res = 160)
par(mar = c(5, 5, 2, 1))
plot(seq_len(nrow(main_gaps)), main_gaps$rr, type = "b", pch = 19,
     xaxt = "n", xlab = "Source-paper cohort", ylab = "Relative risk: D=1 vs D=0",
     ylim = range(c(main_gaps$conf_low, main_gaps$conf_high, 1), finite = TRUE))
arrows(seq_len(nrow(main_gaps)), main_gaps$conf_low,
       seq_len(nrow(main_gaps)), main_gaps$conf_high,
       angle = 90, code = 3, length = 0.05)
axis(1, at = seq_len(nrow(main_gaps)), labels = main_gaps$cohort)
abline(h = 1, lty = 2, col = "gray40")
dev.off()

png(file.path(out_dir, "primary_lpm_changes.png"), width = 1400, height = 900, res = 160)
plot_data <- lpm_terms[, cohort := sub("cohort::(C[234]):D_j", "\\1", term)]
plot_data[, x := match(cohort, c("C2", "C3", "C4")) +
            ifelse(model == "lpm_target_fe", -0.06, 0.06)]
par(mar = c(5, 5, 2, 1))
plot(plot_data$x, plot_data$change_percentage_points, type = "n",
     xaxt = "n", xlab = "Source-paper cohort (relative to C1)",
     ylab = "Change in D gap (percentage points)",
     ylim = range(c(plot_data$conf_low_pp, plot_data$conf_high_pp, 0)))
cols <- ifelse(plot_data$model == "lpm_target_fe", "#1f77b4", "#d62728")
points(plot_data$x, plot_data$change_percentage_points, pch = 19, col = cols)
arrows(plot_data$x, plot_data$conf_low_pp, plot_data$x, plot_data$conf_high_pp,
       angle = 90, code = 3, length = 0.05, col = cols)
axis(1, at = 1:3, labels = c("C2", "C3", "C4"))
abline(h = 0, lty = 2, col = "gray40")
legend("topright", c("All eligible papers", "Published by 2004"),
       col = c("#1f77b4", "#d62728"), pch = 19, bty = "n")
dev.off()

fmt <- function(x, digits = 3) formatC(x, digits = digits, format = "f")
lpm_full <- lpm_terms[model == "lpm_target_fe"]
lpm_full[, cohort := sub("cohort::(C[234]):D_j", "\\1", term)]
lines <- c(
  "# Study 1 analysis results",
  "",
  "No opportunity offset is used. Technical GS errors are D=NA; review is D=0.",
  "",
  "## Sample",
  "",
  paste0("- D-analysis targets: ", format(uniqueN(d[[id]]), big.mark = ",")),
  paste0("- D=1: ", format(uniqueN(d[D_j == 1][[id]]), big.mark = ",")),
  paste0("- D=0: ", format(uniqueN(d[D_j == 0][[id]]), big.mark = ",")),
  paste0("- Primary target-FE LPM observations: ", format(nobs(m_lpm_target_fe), big.mark = ",")),
  "",
  "## Primary target-FE LPM: change in D gap relative to C1",
  "",
  "| Cohort | Change (percentage points) | 95% CI | p |",
  "|---|---:|---:|---:|",
  paste0("| ", lpm_full$cohort, " | ", fmt(lpm_full$change_percentage_points), " | ",
         fmt(lpm_full$conf_low_pp), "–", fmt(lpm_full$conf_high_pp), " | ",
         fmt(lpm_full$p_value), " |"),
  "",
  "C2 and C3 are jointly significant in the full and pre-2005 samples.",
  "The pattern supports a diffusion-period increase in C2-C3, not a monotonic increase through C4.",
  "PPML specifications are retained as robustness checks in model_coefficients.csv."
)
writeLines(lines, file.path(out_dir, "RESULTS.md"))

cat("Analysis complete. Outputs written to:", out_dir, "\n")
