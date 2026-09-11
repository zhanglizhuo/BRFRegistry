# BRF Initiative -- Roadmap

> The **Benchmark Reliability Framework (BRF)** establishes reproducible measurement
> standards for assessing the structural reliability of predictive benchmarks.
> From a single SR paper, BRF has grown into a research program: Framework, Package,
> Registry, Audit, and meta-analytic discovery.

---

## Current Status

- **BehaviorAudit** (SR, R2 submitted -- awaiting decision)
- **BRF Package v0.3.0**: `pip install benchmark-reliability` — includes `brf.registry` subpackage (51 datasets), diagnose/rank/recommend, CLI
- **BRF Benchmark Registry v2.1**: 58 entries (51 unique + 7 alt groupings); 35 Reliable, 16 Void, 0 Fragile
  - Dataset-as-Code architecture; CLI; SHA-256 35/51 (69%)
  - 39 self-contained source modules (0 external dependencies)
  - Multi-domain: education, engineering, energy, transportation, food science, etc.
  - Data pipeline automated: sync_scatter_data.py joins registry JSON + alt results + paper metadata
  - Paper 2 & Paper 3 reference v2.0 (35 datasets); Registry continues independently
- **Paper 3** (Meta-analysis): 30-page manuscript complete; 35 datasets, 12 tables, 6 figures, 31 refs

---

## Repository Architecture

```
BenchmarkReliability (PyPI: benchmark-reliability)
├── src/brf/analyzer.py        ← BRF core algorithm (S/E/B/I/N/M)
├── src/brf/registry/          ← bundled dataset registry (copy for pip users)
│   └── sources/               ← 39 DatasetSource modules
└── tests/                     ← 50 tests

BRFRegistry (development + results)
├── registry/sources/          ← source of truth for datasets
├── run_registry.py            ← from brf import BRFAnalyzer → runs all 51
├── results/registry_v2.1.json ← BRF results archive
└── version_policy.yaml

MetaAnalysis
├── scripts/sync_scatter_data.py  ← auto-generates scatter_data.csv
├── data/scatter_data.csv         ← single source for all figures/tables
├── data/dataset_meta.csv         ← paper-specific metadata (domain, level, country)
├── data/alt_results.csv          ← 7 alternative grouping BRF results
├── figures/ (6 PDFs), tables/ (12 .tex)
└── manuscript/paper3.tex         ← 30 pages, 0 compile errors
```

Dependency: BRFRegistry → BenchmarkReliability (imports BRFAnalyzer).
Paper3 reads registry JSON via sync script; no hard dependency on either repo at runtime.

---

## Papers

| # | Project | Contribution | Target | Status |
|---|---------|--------------|--------|--------|
| 1 | **BehaviorAudit** | BRF measurement framework (four-dimension audit protocol) | *Scientific Reports* | R2 submitted |
| 2 | **BRF Benchmark Registry** | Data Descriptor: 35 unique datasets + 7 alt groupings; Dataset-as-Code; SHA-256 100%; version policy | *Scientific Data* | Manuscript needs update (18→35 datasets) |
| 3 | **Benchmark Reliability Meta-analysis** | Discovery: Fragile is a measurement convention, not a data property. 35 datasets, bounded formulation, Bayesian MR, LOO-CV 100%, MM-TBA case study | *Computers & Education* / *TMLR* | Manuscript complete (30 pp) |
| 4 | **LLM Scoring Reliability** | Controlled re-scoring experiment: same data, human vs LLM target. Measures ΔBRF (scorer reliability footprint). Bias taxonomy, multi-scorer comparison, mitigation strategies. | *C&E* / *NeurIPS D&B* | Designed; depends on Paper 3 |
| 5 | **benchmark-reliability (JOSS)** | Software paper: BRF audit engine, Registry, CLI | *JOSS* | Waiting: 6+ months public history (~Dec 2026) |
| 6 | **Subgroup BRF** | Benchmark reliability across demographic subgroups. Reliability Gap metric. 10 splits, 5 US benchmarks. | *TNNLS* / *C&E* | Full precision complete; Major Revision from peer review simulation |
| 7 | **DomainAudit: Cross-Domain Subgroup BRF** | Cross-domain replication of Paper 6: does structural > identity RG hold across medical imaging, NLP, robotics, and non-US education? Requires Registry v3.0 (embedding support). | High-impact ML/EDM journal | Designing; after Paper 6 |
| 8 | **Benchmark Design Guidelines** | Capstone synthesis: minimum reliability standards distilled from Papers 1-7 into actionable design guidelines for benchmark creators | *Review of Educational Research* | After Papers 3-7 |

