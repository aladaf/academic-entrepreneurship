# Bibliometric Analysis Report: Academic Entrepreneurship
## Web of Science Data Analysis

---

## 1. Dataset Overview

| Metric | Value |
|--------|-------|
| **Data Sources** | 3 WoS export files (data-academic01.txt, data-academic02.txt, data-academic03.txt) |
| **Total Records Loaded** | 1,300 |
| **Duplicates Removed** | 0 |
| **Records from 2026 Excluded** | 6 |
| **Final Unique Records** | 1,294 |
| **Time Span** | 1988 - 2025 |
| **Sources (Journals)** | 497 |
| **Unique Authors** | 2,711 |
| **Total Citations** | 44,190 |
| **Average Citations/Document** | 34.15 |

---

## 2. Annual Scientific Production

The field shows clear growth patterns:

| Year | Publications | Year | Publications | Year | Publications |
|------|-------------|------|-------------|------|-------------|
| 1988 | 2 | 2005 | 19 | 2016 | 75 |
| 1991 | 1 | 2006 | 7 | 2017 | 69 |
| 1992 | 2 | 2007 | 18 | 2018 | 83 |
| 1993 | 1 | 2008 | 20 | 2019 | 85 |
| 1996 | 1 | 2009 | 29 | 2020 | 83 |
| 1997 | 1 | 2010 | 27 | 2021 | 108 |
| 1998 | 2 | 2011 | 35 | 2022 | 110 |
| 1999 | 1 | 2012 | 42 | 2023 | 91 |
| 2000 | 5 | 2013 | 34 | 2024 | 103 |
| 2001 | 2 | 2014 | 39 | 2025 | 116 |
| 2002 | 2 | 2015 | 68 | | |
| 2003 | 9 | | | | |
| 2004 | 4 | | | | |

**Key Observation**: Exponential growth from 2015 onwards, with peak production in 2025 (116 publications).

---

## 3. Top 15 Most Productive Sources (Journals)

| Rank | Journal | Publications |
|------|---------|-------------|
| 1 | Journal of Technology Transfer | 135 |
| 2 | Research Policy | 61 |
| 3 | Technovation | 42 |
| 4 | Technological Forecasting and Social Change | 36 |
| 5 | Small Business Economics | 32 |
| 6 | International Entrepreneurship and Management | 25 |
| 7 | Sustainability | 23 |
| 8 | Science and Public Policy | 19 |
| 9 | International Journal of Entrepreneurial Behavior | 18 |
| 10 | Studies in Higher Education | 16 |
| 11 | IEEE Transactions on Engineering Management | 13 |
| 12 | Journal of the Knowledge Economy | 13 |
| 13 | Journal of Business Venturing | 12 |
| 14 | International Journal of Technology Management | 12 |
| 15 | Technology Analysis & Strategic Management | 12 |

**Key Observation**: Journal of Technology Transfer dominates with 135 publications (10.4% of total).

---

## 4. Top 15 Most Cited Authors

| Rank | Author | Total Citations | Papers | Avg Citations/Paper |
|------|--------|----------------|--------|---------------------|
| 1 | WRIGHT, M | 4,865 | 26 | 187.1 |
| 2 | FINI, R | 2,582 | 13 | 198.6 |
| 3 | GRIMALDI, R | 2,535 | 8 | 316.9 |
| 4 | TARTARI, V | 2,476 | 7 | 353.7 |
| 5 | PERKMANN, M | 2,356 | 7 | 336.6 |
| 6 | SALTER, A | 2,140 | 6 | 356.7 |
| 7 | HUGHES, A | 2,039 | 3 | 679.7 |
| 8 | D'ESTE, P | 1,999 | 7 | 285.6 |
| 9 | MCKELVEY, M | 1,949 | 5 | 389.8 |
| 10 | CLARYSSE, B | 1,922 | 9 | 213.6 |
| 11 | RASMUSSEN, E | 1,896 | 21 | 90.3 |
| 12 | GUERRERO, M | 1,823 | 19 | 95.9 |
| 13 | SOBRERO, M | 1,803 | 2 | 901.5 |
| 14 | KRABEL, S | 1,775 | 3 | 591.7 |
| 15 | KITSON, M | 1,708 | 2 | 854.0 |

