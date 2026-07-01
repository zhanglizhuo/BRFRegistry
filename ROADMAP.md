# BRF Initiative -- Roadmap

> The **Benchmark Reliability Framework (BRF)** establishes reproducible measurement
> standards for assessing the structural reliability of predictive benchmarks.
> From a single SR paper, BRF has grown into a research program: Framework, Package,
> Registry, Audit, and meta-analytic discovery.

---

## Current Status

- **BehaviorAudit** (SR, R2 submitted -- awaiting decision)
- **BRF Package v0.2.1**: `pip install benchmark-reliability` — includes `brf.registry` subpackage, diagnose/rank/recommend, CLI
- **BRF Benchmark Registry v1.6**: 27 entries (20 unique + 7 alt views); 21 Reliable, 6 Void, 0 Fragile
  - Dataset-as-Code architecture; CLI; SHA-256 (9/11 downloadable, 82%)
  - All 20 source modules self-contained (0 external dependencies)
  - GitHub release v1.6; Zenodo DOI: 10.5281/zenodo.21098157
  - 14 tables, 1 figure, 20 YAML Dataset Cards, taxonomy, version policy
  - Paper 2 & Paper 3 both reference v1.6; Registry independently evolves to v1.7+

---

## Papers

| # | Project | Contribution | Target | Status |
|---|---------|--------------|--------|--------|
| 1 | **BehaviorAudit** | BRF measurement framework (four-dimension audit protocol) | *Scientific Reports* | R2 submitted |
| 2 | **BRF Benchmark Registry** | Data Descriptor / Collection: 18 unique datasets + 7 grouping views; Dataset-as-Code pipeline; metadata cards, taxonomy, version policy; zero BRF analysis | *Scientific Data* | Manuscript v4 ready (14 tables, 1 figure, 18 YAML cards) |
| 3 | **Benchmark Reliability Meta-analysis** | Discovery: *What dataset characteristics predict S, E, B, I?* Central finding: Fragile=0 across 25 group-aware benchmarks. S-vs-E 2D visualization, bootstrap CI, meta-regression, grouping sensitivity. Registry v1.6 as data source. | *Computers & Education* / *TMLR* | Registry v1.6 ready |
| 4 | **LLM Scoring Reliability** | Effects of LLM-as-scorer on benchmark reliability | *C&E* / *BJET* | Depends on Paper 3 |
| 5 | **benchmark-reliability (JOSS)** | Software paper: BRF audit engine, diagnose/rank/recommend, Registry, CLI — after multi-paper usage demonstrated | *JOSS* | Waiting: repo needs 6+ months public history (~Dec 2026) |
| 6 | **Fairness + Explanation Stability** | From statistical reliability to trustworthiness | *TNNLS* / *C&E* | Conditional on demographic data |
| 7 | **Benchmark Design Guidelines** | Minimum reliability standards for future dataset construction | *Review of Educational Research* | Synthesizes Papers 3-6 |
| 8 | **LLM Scoring Mechanism** | Causal evidence linking scorer bias to BRF shift | High-impact ML journal | Evidence-driven |

### Paper Roles

- **Paper 1** (done): Measurement framework. "Here is a way to audit benchmarks."
- **Paper 2** (drafted): Data infrastructure. "Here is a versioned, reproducible registry of group-aware benchmarks — not just data, but Dataset-as-Code with metadata, verification, and CLI."
- **Paper 3** (planned): Scientific discovery. "Using this infrastructure on 25 benchmarks, we find Fragile=0. Grouping sensitivity is the dominant factor."
- **Paper 5** (waiting): Tool identity. "This software has been used in Papers 2-4."

### Registry Positioning

The Registry **is** Paper 2 — a standalone Data Descriptor. The 625-line manuscript
documents its architecture (Dataset-as-Code), metadata schema (16 fields),
software infrastructure (CLI, SHA-256), dataset curation (18 unique datasets,
15 domains), and technical validation.

JOSS (Paper 5) is deferred until the repo has 6+ months public history and papers
2-4 provide citation evidence — transforming JOSS from a "promise of future use"
into "documentation of demonstrated use."

Registry has its own lifecycle (v1.6 → v1.7 → v2.0), independent of any paper.
Papers 2 and 3 both freeze at v1.6 for reproducibility.

---

## Unified BRF Branding

All artifacts share the **BRF** prefix:

