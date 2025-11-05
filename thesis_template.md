---
title: "Your Thesis Title"
author:
  - name: "Your Full Name"
degree: "Doctor of Philosophy (PhD)"
university: "Your University Name"
faculty: "Your Faculty/School"
department: "Your Department"
supervisors:
  - name: "Supervisor One, PhD"
  - name: "Supervisor Two, PhD"
date: 2025-10
keywords: [keyword1, keyword2, keyword3]
lang: en-US

# Pandoc/PDF options (adjust/remove if not using Pandoc)
documentclass: book
fontsize: 12pt
linestretch: 1.5
geometry: margin=1in
toc: true
toc-depth: 3
numbersections: true
link-citations: true
bibliography: references.bib
csl: apa.csl
---

<!--
Thesis Markdown Template

Instructions:
- Replace YAML metadata above with your details.
- Write content in sections below. Use Pandoc to build PDF/Docx/HTML if desired.
- Citations require a BibTeX file (see `references.bib`).
-->

# Title Page

<!-- Pandoc will generate a title page from YAML for many outputs. If your institution
requires a specific layout, replace this section with a custom title page. -->

> This thesis is submitted in partial fulfillment of the requirements for the degree of
> Doctor of Philosophy at {university}.

\newpage

# Declaration

I certify that the work presented in this thesis is, to the best of my knowledge and belief,
original, except as acknowledged. The material has not been submitted, either in whole or in part,
for a degree at this or any other institution.

Signature: _________________________  Date: ___________________

\newpage

# Abstract

Provide a concise summary of the research problem, methods, key results, and conclusions.
Aim for 150–300 words, depending on your institution's rules.

\newpage

# Acknowledgements

Thank those who supported your research (supervisors, collaborators, funding bodies, family, etc.).

\newpage

# Table of Contents

<!-- Generated automatically when `toc: true`. Keep a manual placeholder for some outputs. -->

\newpage

# List of Figures

<!-- If required by your institution. Pandoc can generate this with filters; otherwise keep manual. -->

\newpage

# List of Tables

<!-- If required by your institution. -->

\newpage

# Abbreviations and Acronyms

| Abbreviation | Definition |
| --- | --- |
| ABC | Your term here |
| XYZ | Your term here |

\newpage

# Preface (optional)

Explain the context, any prior publications included, and your contribution if the thesis
includes co-authored work.

\newpage

# Chapter 1 — Introduction

- State the research problem and motivation.
- Define scope, objectives, and contributions.
- Outline structure of the thesis.

## Background and Motivation

Provide sufficient context for readers unfamiliar with the domain.

## Research Questions and Objectives

List your primary and secondary research questions and measurable objectives.

## Thesis Structure

Briefly summarize what each chapter contains.

\newpage

# Chapter 2 — Literature Review

- Synthesize prior work, identify gaps, and position your contribution.
- Establish theoretical framework if applicable.

## Thematic Area A

Discuss key papers [@doe2020; @smith2019] and their limitations.

## Thematic Area B

Compare methods, datasets, and results across studies.

## Summary of Gaps

Summarize gaps that motivate your approach.

\newpage

# Chapter 3 — Methods

- Describe methodology, data, materials, and analysis procedures in reproducible detail.

## Data and Materials

Describe datasets, inclusion criteria, and pre-processing steps.

## Experimental Design / Algorithm

Provide step-by-step methods with parameters, hyperparameters, or protocol details.

```python
# Example: Pseudocode or code listing
def train_model(training_data, learning_rate, num_epochs):
    for epoch in range(num_epochs):
        loss = optimize(training_data, learning_rate)
        print(f"Epoch {epoch}: loss={loss}")
```

## Statistical Analysis

Describe statistical tests, confidence intervals, effect sizes, and assumptions.

## Ethics (if applicable)

Summarize approvals and consent.

\newpage

# Chapter 4 — Results

- Present findings objectively with appropriate figures, tables, and statistics.

## Primary Outcomes

Summarize main results with measures of variability and uncertainty.

![Example figure caption](figures/example-plot.png){#fig:example width=80%}

Refer to Figure @fig:example for an illustration of the trend.

Table: Example results table {#tbl:results}

| Group | Metric A | Metric B |
| --- | ---: | ---: |
| Control | 1.23 | 4.56 |
| Treatment | 2.34 | 5.67 |

## Secondary Analyses

Report supplementary results and robustness checks.

\newpage

# Chapter 5 — Discussion

- Interpret results, relate to literature, and discuss implications.
- Address limitations and threats to validity.

## Interpretation of Findings

Explain how results answer the research questions.

## Limitations

Be explicit about constraints and potential biases.

## Implications and Future Work

Propose next steps and broader impact.

\newpage

# Chapter 6 — Conclusion

- Recap problem, approach, and key contributions.
- Provide a concise closing statement.

\newpage

# References

<!-- Pandoc will populate from `references.bib`. Ensure `csl` matches your required style. -->

\newpage

# Appendices

## Appendix A — Additional Figures

Add supplementary figures, methods, or extended results.

## Appendix B — Questionnaires / Protocols

Include instruments or detailed protocols.

\newpage

# Writing and Formatting Notes (remove before submission)

- Use active voice and clear, concise sentences.
- Ensure figure/table captions are self-contained.
- Cite sources consistently (e.g., APA/IEEE/Chicago via CSL).
- Keep a consistent notation section if using heavy mathematics.

## Math and Notation Examples

Inline math like \(E = mc^2\) and display equations:

\[
\hat{y} = f(\mathbf{x};\, \theta) = \sum_{i=1}^{n} w_i x_i + b
\]

Define symbols on first use and keep a symbol glossary if needed.

## Cross-References

- Label figures/tables with `{#fig:...}` and `{#tbl:...}` and reference as `@fig:...` or `@tbl:...`.
- Label equations with `\label{eq:...}` in LaTeX blocks and reference as `\eqref{eq:...}`.

## Build Tips (Pandoc)

```bash
pandoc thesis_template.md \
  --from markdown+tex_math_dollars \
  --pdf-engine=xelatex \
  --output thesis.pdf
```

For Word output:

```bash
pandoc thesis_template.md --output thesis.docx
```

For HTML output:

```bash
pandoc thesis_template.md --toc --standalone --output thesis.html
```