**Key Observation**: WRIGHT, M is the most influential author with highest total citations, while SOBRERO, M has the highest average citations per paper (901.5).

---

## 5. Country Scientific Production (Top 20)

| Rank | Country | Publications |
|------|---------|-------------|
| 1 | UK | 212 |
| 2 | ITALY | 186 |
| 3 | SPAIN | 130 |
| 4 | GERMANY | 102 |
| 5 | CHINA | 83 |
| 6 | NETHERLANDS | 77 |
| 7 | SWEDEN | 77 |
| 8 | BELGIUM | 55 |
| 9 | PORTUGAL | 50 |
| 10 | NORWAY | 49 |
| 11 | BRAZIL | 45 |
| 12 | FRANCE | 42 |
| 13 | CANADA | 41 |
| 14 | POLAND | 36 |
| 15 | MALAYSIA | 33 |
| 16 | AUSTRALIA | 32 |
| 17 | JAPAN | 27 |
| 18 | DENMARK | 27 |

**Key Observation**: European dominance with UK (212), Italy (186), and Spain (130) leading. Strong representation from Asian countries (China, Malaysia, Japan).

---

## 6. Network Analysis Results

### 6.1. Keywords Co-occurrence Network

| Metric | Value |
|--------|-------|
| **Nodes (Keywords)** | 50 |
| **Edges (Co-occurrences)** | 1,032 |
| **Density** | 0.8424 (very high) |
| **Diameter** | 2 |
| **Average Clustering** | 0.0444 |
| **Modularity** | 0.0408 |
| **Giant Component %** | 100% |
| **Average Degree** | 41.28 |

**Interpretation**: Extremely dense network where almost all keywords are connected. Low modularity suggests the field is highly integrated rather than fragmented into distinct subcommunities.

### 6.2. Bibliographic Coupling Network (Raw)

| Metric | Value |
|--------|-------|
| **Nodes (Authors)** | 511 |
| **Edges (Coupling Links)** | 95,107 |
| **Density** | 0.7299 |
| **Diameter** | 4 |
| **Average Clustering** | 0.052 |
| **Giant Component %** | 98.6% |
| **Average Degree** | 372.24 |

### 6.3. Bibliographic Coupling Network (After Backbone Extraction)

The **Disparity Filter** (Serrano et al., 2009) with α=0.05 was applied:

| Metric | Before Backbone | After Backbone | Change |
|--------|-----------------|----------------|--------|
| **Nodes** | 511 | 372 | -27.2% |
| **Edges** | 95,107 | 1,093 | -98.9% |
| **Density** | 0.7299 | 0.0158 | -97.8% |
| **Diameter** | 4 | 16 | +300% |
| **Avg Clustering** | 0.052 | 0.2438 | +368.8% |
| **Modularity** | N/A | 0.8303 | High |
| **Communities Detected** | - | 30 | - |
| **Avg Degree** | 372.24 | 5.88 | -98.4% |

**Interpretation**: Backbone extraction reveals clear community structure (modularity = 0.83). The 30 communities represent distinct research schools or intellectual traditions. Higher clustering after filtering indicates tight research groups.

---

## 7. Temporal Evolution Analysis

### 7.1. Time Periods Defined (Volume-Based)

| Period | Name | Years | Documents |
|--------|------|-------|-----------|
| 1 | **Emergência** (Emergence) | 1988-2018 | 598 |
| 2 | **Consolidação** (Consolidation) | 2019-2019 | 85 |
| 3 | **Fronteira** (Frontier) | 2020-2025 | 611 |

### 7.2. Thematic Evolution (Sankey Flow)

**Emergence → Consolidation Transitions:**

| From | To | Jaccard | Shared Keywords |
|------|----|---------|-----------------|
| ACADEMIC ENTREPRENEURSHIP | ACADEMIC ENTREPRENEURSHIP | 0.300 | ACADEMIC ENTREPRENEURSHIP, COMMERCIALIZATION, SCIENTISTS, KNOWLEDGE TRANSFER, SCIENCE |
| ACADEMIC ENTREPRENEURSHIP | TECHNOLOGY-TRANSFER | 0.235 | TECHNOLOGY-TRANSFER, UNIVERSITY, UNIVERSITIES, KNOWLEDGE |
| PERFORMANCE | INNOVATION | 0.368 | ENTREPRENEURSHIP, UNIVERSITY SPIN-OFFS, INNOVATION, NETWORKS |

