# BRF Initiative -- Roadmap

> The **Benchmark Reliability Framework (BRF)** establishes reproducible measurement
> standards for assessing the structural reliability of predictive benchmarks.
> From a single SR paper, BRF has grown into a research program: Framework, Package,
> Registry, Audit, and meta-analytic discovery.

---

## Current Status

- **BehaviorAudit** (SR, R2 submitted -- awaiting decision)
- **BRF Package v0.1.5**: `pip install benchmark-reliability` (PyPI + GitHub)
- **BRF Benchmark Registry v1.5**: 25 datasets (20 Reliable, 5 Void, 0 Fragile)
  - Dataset-as-Code architecture: one `.py` per dataset, auto-discovered
  - CLI: `list`, `download`, `verify`, `sync`, `info`
  - Manifest-based versioning; SHA-256 verification
  - Ready for Paper 2 submission as-is

---

## Papers

| # | Project | Contribution | Target | Status |
|---|---------|--------------|--------|--------|
| 1 | **BehaviorAudit** | BRF measurement framework (four-dimension audit protocol) | *Scientific Reports* | R2 submitted |
| 2 | **BRF Benchmark Registry** | Data Descriptor: versioned, reproducible collection of group-aware benchmarks; software infrastructure (Dataset-as-Code, CLI, manifest, verification) | *Scientific Data* / *Data in Brief* | Data complete |
| 3 | **Benchmark Reliability Meta-analysis** | Discovery: *What dataset characteristics predict S, E, B, I?* Meta-regression; Fragile-absence analysis; S-vs-E 2D visualization; bootstrap CI | *Computers & Education* / *TMLR* | Registry v1.5 ready |
| 4 | **LLM Scoring Reliability** | Flagship: effects of LLM-as-scorer on benchmark reliability | *C&E* / *BJET* | Depends on Paper 3 |
| 5 | **Fairness + Explanation Stability** | From statistical reliability to trustworthiness | *TNNLS* / *C&E* | Conditional on demographic data |
| 6 | **Benchmark Design Guidelines** | Minimum reliability standards for future dataset construction | *Review of Educational Research* | Synthesizes Papers 3-5 |
| 7 | **JOSS Package Paper (benchmark-reliability)** | Software paper: BRF algorithms, CLI, visualization — already demonstrated across Papers 2-4 | *JOSS* | Stable API + Papers 3-4 usage |
| 8 | **LLM Scoring Mechanism** | Causal evidence linking scorer bias to BRF shift | High-impact ML journal | Evidence-driven |

### Paper Roles

- **Paper 1** (done): Protocol. "Here is a way to audit benchmarks."
- **Paper 2** (data-ready): Resource. "Here is a versioned, reproducible registry of group-aware datasets, ready to audit." Describes *what* the Registry is and *how* it works — zero BRF analysis.
- **Paper 3** (data-ready): Discovery. "Using BRF Registry v1.5 (25 datasets), we find..."

### Two Assets, Two Papers

| Asset | Paper | Journal | Content |
|-------|-------|---------|---------|
| BRF Registry (25 datasets) | Paper 2 | *Scientific Data* | Data Descriptor: architecture, metadata, versioning, provenance, CLI |
| benchmark-reliability (PyPI) | Paper 7 | *JOSS* | Software: BRFAnalyzer, audit(), report(), visualization, CLI |

**Key insight**: The Registry integrates into the benchmark-reliability package
(`pip install benchmark-reliability` includes `brf.registry`), but the two are
published separately. Paper 2 describes the Registry as infrastructure;
Paper 7 (JOSS) describes the package as software — after Papers 3-4 have
demonstrated multi-paper usage.

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
- **Registry is a product, not a paper appendix.** Own DOI, own lifecycle.
- **Paper 2 is a Data Descriptor, not a research paper.** Documents Registry design,
  software architecture, dataset curation, metadata schema, availability. Zero BRF analysis.
- **Paper 3 is the research paper.** Uses Registry v1.5; asks scientific questions.
- **JOSS is Paper 7, not Paper 2.** After the package is battle-tested by Papers 3-4.
- **Community Adoption is the endgame.** "Did you run BRF?"

---

## Research Principles

- Methods before claims.
- Resources before publications.
- Evidence before ambition.
- Adoption before recognition.

---

## What Changed (since last version)

1. **Paper 2 redefined as Data Descriptor.** For *Scientific Data*. Focus: software
   infrastructure (Dataset-as-Code, CLI, manifest, SHA verification), NOT BRF analysis.
2. **Paper 3 centered on Fragile absence.** N=25, Fragile=0 is the central finding.
   Bootstrap CI, S-vs-E visualization, meta-regression.
3. **BRF unified branding.** All artifacts prefixed with BRF. No BBR, EduBRF, etc.
4. **JOSS moved to Paper 7.** After multi-paper usage demonstrates maturity.
5. **Registry lifecycle decoupled from papers.** v1.5 is frozen for Paper 3;
   Registry independently evolves to v1.6, v1.7, v2.0.
6. **Stop pursuing dataset count.** 25 quality datasets > 30 rushed. Quality over quantity.
7. **Enriched metadata schema.** education_level, country, year added for meta-regression.
8. **Continuous measurement over discrete classification.** S and E are continuous;
   Reliable/Void/Fragile is communication shorthand only.
