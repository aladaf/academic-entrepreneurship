# Bibliometric Analysis Report: Academic Entrepreneurship
## Web of Science + Scopus Consolidated Analysis

---

## 1. Dataset Overview

| Metric | Value |
|--------|-------|
| **Data Sources** | 4 WoS files (data-wos-01 to 04.txt) + 1 Scopus file (data-scopus-01.csv) |
| **WoS Records** | 1,606 |
| **Scopus Records** | 2,423 |
| **Duplicates Removed (by DOI)** | 1,206 |
| **Duplicates Removed (by Title)** | 8 |
| **Records from 2026 Excluded** | 20 |
| **Final Unique Records** | 2,795 |
| **Time Span** | 1972 - 2025 |
| **Sources (Journals)** | 976 |
| **Unique Authors** | 5,877 |
| **Total Citations** | 94,128 |
| **Average Citations/Document** | 33.68 |

---

## 2. Annual Scientific Production

The field shows clear exponential growth patterns:

| Year | Pubs | Year | Pubs | Year | Pubs | Year | Pubs |
|------|------|------|------|------|------|------|------|
| 1972 | 1 | 1998 | 11 | 2010 | 75 | 2019 | 183 |
| 1980 | 1 | 1999 | 5 | 2011 | 80 | 2020 | 183 |
| 1983 | 2 | 2000 | 8 | 2012 | 83 | 2021 | 222 |
| 1988 | 3 | 2001 | 13 | 2013 | 105 | 2022 | 224 |
| 1990 | 3 | 2002 | 8 | 2014 | 101 | 2023 | 218 |
| 1993 | 5 | 2003 | 20 | 2015 | 125 | 2024 | 227 |
| 1996 | 5 | 2004 | 23 | 2016 | 137 | 2025 | 218 |
| 1997 | 3 | 2005 | 41 | 2017 | 131 | | |
| | | 2006 | 41 | 2018 | 151 | | |
| | | 2007 | 29 | | | | |
| | | 2008 | 52 | | | | |
| | | 2009 | 49 | | | | |

**Key Observation**: Exponential growth from 2010 onwards, with consistent 200+ publications per year since 2021.

---

## 3. Top 15 Most Productive Sources (Journals)

| Rank | Journal | Publications |
|------|---------|-------------|
| 1 | Journal of Technology Transfer | 211 |
| 2 | Industry and Higher Education | 96 |
| 3 | Research Policy | 92 |
| 4 | Technovation | 72 |
| 5 | Technological Forecasting and Social Change | 56 |
| 6 | Small Business Economics | 51 |
| 7 | Sustainability | 45 |
| 8 | Science and Public Policy | 42 |
| 9 | Studies in Higher Education | 38 |
| 10 | International Entrepreneurship and Management | 37 |
| 11 | Journal of the Knowledge Economy | 34 |
| 12 | International Journal of Technology Management | 28 |
| 13 | Higher Education | 24 |
| 14 | Triple Helix | 20 |
| 15 | International Journal of Entrepreneurial Behavior | 20 |

**Key Observation**: Journal of Technology Transfer dominates with 211 publications (7.5% of total).

---

## 4. Top 15 Most Cited Authors

| Rank | Author | Total Citations | Papers | Avg Citations/Paper |
|------|--------|----------------|--------|---------------------|
| 1 | ETZKOWITZ, H | 5,583 | 21 | 265.9 |
| 2 | WRIGHT, M. | 4,893 | 23 | 212.7 |
| 3 | WRIGHT, M | 4,208 | 22 | 191.3 |
| 4 | GUERRERO, M | 3,289 | 35 | 94.0 |
| 5 | PERKMANN, M | 3,037 | 8 | 379.6 |
| 6 | URBANO, D | 2,872 | 19 | 151.2 |
| 7 | CLARYSSE, B. | 2,771 | 13 | 213.2 |
| 8 | D'ESTE, P | 2,678 | 8 | 334.8 |
| 9 | GRIMALDI, R | 2,650 | 9 | 294.4 |
| 10 | TARTARI, V | 2,478 | 7 | 354.0 |
| 11 | FINI, R | 2,433 | 12 | 202.8 |
| 12 | LOCKETT, A. | 2,327 | 9 | 258.6 |
| 13 | SALTER, A | 2,141 | 6 | 356.8 |
| 14 | HUGHES, A | 2,041 | 3 | 680.3 |
| 15 | MCKELVEY, M | 1,951 | 5 | 390.2 |

**Key Observation**: ETZKOWITZ, H is now the most cited author (5,583 citations), overtaking WRIGHT, M.

---

## 5. Country Scientific Production (Top 20)

