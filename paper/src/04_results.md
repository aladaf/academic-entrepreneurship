# 4. Results

<!-- 
WRITING INSTRUCTIONS:
- Target: ~2,000 words
- Present ALL results from data reports with exact figures
- Use tables and visualizations references
- Structure by analysis type, not by hypothesis
- Data source: /data/BIBLIOMETRIC_ANALYSIS_REPORT.md, /data/LDA_ANALYSIS_REPORT.md
-->

## 4.1 Descriptive Analysis

### 4.1.1 Temporal Distribution
[Use annual production data from report]

### 4.1.2 Geographic Distribution
| Rank | Country | Publications |
|------|---------|-------------|
| 1 | UK | 212 |
| 2 | Italy | 186 |
| 3 | Spain | 130 |
| 4 | Germany | 102 |
| 5 | China | 83 |

### 4.1.3 Most Influential Authors
| Author | Total Citations | Papers | Avg Citations |
|--------|----------------|--------|---------------|
| Wright, M | 4,865 | 26 | 187.1 |
| Fini, R | 2,582 | 13 | 198.6 |
| Grimaldi, R | 2,535 | 8 | 316.9 |

## 4.2 Network Analysis Results

### 4.2.1 Keyword Co-occurrence
- Nodes: 50
- Edges: 1,032
- Density: 0.8424 (extremely high)
- Modularity: 0.0408 (low - highly integrated field)

### 4.2.2 Bibliographic Coupling (Post-Backbone)
- Nodes: 372 authors
- Edges: 1,093
- Modularity: 0.8303 (high community structure)
- Communities: 30

## 4.3 Historical Roots (RPYS)

### Peak Citation Years
| Year | Citations | Deviation | Interpretation |
|------|-----------|-----------|----------------|
| 2011 | 4,422 | +840 | Hayter's behavioral turn |
| 2007 | 4,121 | +829 | Wright/Clarysse institutional frameworks |
| 1998 | 1,481 | +385 | Technology transfer consolidation |

### Foundational Works
- Schumpeter (1912): Economic development theory
- Bush (1945): Science policy foundations
- Granovetter (1973): Network theory
- Ajzen (1991): Behavioral theory

## 4.4 Main Path Analysis

[Insert Main Path trajectory from report with 13 key papers]

## 4.5 Semantic Topic Modeling (BERTopic)

### 4.5.1 Topic Distribution
| Topic | Documents | % | Status |
|-------|-----------|---|--------|
| Topic 1 (Core) | 1,213 | 98% | EMERGING |
| Topic 0 (Digital) | 25 | 2% | FRONTIER |

### 4.5.2 Frontier Topic Characterization
- Keywords: digital, entrepreneurship, technologies, academic, learning, dt
- Bibliometric overlap: 10%
- Representative documents: [cite Secundo et al., 2020]

## 4.6 LDA Confirmatory Analysis

### 4.6.1 Topic Distributions
**k=5 Model**:
| Topic | Top Keywords |
|-------|--------------|
| 0 | academic, entrepreneurship, entrepreneurial, university |
| 1 | feasibility, cost, targeted, vehicle, commercialized |
| 2 | networks, network, uic, phd, internationalization |
| 3 | spin, university, offs, usos, firms |
| 4 | logics, lean, startup, story, analytic |

**k=10 Model**: [Similar structure]

### 4.6.2 Digital Signal Dispersion

| Model | Topics with Digital Signal | HHI | Interpretation |
|-------|---------------------------|-----|----------------|
| k=5 | 3 topics (45% each) | 0.645 | Dispersed |
| k=10 | 4 topics (45-48% each) | 0.536 | Highly dispersed |

**Finding**: LDA failed to isolate Digital theme - signal dispersed across multiple generic clusters.

## 4.7 Methodological Triangulation Outcome

| Method | Digital Isolation | Conclusion |
|--------|-------------------|------------|
| BERTopic | ✅ Isolated (2%) | Semantic sensitivity detects weak signal |
| LDA k=5 | ❌ Dispersed | Frequency-based method fails |
| LDA k=10 | ❌ Dispersed | Frequency-based method fails |

**Thesis Validation**: The "Digital Academic Entrepreneurship" theme constitutes a **weak signal** - detectable only through semantic embeddings, invisible to traditional frequency-based methods.

---
*Data-driven: All metrics must match /data/ sources exactly*
