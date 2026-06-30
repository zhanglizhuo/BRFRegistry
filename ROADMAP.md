# Reliable Benchmark Initiative -- Roadmap

> Establish reproducible measurement standards for assessing the structural reliability
> of predictive benchmarks before model development, enabling more trustworthy empirical
> machine learning research.

---

## Current Status

- **BehaviorAudit** (SR, R2 submitted -- awaiting decision)
- **BRF Package v0.1.5**: Released on PyPI (`pip install benchmark-reliability`) and GitHub
- **BRF Benchmark Registry v1.5**: 10 datasets audited (7 Reliable, 3 Void, 0 Fragile; added ASSISTments, TAE, Turkiye)

---

## Papers (Updated)

| # | Project | Contribution | Target | Depends On |
|---|---------|--------------|--------|------------|
| 1 | **BehaviorAudit** | Protocol paper: four-dimension audit protocol for educational benchmarks | *Scientific Reports* | -- |
| 2 | **BRF Benchmark Registry v1** | Data Descriptor: curated collection of group-aware educational benchmarks with standardized metadata, adapters, and BRF audit results | *Scientific Data* | BRF Package |
| 3 | **Large-scale Benchmark Reliability Study** | Research paper: reliability patterns across 12-15+ educational benchmarks | *Computers & Education* / *TMLR* | Registry v1 |
| 4 | **LLM Scoring Reliability** (flagship) | Effects of LLM-as-scorer on benchmark reliability | *C&E* / *BJET* | Registry v1 + Paper 3 |
| 5 | **Fairness + Explanation Stability** | From statistical reliability to trustworthiness | *TNNLS* / *C&E* | Paper 3 + suitable demographic data (conditional) |
| 6 | **Benchmark Design Guidelines** | Minimum reliability standards for future dataset construction | *Review of Educational Research* | Papers 3-5 |
| 7 | **JOSS Package Paper** | Software paper with demonstrated usage in Papers 3-4 | *JOSS* | Stable API + Papers 3-4 usage |
| 8 | **LLM Scoring Mechanism** | Causal evidence linking scorer bias to BRF shift | High-impact ML journal (if evidence supports) | Paper 4 + Registry |

### Paper Roles

- **Paper 1** (done): Protocol. "Here is a way to audit benchmarks."
- **Paper 2** (in progress): Resource. "Here is a curated registry of group-aware datasets, ready to use."
- **Paper 3** (planned): Discovery. "Here is what we found when we audited them at scale."

---

## Registry Strategy

Registry is a **continuously maintained community resource**, not a one-time paper deliverable.

### Version Plan

| Version | Datasets | Goal | Target |
|---------|----------|------|--------|
| v1.0 | 10-12 | Cover major educational scenarios, validate pipeline | Paper 2 submission |
| v1.5 | 15-18 | Add international assessments, MOOC, teacher eval | Paper 3 data collection |
| v2.0 | 25-30 | Suffice for meta-regression and large-scale pattern analysis | Registry update |

### Inclusion Criteria

A dataset must satisfy **all** of the following to enter the Registry:

- [x] Predictive task (classification or regression)
- [x] Publicly available (open access or with permissive license)
- [x] Group metadata present (teacher, school, course, institution, cohort, etc.)
- [x] >= 100 samples
- [x] Enough groups for group-aware holdout (preferably >= 5)
- [x] Clear, well-defined target variable

Non-qualifying examples: Student Academics (UCI 467) -- no grouping column.

### Data Sources (Priority)

| Tier | Dataset | Priority | Grouping | Status |
|------|---------|----------|----------|--------|
| 1 | OULAD | ***** | Course (22) | v1.0 |
| 1 | xAPI-Edu-Data | ***** | Student (12) | v1.0 |
| 1 | MM-TBA | ***** | None (0) | v1.0 |
| 1 | Teaching Assistant Eval | ***** | Instructor (25) | v1.5 |
| 1 | Turkiye Student Eval | ***** | Course (13) | v1.5 |
| 2 | Student Dropout | **** | Course (17) | v1.0 |
| 2 | UCI Student Performance | **** | School (2) | v1.0 |
| 2 | Entrance Exam | **** | Qualification (3) | v1.0 |
| 2 | Higher Ed | **** | Course (9) | v1.0 |
| 2 | ASSISTments | ***** | Teacher (124) | v1.5 |
| 2 | EdNet | ***** | Student / Content | Candidate |
| 3 | Math Score / Teaching Style | *** | Teacher (3) | Candidate |
| 3 | PISA, TIMSS, PIRLS | *** | Country / School | Future |
| 3 | NAEP | *** | State / School | Future |
| 3 | MOOC (HarvardX, Coursera, edX) | *** | Course | Future |

---