| Rank | Country | Publications |
|------|---------|-------------|
| 1 | ITALY | 348 |
| 2 | UK | 294 |
| 3 | SPAIN | 231 |
| 4 | GERMANY | 204 |
| 5 | UNITED KINGDOM | 144 |
| 6 | CHINA | 143 |
| 7 | SWEDEN | 141 |
| 8 | USA | 125 |
| 9 | NETHERLANDS | 124 |
| 10 | BRAZIL | 110 |
| 11 | BELGIUM | 99 |
| 12 | PORTUGAL | 92 |
| 13 | FRANCE | 87 |
| 14 | AUSTRALIA | 87 |
| 15 | NORWAY | 81 |
| 16 | CANADA | 80 |
| 17 | MALAYSIA | 74 |
| 18 | FINLAND | 69 |
| 19 | DENMARK | 61 |

**Key Observation**: European dominance with Italy (348) and UK (294+144) leading. Strong representation from emerging economies (China, Brazil, Malaysia).

---

## 6. Network Analysis Results

### 6.1. Keywords Co-occurrence Network

| Metric | Value |
|--------|-------|
| **Nodes (Keywords)** | 50 |
| **Edges (Co-occurrences)** | 1,058 |
| **Density** | 0.8637 (very high) |
| **Diameter** | 2 |
| **Average Clustering** | 0.057 |
| **Modularity** | 0.055 |
| **Giant Component %** | 100% |
| **Average Degree** | 42.32 |

### 6.2. Bibliographic Coupling Network (After Backbone Extraction)

| Metric | Before Backbone | After Backbone |
|--------|-----------------|----------------|
| **Nodes** | 949 | 468 |
| **Edges** | 143,285 | 1,501 |
| **Density** | 0.3185 | 0.0137 |
| **Diameter** | 4 | 11 |
| **Avg Clustering** | 0.0734 | 0.2256 |
| **Modularity** | N/A | 0.8292 |
| **Communities** | - | 30 |

---

## 7. Core Authors by Thematic Cluster

### Cluster 0: ACADEMIC ENTREPRENEURSHIP (Growing)
- **Authors**: 2,811
- **Top Authors**: GUERRERO, M; WRIGHT, M; RASMUSSEN, E; CUNNINGHAM, JA; HAYTER, CS

### Cluster 1: INNOVATION (Growing)
- **Authors**: 2,016
- **Top Authors**: WRIGHT, M; RASMUSSEN, E; RODEIRO-PAZOS, D; VISMARA, S

### Cluster 2: DETERMINANTS (Growing)
- **Authors**: 29

---

## 8. Keyword Burst Detection (2024-2025)

Top bursting keywords (Z-score > 2.0):

| Keyword | Z-Score | Trend |
|---------|---------|-------|
| L26 | 40.50 | ↑ |
| I23 | 34.27 | ↑ |
| O32 | 31.00 | ↑ |
| INTRAPRENEURSHIP | 13.24 | ↑ |
| ENTREPRENEURIAL BEHAVIOR | 12.85 | ↑ |
| SUSTAINABLE DEVELOPMENT GOALS | 12.62 | ↑ |
| UNIVERSITY TECHNOLOGY TRANSFER | 10.78 | ↑ |

---

## 9. Historical Roots (RPYS)

**Total cited references analyzed**: 132,689

### Peak Years (Historical Roots)

| Year | Citations | Deviation | Key Works |
|------|-----------|-----------|-----------|
| 2007 | 5,731 | +992 | CLARYSSE - spin-offs; SIEGEL - technology transfer |
| 2011 | 5,908 | +914 | HAYTER - motivations; D'ESTE - industry engagement |
| 1998 | 2,310 | +678 | CLARK - entrepreneurial university; ETZKOWITZ - triple helix |
| 2005 | 4,984 | +370 | SHANE - academic entrepreneurship |

---

## 10. Main Path Analysis

> [!IMPORTANT]
> Main Path Analysis successfully identified the central knowledge trajectory with **27,636 internal citations** across **27,081 edges**.

### Citation Network Statistics
- **Papers indexed**: 2,794
- **DOI index entries**: 2,632
- **Internal citations found**: 27,636
- **Citation network edges**: 27,081

### Main Path Evolution (20 Key Papers)

