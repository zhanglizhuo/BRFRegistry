# BRF Initiative -- Roadmap

> The **Benchmark Reliability Framework (BRF)** establishes reproducible measurement
> standards for assessing the structural reliability of predictive benchmarks.
> From a single SR paper, BRF has grown into a research program: Framework, Package,
> Registry, Audit, and meta-analytic discovery.

---

## Current Status

- **BehaviorAudit** (SR, R2 submitted -- awaiting decision)
- **BRF Package v0.2.1**: `pip install benchmark-reliability` — includes `brf.registry` subpackage (35 sources), diagnose/rank/recommend, CLI
- **BRF Benchmark Registry v2.0**: 42 entries (35 unique + 7 alt groupings); 27 Reliable, 8 Void, 0 Fragile
  - Dataset-as-Code architecture; CLI; SHA-256 35/35 (100%)
  - 35 self-contained source modules (0 external dependencies)
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
│   └── sources/               ← 35 DatasetSource modules
└── tests/                     ← 50 tests

BRFRegistry (development + results)
├── registry/sources/          ← source of truth for datasets
├── run_registry.py            ← from brf import BRFAnalyzer → runs all 35
├── results/registry_v2.0.json ← BRF results archive
└── version_policy.yaml

Paper3-MetaAnalysis
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
| 6 | **Fairness + Explanation Stability** | Subgroup BRF: benchmark reliability across demographic partitions. Fairness Gap metric. Which benchmarks are reliable overall but unfair across subgroups? | *TNNLS* / *C&E* | Designed; needs demographic metadata |
| 7 | **LLM Scoring Mechanism** | Causal evidence linking scorer bias to BRF shift. Why does LLM scoring reduce reliability? Mechanism analysis beyond Paper 4's observational findings. | High-impact ML journal | Evidence-driven; after Paper 4 |
| 8 | **Benchmark Design Guidelines** | Capstone synthesis: minimum reliability standards distilled from Papers 1-7 into actionable design guidelines for benchmark creators | *Review of Educational Research* | After Papers 3-7 |

### Paper Roles

- **Paper 1** (done): Measurement framework. "Here is a way to audit benchmarks."
- **Paper 2** (needs update): Data infrastructure. "35 versioned, reproducible group-aware benchmarks with executable pipeline."
- **Paper 3** (complete): Scientific discovery. "Fragile is a measurement convention. Bounded formulation reveals 3 Fragile entries. LOO-CV 100% agreement at E=0.5."
- **Paper 4** (designed): Scorer reliability. "When the scorer is the variable: LLM-generated targets systematically shift BRF metrics."
- **Paper 5** (waiting): Tool identity. "This software has been used in Papers 2-4."
- **Paper 6** (designed): Benchmark fairness. "Is the benchmark itself fair across demographic subgroups?"
- **Paper 7** (designed): LLM scoring mechanism. "Why does LLM scoring reduce reliability? Causal evidence."
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

Experimental code and results preserved at:
  Paper4-ScoringReliability/ (for reference, no manuscript planned)

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

## Paper 6 Design: Fairness + Explanation Stability

### Core Question

BRF 测的是"模型排名稳不稳定"。Paper 6 问更深一层：**benchmark 本身对不同人群公平吗？**

```
传统算法公平性：模型对不同人群公平吗？ (is the model fair?)
Paper 6：        benchmark 对不同人群公平吗？ (is the benchmark fair?)
```

一个 benchmark 整体可能 Reliable (S>0)，但在子群体上产生完全不同的模型排名——
用这个 benchmark 选出的"最优模型"可能只对优势群体最优。

### Study Design

**Study 1: Subgroup BRF**

对同一数据集按人口统计变量分区，分别跑 BRF：
- S_male vs S_female, S_group_A vs S_group_E
- 定义 **Fairness Gap** = max(S_subgroup) − min(S_subgroup)
- 定义 **Fairness Violation** = 1 if any subgroup S ≤ 0 while overall S > 0

