#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LDA Confirmatory Analysis for Academic Entrepreneurship
=========================================================

Implements Latent Dirichlet Allocation as methodological counterproof
to BERTopic semantic analysis. Tests whether a probabilistic frequency-based
model can isolate the "Digital" signal that BERTopic identified as a 2% frontier.

Features:
- Preprocessing with spaCy lemmatization
- LDA with k=5 and k=10 topics
- pyLDAvis interactive visualization
- Coherence score (Cv) calculation
- BERTopic cross-comparison

Author: Generated for bibliometric analysis
Date: 2026-01-30
"""

import os
import sys
import warnings
from collections import Counter

warnings.filterwarnings('ignore')

# =============================================================================
# IMPORTS
# =============================================================================

try:
    import pandas as pd
except ImportError:
    print("Error: pandas not installed. Run: pip install pandas")
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print("Error: numpy not installed. Run: pip install numpy")
    sys.exit(1)

try:
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
except ImportError:
    print("Error: scikit-learn not installed. Run: pip install scikit-learn")
    sys.exit(1)

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    print("Warning: spaCy not available. Using basic tokenization.")
    SPACY_AVAILABLE = False

try:
    import pyLDAvis
    import pyLDAvis.lda_model
    PYLDAVIS_AVAILABLE = True
except ImportError:
    print("Warning: pyLDAvis not available. Interactive visualizations will be skipped.")
    PYLDAVIS_AVAILABLE = False

try:
    from gensim.models import CoherenceModel
    from gensim.corpora import Dictionary
    GENSIM_AVAILABLE = True
except ImportError:
    print("Warning: gensim not available. Coherence scores will be skipped.")
    GENSIM_AVAILABLE = False

import re

# =============================================================================
# CONFIGURATION
# =============================================================================

DATA_DIR = "./"
OUTPUT_DIR = "./output"
RANDOM_STATE = 42

# Domain-specific stopwords to remove
DOMAIN_STOPWORDS = {
    'study', 'research', 'paper', 'article', 'result', 'results', 'finding',
    'findings', 'analysis', 'data', 'method', 'methodology', 'approach',
    'literature', 'review', 'purpose', 'aim', 'objective', 'conclusion',
    'implication', 'implications', 'however', 'therefore', 'thus', 'also',
    'using', 'based', 'show', 'shows', 'shown', 'indicate', 'indicates',
    'suggest', 'suggests', 'examine', 'examines', 'explore', 'explores',
    'investigate', 'investigates', 'propose', 'proposes', 'develop',
    'develops', 'provide', 'provides', 'present', 'presents', 'focus',
    'focuses', 'discuss', 'discusses', 'highlight', 'highlights',
    'context', 'contribute', 'contribution', 'contributions', 'framework',
    'model', 'theory', 'theories', 'theoretical', 'empirical', 'qualitative',
    'quantitative', 'case', 'sample', 'survey', 'interview', 'interviews'
}


# =============================================================================
# DATA LOADING
# =============================================================================

def load_wos_data(data_dir: str) -> pd.DataFrame:
    """Load consolidated WoS + Scopus data using bibliometric_analysis module."""
    print("\n" + "=" * 70)
    print("DATA LOADING (WoS + Scopus Consolidated)")
    print("=" * 70)
    
    # Import the combined loader from bibliometric_analysis
    try:
        from bibliometric_analysis import load_combined_data
        df = load_combined_data(data_dir)
        return df
    except ImportError:
        print("  Warning: Could not import load_combined_data, falling back to WoS only")
    
    # Fallback to WoS-only loading
    txt_files = [f for f in os.listdir(data_dir) if f.endswith('.txt') and f.startswith('data-')]
    
    if not txt_files:
        print(f"Error: No data .txt files found in {data_dir}")
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


def preprocess_data(df: pd.DataFrame, exclude_year: int = 2026) -> pd.DataFrame:
    """Preprocess: remove duplicates and filter by year."""
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
    
    # Filter out records from excluded year
    if 'PY' in df.columns and exclude_year is not None:
        df['_year_num'] = pd.to_numeric(df['PY'], errors='coerce')
        excluded_records = len(df[df['_year_num'] == exclude_year])
        df = df[df['_year_num'] != exclude_year]
        df = df.drop(columns=['_year_num'])
        print(f"Initial records: {initial_count}")
        print(f"Duplicates removed: {duplicates}")
        print(f"Records from {exclude_year} excluded: {excluded_records}")
        print(f"Final unique records: {len(df)}")
    
    return df


# =============================================================================
# TEXT PREPROCESSING
# =============================================================================

def load_spacy_model():
    """Load spaCy model for lemmatization."""
    if not SPACY_AVAILABLE:
        return None
    
    try:
        nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        print("  ✓ spaCy model loaded (en_core_web_sm)")
        return nlp
    except OSError:
        print("  Downloading spaCy model...")
        os.system("python -m spacy download en_core_web_sm")
        try:
            nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
            print("  ✓ spaCy model loaded (en_core_web_sm)")
            return nlp
        except:
            print("  ✗ Failed to load spaCy model")
            return None


def clean_text(text: str) -> str:
    """Basic text cleaning."""
    if pd.isna(text) or not text:
        return ""
    
    text = str(text).lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text


def lemmatize_text(text: str, nlp) -> str:
    """Lemmatize text using spaCy."""
    if nlp is None or not text:
        return text
    
    doc = nlp(text)
    lemmas = []
    
    for token in doc:
        # Keep only alphabetic tokens, not stopwords, length > 2
        if (token.is_alpha and 
            not token.is_stop and 
            len(token.lemma_) > 2 and
            token.lemma_.lower() not in DOMAIN_STOPWORDS):
            lemmas.append(token.lemma_.lower())
    
    return ' '.join(lemmas)


def preprocess_abstracts(df: pd.DataFrame) -> tuple:
    """Extract and preprocess abstracts."""
    print("\n" + "=" * 70)
    print("TEXT PREPROCESSING")
    print("=" * 70)
    
    nlp = load_spacy_model()
    
    abstracts = []
    doc_indices = []
    doc_titles = []
    
    print("  Processing abstracts...")
    
    for idx, row in df.iterrows():
        abstract = row.get('AB', '')
        if pd.notna(abstract) and len(str(abstract).strip()) > 100:
            cleaned = clean_text(abstract)
            if nlp is not None:
                processed = lemmatize_text(cleaned, nlp)
            else:
                # Basic tokenization fallback
                words = cleaned.split()
                processed = ' '.join(w for w in words if len(w) > 2 and w not in DOMAIN_STOPWORDS)
            
            if len(processed.split()) > 10:  # Minimum 10 words after processing
                abstracts.append(processed)
                doc_indices.append(idx)
                doc_titles.append(str(row.get('TI', ''))[:100])
    
    print(f"  Abstracts processed: {len(abstracts)} (of {len(df)} total records)")
    
    return abstracts, doc_indices, doc_titles


# =============================================================================
# LDA MODELING
# =============================================================================

def create_vectorizer():
    """Create CountVectorizer with specified parameters."""
    vectorizer = CountVectorizer(
        max_df=0.95,  # Ignore terms in >95% of docs
        min_df=5,     # Ignore terms in <5 docs
        stop_words='english',
        ngram_range=(1, 1),  # Unigrams only
        max_features=5000
    )
    return vectorizer


def train_lda_model(dtm, n_topics: int, random_state: int = RANDOM_STATE):
    """Train LDA model with specified number of topics."""
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        max_iter=30,
        learning_method='online',
        learning_offset=50.0,
        random_state=random_state,
        n_jobs=-1
    )
    lda.fit(dtm)
    return lda


def get_top_words(lda_model, vectorizer, n_words: int = 15) -> list:
    """Extract top words for each topic."""
    feature_names = vectorizer.get_feature_names_out()
    topics = []
    
    for topic_idx, topic in enumerate(lda_model.components_):
        top_indices = topic.argsort()[:-n_words - 1:-1]
        top_words = [feature_names[i] for i in top_indices]
        top_weights = [topic[i] for i in top_indices]
        topics.append({
            'Topic_ID': topic_idx,
            'Top_Words': ', '.join(top_words),
            'Words_List': top_words,
            'Weights': top_weights
        })
    
    return topics


def calculate_coherence_cv(lda_model, vectorizer, texts: list) -> float:
    """Calculate Cv coherence score using gensim."""
    if not GENSIM_AVAILABLE:
        return None
    
    try:
        # Get topic words
        feature_names = vectorizer.get_feature_names_out()
        topics_words = []
        for topic in lda_model.components_:
            top_indices = topic.argsort()[:-11:-1]  # Top 10 words
            topics_words.append([feature_names[i] for i in top_indices])
        
        # Tokenize texts for gensim
        tokenized_texts = [text.split() for text in texts]
        
        # Create dictionary and corpus
        dictionary = Dictionary(tokenized_texts)
        
        # Calculate coherence
        coherence_model = CoherenceModel(
            topics=topics_words,
            texts=tokenized_texts,
            dictionary=dictionary,
            coherence='c_v'
        )
        
        return coherence_model.get_coherence()
    except Exception as e:
        print(f"  Warning: Could not calculate coherence: {e}")
        return None


def generate_pyldavis(lda_model, dtm, vectorizer, output_path: str):
    """Generate pyLDAvis visualization."""
    if not PYLDAVIS_AVAILABLE:
        print(f"  ✗ pyLDAvis not available, skipping: {output_path}")
        return
    
    try:
        # Prepare visualization data
        vis_data = pyLDAvis.lda_model.prepare(
            lda_model, dtm, vectorizer, mds='mmds'
        )
        
        # Save to HTML
        pyLDAvis.save_html(vis_data, output_path)
        print(f"  ✓ pyLDAvis saved to: {output_path}")
    except Exception as e:
        print(f"  ✗ Failed to generate pyLDAvis: {e}")


# =============================================================================
# BERTOPIC COMPARISON
# =============================================================================

def load_bertopic_results(output_dir: str) -> pd.DataFrame:
    """Load BERTopic results for comparison."""
    semantic_path = os.path.join(output_dir, 'semantic_topics.csv')
    
    if not os.path.exists(semantic_path):
        print("  Warning: BERTopic results not found (semantic_topics.csv)")
        return None
    
    return pd.read_csv(semantic_path)


def identify_digital_documents(df: pd.DataFrame) -> set:
    """
    Identify documents likely related to 'Digital' theme based on keywords.
    Used to approximate BERTopic Topic 0 membership.
    """
    digital_keywords = {
        'digital', 'technology', 'technologies', 'platform', 'platforms',
        'online', 'internet', 'software', 'app', 'apps', 'artificial',
        'intelligence', 'machine', 'learning', 'blockchain', 'fintech',
        'iot', 'cloud', 'virtual', 'cyber', 'data', 'analytics',
        'automation', 'robotics', 'ai', 'ml'
    }
    
    digital_docs = set()
    
    for idx, row in df.iterrows():
        abstract = str(row.get('AB', '')).lower()
        title = str(row.get('TI', '')).lower()
        keywords = str(row.get('DE', '')).lower() + ' ' + str(row.get('ID', '')).lower()
        
        combined_text = f"{title} {abstract} {keywords}"
        
        # Count digital keyword matches
        matches = sum(1 for kw in digital_keywords if kw in combined_text)
        
        if matches >= 3:  # At least 3 digital keywords
            digital_docs.add(idx)
    
    return digital_docs


def compare_with_bertopic(df: pd.DataFrame, doc_indices: list, 
                          doc_topics: np.ndarray, output_dir: str) -> pd.DataFrame:
    """Compare LDA topic assignments with BERTopic Digital cluster."""
    print("\n" + "=" * 70)
    print("BERTOPIC COMPARISON")
    print("=" * 70)
    
    # Identify digital-themed documents
    digital_docs = identify_digital_documents(df)
    print(f"  Documents with Digital theme signals: {len(digital_docs)}")
    
    # Count how many digital docs fall into each LDA topic
    topic_digital_counts = Counter()
    topic_total_counts = Counter()
    
    for i, doc_idx in enumerate(doc_indices):
        dominant_topic = doc_topics[i].argmax()
        topic_total_counts[dominant_topic] += 1
        
        if doc_idx in digital_docs:
            topic_digital_counts[dominant_topic] += 1
    
    # Build comparison results
    comparison_rows = []
    n_topics = doc_topics.shape[1]
    
    for topic_id in range(n_topics):
        total = topic_total_counts.get(topic_id, 0)
        digital = topic_digital_counts.get(topic_id, 0)
        pct_digital = (digital / total * 100) if total > 0 else 0
        
        comparison_rows.append({
            'LDA_Topic': topic_id,
            'Total_Docs': total,
            'Digital_Docs': digital,
            'Digital_Percentage': round(pct_digital, 1),
            'Concentration': 'HIGH' if pct_digital > 15 else ('MEDIUM' if pct_digital > 8 else 'LOW')
        })
    
    comparison_df = pd.DataFrame(comparison_rows)
    comparison_df = comparison_df.sort_values('Digital_Percentage', ascending=False)
    
    # Print analysis
    print(f"\n  Digital Document Distribution Across LDA Topics:")
    for _, row in comparison_df.iterrows():
        if row['Total_Docs'] > 0:
            bar = "█" * int(row['Digital_Percentage'] / 2)
            print(f"    Topic {row['LDA_Topic']}: {row['Digital_Percentage']:5.1f}% ({row['Digital_Docs']}/{row['Total_Docs']}) {bar}")
    
    # Assess if LDA isolated Digital - check if concentration is in ONE topic
    # Count topics with significant Digital concentration (>10%)
    significant_topics = comparison_df[comparison_df['Digital_Percentage'] > 10]
    n_significant = len(significant_topics)
    max_concentration = comparison_df['Digital_Percentage'].max()
    
    # Calculate entropy-like dispersion: if Digital is spread evenly = HIGH dispersion = FAILED isolation
    digital_by_topic = comparison_df[comparison_df['Digital_Docs'] > 0]['Digital_Docs'].tolist()
    total_digital_assigned = sum(digital_by_topic)
    
    if total_digital_assigned > 0 and len(digital_by_topic) > 1:
        # Herfindahl index: closer to 1 = concentrated, closer to 0 = dispersed
        shares = [d / total_digital_assigned for d in digital_by_topic]
        hhi = sum(s**2 for s in shares)
    else:
        hhi = 1.0  # Only one topic = fully concentrated
    
    print(f"\n  Dispersion Analysis:")
    print(f"    Topics with Digital signal (>10%): {n_significant}")
    print(f"    Herfindahl Index: {hhi:.3f} (1.0=concentrated, 0.1=dispersed)")
    
    if hhi < 0.5 or n_significant > 2:
        conclusion = "LDA FAILED to isolate Digital theme (DISPERSED across multiple topics)"
        conclusion_detail = "Digital signal mixed into broader clusters - supports WEAK SIGNAL thesis"
    elif hhi < 0.7:
        conclusion = "LDA PARTIALLY isolated Digital theme"
        conclusion_detail = "Some concentration but not clear separation"
    else:
        conclusion = "LDA ISOLATED Digital theme (concentrated in one topic)"
        conclusion_detail = "Digital documents clustered together"
    
    print(f"\n  Conclusion: {conclusion}")
    print(f"  Interpretation: {conclusion_detail}")
    
    return comparison_df


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_lda_analysis():
    """Run complete LDA analysis."""
    print("\n" + "=" * 70)
    print("   LDA CONFIRMATORY ANALYSIS - ACADEMIC ENTREPRENEURSHIP")
    print("=" * 70)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Load and preprocess data
    df = load_wos_data(DATA_DIR)
    df = preprocess_data(df)
    
    # 2. Preprocess abstracts
    abstracts, doc_indices, doc_titles = preprocess_abstracts(df)
    
    if len(abstracts) < 50:
        print("Error: Insufficient abstracts for LDA analysis")
        sys.exit(1)
    
    # 3. Vectorize
    print("\n" + "=" * 70)
    print("VECTORIZATION")
    print("=" * 70)
    
    vectorizer = create_vectorizer()
    dtm = vectorizer.fit_transform(abstracts)
    
    print(f"  Document-Term Matrix: {dtm.shape[0]} docs × {dtm.shape[1]} terms")
    
    # 4. Train LDA models
    print("\n" + "=" * 70)
    print("LDA MODELING")
    print("=" * 70)
    
    results = {}
    coherence_scores = []
    
    for k in [5, 10]:
        print(f"\n  Training LDA with k={k} topics...")
        lda_model = train_lda_model(dtm, k)
        
        # Get topic words
        topics = get_top_words(lda_model, vectorizer, n_words=15)
        
        # Calculate coherence
        coherence = calculate_coherence_cv(lda_model, vectorizer, abstracts)
        coherence_str = f"{coherence:.4f}" if coherence else "N/A"
        print(f"    Coherence (Cv): {coherence_str}")
        
        coherence_scores.append({
            'K_Topics': k,
            'Coherence_Cv': coherence
        })
        
        # Get document-topic distributions
        doc_topics = lda_model.transform(dtm)
        
        # Store results
        results[k] = {
            'model': lda_model,
            'topics': topics,
            'doc_topics': doc_topics,
            'coherence': coherence
        }
        
        # Export topic words table
        topics_df = pd.DataFrame([{
            'Topic_ID': t['Topic_ID'],
            'Top_15_Words': t['Top_Words']
        } for t in topics])
        
        topics_path = os.path.join(OUTPUT_DIR, f'lda_topics_k{k}.csv')
        topics_df.to_csv(topics_path, index=False)
        print(f"    ✓ Topics exported to: {topics_path}")
        
        # Print topics
        print(f"\n    Topic Summary (k={k}):")
        for t in topics:
            print(f"      Topic {t['Topic_ID']}: {t['Top_Words'][:70]}...")
        
        # Generate pyLDAvis
        pyldavis_path = os.path.join(OUTPUT_DIR, f'lda_pyldavis_k{k}.html')
        generate_pyldavis(lda_model, dtm, vectorizer, pyldavis_path)
    
    # 5. Export coherence scores
    coherence_df = pd.DataFrame(coherence_scores)
    coherence_path = os.path.join(OUTPUT_DIR, 'lda_coherence_scores.csv')
    coherence_df.to_csv(coherence_path, index=False)
    print(f"\n  ✓ Coherence scores exported to: {coherence_path}")
    
    # 6. Export document-topic mapping (using k=10)
    print("\n" + "=" * 70)
    print("DOCUMENT-TOPIC MAPPING")
    print("=" * 70)
    
    doc_topics_k10 = results[10]['doc_topics']
    
    doc_mapping = []
    for i, doc_idx in enumerate(doc_indices):
        probs = doc_topics_k10[i]
        dominant_topic = probs.argmax()
        
        doc_mapping.append({
            'Doc_Index': doc_idx,
            'Title': doc_titles[i],
            'Dominant_Topic': dominant_topic,
            'Dominant_Prob': round(probs[dominant_topic], 4),
            **{f'Topic_{j}_Prob': round(p, 4) for j, p in enumerate(probs)}
        })
    
    doc_mapping_df = pd.DataFrame(doc_mapping)
    doc_mapping_path = os.path.join(OUTPUT_DIR, 'lda_document_topics.csv')
    doc_mapping_df.to_csv(doc_mapping_path, index=False)
    print(f"  ✓ Document mapping exported to: {doc_mapping_path}")
    
    # 7. BERTopic comparison
    for k in [5, 10]:
        comparison_df = compare_with_bertopic(
            df, doc_indices, results[k]['doc_topics'], OUTPUT_DIR
        )
        comparison_path = os.path.join(OUTPUT_DIR, f'lda_bertopic_comparison_k{k}.csv')
        comparison_df.to_csv(comparison_path, index=False)
        print(f"  ✓ Comparison exported to: {comparison_path}")
    
    # Final summary
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print(f"\nOutput files saved to: {os.path.abspath(OUTPUT_DIR)}")
    print("\n  Topic Tables:")
    print("    - lda_topics_k5.csv")
    print("    - lda_topics_k10.csv")
    print("\n  Visualizations:")
    print("    - lda_pyldavis_k5.html")
    print("    - lda_pyldavis_k10.html")
    print("\n  Analysis Files:")
    print("    - lda_coherence_scores.csv")
    print("    - lda_document_topics.csv")
    print("    - lda_bertopic_comparison_k5.csv")
    print("    - lda_bertopic_comparison_k10.csv")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    run_lda_analysis()