### Paper Roles

- **Paper 1** (done): Measurement framework. "Here is a way to audit benchmarks."
- **Paper 2** (needs update): Data infrastructure. "35 versioned, reproducible group-aware benchmarks with executable pipeline."
- **Paper 3** (complete): Scientific discovery. "Fragile is a measurement convention. Bounded formulation reveals 3 Fragile entries. LOO-CV 100% agreement at E=0.5."
- **Paper 4** (designed): Scorer reliability. "When the scorer is the variable: LLM-generated targets systematically shift BRF metrics."
- **Paper 5** (waiting): Tool identity. "This software has been used in Papers 2-4."
- **Paper 6** (designed → manuscript complete → major revision): Benchmark fairness. "Is the benchmark itself fair across demographic subgroups?" Full precision complete; review identified N confounding reframe needed.
- **Paper 7** (designed): Cross-domain replication. "Does Paper 6's structural > identity RG pattern hold across medical, NLP, robotics?"
- **Paper 8** (capstone): Design guidelines. "How to build a reliable benchmark: standards distilled from 7 papers."

### Paper 3 Key Findings

1. **Fragile regime is convention-dependent**: 0/35 Fragile under S=N-I; 3/35 under S'=N-I/(1+I). The Fragile zone's occupancy depends on the choice of transform, not the data.
2. **Bounded formulation**: S'=N-I/(1+I) collapses Void count from 8 to 1; three datasets enter Fragile (MM-TBA, UCI Student Math, Student Absences).
3. **E=0.5 threshold robust**: LOO-CV 100% agreement (34/34); optimal E=0.65±0.06; τ gap peaks at E≈0.67 (gap=0.43).
4. **Bayesian meta-regression**: log₁₀N positively predicts S (β=+0.32, CrI [-0.01,+0.65]); negatively predicts I (β=-0.36, CrI [-0.68,-0.03]).
5. **MM-TBA case study**: Pre-publication screening demonstration; Void under S, Fragile under S'.
6. **Failure modes**: Mode 1 (feature irrelevance), Mode 2 (small-N instability), Mode 3 (negative baseline gain).

---

## Paper 4 Design: LLM Scoring Reliability

### Status: ABANDONED — Design flaw identified in prototyping (2026-07)

Core problem: swapping y (human → LLM) and observing BRF change is tautological.
Different y → different BRF tells us nothing about LLM scoring quality.
The experiment collapsed under its own logic.

Key lesson for future papers: BRF is a property of (X, y, groups, scorer),
not of y alone. Controlled experiments must hold scoring constant,
varying only the factor of interest.

### Core Question (Original, Now Retracted)

传统 benchmark 的 y 是人工真值。当 y 改为 LLM 生成时，评分者变成 benchmark 误差结构的一部分。
Paper 3 的 MM-TBA 是唯一 E<0 的数据集——Paper 4 问：这是孤例还是系统性问题？
——实际上这个问题无法通过"换 y 后看 BRF 是否变化"来回答，因为 BRF 对 y 的变化天然敏感。

### Study Design

**Study 1: Controlled Re-scoring (core contribution)**

从 Registry 选 5-8 个有人工评分的数据集，用 GPT-4 重评分，配对比较 BRF：

| Dataset | Human Target | LLM Re-scoring | N |
|---|---|---|---|
| TAE | TA performance (1-3) | GPT-4 rates classroom description | 151 |
| Turkiye | Course difficulty (1-5) | GPT-4 rates from Q1-Q28 | 5,820 |
| OLI | Answer correctness | GPT-4 evaluates solution process | ~5K subsample |
| Student Dropout | Graduate/Dropout | GPT-4 predicts from student profile | ~2K subsample |
| MathE | Question difficulty | GPT-4 estimates from question content | 833 |

对每个数据集：BRF(X, y_human, groups) vs BRF(X, y_LLM, groups)，测量 ΔS, ΔE, ΔB, ΔI。

**Study 2: Bias Taxonomy**