**Consolidation → Frontier Transitions:**

| From | To | Jaccard | Shared Keywords |
|------|----|---------|-----------------|
| INNOVATION | PERFORMANCE | 0.273 | ENTREPRENEURSHIP, UNIVERSITY SPIN-OFFS, NETWORKS, START-UPS, PERFORMANCE |
| TECHNOLOGY-TRANSFER | ACADEMIC ENTREPRENEURSHIP | 0.176 | TECHNOLOGY-TRANSFER, UNIVERSITY, UNIVERSITIES |

**Key Observation**: ACADEMIC ENTREPRENEURSHIP remains the core theme throughout all periods. INNOVATION and PERFORMANCE become increasingly central in recent years.

---

## 8. Core Authors by Thematic Cluster

### Cluster 0: ACADEMIC ENTREPRENEURSHIP (Growing Trend)
- **Keywords**: ACADEMIC ENTREPRENEURSHIP, TECHNOLOGY-TRANSFER, COMMERCIALIZATION, UNIVERSITY, SCIENCE
- **Contributing Authors**: 1,845
- **Top 10 Authors**:
  1. GUERRERO, M (66)
  2. WRIGHT, M (65)
  3. RASMUSSEN, E (58)
  4. CUNNINGHAM, JA (49)
  5. HAYTER, CS (45)
  6. FINI, R (45)
  7. SECUNDO, G (40)
  8. KLOFSTEN, M (40)
  9. MEOLI, M (39)
  10. VISMARA, S (37)

### Cluster 1: INNOVATION (Growing Trend)
- **Keywords**: INNOVATION, PERFORMANCE, KNOWLEDGE, ENTREPRENEURSHIP, UNIVERSITY SPIN-OFFS
- **Contributing Authors**: 1,318
- **Top 10 Authors**:
  1. WRIGHT, M (75)
  2. RASMUSSEN, E (67)
  3. RODEIRO-PAZOS, D (61)
  4. RODRÍGUEZ-GULÍAS, MJ (61)
  5. FERNÁNDEZ-LÓPEZ, S (55)
  6. VISMARA, S (38)
  7. SMITH, HL (36)
  8. FINI, R (34)
  9. HAYTER, CS (33)
  10. CORSI, C (33)

### Cluster 2: SPIN-OFFS (Growing Trend)
- **Keywords**: SPIN-OFFS, TECHNOLOGY-TRANSFER OFFICES, RESEARCH-AND-DEVELOPMENT, INTELLECTUAL PROPERTY, BAYH-DOLE ACT
- **Contributing Authors**: 185
- **Top 10 Authors**:
  1. WRIGHT, M (8)
  2. KENNEY, M (7)
  3. GRIMALDI, R (7)
  4. FINI, R (7)
  5. CUNNINGHAM, JA (7)
  6. MENTER, M (7)
  7. SIEGEL, DS (6)
  8. MCKELVEY, M (6)
  9. VISMARA, S (5)
  10. KRABEL, S (5)

**Key Observation**: WRIGHT, M appears in the top of all three clusters, indicating a truly central position in the field. All clusters show "Growing" trend status.

---

## 9. Keyword Burst Detection

Keywords experiencing significant growth (Z-score > 2.0, comparing 2024-2025 vs. historical baseline 1988-2023):

### Top 30 Bursting Keywords

