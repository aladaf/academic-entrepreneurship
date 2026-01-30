# 3. Methodology

<!-- 
WRITING INSTRUCTIONS:
- Target: ~1,200 words
- Describe bibliometric approach with technical rigor
- Justify hybrid methodology (bibliometric + semantic NLP)
- Report exact parameters and reproducibility details
- Data source: /data/BIBLIOMETRIC_ANALYSIS_REPORT.md, /data/LDA_ANALYSIS_REPORT.md
-->

## 3.1 Research Design

Mixed-methods bibliometric and semantic analysis combining:
- Traditional bibliometric techniques
- Transformer-based topic modeling (BERTopic)
- Probabilistic topic modeling (LDA) for triangulation

## 3.2 Data Collection

### 3.2.1 Database and Search Strategy
- **Source**: Web of Science Core Collection
- **Query**: "academic entrepreneurship" (topic search)
- **Records retrieved**: 1,300
- **After deduplication and filtering (excluding 2026)**: **1,294**
- **Time span**: 1988-2025

### 3.2.2 Dataset Characteristics
| Metric | Value |
|--------|-------|
| Unique records | 1,294 |
| Unique authors | 2,711 |
| Unique sources | 497 |
| Total citations | 44,190 |
| Average citations/doc | 34.15 |

## 3.3 Analytical Framework

### 3.3.1 Bibliometric Analyses
1. **Descriptive statistics**: Annual production, top sources, top authors
2. **Network analysis**: 
   - Keyword co-occurrence (50 nodes, 1,032 edges, density=0.8424)
   - Bibliographic coupling with Salton's Cosine normalization
   - Disparity Filter backbone extraction (α=0.05)
3. **RPYS**: Reference Publication Year Spectroscopy (90,252 references)
4. **Main Path Analysis**: Citation trajectory identification

### 3.3.2 Semantic Topic Modeling (BERTopic)
- **Model**: BERTopic with `all-MiniLM-L6-v2` embeddings
- **Dimensionality reduction**: UMAP (n_neighbors=15, n_components=5, min_dist=0.0)
- **Clustering**: HDBSCAN (min_cluster_size=8, min_samples=3)
- **Abstracts analyzed**: 1,238
- **Topics identified**: 2 (indicating high semantic cohesion)

### 3.3.3 LDA Confirmatory Analysis
- **Preprocessing**: spaCy lemmatization, domain-specific stopword removal
- **Vectorization**: CountVectorizer (max_df=0.95, min_df=5)
- **Parameters**: k=5 and k=10 topics, random_state=42, max_iter=30
- **Coherence metric**: Cv (gensim)
- **Concentration metric**: Herfindahl-Hirschman Index (HHI)

## 3.4 Methodological Triangulation

The dual-method approach (BERTopic + LDA) serves as methodological triangulation:
- BERTopic: Semantic sensitivity via transformer embeddings
- LDA: Frequency-based probabilistic benchmark

**Rationale**: If LDA fails to isolate a theme that BERTopic detects, this validates the "weak signal" hypothesis.

## 3.5 Limitations

[TO BE WRITTEN]

---
*Data-driven: All metrics must match /data/ sources exactly*