注入已知偏差，测量每种偏差如何映射到 BRF 指标：

| Bias | Operation | Expected BRF Impact |
|---|---|---|
| Length preference | y' = y + α·length | B↓ (features become irrelevant) |
| Leniency | compress y to high range | N↓ (null separation weakens) |
| Position effect | order-dependent shift | I↑ (instability) |
| Anchoring | y clusters at specific values | E↓ (grouping evidence weakens) |

**Study 3: Multi-Scorer Comparison**

同一数据用 GPT-4 / Claude / Llama / Gemini 评分：
- 哪个 scorer 构建的 benchmark 最可靠？
- 评分集成（多模型平均）能否提升 BRF？

**Study 4: Mitigation**

- Scorer ensemble: average multiple LLM scores → reduce random noise
- Human-LLM disagreement filtering: remove high-disagreement samples → improve B
- Score calibration: post-hoc alignment of LLM distribution to human distribution

### Expected Findings

1. LLM re-scoring systematically reduces B (baseline gain) — LLM noise uncorrelated with features
2. Leniency bias is most dangerous — directly weakens null separation (N↓)
3. Scorer ensemble improves I (stability) but not necessarily B (if bias is shared)
4. MM-TBA's E<0 is not an outlier — LLM-scored benchmarks普遍面临 B 偏低的风险

### Contribution

- **Acceptance criteria** for LLM-scored benchmarks (BRF pre-publication screening with scorer audit)
- **Scorer reliability audit protocol**: standardized quality check for LLM-generated targets
- **Design guidelines**: when is LLM scoring safe? When is it risky?

### Cost & Feasibility

- API budget: ~$200-500 (GPT-4/Claude scoring 10K-30K samples)
- Requires datasets with textual features (abalone/wine_quality excluded)
- MM-TBA anchors the paper as known case study from Paper 3
- Timeline: 2-3 months after Paper 3 acceptance

### Paper 4 vs Paper 7

| | Paper 4 | Paper 7 |
|---|---|---|
| Question | Does LLM scoring affect reliability? | Why does it affect? |
| Method | Controlled experiment + observational | Causal inference + mechanism |
| Depth | What happens | Why it happens |

---

## Paper 6 Design: Subgroup BRF

### Core Question

BRF 测的是"模型排名稳不稳定"。Paper 6 问更深一层：**benchmark 本身对不同人群公平吗？**

```
传统算法公平性：模型对不同人群公平吗？ (is the model fair?)
Paper 6：        benchmark 对不同人群公平吗？ (is the benchmark fair?)
```

一个 benchmark 整体可能 Reliable (S>0)，但在子群体上产生完全不同的模型排名——
用这个 benchmark 选出的"最优模型"可能只对优势群体最优。

### Status: Full Precision Complete, Major Revision Needed

- Full precision (n_splits=30, n_perm=200) done for all 10 splits
- Peer review simulation (2026-07-08): DA CRITICAL on N confounding (ρ=0.90, r²=0.81)
- Ownership inconsistency resolved: 19/20 seeds (was 16/20 quick mode), passes Bonferroni
- Bug fixes: bootstrap CI X-y pairing, fairness_gap now uses S'

### Remaining Before Submission

1. Reframe contribution: N dominance is primary finding, dissociation is tentative
2. Bootstrap CI figure needs re-running with bounded S'
3. Paper 6 is not submission-ready in current form

### Target Venue

- *TNNLS* (if methodology-focused: subgroup BRF metrics)
- *Computers & Education* (if application-focused: fair educational benchmarks)

---

## Paper 7 Design: DomainAudit — Cross-Domain Subgroup BRF

### Core Question

Paper 6 发现"structural splits > identity splits"（observational, 5 US benchmarks）。Paper 7 问：**这个模式跨领域成立吗？**

### Research Questions

| RQ | Method | What it tests |
|---|---|---|
| RQ1: Do structural splits (task, region) consistently produce larger RG than identity splits (gender, race)? | Subgroup BRF per benchmark | Generalizability of Paper 6's core finding |
| RQ2: Is the N−S' confound universal (ρ ≈ 0.90) or domain-dependent? | Spearman ρ per domain | Whether sample size correction is universally needed |
| RQ3: Does feature divergence predict RG across all domains? | SHAP-based feature correlation vs. RG | Mechanism generality |

