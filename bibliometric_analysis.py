#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Bibliometric Analysis Script for Web of Science Data
==============================================================

Professional script for comprehensive bibliometric analysis of WoS data
on 'Digital Entrepreneurship' for high-impact scientific article (Q1 journals).

Features:
- Normalized bibliographic coupling (Salton's Cosine)
- Backbone extraction (Disparity Filter)
- Temporal evolution analysis (Sankey diagram data)
- Core authors identification by thematic cluster
- Burst detection (Z-score based Kleinberg approximation)
- Pre-calculated network attributes for Gephi

Author: Bibliometric Analysis Tool
Date: 2026-01-25
Libraries: pandas, networkx, numpy, scipy
"""

import os
import sys
import argparse
import math
from collections import Counter, defaultdict
from itertools import combinations
import warnings

warnings.filterwarnings('ignore')

try:
    import pandas as pd
except ImportError:
    print("Error: pandas library not installed. Run: pip install pandas")
    sys.exit(1)

try:
    import networkx as nx
    from networkx.algorithms import community
except ImportError:
    print("Error: networkx library not installed. Run: pip install networkx")
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print("Error: numpy library not installed. Run: pip install numpy")
    sys.exit(1)

try:
    from scipy import stats
except ImportError:
    print("Error: scipy library not installed. Run: pip install scipy")
    sys.exit(1)


# =============================================================================
# CONFIGURATION
# =============================================================================

DEFAULT_DATA_DIR = "./"
DEFAULT_OUTPUT_DIR = "./output"
TOP_N_SOURCES = 15
TOP_N_AUTHORS = 15
TOP_N_KEYWORDS = 50
MIN_KEYWORD_FREQ = 2
BACKBONE_ALPHA = 0.05  # Significance level for disparity filter
N_TIME_PERIODS = 3
BURST_ZSCORE_THRESHOLD = 2.0
TOP_AUTHORS_PER_CLUSTER = 10


# =============================================================================
# DATA LOADING MODULE
# =============================================================================

def load_wos_data(data_dir: str) -> pd.DataFrame:
    """Load all Web of Science .txt files from the specified directory."""
    print("\n" + "=" * 70)
    print("DATA LOADING")
    print("=" * 70)
    
    txt_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
    
    if not txt_files:
        print(f"Error: No .txt files found in {data_dir}")
        sys.exit(1)
    
    print(f"Found {len(txt_files)} WoS files: {', '.join(txt_files)}")
    
    all_dfs = []
    
    for filename in txt_files:
        filepath = os.path.join(data_dir, filename)
        try:
            df = pd.read_csv(filepath, sep='\t', encoding='utf-8', 
                           dtype=str, on_bad_lines='skip')
            print(f"  ✓ {filename}: {len(df)} records loaded")
            all_dfs.append(df)
        except Exception as e:
            print(f"  ✗ {filename}: Failed - {str(e)[:50]}")
    
    if not all_dfs:
        print("Error: No records could be loaded.")
        sys.exit(1)
    
    combined_df = pd.concat(all_dfs, ignore_index=True)
    print(f"\nTotal records loaded: {len(combined_df)}")
    
    return combined_df


# =============================================================================
# PREPROCESSING MODULE
# =============================================================================

def preprocess_data(df: pd.DataFrame, exclude_year: int = 2026) -> pd.DataFrame:
    """Preprocess: remove duplicates, standardize fields, and filter by year.
    
    Args:
        df: Input DataFrame with WoS data
        exclude_year: Year to exclude from analysis (default: 2026 for early access)
    """
    print("\n" + "=" * 70)
    print("PREPROCESSING")
    print("=" * 70)
    
    initial_count = len(df)
    
    # Remove duplicates
    if 'UT' in df.columns:
        df = df.drop_duplicates(subset=['UT'], keep='first')
    else:
        df = df.drop_duplicates(subset=['TI', 'PY'], keep='first')
    
    duplicates = initial_count - len(df)
    after_dedup = len(df)
    
    # Filter out records from the excluded year (typically early access publications)
    if 'PY' in df.columns and exclude_year is not None:
        df['_year_num'] = pd.to_numeric(df['PY'], errors='coerce')
        excluded_records = len(df[df['_year_num'] == exclude_year])
        df = df[df['_year_num'] != exclude_year]
        df = df.drop(columns=['_year_num'])
        print(f"Initial records: {initial_count}")
        print(f"Duplicates removed: {duplicates}")
        print(f"Records from {exclude_year} excluded: {excluded_records}")
        print(f"Final unique records: {len(df)}")
    else:
        print(f"Initial records: {initial_count}")
        print(f"Duplicates removed: {duplicates}")
        print(f"Unique records: {len(df)}")
    
    return df


def standardize_author_name(name: str) -> str:
    """Standardize author name format."""
    if pd.isna(name) or not name:
        return ""
    return ' '.join(str(name).upper().split())


def parse_authors(au_field) -> list:
    """Parse author field from WoS format."""
    if pd.isna(au_field) or not au_field:
        return []
    return [standardize_author_name(a.strip()) for a in str(au_field).split(';') if a.strip()]


def parse_keywords(kw_field) -> list:
    """Parse keyword field from WoS format."""
    if pd.isna(kw_field) or not kw_field:
        return []
    return [k.strip().upper() for k in str(kw_field).split(';') if k.strip() and len(k.strip()) > 2]


def parse_references(cr_field) -> list:
    """Parse references field from WoS format."""
    if pd.isna(cr_field) or not cr_field:
        return []
    return [r.strip()[:50].upper() for r in str(cr_field).split(';') if r.strip()]


def extract_country_from_affiliation(affiliation: str) -> str:
    """Extract country from affiliation string."""
    if pd.isna(affiliation) or not affiliation:
        return None
    
    parts = str(affiliation).split(',')
    if parts:
        country = parts[-1].strip().upper()
        country_mapping = {
            'USA': 'USA', 'UNITED STATES': 'USA',
            'PEOPLES R CHINA': 'CHINA', "PEOPLE'S R CHINA": 'CHINA', 'P R CHINA': 'CHINA',
            'ENGLAND': 'UK', 'SCOTLAND': 'UK', 'WALES': 'UK',
            'NORTH IRELAND': 'UK', 'NORTHERN IRELAND': 'UK',
        }
        return country_mapping.get(country, country)
    return None


# =============================================================================
# QUANTITATIVE ANALYSIS MODULE
# =============================================================================

def analyze_annual_production(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze annual scientific production."""
    df_years = df[df['PY'].notna()].copy()
    df_years['PY'] = pd.to_numeric(df_years['PY'], errors='coerce')
    df_years = df_years[df_years['PY'].notna()]
    
    year_counts = df_years['PY'].astype(int).value_counts().sort_index()
    result_df = pd.DataFrame({'Year': year_counts.index, 'Publications': year_counts.values})
    return result_df.sort_values('Year', ascending=True).reset_index(drop=True)


def analyze_top_sources(df: pd.DataFrame, top_n: int = TOP_N_SOURCES) -> pd.DataFrame:
    """Identify top productive sources (journals)."""
    sources = df[df['SO'].notna()]['SO'].str.upper()
    source_counts = sources.value_counts().head(top_n)
    
    return pd.DataFrame({
        'Rank': range(1, len(source_counts) + 1),
        'Source': source_counts.index,
        'Publications': source_counts.values
    })


def analyze_top_cited_authors(df: pd.DataFrame, top_n: int = TOP_N_AUTHORS) -> pd.DataFrame:
    """Identify most cited authors in the dataset."""
    author_citations = defaultdict(int)
    author_papers = defaultdict(int)
    
    for _, row in df.iterrows():
        authors = parse_authors(row.get('AU', ''))
        try:
            citations = int(float(row.get('TC', 0))) if pd.notna(row.get('TC')) else 0
        except (ValueError, TypeError):
            citations = 0
        
        for author in authors:
            if author:
                author_citations[author] += citations
                author_papers[author] += 1
    
    sorted_authors = sorted(author_citations.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    result_df = pd.DataFrame(sorted_authors, columns=['Author', 'Total Citations'])
    result_df['Papers'] = result_df['Author'].map(author_papers)
    result_df['Avg Citations'] = (result_df['Total Citations'] / result_df['Papers']).round(1)
    result_df.insert(0, 'Rank', range(1, len(result_df) + 1))
    
    return result_df


def analyze_country_collaboration(df: pd.DataFrame) -> tuple:
    """Analyze country distribution and collaboration."""
    country_counts = Counter()
    country_collaborations = Counter()
    
    for _, row in df.iterrows():
        affiliations = str(row.get('C1', '')) if pd.notna(row.get('C1')) else ''
        aff_list = affiliations.replace('[', ';').replace(']', ';').split(';')
        
        record_countries = set()
        for aff in aff_list:
            if aff.strip():
                country = extract_country_from_affiliation(aff.strip())
                if country and len(country) > 1:
                    record_countries.add(country)
        
        for country in record_countries:
            country_counts[country] += 1
        
        if len(record_countries) > 1:
            for pair in combinations(sorted(record_countries), 2):
                country_collaborations[pair] += 1
    
    country_df = pd.DataFrame(country_counts.most_common(20), columns=['Country', 'Publications'])
    country_df.insert(0, 'Rank', range(1, len(country_df) + 1))
    
    top_collab = country_collaborations.most_common(10)
    collab_df = pd.DataFrame(
        [(f"{c[0][0]} - {c[0][1]}", c[1]) for c in top_collab], 
        columns=['Country Pair', 'Collaborations']
    )
    
    return country_df, collab_df


# =============================================================================
# NETWORK ANALYSIS MODULE - BASIC
# =============================================================================

def build_keyword_cooccurrence_network(df: pd.DataFrame, top_n: int = TOP_N_KEYWORDS) -> nx.Graph:
    """Build keyword co-occurrence network."""
    print("\n  Building keyword co-occurrence network...")
    
    all_keywords = Counter()
    record_keywords = []
    
    for _, row in df.iterrows():
        keywords = set()
        keywords.update(parse_keywords(row.get('DE', '')))
        keywords.update(parse_keywords(row.get('ID', '')))
        
        if keywords:
            record_keywords.append(keywords)
            all_keywords.update(keywords)
    
    top_keywords = {kw for kw, _ in all_keywords.most_common(top_n)}
    
    cooccurrence = Counter()
    for keywords in record_keywords:
        filtered = keywords & top_keywords
        for pair in combinations(sorted(filtered), 2):
            cooccurrence[pair] += 1
    
    G = nx.Graph()
    
    for kw in top_keywords:
        G.add_node(kw, frequency=all_keywords[kw], label=kw)
    
    for (kw1, kw2), weight in cooccurrence.items():
        if weight >= MIN_KEYWORD_FREQ:
            G.add_edge(kw1, kw2, weight=weight)
    
    isolated = list(nx.isolates(G))
    G.remove_nodes_from(isolated)
    
    print(f"    Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
    
    return G


# =============================================================================
# ADVANCED NETWORK ANALYSIS - NORMALIZED COUPLING
# =============================================================================

def build_normalized_coupling_network(df: pd.DataFrame, min_papers: int = 2) -> nx.Graph:
    """
    Build bibliographic coupling network with Salton's Cosine normalization.
    
    Salton's Cosine: weight = shared_refs / sqrt(refs_a * refs_b)
    This normalizes for authors with many publications.
    """
    print("\n  Building normalized bibliographic coupling network...")
    
    author_refs = defaultdict(set)
    author_papers = Counter()
    author_citations = defaultdict(int)
    
    for _, row in df.iterrows():
        authors = parse_authors(row.get('AU', ''))
        refs = parse_references(row.get('CR', ''))
        try:
            citations = int(float(row.get('TC', 0))) if pd.notna(row.get('TC')) else 0
        except (ValueError, TypeError):
            citations = 0
        
        for author in authors:
            if author:
                author_refs[author].update(refs)
                author_papers[author] += 1
                author_citations[author] += citations
    
    # Filter to authors with at least min_papers
    active_authors = {a for a, count in author_papers.items() if count >= min_papers}
    
    # Calculate normalized coupling strength
    coupling = {}
    authors_list = list(active_authors)
    
    for i, author1 in enumerate(authors_list):
        refs1 = author_refs[author1]
        len_refs1 = len(refs1)
        if len_refs1 == 0:
            continue
            
        for author2 in authors_list[i+1:]:
            refs2 = author_refs[author2]
            len_refs2 = len(refs2)
            if len_refs2 == 0:
                continue
                
            shared = len(refs1 & refs2)
            if shared >= 2:  # Minimum coupling
                # Salton's Cosine normalization
                normalized_weight = shared / math.sqrt(len_refs1 * len_refs2)
                coupling[(author1, author2)] = {
                    'raw': shared,
                    'normalized': normalized_weight
                }
    
    # Create network
    G = nx.Graph()
    
    for author in active_authors:
        if any(author in pair for pair in coupling.keys()):
            G.add_node(author, 
                      papers=author_papers[author], 
                      citations=author_citations[author],
                      label=author)
    
    for (a1, a2), weights in coupling.items():
        G.add_edge(a1, a2, 
                  weight=weights['normalized'],
                  weight_raw=weights['raw'])
    
    isolated = list(nx.isolates(G))
    G.remove_nodes_from(isolated)
    
    print(f"    Before backbone: Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
    
    return G


def apply_disparity_filter(G: nx.Graph, alpha: float = BACKBONE_ALPHA) -> nx.Graph:
    """
    Apply disparity filter (Serrano et al., 2009) for backbone extraction.
    
    Keeps edges that are statistically significant given the local topology.
    """
    print(f"  Applying disparity filter (alpha={alpha})...")
    
    if G.number_of_edges() == 0:
        return G
    
    edges_to_remove = []
    
    for u, v, data in G.edges(data=True):
        weight = data.get('weight', 1.0)
        
        # Calculate strength (sum of weights) for both nodes
        strength_u = sum(G[u][neighbor].get('weight', 1.0) for neighbor in G.neighbors(u))
        strength_v = sum(G[v][neighbor].get('weight', 1.0) for neighbor in G.neighbors(v))
        
        degree_u = G.degree(u)
        degree_v = G.degree(v)
        
        # Normalized weight for each endpoint
        p_u = weight / strength_u if strength_u > 0 else 0
        p_v = weight / strength_v if strength_v > 0 else 0
        
        # P-value based on null model (uniform distribution)
        # p-value = (1 - p)^(k-1) where k is degree
        try:
            pval_u = (1 - p_u) ** (degree_u - 1) if degree_u > 1 else 1.0
            pval_v = (1 - p_v) ** (degree_v - 1) if degree_v > 1 else 1.0
        except:
            pval_u = pval_v = 1.0
        
        # Keep edge if significant for at least one endpoint
        if pval_u > alpha and pval_v > alpha:
            edges_to_remove.append((u, v))
    
    G_backbone = G.copy()
    G_backbone.remove_edges_from(edges_to_remove)
    
    # Remove isolated nodes after edge removal
    isolated = list(nx.isolates(G_backbone))
    G_backbone.remove_nodes_from(isolated)
    
    print(f"    After backbone: Nodes: {G_backbone.number_of_nodes()}, Edges: {G_backbone.number_of_edges()}")
    print(f"    Edges removed: {len(edges_to_remove)}")
    
    return G_backbone


def extract_giant_component(G: nx.Graph) -> nx.Graph:
    """Extract the largest connected component."""
    if G.number_of_nodes() == 0:
        return G
    
    components = list(nx.connected_components(G))
    if not components:
        return G
    
    giant = max(components, key=len)
    G_giant = G.subgraph(giant).copy()
    
    print(f"  Giant component: {G_giant.number_of_nodes()} nodes ({100*len(giant)/G.number_of_nodes():.1f}% of network)")
    
    return G_giant


# =============================================================================
# COMMUNITY DETECTION AND ENRICHMENT
# =============================================================================

def detect_communities(G: nx.Graph) -> dict:
    """Detect communities using Louvain-like greedy modularity optimization."""
    if G.number_of_nodes() == 0:
        return {}
    
    try:
        communities = community.greedy_modularity_communities(G, weight='weight')
        
        node_community = {}
        for idx, comm in enumerate(communities):
            for node in comm:
                node_community[node] = idx
        
        return node_community
    except Exception as e:
        print(f"    Warning: Community detection failed: {e}")
        return {node: 0 for node in G.nodes()}


def enrich_network_attributes(G: nx.Graph) -> nx.Graph:
    """Add pre-calculated attributes for Gephi visualization."""
    if G.number_of_nodes() == 0:
        return G
    
    print("  Enriching network with attributes...")
    
    G_enriched = G.copy()
    
    # Community detection
    communities = detect_communities(G_enriched)
    nx.set_node_attributes(G_enriched, communities, 'modularity_class')
    
    # Degree
    degrees = dict(G_enriched.degree())
    nx.set_node_attributes(G_enriched, degrees, 'degree')
    
    # Weighted degree
    weighted_degrees = dict(G_enriched.degree(weight='weight'))
    nx.set_node_attributes(G_enriched, weighted_degrees, 'weighted_degree')
    
    # Betweenness centrality
    try:
        betweenness = nx.betweenness_centrality(G_enriched, weight='weight')
        nx.set_node_attributes(G_enriched, betweenness, 'betweenness')
    except:
        pass
    
    # PageRank
    try:
        pagerank = nx.pagerank(G_enriched, weight='weight')
        nx.set_node_attributes(G_enriched, pagerank, 'pagerank')
    except:
        pass
    
    # Calculate modularity score
    try:
        comm_sets = defaultdict(set)
        for node, comm_id in communities.items():
            comm_sets[comm_id].add(node)
        modularity = nx.algorithms.community.modularity(G_enriched, comm_sets.values())
        G_enriched.graph['modularity'] = modularity
        print(f"    Modularity: {modularity:.3f}")
    except Exception as e:
        print(f"    Warning: Could not calculate modularity: {e}")
    
    n_communities = len(set(communities.values())) if communities else 0
    print(f"    Communities detected: {n_communities}")
    
    return G_enriched


# =============================================================================
# TEMPORAL EVOLUTION ANALYSIS
# =============================================================================

def define_time_periods(df: pd.DataFrame, n_periods: int = N_TIME_PERIODS) -> list:
    """
    Define time periods based on publication volume, not equal time spans.
    This ensures each period has enough documents for meaningful analysis.
    """
    years = pd.to_numeric(df['PY'], errors='coerce').dropna().astype(int)
    
    if len(years) == 0:
        return []
    
    # Count documents per year
    year_counts = years.value_counts().sort_index()
    min_year = int(years.min())
    max_year = int(years.max())
    
    # Try to find meaningful breakpoints based on literature growth
    # For Digital Entrepreneurship: typically pre-2018, 2018-2021, 2022+
    total_docs = len(years)
    
    # Find year where we have at least 15% of documents (early period ends)
    cumsum = year_counts.cumsum()
    
    # Define meaningful periods based on actual data distribution
    # Period 1: Earlier work (until ~15-20% of docs)
    # Period 2: Growth phase (next ~30-40%)
    # Period 3: Recent frontier (remaining ~40-50%)
    
    threshold_1 = max(10, int(total_docs * 0.15))
    threshold_2 = int(total_docs * 0.50)
    
    period_1_end = min_year
    period_2_end = min_year
    
    for year, cum in cumsum.items():
        if cum >= threshold_1 and period_1_end == min_year:
            period_1_end = int(year)
        if cum >= threshold_2:
            period_2_end = int(year)
            break
    
    # Ensure we don't have degenerate periods
    if period_1_end < 2018:
        period_1_end = 2018
    if period_2_end <= period_1_end:
        period_2_end = period_1_end + 2
    if period_2_end > max_year - 1:
        period_2_end = max_year - 1
    
    periods = [
        {'name': 'Emergência', 'start': min_year, 'end': period_1_end, 'index': 0},
        {'name': 'Consolidação', 'start': period_1_end + 1, 'end': period_2_end, 'index': 1},
        {'name': 'Fronteira', 'start': period_2_end + 1, 'end': max_year, 'index': 2}
    ]
    
    print(f"\n  Time periods defined (volume-based):")
    for p in periods:
        docs_in_period = len(years[(years >= p['start']) & (years <= p['end'])])
        print(f"    {p['name']}: {p['start']}-{p['end']} ({docs_in_period} docs)")
    
    return periods


def build_period_keyword_network(df: pd.DataFrame, start_year: int, end_year: int) -> tuple:
    """Build keyword network for a specific time period."""
    # Filter by year
    df_period = df.copy()
    df_period['year_num'] = pd.to_numeric(df_period['PY'], errors='coerce')
    df_period = df_period[(df_period['year_num'] >= start_year) & (df_period['year_num'] <= end_year)]
    
    if len(df_period) == 0:
        return nx.Graph(), Counter()
    
    all_keywords = Counter()
    record_keywords = []
    
    for _, row in df_period.iterrows():
        keywords = set()
        keywords.update(parse_keywords(row.get('DE', '')))
        keywords.update(parse_keywords(row.get('ID', '')))
        
        if keywords:
            record_keywords.append(keywords)
            all_keywords.update(keywords)
    
    # Get top keywords for this period
    top_n = min(30, len(all_keywords))
    top_keywords = {kw for kw, _ in all_keywords.most_common(top_n)}
    
    # Build co-occurrence
    cooccurrence = Counter()
    for keywords in record_keywords:
        filtered = keywords & top_keywords
        for pair in combinations(sorted(filtered), 2):
            cooccurrence[pair] += 1
    
    G = nx.Graph()
    for kw in top_keywords:
        G.add_node(kw, frequency=all_keywords[kw])
    
    for (kw1, kw2), weight in cooccurrence.items():
        if weight >= 1:
            G.add_edge(kw1, kw2, weight=weight)
    
    return G, all_keywords


def analyze_temporal_evolution(df: pd.DataFrame, output_dir: str) -> pd.DataFrame:
    """
    Analyze temporal evolution of themes for Sankey diagram.
    Returns DataFrame for Sankey visualization.
    """
    print("\n" + "=" * 70)
    print("TEMPORAL EVOLUTION ANALYSIS")
    print("=" * 70)
    
    periods = define_time_periods(df)
    
    if len(periods) < 2:
        print("  Insufficient time span for temporal analysis")
        return pd.DataFrame()
    
    # Build networks and detect communities for each period
    period_data = []
    
    for period in periods:
        G, keywords = build_period_keyword_network(df, period['start'], period['end'])
        
        if G.number_of_nodes() > 0:
            communities = detect_communities(G)
            
            # Group keywords by community
            cluster_keywords = defaultdict(list)
            for kw, comm_id in communities.items():
                cluster_keywords[comm_id].append((kw, keywords[kw]))
            
            # Sort keywords within each cluster by frequency
            for comm_id in cluster_keywords:
                cluster_keywords[comm_id].sort(key=lambda x: x[1], reverse=True)
            
            period_data.append({
                'period': period,
                'graph': G,
                'communities': communities,
                'cluster_keywords': dict(cluster_keywords),
                'keywords': keywords
            })
            
            print(f"\n  {period['name']}: {G.number_of_nodes()} keywords, {len(set(communities.values()))} clusters")
    
    # Generate Sankey data
    sankey_rows = []
    
    for i in range(len(period_data) - 1):
        p1 = period_data[i]
        p2 = period_data[i + 1]
        
        transition = f"{p1['period']['name']}→{p2['period']['name']}"
        
        # For each cluster in p1, find ALL clusters in p2 with meaningful overlap
        for c1_id, c1_keywords in p1['cluster_keywords'].items():
            c1_kw_set = set(kw for kw, _ in c1_keywords[:15])  # Top 15 keywords for better matching
            c1_name = c1_keywords[0][0] if c1_keywords else f"Cluster_{c1_id}"
            
            # Find all clusters in p2 with meaningful overlap
            for c2_id, c2_keywords in p2['cluster_keywords'].items():
                c2_kw_set = set(kw for kw, _ in c2_keywords[:15])
                c2_name = c2_keywords[0][0] if c2_keywords else f"Cluster_{c2_id}"
                
                if len(c1_kw_set | c2_kw_set) > 0:
                    # Calculate multiple similarity metrics
                    intersection = c1_kw_set & c2_kw_set
                    jaccard = len(intersection) / len(c1_kw_set | c2_kw_set)
                    overlap_coef = len(intersection) / min(len(c1_kw_set), len(c2_kw_set)) if min(len(c1_kw_set), len(c2_kw_set)) > 0 else 0
                    
                    # Use a lower threshold (0.05) and also consider overlap coefficient
                    if jaccard > 0.05 or overlap_coef > 0.15:
                        sankey_rows.append({
                            'Source': f"{p1['period']['name']}_{c1_name}",
                            'Target': f"{p2['period']['name']}_{c2_name}",
                            'Value': round(max(jaccard, overlap_coef * 0.5), 3),
                            'Jaccard': round(jaccard, 3),
                            'Overlap_Coef': round(overlap_coef, 3),
                            'Shared_Keywords': len(intersection),
                            'Period_Transition': transition,
                            'Source_Keywords': ", ".join([kw for kw, _ in c1_keywords[:5]]),
                            'Target_Keywords': ", ".join([kw for kw, _ in c2_keywords[:5]]),
                            'Common_Keywords': ", ".join(list(intersection)[:5])
                        })
    
    sankey_df = pd.DataFrame(sankey_rows)
    
    if not sankey_df.empty:
        sankey_path = os.path.join(output_dir, 'temporal_evolution_sankey.csv')
        sankey_df.to_csv(sankey_path, index=False)
        print(f"\n  ✓ Sankey data exported to: {sankey_path}")
    
    return sankey_df


# =============================================================================
# CORE AUTHORS BY CLUSTER
# =============================================================================

def identify_core_authors(df: pd.DataFrame, keyword_network: nx.Graph, output_dir: str) -> pd.DataFrame:
    """
    Identify core authors for each thematic cluster.
    """
    print("\n" + "=" * 70)
    print("CORE AUTHORS BY CLUSTER")
    print("=" * 70)
    
    if keyword_network.number_of_nodes() == 0:
        print("  No keyword network available")
        return pd.DataFrame()
    
    # Get communities from keyword network
    communities = detect_communities(keyword_network)
    
    # Group keywords by cluster
    cluster_keywords = defaultdict(set)
    for kw, comm_id in communities.items():
        cluster_keywords[comm_id].add(kw)
    
    print(f"  Found {len(cluster_keywords)} thematic clusters")
    
    # For each cluster, find authors whose papers contain these keywords
    cluster_authors = defaultdict(lambda: defaultdict(int))
    author_papers_in_cluster = defaultdict(lambda: defaultdict(list))
    
    # Calculate keyword frequencies for trend detection
    years = pd.to_numeric(df['PY'], errors='coerce')
    max_year = int(years.max()) if len(years) > 0 else 2025
    recent_years = [max_year, max_year - 1]
    
    keyword_freq_recent = Counter()
    keyword_freq_historical = Counter()
    
    for _, row in df.iterrows():
        authors = parse_authors(row.get('AU', ''))
        paper_keywords = set()
        paper_keywords.update(parse_keywords(row.get('DE', '')))
        paper_keywords.update(parse_keywords(row.get('ID', '')))
        
        try:
            year = int(float(row.get('PY', 0)))
        except:
            year = 0
        
        # Count keyword frequencies by period
        for kw in paper_keywords:
            if year in recent_years:
                keyword_freq_recent[kw] += 1
            else:
                keyword_freq_historical[kw] += 1
        
        # Match paper to clusters
        for cluster_id, cluster_kws in cluster_keywords.items():
            overlap = paper_keywords & cluster_kws
            if len(overlap) >= 2:  # Paper contributes to cluster if >=2 keywords match
                for author in authors:
                    if author:
                        cluster_authors[cluster_id][author] += len(overlap)
                        author_papers_in_cluster[cluster_id][author].append(row.get('TI', ''))
    
    # Build results
    results = []
    
    for cluster_id, authors_scores in cluster_authors.items():
        cluster_kws = cluster_keywords[cluster_id]
        
        # Determine cluster name from top keyword
        kw_freqs = [(kw, keyword_network.nodes[kw].get('frequency', 0)) for kw in cluster_kws if kw in keyword_network.nodes]
        kw_freqs.sort(key=lambda x: x[1], reverse=True)
        cluster_name = kw_freqs[0][0] if kw_freqs else f"Cluster_{cluster_id}"
        
        # Top authors by contribution score
        top_authors = sorted(authors_scores.items(), key=lambda x: x[1], reverse=True)[:TOP_AUTHORS_PER_CLUSTER]
        
        # Key keywords
        key_keywords = [kw for kw, _ in kw_freqs[:5]]
        
        # Trend status
        recent_freq = sum(keyword_freq_recent.get(kw, 0) for kw in cluster_kws)
        historical_freq = sum(keyword_freq_historical.get(kw, 0) for kw in cluster_kws)
        
        if historical_freq > 0:
            ratio = recent_freq / (historical_freq / max(1, max_year - int(years.min()) - 2))
            if ratio > 1.3:
                trend = "Growing"
            elif ratio < 0.5:
                trend = "Fading"
            else:
                trend = "Stable"
        else:
            trend = "Emerging" if recent_freq > 0 else "Unknown"
        
        results.append({
            'Cluster_ID': cluster_id,
            'Nome_Sugerido': cluster_name,
            'Top_Authors': "; ".join([f"{a[0]} ({a[1]})" for a in top_authors]),
            'Key_Keywords': "; ".join(key_keywords),
            'Trend_Status': trend,
            'N_Keywords': len(cluster_kws),
            'N_Contributing_Authors': len(authors_scores)
        })
    
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('N_Contributing_Authors', ascending=False).reset_index(drop=True)
    
    if not results_df.empty:
        output_path = os.path.join(output_dir, 'core_authors_by_cluster.csv')
        results_df.to_csv(output_path, index=False)
        print(f"\n  ✓ Core authors exported to: {output_path}")
        
        # Print summary
        print(f"\n  Cluster Summary:")
        for _, row in results_df.iterrows():
            print(f"    [{row['Trend_Status']:8}] {row['Nome_Sugerido'][:25]:25} - {row['N_Contributing_Authors']} authors")
    
    return results_df


# =============================================================================
# BURST DETECTION
# =============================================================================

def detect_keyword_bursts(df: pd.DataFrame, output_dir: str, n_recent_years: int = 2) -> pd.DataFrame:
    """
    Detect keywords with frequency bursts using Z-score method.
    
    A keyword is in "burst" if its recent frequency is significantly higher
    than its historical average (z-score > threshold).
    """
    print("\n" + "=" * 70)
    print("BURST DETECTION")
    print("=" * 70)
    
    years = pd.to_numeric(df['PY'], errors='coerce').dropna().astype(int)
    
    if len(years) == 0:
        print("  No year data available")
        return pd.DataFrame()
    
    max_year = int(years.max())
    min_year = int(years.min())
    recent_years = set(range(max_year - n_recent_years + 1, max_year + 1))
    
    print(f"  Analyzing bursts for years: {list(recent_years)}")
    print(f"  Historical baseline: {min_year}-{max_year - n_recent_years}")
    
    # Count keyword frequencies by year
    keyword_by_year = defaultdict(lambda: defaultdict(int))
    
    for _, row in df.iterrows():
        try:
            year = int(float(row.get('PY', 0)))
        except:
            continue
        
        keywords = set()
        keywords.update(parse_keywords(row.get('DE', '')))
        keywords.update(parse_keywords(row.get('ID', '')))
        
        for kw in keywords:
            keyword_by_year[kw][year] += 1
    
    # Calculate z-scores
    burst_results = []
    
    for kw, year_counts in keyword_by_year.items():
        historical_counts = [year_counts.get(y, 0) for y in range(min_year, max_year - n_recent_years + 1)]
        recent_counts = [year_counts.get(y, 0) for y in recent_years]
        
        if len(historical_counts) < 3:  # Need enough historical data
            continue
        
        mean_hist = np.mean(historical_counts)
        std_hist = np.std(historical_counts)
        
        if std_hist == 0:
            std_hist = 0.5  # Avoid division by zero
        
        mean_recent = np.mean(recent_counts)
        z_score = (mean_recent - mean_hist) / std_hist
        
        total_freq = sum(year_counts.values())
        
        burst_results.append({
            'Keyword': kw,
            'Z_Score': round(z_score, 2),
            'Recent_Avg_Freq': round(mean_recent, 2),
            'Historical_Avg_Freq': round(mean_hist, 2),
            'Total_Frequency': total_freq,
            'Is_Burst': z_score > BURST_ZSCORE_THRESHOLD,
            'Years_Active': len([y for y, c in year_counts.items() if c > 0])
        })
    
    burst_df = pd.DataFrame(burst_results)
    burst_df = burst_df.sort_values('Z_Score', ascending=False)
    
    if not burst_df.empty:
        output_path = os.path.join(output_dir, 'keyword_bursts.csv')
        burst_df.to_csv(output_path, index=False)
        print(f"\n  ✓ Burst analysis exported to: {output_path}")
        
        # Print top bursts
        bursting = burst_df[burst_df['Is_Burst'] == True]
        print(f"\n  Keywords in BURST (z > {BURST_ZSCORE_THRESHOLD}):")
        for _, row in bursting.head(15).iterrows():
            print(f"    {row['Keyword'][:30]:30} z={row['Z_Score']:5.2f} (↑ {row['Recent_Avg_Freq']:.1f} vs hist {row['Historical_Avg_Freq']:.1f})")
    
    return burst_df


# =============================================================================
# NETWORK STATISTICS
# =============================================================================

def calculate_network_statistics(networks: dict, output_dir: str) -> pd.DataFrame:
    """Calculate and export network statistics."""
    print("\n" + "=" * 70)
    print("NETWORK STATISTICS")
    print("=" * 70)
    
    stats_rows = []
    
    for name, G in networks.items():
        if G is None or G.number_of_nodes() == 0:
            continue
        
        stats = {'Network': name}
        
        # Basic stats
        stats['Nodes'] = G.number_of_nodes()
        stats['Edges'] = G.number_of_edges()
        
        # Density
        stats['Density'] = round(nx.density(G), 4)
        
        # Diameter (for connected graphs)
        try:
            if nx.is_connected(G):
                stats['Diameter'] = nx.diameter(G)
            else:
                # Use largest component
                giant = max(nx.connected_components(G), key=len)
                stats['Diameter'] = nx.diameter(G.subgraph(giant))
        except:
            stats['Diameter'] = 'N/A'
        
        # Average clustering coefficient
        try:
            stats['Avg_Clustering'] = round(nx.average_clustering(G, weight='weight'), 4)
        except:
            stats['Avg_Clustering'] = 'N/A'
        
        # Modularity
        stats['Modularity'] = G.graph.get('modularity', 'N/A')
        if isinstance(stats['Modularity'], float):
            stats['Modularity'] = round(stats['Modularity'], 4)
        
        # Giant component percentage
        try:
            giant = max(nx.connected_components(G), key=len)
            stats['Giant_Component_%'] = round(100 * len(giant) / G.number_of_nodes(), 1)
        except:
            stats['Giant_Component_%'] = 'N/A'
        
        # Average degree
        stats['Avg_Degree'] = round(2 * G.number_of_edges() / G.number_of_nodes(), 2)
        
        stats_rows.append(stats)
        
        print(f"\n  {name}:")
        for k, v in stats.items():
            if k != 'Network':
                print(f"    {k}: {v}")
    
    stats_df = pd.DataFrame(stats_rows)
    
    if not stats_df.empty:
        output_path = os.path.join(output_dir, 'network_statistics.csv')
        stats_df.to_csv(output_path, index=False)
        print(f"\n  ✓ Statistics exported to: {output_path}")
    
    return stats_df


# =============================================================================
# OUTPUT MODULE
# =============================================================================

def print_formatted_table(df: pd.DataFrame, title: str, max_col_width: int = 45):
    """Print a nicely formatted table for console output."""
    print(f"\n{title}")
    print("-" * len(title))
    
    df_display = df.copy()
    for col in df_display.columns:
        if df_display[col].dtype == 'object':
            df_display[col] = df_display[col].astype(str).str[:max_col_width]
    
    print(df_display.to_string(index=False))
    print()


def print_summary_statistics(df: pd.DataFrame):
    """Print overall summary statistics."""
    print("\n" + "=" * 70)
    print("SUMMARY STATISTICS")
    print("=" * 70)
    
    total = len(df)
    
    years = df[df['PY'].notna()]['PY'].astype(str).str[:4]
    years = pd.to_numeric(years, errors='coerce').dropna()
    
    citations = pd.to_numeric(df['TC'], errors='coerce').fillna(0)
    
    year_range = f"{int(years.min())} - {int(years.max())}" if len(years) > 0 else "N/A"
    total_citations = int(citations.sum())
    avg_citations = round(citations.mean(), 2) if len(citations) > 0 else 0
    
    unique_sources = df['SO'].nunique() if 'SO' in df.columns else 0
    
    all_authors = set()
    for au in df['AU'].dropna():
        all_authors.update(parse_authors(au))
    unique_authors = len(all_authors)
    
    print(f"""
┌─────────────────────────────────────────────────────────────────────┐
│                    BIBLIOMETRIC SUMMARY                             │
├─────────────────────────────────────────────────────────────────────┤
│  Total Documents:           {total:<10}                             │
│  Time Span:                 {year_range:<20}                        │
│  Sources (Journals):        {unique_sources:<10}                             │
│  Unique Authors:            {unique_authors:<10}                             │
│  Total Citations:           {total_citations:<10}                             │
│  Average Citations/Doc:     {avg_citations:<10}                             │
└─────────────────────────────────────────────────────────────────────┘
""")


def export_network_to_gexf(G: nx.Graph, filepath: str, network_type: str):
    """Export network to GEXF format for Gephi."""
    try:
        nx.write_gexf(G, filepath)
        print(f"  ✓ {network_type} network exported to: {filepath}")
    except Exception as e:
        print(f"  ✗ Failed to export {network_type}: {str(e)}")


# =============================================================================
# MAIN FUNCTION
# =============================================================================

def main():
    """Main function to run advanced bibliometric analysis."""
    parser = argparse.ArgumentParser(description='Advanced Bibliometric Analysis for Web of Science Data')
    parser.add_argument('--data-dir', type=str, default=DEFAULT_DATA_DIR,
                        help='Directory containing WoS .txt files')
    parser.add_argument('--output-dir', type=str, default=DEFAULT_OUTPUT_DIR,
                        help='Directory for output files')
    parser.add_argument('--top-keywords', type=int, default=TOP_N_KEYWORDS,
                        help='Number of top keywords for network')
    parser.add_argument('--backbone-alpha', type=float, default=BACKBONE_ALPHA,
                        help='Significance level for backbone filter')
    
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("\n" + "=" * 70)
    print("   ADVANCED BIBLIOMETRIC ANALYSIS - DIGITAL ENTREPRENEURSHIP")
    print("=" * 70)
    
    # 1. Load data
    df = load_wos_data(args.data_dir)
    
    # 2. Preprocess
    df = preprocess_data(df)
    
    # 3. Summary Statistics
    print_summary_statistics(df)
    
    # 4. Quantitative Analyses
    print("\n" + "=" * 70)
    print("QUANTITATIVE ANALYSES")
    print("=" * 70)
    
    annual_df = analyze_annual_production(df)
    print_formatted_table(annual_df, "ANNUAL SCIENTIFIC PRODUCTION")
    
    sources_df = analyze_top_sources(df)
    print_formatted_table(sources_df, f"TOP {TOP_N_SOURCES} MOST PRODUCTIVE SOURCES")
    
    authors_df = analyze_top_cited_authors(df)
    print_formatted_table(authors_df, f"TOP {TOP_N_AUTHORS} MOST CITED AUTHORS")
    
    countries_df, collab_df = analyze_country_collaboration(df)
    print_formatted_table(countries_df, "COUNTRY SCIENTIFIC PRODUCTION (Top 20)")
    print_formatted_table(collab_df, "TOP 10 COUNTRY COLLABORATIONS")
    
    # 5. Network Analyses
    print("\n" + "=" * 70)
    print("NETWORK ANALYSES")
    print("=" * 70)
    
    # 5.1 Keywords Network (enriched)
    keyword_network = build_keyword_cooccurrence_network(df, args.top_keywords)
    keyword_network = enrich_network_attributes(keyword_network)
    keyword_gexf = os.path.join(args.output_dir, 'keywords_cooccurrence_enriched.gexf')
    export_network_to_gexf(keyword_network, keyword_gexf, "Keywords Co-occurrence (Enriched)")
    
    # 5.2 Normalized Bibliographic Coupling
    coupling_network = build_normalized_coupling_network(df)
    coupling_backbone = apply_disparity_filter(coupling_network, args.backbone_alpha)
    coupling_giant = extract_giant_component(coupling_backbone)
    coupling_giant = enrich_network_attributes(coupling_giant)
    coupling_gexf = os.path.join(args.output_dir, 'bibliographic_coupling_normalized.gexf')
    export_network_to_gexf(coupling_giant, coupling_gexf, "Bibliographic Coupling (Normalized)")
    
    # 6. Temporal Evolution (Sankey)
    sankey_df = analyze_temporal_evolution(df, args.output_dir)
    
    # 7. Core Authors by Cluster
    core_authors_df = identify_core_authors(df, keyword_network, args.output_dir)
    
    # 8. Burst Detection
    burst_df = detect_keyword_bursts(df, args.output_dir)
    
    # 9. Network Statistics
    networks = {
        'Keywords_Cooccurrence': keyword_network,
        'Bibliographic_Coupling_Raw': coupling_network,
        'Bibliographic_Coupling_Backbone': coupling_giant
    }
    stats_df = calculate_network_statistics(networks, args.output_dir)
    
    # Final message
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print(f"\nOutput files saved to: {os.path.abspath(args.output_dir)}")
    print("\n  Network files (.gexf):")
    print("    - keywords_cooccurrence_enriched.gexf")
    print("    - bibliographic_coupling_normalized.gexf")
    print("\n  Analysis files (.csv):")
    print("    - temporal_evolution_sankey.csv")
    print("    - core_authors_by_cluster.csv")
    print("    - keyword_bursts.csv")
    print("    - network_statistics.csv")
    print("\nOpen .gexf files in Gephi for network visualization.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