```
BRF Framework    -- the measurement theory (Paper 1)
BRF Package      -- Python library on PyPI
BRF Registry     -- versioned dataset collection (Paper 2)
BRF Audit        -- run BRF on a dataset
BRF Score        -- individual dataset BRF results
BRF Report       -- multi-dataset comparative report
BRF CLI          -- command-line interface
```

This avoids inventing new names. The brand is **BRF**.

---

## Registry Strategy

Registry is a **continuously maintained community resource** with its own lifecycle,
independent of any single paper.

| Version | Datasets | Goal | Paper |
|---------|----------|------|-------|
| v1.0 | 7 | Initial SR validation set | BehaviorAudit reference |
| v1.5 | 25 | Initial large-scale collection | Historical |
| v1.6 | 27 | + Kaggle + UCI Math; 0 external deps | Paper 2 & Paper 3 |
| v1.7+ | 27-35 | Enriched metadata, additional domains | Continuous updates |
| v2.0 | 35+ | Multi-domain (health, HR, etc.) | Future versions |

**Key principle**: Registry versions advance independently of the paper pipeline.
Papers 2 and 3 both freeze at v1.6 for reproducibility; Registry continues to v1.7, v2.0.

### Inclusion Criteria

- [x] Predictive task (classification or regression)
- [x] Publicly available (open access or permissive license)
- [x] Group metadata present (teacher, school, course, institution, country, etc.)
- [x] >= 100 samples
- [x] Enough groups for group-aware holdout (preferably >= 5)
- [x] Clear, well-defined target variable

### Metadata Schema (enriched for Paper 3 meta-regression)

Each dataset records:

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Canonical key | `tae` |
| `education_level` | K12 / Higher Ed / MOOC / Assessment / Mixed | `Higher Education` |
| `country` | Geographic origin | `US` |
| `year` | Data collection year | `1997` |
| `task` | regression / classification | `classification` |
| `target` | Target variable description | `TA performance (3-class)` |
| `grouping` | Grouping variable description | `Instructor` |
| `license` | License type | `CC BY 4.0` |
| `reference` | Citation | `Loh (1997); UCI ID 100` |

---

## Paper 3 Key Scientific Questions

1. **Fragile absence**: Across 25 datasets, 0 Fragile. Bootstrap 95% CI.
   Hypotheses: (A) educational benchmarks are bimodal, (B) Fragile exists but rare,
   (C) S and E are structurally correlated — E rarely falls below 0.5 when S > 0,
   (D) current domain scope limits observation.

2. **S vs E 2D visualization**: Plot all 25 datasets in (S, E) space.
   Are they bimodal clusters or a continuous distribution?

3. **Meta-regression**: Predict S, E, B, I from metadata:
   N, p, G, group balance, target entropy, task type, education level, country, year.

4. **Grouping sensitivity**: Same data, different grouping → how do S, E shift?

---

## Key Positioning

- **BRF is a measurement framework, not a theory.**
- **Registry is Paper 2 — a Data Descriptor (collection), not a research paper.** Contribution: 18 unique group-aware datasets with executable pipeline, versioned metadata cards, taxonomy, and policy. Documents *what* and *how* — zero BRF analysis.
- **Paper 3 is the research paper.** Uses Registry v1.6; Fragile=0 is the central finding.
- **JOSS (Paper 5) is the tool identity, not the core contribution.** After multi-paper usage, it documents demonstrated impact — not promised future use. Blocked by JOSS 6-month public-history requirement (~Dec 2026).
- **Community Adoption is the endgame.** "Did you run BRF?"

---

## Research Principles

- Methods before claims.
- Resources before publications.
- Evidence before ambition.
- Adoption before recognition.

---

## What Changed (July 2026, final)

1. **Paper 2 returned to Registry Data Descriptor.** JOSS cannot be submitted now
   (repo needs 6+ months public history, ~Dec 2026). The 625-line Registry
   manuscript is ready now. Paper 2 = Registry (Scientific Data), not JOSS.
2. **JOSS moved to Paper 5.** After Papers 2-4 have cited the tool, JOSS documents
   demonstrated impact rather than promised future use — strengthening the case.
3. **v0.2.1 released.** diagnose(), rank(), recommend() provide context-aware
   per-dimension diagnostics instead of opaque 3-class labels.
4. **Fragile=0 confirmed at N=25.** Bootstrap CI, rule-of-three upper bound ~12%.
   Core finding for Paper 3.
5. **BRF unified branding.** All artifacts prefixed with BRF.
