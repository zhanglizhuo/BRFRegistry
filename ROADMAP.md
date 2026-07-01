# BRF Initiative -- Roadmap

> The **Benchmark Reliability Framework (BRF)** establishes reproducible measurement
> standards for assessing the structural reliability of predictive benchmarks.
> From a single SR paper, BRF has grown into a research program: Framework, Package,
> Registry, Audit, and meta-analytic discovery.

---

## Current Status

- **BehaviorAudit** (SR, R2 submitted -- awaiting decision)
- **BRF Package v0.1.5**: `pip install benchmark-reliability` — includes `brf.registry` subpackage
- **BRF Benchmark Registry v1.5**: 25 entries (18 unique + 7 alt views); 20 Reliable, 5 Void, 0 Fragile
  - Dataset-as-Code architecture; CLI; SHA-256 verification
  - v1.5 frozen as Paper 3 data source; Registry independently evolves to v1.6+

---

## Papers

| # | Project | Contribution | Target | Status |
|---|---------|--------------|--------|--------|
| 1 | **BehaviorAudit** | BRF measurement framework (four-dimension audit protocol) | *Scientific Reports* | R2 submitted |
| 2 | **benchmark-reliability** | Software paper: BRF audit engine, Registry, CLI, verification | *JOSS* | Writing |
| 3 | **Benchmark Reliability Meta-analysis** | Discovery: *What dataset characteristics predict S, E, B, I?* Central finding: Fragile=0 across 25 group-aware benchmarks. S-vs-E 2D visualization, bootstrap CI, meta-regression, grouping sensitivity. Registry v1.5 as data source. | *Computers & Education* / *TMLR* | Registry v1.5 ready |
| 4 | **LLM Scoring Reliability** | Effects of LLM-as-scorer on benchmark reliability | *C&E* / *BJET* | Depends on Paper 3 |
| 5 | **Fairness + Explanation Stability** | From statistical reliability to trustworthiness | *TNNLS* / *C&E* | Conditional on demographic data |
| 6 | **Benchmark Design Guidelines** | Minimum reliability standards for future dataset construction | *Review of Educational Research* | Synthesizes Papers 3-5 |
| 7 | **LLM Scoring Mechanism** | Causal evidence linking scorer bias to BRF shift | High-impact ML journal | Evidence-driven |

### Paper Roles

- **Paper 1** (done): Measurement framework. "Here is a way to audit benchmarks."
- **Paper 2** (in progress): Software tool. "This package implements the framework with a CLI, Registry, and verification." Zero scientific claims — tool identity only.
- **Paper 3** (planned): Scientific discovery. "Using this tool on 25 benchmarks, we find Fragile=0. What dataset characteristics predict reliability?"

### Registry Positioning

The Registry is **not** a standalone paper. It is the data infrastructure that
Paper 3 is built on. The 625-line Data Descriptor manuscript written during
development becomes Paper 3's Methods + Data Availability chapter.

Registry has its own lifecycle (v1.5 → v1.6 → v2.0), independent of any paper.
Paper 3 freezes at v1.5 for reproducibility. If the Registry accumulates
sufficient external citations and usage, a standalone Data Descriptor
(Scientific Data) may be revisited later — with citation evidence that
currently doesn't exist.

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
| v1.5 | 25 | Diverse educational benchmarks + infrastructure | Paper 2 submission; Paper 3 data |
| v1.6+ | 25-30 | Enriched metadata, additional domains | Continuous updates |
| v2.0 | 30+ | Multi-domain (health, HR, etc.) | Future versions |

**Key principle**: Registry versions advance independently of the paper pipeline.
Paper 3 freezes at v1.5 for reproducibility; Registry continues to v1.6, v1.7, v2.0.

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
- **Registry is a product, not a paper.** Own lifecycle, own versions. Data source for Paper 3, DOI-versioned for reproducibility. May become a standalone Data Descriptor later if external citations justify it.
- **JOSS (Paper 2) is a tool identity card, not a scientific claim.** Proves the tool exists and works. Zero dependency on downstream papers.
- **Paper 3 is the research paper.** Uses Registry v1.5; asks scientific questions; Fragile=0 is the central finding.
- **Community Adoption is the endgame.** "Did you run BRF?"

---

## Research Principles

- Methods before claims.
- Resources before publications.
- Evidence before ambition.
- Adoption before recognition.

---

## What Changed (July 2026 update)

1. **Paper 2 redefined: Registry Data Descriptor → JOSS software paper.**
   The 625-line Registry manuscript (Dataset-as-Code architecture, metadata schema,
   9 tables) is merged into Paper 3's Methods + Data Availability chapter.
   Paper 2 is now `benchmark-reliability` → JOSS: tool identity, zero dependencies.
2. **JOSS moved from Paper 7 to Paper 2.** Tool ships first, establishes its
   academic identity before being used by Papers 3-4.
3. **Registry no longer a standalone paper.** v1.5 is Paper 3's data source.
   Registry lifecycles independently (v1.6, v2.0...). A standalone Data Descriptor
   may be revisited if future external citations justify it.
4. **Fragile absence is the central finding of Paper 3.** N=25, Fragile=0,
   bootstrap CI, rule-of-three upper bound ~12%, S-vs-E bimodal distribution.
5. **BRF unified branding.** All artifacts prefixed with BRF.
6. **Continuous measurement over discrete classification.** S and E are continuous;
   Reliable/Void/Fragile is communication shorthand only.