### Target Datasets

| Domain | Benchmarks | Feature strategy | Splits |
|---|---|---|---|
| Medical imaging | CheXpert, MIMIC, HAM10000, ODIR | Foundation model embeddings | Sex, age, race, insurance |
| NLP | WinoBias, BBQ, GLUE subsets, Toxicity | Sentence embeddings (BERT/LLM) | Gender, race, dialect |
| Robotics | Meta-World, D4RL, Robomimic | Environment state (tabular) | Task type, difficulty |
| Non-US education | PISA, TIMSS | Raw features (tabular) | Country, SES, language |

### Methodology

- Extend BRFRegistry to **v3.0**: add `extract_features()` to DatasetSource protocol, add demographic split metadata
- Build cross-domain benchmark modules (each implements the extended DatasetSource interface)
- Run Subgroup BRF per benchmark → RG, S' distributions
- Feature divergence analysis for splits with RG > 0.10
- Cross-domain meta-analysis: does RG distribution differ by domain or split type?

### Expected Findings

- Structural > identity RG holds across domains → universal pattern → strong claim for high-impact venue
- N−S' correlation weaker in medical (more homogeneous features) or stronger in NLP → domain-specific correction
- Feature divergence predicts RG only when subgroups differ in **which features predict y**, not just in residual variance

### Prerequisites

- Paper 6 submitted (observational finding to replicate)
- Registry v3.0 protocol designed and implemented (embedding + splits)
- Cross-domain benchmark modules built (~12 new DatasetSource modules)
- 因果推断方法（mediation analysis, counterfactual reasoning）
- Timeline: Paper 4 发表后 3-4 个月

---

## Paper 8 Design: Benchmark Design Guidelines

### Core Question

如果你要建一个新的 benchmark，怎样确保它是可靠的？

**综述论文（capstone）**——把 Papers 1-7 的发现蒸馏成可操作的实践标准。没有新实验，是知识的系统化。

### Structure

每条指南对应前序论文的具体发现：

| Guideline | Source | Rule | Rationale |
|---|---|---|---|
| Minimum sample size | Paper 3 Mode 2 | N ≥ 500 | higher_ed (N=145) and TAE (N=151) 都是 Void |
| Feature-target relevance | Paper 3 Mode 1 | B > 0 required | mm_tba B=-0.034 → signal absent |
| Grouping metadata | Paper 2 Registry | ≥ 5 meaningful groups | enables cross-group evaluation |
| Group balance | Paper 3 | N/G ≥ 100 | sparse groups (ASSISTments G=124) reduce E |
| Scorer validation | Paper 4 | scorer audit for LLM-scored y | LLM scoring systematically lowers B |
| Cross-domain replication | Paper 7 | structural > identity RG is universal? | cross-domain validation for guideline |
| Fairness check | Paper 6 | Fairness Gap < threshold | benchmark must be fair across subgroups |
| Pre-publication screening | Paper 3 MM-TBA | run BRF before publication | 30-second automated check |
| Acceptance thresholds | Paper 3 calibration | E > 0.5 and S > 0 for "Reliable" | LOO-CV 100% agreement at E=0.5 |

### Contribution

- **不是新发现，而是标准化**：把散落在 7 篇论文里的经验变成一套 checklist
- 教育领域目前没有 benchmark 设计的可靠性指南——这是空白
- 类比：心理学有 pre-registration 标准，医学有 CONSORT，benchmark 领域缺类似规范

### Target Venue

*Review of Educational Research* (影响因子 ~8-11，教育领域顶级综述期刊)

### Prerequisites

Papers 3-7 基本完成。Paper 8 是整个系列的**收尾**。

### Paper Series Summary

```
原创研究
  Paper 1 (Framework)   → 这里有一个审计方法
  Paper 2 (Registry)    → 这里有一批标准化的数据
  Paper 3 (Discovery)   → 我们发现了什么（Fragile 是测量约定）
  Paper 4 (LLM Scoring) → LLM 评分会破坏可靠性吗？
  Paper 6 (Fairness)    → benchmark 对子群体公平吗？
  Paper 7 (DomainAudit) → 跨领域复制验证：structural > identity 是否普遍成立？

综合
  Paper 5 (JOSS)        → 这个工具已经被用了
  Paper 8 (Guidelines)  → 怎样建一个可靠的 benchmark（收尾）
```