## Timeline

| Step | Item | Start | Depends On | Independently Publishable? |
|------|------|-------|-------------|----------------------------|
| 1 | BehaviorAudit (SR) | Done | -- | Yes |
| 2 | BRF Package | Done (v0.1.5) | Paper 1 | Infrastructure |
| 3 | Registry v1 construction | Month 1-3 | BRF Package | Yes (Data Descriptor) |
| 4 | Large-scale Study | Month 3-9 | Registry v1 | Yes |
| 4b | *(parallel)* LLM data collection | Month 1 onward | -- | Prep only |
| 5 | LLM Reliability (writing) | Month 9-14 | Registry v1 + Paper 3 | Yes |
| 6 | Fairness / Explainability | Month 9+ (conditional) | Suitable data confirmed | Yes |
| 7 | JOSS Submission | Month 12-16 | Stable API + Papers 3-4 | Yes |
| 8 | Design Guidelines | Month 16-20 | Papers 3-5 | Yes |
| 9 | Mechanism | Evidence-driven | Paper 4 + Registry | Yes |

---

## Key Positioning

- **BRF is a measurement framework, not a theory.** No "phase transition" or "BRF theory" claims.
- **Registry is an asset, not a paper.** Designed as a continuously versioned community resource (v1.0 -> v1.5 -> v2.0) with its own DOI. The most cited output long-term.
- **Paper 2 is a Data Descriptor, not a research paper.** It documents the Registry: data sources, cleaning, group definition principles, metadata schema, BRF JSON format, quality control, API.
- **Paper 3 is a meta-analysis, not a classification study.** Research question: *What dataset characteristics predict benchmark reliability?* Uses meta-regression with S, E, B, I as continuous responses and dataset descriptors (N, p, G, group balance, target entropy, task type, feature types, missing ratio) as predictors. Does NOT force a three-regime taxonomy — let data determine if clusters exist.
- **LLM data preparation starts now; LLM paper writing waits.** Preserves narrative continuity: BehaviorAudit -> BRF -> Registry -> Large-scale -> LLM.
- **Fairness is conditional, not scheduled.** Proceeds only when suitable demographic datasets are confirmed.
- **Design Guidelines synthesize, not experiment.** Evidence base is cumulative findings from Papers 3-5.
- **Mechanism paper is evidence-driven, not timeline-driven.**
- **Every paper can be submitted independently.** The dependency chain is directional but not blocking.
- **Community Adoption is the hidden endgame.** Success metric: "Did you run BRF?" becomes a standard reviewer question.

---

## Research Principles

- Methods before claims.
- Resources before publications.
- Evidence before ambition.
- Adoption before recognition.

---

## What Changed From the Previous Version

1. **Paper 2 redefined.** Was "Large-scale Study (30+ datasets)" and "Registry Data Descriptor (2.5)". Now Paper 2 = Registry Data Descriptor for *Scientific Data* (~12-15 datasets). Paper 3 = Large-scale meta-analysis with scientific claims.
2. **Registry strategy de-emphasized dataset count.** 12-15 high-quality datasets with diverse grouping structures > 30 rushed datasets. Focus on coverage, not numbers.
3. **Inclusion criteria formalized.** A checklist for dataset admission, enabling community contributions in the future.
4. **Registry version plan rescheduled.** v1 (10-12 datasets) = Paper 2 submission target. v1.5 (15-18) = Paper 3 data. v2.0 (25-30) = post-publication update.
5. **Paper 3 reframed as meta-regression.** Instead of three-regime classification, ask: *What dataset characteristics predict S, E, B, I?* Uses S, E as continuous responses, regressed on N, p, G, group balance, target entropy, feature types, missingness. Absence of Fragile (0/9 at v1.5) is a dataset characteristic finding, not a theory refutation.
6. **Continuous measurement framework > discrete 3-classification.** BRF class (Reliable/Fragile/Void) is communication shorthand, not a scientific claim. The real signal is in continuous S and E values and their relationship to dataset descriptors. Paper 3 avoids "proving" or "disproving" the three-regime taxonomy.
7. **Registry metadata expansion.** Beyond basic counts (N, p, G), Registry v1.5+ collects: avg group size, largest group proportion, target type, target entropy, missing ratio, feature types, task type, institution level, license type — enabling Paper 3 meta-regression without manual re-annotation.
8. **MM-TBA retains distinct role.** Void (E<0) but represents an emerging class (LLM-scored benchmarks). Paper 3 cites it as "investigated separately" in Paper 4. Avoids diluting the meta-regression with a structurally different benchmark class.
9. **Turkiye provides strong positive evidence.** S=0.56 with N=5820, 13 groups shows group-aware validation doesn't always collapse performance — counters potential reviewer criticism.