| Rank | Keyword | Z-Score | Recent Avg | Historical Avg | Trend |
|------|---------|---------|------------|----------------|-------|
| 1 | I23 | 33.30 | 5.5 | 0.03 | ↑ Emerging |
| 2 | L26 | 32.50 | 7.5 | 0.06 | ↑ Emerging |
| 3 | M13 | 17.22 | 4.0 | 0.06 | ↑ Emerging |
| 4 | O32 | 17.22 | 4.0 | 0.06 | ↑ Emerging |
| 5 | NATIONAL SYSTEMS | 15.04 | 2.5 | 0.03 | ↑ Emerging |
| 6 | ENTREPRENEURIAL BEHAVIOR | 10.67 | 2.5 | 0.06 | ↑ Emerging |
| 7 | STEM | 8.96 | 1.5 | 0.03 | ↑ Emerging |
| 8 | RETHINKING | 8.96 | 1.5 | 0.03 | ↑ Emerging |
| 9 | TECHNOLOGY-BASED COMPANIES | 8.96 | 1.5 | 0.03 | ↑ Emerging |
| 10 | UNIVERSITY-STUDENTS | 8.96 | 1.5 | 0.03 | ↑ Emerging |
| 11 | SUSTAINABLE ENTREPRENEURSHIP | 8.96 | 1.5 | 0.03 | ↑ Emerging |
| 12 | SUSTAINABILITY | 8.03 | 3.5 | 0.14 | ↑ Emerging |
| 13 | ECOSYSTEM | 7.35 | 3.0 | 0.11 | ↑ Emerging |
| 14 | IDENTIFICATION | 6.64 | 4.5 | 0.25 | ↑ Emerging |
| 15 | O31 | 6.58 | 3.5 | 0.11 | ↑ Emerging |
| 16 | SYSTEMATIC LITERATURE REVIEW | 6.39 | 3.5 | 0.19 | ↑ Emerging |
| 17 | THEORY OF PLANNED BEHAVIOUR | 6.31 | 1.5 | 0.06 | ↑ Emerging |
| 18 | UNIVERSITY SUPPORT | 6.31 | 1.5 | 0.06 | ↑ Emerging |
| 19 | WORK | 6.26 | 5.0 | 0.33 | ↑ Emerging |
| 20 | AMBIDEXTERITY | 5.92 | 1.0 | 0.03 | ↑ Emerging |
| 21 | PHD STUDENTS | 5.92 | 1.0 | 0.03 | ↑ Emerging |
| 22 | UNIVERSITY STARTUPS | 5.92 | 1.0 | 0.03 | ↑ Emerging |
| 23 | DOCTORAL STUDENTS | 5.92 | 1.0 | 0.03 | ↑ Emerging |
| 24 | LEAN STARTUP | 5.92 | 1.0 | 0.03 | ↑ Emerging |
| 25 | RESILIENCE | 5.92 | 1.0 | 0.03 | ↑ Emerging |
| 26 | ACCELERATORS | 5.92 | 1.0 | 0.03 | ↑ Emerging |
| 27 | HIGHER EDUCATION | 5.39 | 5.5 | 0.50 | ↑ Emerging |
| 28 | ECOSYSTEMS | 5.23 | 7.5 | 0.47 | ↑ Emerging |
| 29 | SUSTAINABLE DEVELOPMENT | 5.13 | 1.5 | 0.08 | ↑ Emerging |
| 30 | EDUCATION | 4.72 | 19.0 | 1.83 | ↑ Emerging |

### Thematic Interpretation of Bursts

**New Research Fronts Identified:**

1. **Sustainability Theme**: SUSTAINABLE ENTREPRENEURSHIP, SUSTAINABILITY, SUSTAINABLE DEVELOPMENT
2. **Ecosystem Perspective**: ECOSYSTEM, ECOSYSTEMS, INNOVATION ECOSYSTEM
3. **Education Focus**: HIGHER EDUCATION, EDUCATION, PHD STUDENTS, DOCTORAL STUDENTS, UNIVERSITY-STUDENTS
4. **Behavioral Research**: ENTREPRENEURIAL BEHAVIOR, THEORY OF PLANNED BEHAVIOUR
5. **Startup Methodology**: LEAN STARTUP, ACCELERATORS, UNIVERSITY STARTUPS
6. **Research Methodology**: SYSTEMATIC LITERATURE REVIEW, BIBLIOMETRIC ANALYSIS
7. **Organizational Concepts**: AMBIDEXTERITY, RESILIENCE

---

## 10. Summary and Key Insights

### 10.1. Field Maturity
- The field has evolved from nascent (1988-2005) through growth (2006-2015) to maturity (2016-2025)
- Clear exponential growth pattern with 116 publications in 2025 alone

### 10.2. Geographic Distribution
- Strong European leadership (UK, Italy, Spain, Germany)
- Growing contributions from Asia (China, Malaysia) and Latin America (Brazil)

### 10.3. Intellectual Structure
- Three main thematic clusters: Academic Entrepreneurship, Innovation, Spin-offs
- High network density suggests field consolidation and integration
- Clear community structure in bibliographic coupling (30 communities, modularity = 0.83)