---

## Unified BRF Branding

All artifacts share the **BRF** prefix:

```
BRF Framework    -- the measurement theory (Paper 1)
BRF Package      -- Python library on PyPI (benchmark-reliability)
BRF Registry     -- versioned dataset collection (Paper 2)
BRF Audit        -- run BRF on a dataset
BRF Score        -- individual dataset BRF results
BRF Report       -- multi-dataset comparative report
BRF CLI          -- command-line interface
```

---

## Registry Strategy

Registry is a **continuously maintained community resource** with its own lifecycle,
independent of any single paper.

| Version | Datasets | Goal | Paper |
|---------|----------|------|-------|
| v1.0 | 7 | Initial SR validation set | BehaviorAudit reference |
| v1.5 | 25 | Initial large-scale collection | Historical |
| v1.6 | 27 | + Kaggle + UCI Math; 0 external deps | Historical (Papers 2 & 3 originally targeted v1.6, updated to v2.0) |
| v1.7 | 27-31 | Enriched metadata, additional domains | Continuous updates |
| v2.0 | 35 | Multi-domain (engineering, energy, transportation) | Paper 2 & Paper 3 (current) |

**Key principle**: Registry versions advance independently of the paper pipeline.
Papers 2 and 3 freeze at v1.6 for reproducibility; Registry continues to v2.0+.

### Inclusion Criteria

- [x] Predictive task (classification or regression)
- [x] Publicly available (open access or permissive license)
- [x] Group metadata present (teacher, school, course, institution, country, etc.)
- [x] >= 100 samples
- [x] Enough groups for group-aware holdout (preferably >= 5)
- [x] Clear, well-defined target variable

---

## Key Positioning

- **BRF is a measurement framework, not a theory.**
- **Registry is Paper 2 — a Data Descriptor.** 35 unique datasets with executable pipeline, SHA-256 verification, version policy.
- **Paper 3 is the research paper.** Central finding: Fragile is a measurement convention.
- **JOSS (Paper 5) is deferred** until 6+ months public history (~Dec 2026).
- **Community Adoption is the endgame.** "Did you run BRF?"

---

## Research Principles

- Methods before claims.
- Resources before publications.
- Evidence before ambition.
- Adoption before recognition.

---

## Changelog

### September 2026 (v2.1 session)

1. **Registry v2.1**: expanded 35→51 unique datasets (added 16 cross-domain benchmarks: health, finance, environment, energy, transportation, systems)
2. **35 Reliable / 16 Void / 0 Fragile** (bimodal; no intermediate regime)
3. **39 self-contained source modules** (0 external dependencies); 58 total entries incl. 7 alt-grouping views
4. **SHA-256 35/51 (69%)**: all file-backed datasets verified; cross-domain additions are scikit-learn-bundled / synthetic / API-sourced
5. **cpu_act → OpenML**; removed house_16h (insufficient samples)
6. **Package v0.3.0 released**: version chain unified, bundled registry synced to v2.1

### July 2026 (v2.0 session)

1. **Registry v2.0**: expanded 20→35 datasets, added multi-domain (engineering, energy, etc.)
2. **SHA-256 35/35 (100%)**: fixed 14 placeholder/invalid hashes; was 21/35
3. **Download cache bugs fixed**: higher_ed, entrance_exam, xapi_edu, mm_tba
4. **n_features/n_samples aligned**: 9 datasets had metadata mismatch with prepare() output
5. **AI traces removed**: net −761 lines across 38 files (unused imports, verbose docstrings)
6. **Data pipeline automated**: sync_scatter_data.py joins registry + alt results + paper metadata
7. **Paper 3 updated**: higher_ed UCI data update (S: −1.03→−5.25); LOO-CV 94%→100%; Bayesian MR coefficients updated
8. **BenchmarkReliability synced**: 35 source modules aligned; student_alcohol→student_absences
9. **Paper 2 manuscript**: needs updating from 18→35 datasets (pending)

### Earlier

1. **Paper 2 returned to Registry Data Descriptor.** JOSS deferred to Paper 5.
2. **v0.2.1 released.** diagnose(), rank(), recommend().
3. **BRF unified branding.** All artifacts prefixed with BRF.