**Study 2: Registry Datasets with Demographics**

| Dataset | Demographic Variable | Subgroups |
|---|---|---|
| kaggle_students_performance | Race/ethnicity | 5 (A-E) |
| students_exam_scores | Race/ethnicity | 5 |
| law_school | Race | LSAC classic fairness dataset |
| student_depression | City / Profession | 30 / 3 (socioeconomic proxy) |
| college_scorecard | Region / Ownership | 9 / 3 |

对每个数据集：BRF(X_sub, y_sub, groups_sub) per subgroup，测量 Fairness Gap。

**Study 3: Explanation Stability**

模型解释（feature importance / SHAP）在不同子群体上是否稳定？
- 如果 top-5 features 在子群体间完全不同 → benchmark 的解释也不公平
- 定义 Explanation Gap = 1 − |top-5∩top-5| / 5

**Study 4: Fairness-Aware BRF Extension**

提出 fairness-augmented BRF metrics:
- S_fair = S − λ · Fairness_Gap (penalize unreliable subgroups)
- E_fair = min(E_subgroup) (worst-case grouping evidence)

### Expected Findings

1. 部分 benchmark 整体 Reliable 但子群体 Fairness Gap 大
2. 小子群体（如 race=E）的 S 可能跌至 0 以下（small-N 效应叠加）
3. Explanation instability 与 subgroup S instability 相关
4. Fairness-aware BRF 可识别传统 BRF 漏掉的不公平 benchmark

### Prerequisites

- 需要人口统计元数据（不是所有数据集都有）
- 子群体样本量可能不足（需要功率分析）
- 伦理审查（涉及人口统计数据）

### Target Venue

- *TNNLS* (if methodology-focused: fairness-aware BRF metrics)
- *Computers & Education* (if application-focused: fair educational benchmarks)

---

## Paper 7 Design: LLM Scoring Mechanism

### Core Question

Paper 4 证明了 LLM 评分会降低 B（what），Paper 7 问**为什么**（why）。

具体：LLM 评分的哪些内在特性（噪声结构、偏差模式、语义压缩）导致了 BRF 指标的系统性偏移？

### Study Design

**Study 1: Bias Decomposition**

将 LLM 评分误差分解为可识别的成分：
- **随机噪声** (ε_random)：评分不可复现（同输入不同输出）
- **系统性偏差** (ε_bias)：与特征相关的评分偏移（如长度偏好）
- **语义压缩** (ε_compress)：LLM 将连续质量映射到离散分值区间

对每种成分，测量其对 ΔB、ΔI、ΔN 的独立贡献。

**Study 2: Causal Mediation**

用中介分析（mediation analysis）建立因果链：
```
LLM scorer → 评分偏差类型 → BRF 指标偏移
```
- 处理：scorer 类型（human vs GPT-4 vs Claude）
- 中介：评分偏差特征（variance, range, feature correlation）
- 结果：ΔS, ΔB, ΔI

**Study 3: Feature Space Distortion**

LLM 评分可能改变特征-目标关系的结构：
- 对比 human-y 和 LLM-y 下的 feature importance（SHAP）
- 测量 feature-target correlation 的变化
- 识别 LLM 评分引入的 spurious correlations

### Expected Findings

1. 系统性偏差（而非随机噪声）是 B 下降的主因
2. 语义压缩削弱 null separation（N↓），因为 LLM 倾向于将质量映射到狭窄的分值区间
3. Feature importance 在 human-y 和 LLM-y 间可能完全不同
4. 因果中介分析量化每种偏差机制的贡献比例

### Target Venue

High-impact ML journal (*NeurIPS* / *ICML* / *JMLR*) — 因果机制分析是方法论贡献

### Prerequisites

- Paper 4 的实验数据（重评分结果）
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
| Scorer mechanism | Paper 7 | understand why LLM scoring fails | causal evidence for guideline |
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
  Paper 7 (Mechanism)   → 为什么 LLM 评分降低可靠性（因果机制）

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