| Year | Author | Title | Citations | Path Score |
|------|--------|-------|-----------|------------|
| 1998 | **CLARK, B.R.** | The entrepreneurial university: Demand and response | 107 | 0.285 |
| 2000 | **ETZKOWITZ, H** | The future of the university and the university of the future | 1,413 | 0.525 |
| 2008 | **BERCOVITZ, J** | Academic entrepreneurs: Organizational change at the individual level | 590 | 0.281 |
| 2011 | **GRIMALDI, R** | 30 years after Bayh-Dole: Reassessing academic entrepreneurship | 560 | 0.312 |
| 2011 | **D'ESTE, P** | Why do academics engage with industry? Entrepreneurial motivations | 678 | 0.247 |
| 2012 | **GUERRERO, M** | The development of an entrepreneurial university | 469 | 0.313 |
| 2013 | **PERKMANN, M** | Academic engagement and commercialisation: A review | 1,566 | 0.483 |
| 2013 | **ABREU, M** | The nature of academic entrepreneurship in the UK | 357 | 0.330 |
| 2014 | **AUDRETSCH, DB** | From the entrepreneurial university to the university for the entrepreneurial society | 532 | 0.241 |
| 2015 | **SIEGEL, DS** | Academic Entrepreneurship: Time for a Rethink? | 439 | 0.355 |
| 2015 | **GUERRERO, M** | Economic impact of entrepreneurial universities' activities | 361 | 0.270 |
| 2016 | **GUERRERO, M** | Entrepreneurial universities: emerging models | 298 | 0.272 |
| 2018 | **CLAUSS, T** | Entrepreneurial university: a stakeholder-based conceptualisation | 43 | 0.400 |
| 2018 | **MIRANDA, FJ** | Re-thinking university spin-off: A critical literature review | 69 | 0.269 |
| 2018 | **FINI, R** | Rethinking the commercialization of public science | 163 | 0.249 |
| 2018 | **HAYTER, CS** | Conceptualizing academic entrepreneurship ecosystems | 187 | 0.600 |
| 2019 | **MATHISEN, MT** | The development, growth, and performance of university spin-offs | 112 | 0.318 |
| 2019 | **KLOFSTEN, M** | The entrepreneurial university as driver for economic growth | 290 | 0.518 |
| 2019 | **CENTOBELLI, P** | Exploration and exploitation in more entrepreneurial universities | 81 | 0.255 |
| 2020 | **COMPAGNUCCI, L** | The Third Mission of the university: A systematic literature review | 418 | 0.315 |

### Trajectory Interpretation

1. **1998-2000**: Foundation phase (CLARK, ETZKOWITZ establish the "entrepreneurial university" concept)
2. **2008-2011**: Theoretical development (BERCOVITZ, GRIMALDI, D'ESTE - motivations and Bayh-Dole impact)
3. **2012-2016**: GUERRERO era - economic impact and model development
4. **2013**: PERKMANN's landmark review (1,566 citations - highest in main path)
5. **2018**: Rethinking and ecosystem perspectives (FINI, HAYTER, MIRANDA)
6. **2019-2020**: Contemporary diversification (third mission, spin-off performance, ecosystems)

---

## 11. Semantic Frontier Analysis (BERTopic)

**Abstracts analyzed**: 2,739
**Topics identified**: 14
**Outlier documents**: 995

### Main Topics

| Topic | Documents | Keywords |
|-------|-----------|----------|
| 0 (Main) | 763 | entrepreneurial, entrepreneurship, academic, university, research |
| 1 | 422 | universities, university, research, innovation, technology |
| 2 | 317 | spin, offs, university, firms, research, companies |
| 3 | 59 | engagement, scientists, research, academic, industry |
| 4 (Frontier) | 53 | **digital**, design, entrepreneurship, technologies |

### Frontier Topics Identified

- **Topic 4**: Digital entrepreneurship, design thinking
- **Topic 8**: Sustainability, sustainable development, environmental impacts
- **Topic 11**: Creative industries, arts, creativity entrepreneurship
- **Topic 12**: Science parks, STPs, NTBFs

---

## 12. Data Source Integration Summary

| Metric | WoS Only | WoS + Scopus |
|--------|----------|--------------|
| Total Documents | 1,294 | 2,795 |
| Time Span | 1988-2025 | 1972-2025 |
| Unique Authors | 2,711 | 5,877 |
| Total Citations | 44,190 | 94,128 |
| Internal Citations (Main Path) | 231 | 27,636 |
| Main Path Quality | Low (Anonymous authors) | High (Real authors) |

---

## 13. Output Files Reference

| File | Description |
|------|-------------|
| `keywords_cooccurrence_enriched.gexf` | Keyword network for Gephi visualization |
| `bibliographic_coupling_normalized.gexf` | Author coupling network (backbone extracted) |
| `temporal_evolution_sankey.csv` | Theme evolution data for Sankey diagram |
| `core_authors_by_cluster.csv` | Top authors per thematic cluster |
| `keyword_bursts.csv` | Keywords with significant recent growth |
| `network_statistics.csv` | Comparative network metrics |
| `historical_roots.csv` | RPYS spectroscopy data |
| `main_path_papers.csv` | 20 key papers in knowledge trajectory |
| `main_path_full_details.csv` | Extended paper metadata for main path |
| `rpys_spectroscopy.pdf` | RPYS visualization plot |
| `main_path_evolution.pdf` | Main path chronological visualization |
| `semantic_topics.csv` | BERTopic semantic topics |
| `semantic_intertopic_distance.html` | Interactive topic distance map |
| `semantic_topics_barchart.html` | Topic keywords bar chart |

---

*Report generated: 2026-01-31*  
*Data sources: Web of Science (1,606 records) + Scopus (2,423 records)*  
*Deduplication: DOI-based matching (1,214 duplicates removed)*  
*Analysis method: Advanced Bibliometric Analysis with Salton's Cosine normalization, Disparity Filter backbone extraction, Z-score burst detection, and BERTopic semantic analysis*
