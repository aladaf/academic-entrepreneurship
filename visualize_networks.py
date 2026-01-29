#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Network Visualization Script
=============================

Creates high-quality interactive and static visualizations for bibliometric networks.
Generates:
- Interactive HTML visualizations (pyvis)
- High-resolution PNG images (matplotlib)

Author: Bibliometric Visualization Tool
Date: 2026-01-25
"""

import os
import sys
import math
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib backend BEFORE importing pyplot (for headless environments)
import matplotlib
matplotlib.use('Agg')

try:
    import networkx as nx
except ImportError:
    print("Error: networkx not installed. Run: pip install networkx")
    sys.exit(1)

try:
    from pyvis.network import Network
except ImportError:
    print("Error: pyvis not installed. Run: pip install pyvis")
    sys.exit(1)

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
except ImportError:
    print("Error: matplotlib not installed. Run: pip install matplotlib")
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print("Error: numpy not installed. Run: pip install numpy")
    sys.exit(1)


# =============================================================================
# CONFIGURATION
# =============================================================================

OUTPUT_DIR = "./output/visualizations"

# Color palettes for clusters (professional, publication-ready)
CLUSTER_COLORS = [
    '#E63946',  # Red
    '#457B9D',  # Steel Blue
    '#2A9D8F',  # Teal
    '#E9C46A',  # Gold
    '#F4A261',  # Orange
    '#9B5DE5',  # Purple
    '#00BBF9',  # Cyan
    '#00F5D4',  # Mint
    '#FEE440',  # Yellow
    '#F15BB5',  # Pink
]

BG_DARK = '#1a1a2e'
BG_LIGHT = '#ffffff'


# =============================================================================
# NETWORK LOADING
# =============================================================================

def load_network(filepath: str) -> nx.Graph:
    """Load network from GEXF file."""
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return None
    
    try:
        G = nx.read_gexf(filepath)
        print(f"  ✓ Loaded: {filepath}")
        print(f"    Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
        return G
    except Exception as e:
        print(f"  ✗ Failed to load: {e}")
        return None


# =============================================================================
# INTERACTIVE VISUALIZATION (PYVIS)
# =============================================================================

def create_interactive_visualization(G: nx.Graph, output_path: str, title: str,
                                     node_size_attr: str = 'frequency',
                                     color_attr: str = 'modularity_class',
                                     dark_mode: bool = True):
    """Create interactive HTML visualization using pyvis."""
    if G is None or G.number_of_nodes() == 0:
        print(f"  ✗ Empty network, skipping {title}")
        return
    
    print(f"\n  Creating interactive visualization: {title}")
    
    net = Network(
        height="800px",
        width="100%",
        bgcolor=BG_DARK if dark_mode else BG_LIGHT,
        font_color='white' if dark_mode else 'black',
        directed=False,
        notebook=False
    )
    
    net.set_options("""
    {
        "physics": {
            "forceAtlas2Based": {
                "gravitationalConstant": -100,
                "centralGravity": 0.01,
                "springLength": 200,
                "springConstant": 0.08,
                "damping": 0.4,
                "avoidOverlap": 0.8
            },
            "solver": "forceAtlas2Based",
            "stabilization": {
                "enabled": true,
                "iterations": 500
            }
        },
        "nodes": {
            "font": {
                "size": 14,
                "face": "arial",
                "strokeWidth": 2,
                "strokeColor": "#000000"
            },
            "borderWidth": 2,
            "borderWidthSelected": 4
        },
        "edges": {
            "color": {
                "inherit": false,
                "color": "#555555",
                "opacity": 0.6
            },
            "smooth": {
                "enabled": true,
                "type": "continuous"
            }
        },
        "interaction": {
            "hover": true,
            "tooltipDelay": 100,
            "hideEdgesOnDrag": true
        }
    }
    """)
    
    # Get node attributes
    sizes = {}
    colors = {}
    
    for node in G.nodes():
        node_data = G.nodes[node]
        
        if node_size_attr in node_data:
            try:
                sizes[node] = float(node_data[node_size_attr])
            except:
                sizes[node] = 10
        else:
            sizes[node] = 10
        
        if color_attr in node_data:
            try:
                cluster = int(node_data[color_attr])
                colors[node] = CLUSTER_COLORS[cluster % len(CLUSTER_COLORS)]
            except:
                colors[node] = CLUSTER_COLORS[0]
        else:
            colors[node] = CLUSTER_COLORS[0]
    
    # Normalize sizes
    if sizes:
        max_size = max(sizes.values())
        min_size = min(sizes.values())
        size_range = max_size - min_size if max_size > min_size else 1
        
        for node in sizes:
            sizes[node] = 15 + 45 * (sizes[node] - min_size) / size_range
    
    # Add nodes
    for node in G.nodes():
        node_data = G.nodes[node]
        label = node_data.get('label', str(node))
        
        tooltip_parts = [f"<b>{label}</b>"]
        for attr in ['frequency', 'papers', 'citations', 'degree', 'betweenness']:
            if attr in node_data:
                tooltip_parts.append(f"{attr}: {node_data[attr]}")
        tooltip = "<br>".join(tooltip_parts)
        
        net.add_node(
            str(node),
            label=label[:25] if len(label) > 25 else label,
            title=tooltip,
            size=sizes.get(node, 20),
            color=colors.get(node, CLUSTER_COLORS[0]),
            font={'size': 12, 'color': 'white' if dark_mode else 'black'}
        )
    
    # Add edges
    for u, v, data in G.edges(data=True):
        weight = data.get('weight', 1)
        width = min(5, max(0.5, weight * 2))
        
        net.add_edge(
            str(u), 
            str(v), 
            width=width,
            title=f"Weight: {weight:.3f}" if isinstance(weight, float) else f"Weight: {weight}"
        )
    
    net.save_graph(output_path)
    print(f"    ✓ Saved: {output_path}")


# =============================================================================
# STATIC VISUALIZATION (MATPLOTLIB)
# =============================================================================

def create_static_visualization(G: nx.Graph, output_path: str, title: str,
                                node_size_attr: str = 'frequency',
                                color_attr: str = 'modularity_class',
                                figsize: tuple = (16, 12),
                                dpi: int = 300):
    """Create high-resolution static PNG visualization."""
    if G is None or G.number_of_nodes() == 0:
        print(f"  ✗ Empty network, skipping {title}")
        return
    
    print(f"\n  Creating static visualization: {title}")
    
    fig, ax = plt.subplots(1, 1, figsize=figsize, facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    # Layout
    if G.number_of_nodes() < 100:
        pos = nx.spring_layout(G, k=2/math.sqrt(G.number_of_nodes()), iterations=100, seed=42)
    else:
        pos = nx.kamada_kawai_layout(G)
    
    # Get node colors and sizes
    node_colors = []
    node_sizes = []
    
    for node in G.nodes():
        node_data = G.nodes[node]
        
        if color_attr in node_data:
            try:
                cluster = int(node_data[color_attr])
                node_colors.append(CLUSTER_COLORS[cluster % len(CLUSTER_COLORS)])
            except:
                node_colors.append(CLUSTER_COLORS[0])
        else:
            node_colors.append(CLUSTER_COLORS[0])
        
        if node_size_attr in node_data:
            try:
                size = float(node_data[node_size_attr])
                node_sizes.append(size)
            except:
                node_sizes.append(10)
        else:
            node_sizes.append(10)
    
    # Normalize sizes
    if node_sizes:
        max_size = max(node_sizes)
        min_size = min(node_sizes)
        size_range = max_size - min_size if max_size > min_size else 1
        node_sizes = [300 + 2000 * (s - min_size) / size_range for s in node_sizes]
    
    # Get edge weights
    edge_weights = [G[u][v].get('weight', 0.5) for u, v in G.edges()]
    if edge_weights:
        max_weight = max(edge_weights)
        min_weight = min(edge_weights)
        weight_range = max_weight - min_weight if max_weight > min_weight else 1
        edge_widths = [0.3 + 2.5 * (w - min_weight) / weight_range for w in edge_weights]
    else:
        edge_widths = [1] * len(G.edges())
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='#555555', alpha=0.4, width=edge_widths)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=node_sizes,
                          alpha=0.9, edgecolors='white', linewidths=1.5)
    
    # Draw labels
    labels = {node: G.nodes[node].get('label', node)[:20] for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=8, font_color='white', font_weight='bold')
    
    ax.set_title(title, fontsize=18, fontweight='bold', color='white', pad=20)
    
    # Legend
    unique_clusters = set()
    for node in G.nodes():
        if color_attr in G.nodes[node]:
            try:
                unique_clusters.add(int(G.nodes[node][color_attr]))
            except:
                pass
    
    if unique_clusters:
        legend_patches = []
        for cluster in sorted(unique_clusters):
            color = CLUSTER_COLORS[cluster % len(CLUSTER_COLORS)]
            legend_patches.append(mpatches.Patch(color=color, label=f'Cluster {cluster}'))
        
        ax.legend(handles=legend_patches, loc='upper left', 
                 facecolor='#2a2a4e', edgecolor='white',
                 labelcolor='white', fontsize=10)
    
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, facecolor='#1a1a2e', edgecolor='none', bbox_inches='tight')
    plt.close()
    
    print(f"    ✓ Saved: {output_path} ({dpi} DPI)")


def create_keyword_bubble_chart(G: nx.Graph, output_path: str, title: str = "Keyword Co-occurrence"):
    """Create a bubble chart visualization for keywords."""
    if G is None or G.number_of_nodes() == 0:
        return
    
    print(f"\n  Creating bubble chart: {title}")
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    nodes = list(G.nodes())
    frequencies = [G.nodes[n].get('frequency', 1) for n in nodes]
    clusters = [int(G.nodes[n].get('modularity_class', 0)) for n in nodes]
    labels = [G.nodes[n].get('label', n) for n in nodes]
    
    max_freq = max(frequencies)
    sizes = [1000 + 4000 * (f / max_freq) for f in frequencies]
    colors = [CLUSTER_COLORS[c % len(CLUSTER_COLORS)] for c in clusters]
    
    sorted_indices = sorted(range(len(frequencies)), key=lambda i: frequencies[i], reverse=True)
    
    n = len(nodes)
    cols = int(math.sqrt(n)) + 1
    positions = []
    for i, idx in enumerate(sorted_indices):
        x = (i % cols) * 2
        y = (i // cols) * 2
        x += (clusters[idx] % 3 - 1) * 0.3
        y += (clusters[idx] % 3 - 1) * 0.3
        positions.append((x, y))
    
    for i, idx in enumerate(sorted_indices):
        circle = plt.Circle(
            positions[i], 
            math.sqrt(sizes[idx]) / 100,
            color=colors[idx],
            alpha=0.7,
            ec='white',
            linewidth=1
        )
        ax.add_patch(circle)
        
        if i < 30:
            ax.annotate(
                labels[idx][:18],
                positions[i],
                ha='center', va='center',
                fontsize=7 + 3 * (frequencies[idx] / max_freq),
                fontweight='bold',
                color='white'
            )
    
    ax.set_xlim(-2, cols * 2 + 1)
    ax.set_ylim(-2, (n // cols + 2) * 2)
    ax.set_aspect('equal')
    ax.axis('off')
    
    ax.set_title(title, fontsize=18, fontweight='bold', color='white', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor='#1a1a2e', bbox_inches='tight')
    plt.close()
    
    print(f"    ✓ Saved: {output_path}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Generate all visualizations."""
    print("\n" + "=" * 70)
    print("   BIBLIOMETRIC NETWORK VISUALIZATION")
    print("=" * 70)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("\n  Loading networks...")
    
    keywords_network = load_network("./output/keywords_cooccurrence_enriched.gexf")
    coupling_network = load_network("./output/bibliographic_coupling_normalized.gexf")
    
    if keywords_network:
        create_interactive_visualization(
            keywords_network,
            os.path.join(OUTPUT_DIR, "keywords_interactive.html"),
            "Keyword Co-occurrence Network",
            node_size_attr='frequency',
            color_attr='modularity_class'
        )
        
        create_static_visualization(
            keywords_network,
            os.path.join(OUTPUT_DIR, "keywords_network.png"),
            "Keyword Co-occurrence Network",
            node_size_attr='frequency',
            color_attr='modularity_class'
        )
        
        create_keyword_bubble_chart(
            keywords_network,
            os.path.join(OUTPUT_DIR, "keywords_bubble.png"),
            "Keywords by Frequency and Cluster"
        )
    
    if coupling_network:
        create_interactive_visualization(
            coupling_network,
            os.path.join(OUTPUT_DIR, "coupling_interactive.html"),
            "Bibliographic Coupling Network (Normalized)",
            node_size_attr='papers',
            color_attr='modularity_class'
        )
        
        create_static_visualization(
            coupling_network,
            os.path.join(OUTPUT_DIR, "coupling_network.png"),
            "Bibliographic Coupling Network (Normalized Backbone)",
            node_size_attr='papers',
            color_attr='modularity_class'
        )
    
    print("\n" + "=" * 70)
    print("VISUALIZATION COMPLETE")
    print("=" * 70)
    print(f"\nFiles saved to: {os.path.abspath(OUTPUT_DIR)}")
    print("\n  Interactive (HTML - open in browser):")
    print("    - keywords_interactive.html")
    print("    - coupling_interactive.html")
    print("\n  Static (PNG - publication ready, 300 DPI):")
    print("    - keywords_network.png")
    print("    - keywords_bubble.png")
    print("    - coupling_network.png")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
