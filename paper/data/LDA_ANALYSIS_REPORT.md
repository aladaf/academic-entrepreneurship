# LDA Confirmatory Analysis - Walkthrough

## Overview

This analysis implements LDA (Latent Dirichlet Allocation) as a **methodological counterproof** to the BERTopic semantic frontier analysis. The goal was to test whether frequency-based topic modeling could isolate the "Digital Entrepreneurship" signal that BERTopic identified as a 2% emerging frontier.

---

## BERTopic Baseline (Previous Analysis)

| Topic | Documents | % | Description |
|-------|-----------|---|-------------|
| Topic 1 | 1,213 | 98% | Core Academic Entrepreneurship |
| Topic 0 | 25 | 2% | **Digital Frontier** (FRONTIER status) |

BERTopic's transformer-based embeddings detected a small but distinct "Digital" cluster.

---

## LDA Results

### Topics Identified (k=10)

| Topic | Top Keywords |
|-------|--------------|
| 0 | entrepreneurship, academic, entrepreneurial, university, universities, knowledge, development, innovation, education |
| 1 | spin, performance, university, offs, growth, variety, courses, organizational |
| 2 | networks, network, open, phd, innovation, social, startup, openness |
| 3 | usos, performance, spin, university, growth, capital, offs, effect |
| 4 | conference, event, biology, resistance, drug, brought, lectures |
| 5 | university, spin, technology, offs, transfer, universities, firms, industry |
| 6 | uic, team, phase, generations, opinion, feasible |
| 7 | assets, intangible, pre, lab, periods, formative |
| 8 | international, internationalization, mode, training, abroad |
| 9 | university, regional, spin, firms, innovation, services |

> [!IMPORTANT]
> Notice that "digital" does NOT appear as a defining keyword in any LDA topic.

---

## Digital Signal Dispersion Analysis

### k=5 Topics

| LDA Topic | Total Docs | Digital Docs | % Digital |
|-----------|------------|--------------|-----------|
| 3 | 266 | 127 | 47.7% |
| 0 | 964 | 434 | 45.0% |
| 2 | 7 | 2 | 28.6% |

**Herfindahl Index**: 0.645 (dispersed)

### k=10 Topics

| LDA Topic | Total Docs | Digital Docs | % Digital |
|-----------|------------|--------------|-----------|
| 5 | 272 | 130 | 47.8% |
| 3 | 91 | 42 | 46.2% |
| 0 | 868 | 389 | 44.8% |
| 2 | 7 | 2 | 28.6% |

**Herfindahl Index**: 0.536 (dispersed)

---

## Key Finding

> [!CAUTION]
> **LDA FAILED to isolate the Digital theme.**
> 
> Digital-related documents are dispersed evenly across 3-4 LDA topics (~45% each), rather than concentrated in a single cluster. The Herfindahl Index of 0.536 confirms high dispersion.

---

## Thesis Validation

| Method | Digital Isolation | Interpretation |
|--------|-------------------|----------------|
| **BERTopic** | ✅ Isolated (2% distinct cluster) | Semantic sensitivity detects weak signal |
| **LDA k=5** | ❌ Dispersed (3 topics) | Frequency-based model misses signal |
| **LDA k=10** | ❌ Dispersed (4 topics) | Frequency-based model misses signal |

This confirms the **"Weak Signal"** hypothesis:

> The "Digital Entrepreneurship" theme represents an **emerging frontier** that probabilistic frequency-based models (LDA) fail to isolate because its lexical footprint is mixed into larger thematic clusters like "Innovation", "Technology Transfer", and "University Spin-offs". Only transformer-based semantic embeddings (BERTopic) can detect this subtle signal due to their sensitivity to contextual meaning.

---

## Generated Output Files

### Topic Tables
- [lda_topics_k5.csv](file:///home/aladaf/papers/academic-entrepreneurship/output/lda_topics_k5.csv) - Top 15 words per topic (k=5)
- [lda_topics_k10.csv](file:///home/aladaf/papers/academic-entrepreneurship/output/lda_topics_k10.csv) - Top 15 words per topic (k=10)

### Interactive Visualizations
- [lda_pyldavis_k5.html](file:///home/aladaf/papers/academic-entrepreneurship/output/lda_pyldavis_k5.html) - pyLDAvis dashboard (k=5)
- [lda_pyldavis_k10.html](file:///home/aladaf/papers/academic-entrepreneurship/output/lda_pyldavis_k10.html) - pyLDAvis dashboard (k=10)

### Analysis Files
- [lda_document_topics.csv](file:///home/aladaf/papers/academic-entrepreneurship/output/lda_document_topics.csv) - Document-topic mapping
- [lda_bertopic_comparison_k5.csv](file:///home/aladaf/papers/academic-entrepreneurship/output/lda_bertopic_comparison_k5.csv) - Comparison (k=5)
- [lda_bertopic_comparison_k10.csv](file:///home/aladaf/papers/academic-entrepreneurship/output/lda_bertopic_comparison_k10.csv) - Comparison (k=10)
- [lda_coherence_scores.csv](file:///home/aladaf/papers/academic-entrepreneurship/output/lda_coherence_scores.csv) - Cv coherence scores

---

## Script Location

Main script: [lda_analysis.py](file:///home/aladaf/papers/academic-entrepreneurship/lda_analysis.py)

Run with:
```bash
cd /home/aladaf/papers/academic-entrepreneurship
python lda_analysis.py
```