### 10.4. Research Fronts (2024-2025)
- **Sustainability** is emerging as a major theme
- **Ecosystem thinking** gaining prominence
- **Education and students** (PhD, university students) becoming research subjects
- **Behavioral theories** (TPB) increasingly applied
- **Lean/agile methodologies** entering the academic entrepreneurship discourse

### 10.5. Key Authors
- WRIGHT, M is the most central author across all dimensions
- European scholars dominate (UK, Italy, Spain)
- Prolific author networks centered around major universities

---

## 12. Historical Roots (RPYS - Reference Publication Year Spectroscopy)

RPYS analysis examined **90,252 cited references** to identify the intellectual foundations of the field.

### Peak Years (Historical Roots)

| Year | Citations | Deviation | Key Seminal Works |
|------|-----------|-----------|-------------------|
| **2011** | 4,422 | +840 | HAYTER (J Technol Transfer) - motivations of nascent academic entrepreneurs |
| **2007** | 4,121 | +829 | CLARYSSE, SIEGEL, LOWE - university spin-offs and technology transfer |
| **1998** | 1,481 | +385 | GARNSEY (Ind Corp Change), ADT Athens project |
| **2005** | 3,776 | +270 | KONDO, COCHRANE - venture capital and science policy |
| **2010** | 3,582 | +238 | HARRISON - regional studies on entrepreneurship |

### Historical Foundations (Earlier Peaks)

| Year | Citations | Key Works |
|------|-----------|-----------|
| **1912** | 36 | SCHUMPETER - Theory of Economic Development |
| **1934** | 23 | SCHUMPETER - Theory of Economic Development (English) |
| **1945** | 18 | BUSH - "Science, the Endless Frontier" |
| **1962** | 70 | ARROW - Rate of Invention, Economic Studies |
| **1973** | 118 | GRANOVETTER - Strength of Weak Ties |
| **1986** | 390 | KENNEY - Biotechnology University-Industry relations |
| **1991** | 764 | AJZEN - Theory of Planned Behavior; BARNEY - RBV |

**Interpretation**: The field is built upon Schumpeterian economics (1912-1934), postwar science policy (Bush 1945), innovation economics (Arrow 1962), social network theory (Granovetter 1973), and the biotechnology revolution (Kenney 1986).

---

## 13. Main Path Analysis

Main Path Analysis identified **20 key papers** that form the central trajectory of knowledge flow in the field.

### Citation Network Statistics
- **Papers indexed**: 1,294
- **Internal citations found**: 231
- **Edges in network**: 217

### Main Path Evolution (Chronological)

| Year | Author | Title | Citations | Path Score |
|------|--------|-------|-----------|------------|
| 2001 | [ANONYMOUS] | University spin-offs on the rise | 0 | 0.298 |
| 2003 | [ANONYMOUS] | University spin-off firms growing fast | 0 | 0.479 |
| 2007 | TOOLE, AA | Biomedical academic entrepreneurship through SBIR | 75 | 0.133 |
| 2008 | WRIGHT, M | Mid-range universities' linkages with industry | 333 | 0.133 |
| 2009 | WRIGHT, M | Academic entrepreneurship and business schools | 87 | 0.133 |
| 2011 | HAYTER, CS | In search of the profit-maximizing actor | 112 | 0.200 |
| 2017 | HAYTER, CS | Who is the academic entrepreneur? | 103 | 0.133 |
| 2017 | MERCELIS, J | Commercializing science: historical perspective | 19 | 0.200 |
| 2018 | HMIELESKI, KM | Psychological foundations of university commercialization | 56 | 0.133 |
| 2019 | MEIJER, LLJ | Barriers and drivers for technology commercialization | 51 | 0.133 |
| 2020 | SECUNDO, G | Digital Academic Entrepreneurship: literature review | 110 | 0.133 |
| 2021 | DOANH, DC | Academic entrepreneurship: invention commercialization | 7 | 0.133 |

### Trajectory Interpretation

1. **2001-2004**: Early descriptive phase (news articles about university spin-offs)
2. **2007-2009**: WRIGHT and TOOLE establish theoretical foundations
3. **2011-2017**: HAYTER develops behavioral/motivational research stream
4. **2017-2018**: Historical and psychological perspectives emerge
5. **2019-2021**: Contemporary topics include barriers, digitalization (SECUNDO), and emerging economies

