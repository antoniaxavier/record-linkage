# CLAUDE.md

## Project
Entity resolution benchmark: deterministic vs probabilistic vs ML/NLP record linkage,
served through a simple API.
Portfolio project (GitHub: antoniaxavier). README and code comments in English.

Research questions:
1. How much recall does probabilistic matching (Fellegi-Sunter via Splink, parameters
   estimated by EM) gain over deterministic exact-key rules, at what precision cost?
2. How should the match-score threshold be chosen, and how well calibrated are the
   match probabilities?
3. Does a supervised classifier (scikit-learn) on similarity features beat the
   unsupervised Fellegi-Sunter model when labels exist?
4. Do semantic embeddings (sentence-transformers) add information beyond character-level
   string similarity (RapidFuzz) for product names and descriptions?
5. (Optional) Can an LLM adjudicate borderline pairs (the "clerical review" zone)
   better than the threshold alone, and at what cost?

## About me
Statistician. Strong in R (tidyverse); I already do deterministic matching by exact keys
at work (R + SQL). Python: working knowledge, used scikit-learn and NLP in coursework,
built a Text2SQL project with an LLM. When writing Python, explain non-obvious idioms
briefly and mention the tidyverse/R equivalent when useful (R analogue of Splink:
`fastLink`). Keep code simple and readable.

## Data (all public; never real personal data from my job)
Main dataset: **Amazon-GoogleProducts** benchmark (Leipzig University, CC BY 4.0).
- Download: https://dbs.uni-leipzig.de/files/datasets/Amazon-GoogleProducts.zip
- Two sources: Amazon (1,363 products) and Google Products (3,226 products);
  1,300 true matching pairs in the perfect-mapping file (ground truth).
- Attributes: name/title, description, manufacturer, price. Inspect actual column names,
  encodings and price formats before using them; do not assume.
- Task type: **link-only** (match records across the two sources), not deduplication.
- Citation required in README: the Leipzig benchmark page and Köpcke, Thor & Rahm,
  "Evaluation of entity resolution approaches on real-world match problems", VLDB 2010.
- Development only: `splink_datasets.fake_1000` (small, fast) to test code paths.
- Optional Brazilian case: link public CNPJ data (Receita Federal) to the CEIS list
  (Portal da Transparência) by company name and address, hiding the CNPJ and using it
  only as ground truth.
- Raw data in `data/raw/` (gitignored); processed as Parquet in `data/processed/`.

## Stack
- Python 3.12, environment managed with `uv`
- Splink 4 with DuckDB backend
- polars for data wrangling (pandas only where a library requires it)
- RapidFuzz for string similarity features
- sentence-transformers (small multilingual model, runs on CPU) for embeddings
- scikit-learn for the supervised comparison
- Great Expectations for input data quality checks (profiling step)
- FastAPI + uvicorn for the model API
- Optional LLM step: API key read from environment variable, never committed
- Jupyter notebooks only for exploration and the final walkthrough
- Tests: pytest. Lint/format: ruff. Version control: git


## Methodological rules (non-negotiable)
- Pipeline order: profiling -> standardization -> blocking -> comparison -> scoring
  -> thresholding -> clustering -> evaluation.
- Report blocking recall (true pairs that survive blocking) and number of comparisons.
- Evaluate at pair level AND cluster level: precision, recall, F1; precision-recall
  curve across thresholds. All methods evaluated on the same pairs and splits.
- Deterministic baseline is mandatory and must be described exactly (e.g. exact match on
  normalized name, or on manufacturer + extracted model number).
- For supervised models, split by product cluster (not by pair) to avoid leakage.
- Embedding comparison is an ablation: same classifier with and without embedding
  features; report the difference with a bootstrap confidence interval.
- LLM step: only on borderline pairs, report cost (calls, tokens) and accuracy vs labels.
- Fixed random seeds; every result reproducible from one command.
- Never state a numeric result that was not produced by code in this repo.
  Every number in the README must come from a file in `reports/`.

## Workflow
- Small steps. Before large changes, propose a plan and wait for my approval.
- After each step: run tests and ruff, then summarize what changed in 3 lines max.
- Commit only when I ask, with clear messages.