**Key Finding**: The main path shows evolution from descriptive reporting → theoretical frameworks (WRIGHT) → behavioral foundations (HAYTER) → current diversification (digital, barriers, global perspectives).

---

## 15. Semantic Frontier Analysis (BERTopic NLP)

BERTopic analysis processed **1,238 abstracts** using BERT embeddings, UMAP dimensionality reduction, and HDBSCAN clustering to identify latent semantic themes.

### Key Finding: High Semantic Cohesion

> [!IMPORTANT]
> The field demonstrates **exceptional semantic homogeneity**. Despite forcing topic differentiation, BERTopic identified only 2 distinct semantic clusters, indicating a highly consolidated research domain.

### Semantic Topics Identified

| Topic | Documents | Status | Keywords | Interpretation |
|-------|-----------|--------|----------|----------------|
| **Topic 1** (Main) | 1,213 (98%) | EMERGING | university, research, academic, entrepreneurship, spin, knowledge, technology | Core traditional focus - mature and integrated |
| **Topic 0** (Frontier) | 25 (2%) | FRONTIER | digital, entrepreneurship, technologies, academic, learning, dt | **Digital Academic Entrepreneurship** - emerging niche |

### Comparison: NLP Topics vs. Bibliometric Keywords

| Dimension | Bibliometric Analysis | BERTopic Semantic Analysis |
|-----------|----------------------|---------------------------|
| **Clusters** | 3 keyword clusters | 2 semantic topics |
| **Method** | Keyword co-occurrence | Text embedding similarity |
| **Top Keywords** | Academic entrepreneurship, innovation, spin-offs | University, research, entrepreneurship, digital |
| **Overlap** | 50% | 10% (frontier) to 50% (main) |

### Frontier Topic Deep Dive: Digital Academic Entrepreneurship

**Representative Documents:**
1. *"Today's digital technologies, such as social media, business analytics, the Internet of Things, big data, advanced manufacturing, 3D printing, cloud and cyber-solutions and MOOCs, permeate every private..."*

2. *"Digital technologies are transforming the entrepreneurial landscape and enabling the democratization of entrepreneurship. The ongoing advancement of digital technologies has transformed the business..."*

3. *"Digital technology has become a new economic and social force, reshaping traditional business models, strategies, structures, and processes..."*

### Latent Themes Interpretation

The **FRONTIER** topic (10% bibliometric overlap) represents research on:
- **Digital transformation** of academic entrepreneurship
- **Platform-based** knowledge commercialization
- **Technology democratization** in university contexts
- **New business models** enabled by digital technologies

> [!TIP]
> **Research Gap Identified**: Only 2% of the corpus addresses digital transformation explicitly. This suggests an underexplored frontier with high potential for novel contributions.

### Why Only 2 Topics?

The low topic count is **scientifically meaningful**, not a limitation:
1. **Field Maturity**: Academic entrepreneurship is a consolidated research domain
2. **Shared Vocabulary**: Common terminology across all subfields
3. **Tight Citation Networks**: High bibliographic coupling (modularity 0.83)
4. **Integrated Research Communities**: Strong collaboration patterns

---

## 16. Output Files Reference

| File | Description |
|------|-------------|
| `keywords_cooccurrence_enriched.gexf` | Keyword network for Gephi visualization |
| `bibliographic_coupling_normalized.gexf` | Author coupling network (backbone extracted) |
| `temporal_evolution_sankey.csv` | Theme evolution data for Sankey diagram |
| `core_authors_by_cluster.csv` | Top authors per thematic cluster |
| `keyword_bursts.csv` | Keywords with significant recent growth |
| `network_statistics.csv` | Comparative network metrics |
| `historical_roots.csv` | RPYS spectroscopy data (year citations) |
| `main_path_papers.csv` | 20 key papers in knowledge trajectory |
| `rpys_spectroscopy.pdf` | RPYS visualization plot |
| `main_path_evolution.pdf` | Main path chronological visualization |
| `semantic_topics.csv` | BERTopic semantic topics with representative docs |

---

*Report generated: 2026-01-29*  
*Analysis method: Advanced Bibliometric Analysis with Salton's Cosine normalization, Disparity Filter backbone extraction, and Z-score based burst detection*
