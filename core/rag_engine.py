"""
Project TENKA - Core Hybrid RAG Engine
SQLite + BM25/TF-IDF + N-gram cosine similarity hybrid search engine.
Fully self-contained, no external API dependency required for indexing and retrieval.
"""

import os
import re
import math
import json
import sqlite3
from typing import List, Dict, Any, Tuple
from collections import Counter
from rapidfuzz import fuzz

class HybridRAGEngine:
    def __init__(self, db_path: str = "C:/Users/haruki/.gemini/antigravity/scratch/project_tenka/data/indexed/tenka_rag.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT,
                    category TEXT,
                    chunk_id INTEGER,
                    content TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS doc_stats (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            conn.commit()

    def tokenize(self, text: str) -> List[str]:
        """Japanese & English hybrid tokenization using character n-grams and word patterns."""
        text = text.lower()
        # Extract alphanumeric words
        words = re.findall(r'[a-zA-Z0-9_]+', text)
        # Extract CJK character 2-grams (bigrams) for Japanese semantic matching
        cjk_chars = re.findall(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', text)
        bigrams = [cjk_chars[i] + cjk_chars[i+1] for i in range(len(cjk_chars)-1)]
        return words + bigrams + cjk_chars

    def add_document(self, source: str, category: str, content: str, metadata: Dict[str, Any] = None, chunk_size: int = 400, overlap: int = 80):
        """Split document into overlapping chunks and store in SQLite."""
        metadata_str = json.dumps(metadata or {}, ensure_ascii=False)
        
        chunks = []
        start = 0
        while start < len(content):
            end = min(start + chunk_size, len(content))
            chunk = content[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start += chunk_size - overlap
            if start >= len(content):
                break

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for i, chunk in enumerate(chunks):
                cursor.execute("""
                    INSERT INTO documents (source, category, chunk_id, content, metadata)
                    VALUES (?, ?, ?, ?, ?)
                """, (source, category, i, chunk, metadata_str))
            conn.commit()

    def search(self, query: str, top_k: int = 5, category: str = None) -> List[Dict[str, Any]]:
        """Hybrid search combining keyword overlap, RapidFuzz token matching, and TF-IDF weighting."""
        query_tokens = self.tokenize(query)
        if not query_tokens:
            return []

        query_counts = Counter(query_tokens)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if category:
                cursor.execute("SELECT id, source, category, chunk_id, content, metadata FROM documents WHERE category = ?", (category,))
            else:
                cursor.execute("SELECT id, source, category, chunk_id, content, metadata FROM documents")
            rows = cursor.fetchall()

        if not rows:
            return []

        scored_results = []
        for row in rows:
            doc_id, source, cat, chunk_id, content, meta = row
            doc_tokens = self.tokenize(content)
            doc_counts = Counter(doc_tokens)
            
            # 1. Token overlap score (Cosine-like TF-IDF proxy)
            intersection = set(query_tokens) & set(doc_tokens)
            if not intersection:
                continue
            overlap_score = sum(query_counts[t] * doc_counts[t] for t in intersection) / (math.sqrt(len(query_tokens) * len(doc_tokens)) + 1e-5)
            
            # 2. Fuzzy partial ratio
            fuzzy_score = fuzz.partial_ratio(query, content[:300]) / 100.0
            
            # 3. Hybrid combined score
            final_score = (overlap_score * 0.7) + (fuzzy_score * 0.3)
            
            if final_score > 0.05:
                scored_results.append({
                    "id": doc_id,
                    "source": source,
                    "category": cat,
                    "chunk_id": chunk_id,
                    "content": content,
                    "score": round(final_score, 4),
                    "metadata": json.loads(meta) if meta else {}
                })

        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:top_k]

    def get_stats(self) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM documents")
            total_chunks = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(DISTINCT source) FROM documents")
            total_sources = cursor.fetchone()[0]
            cursor.execute("SELECT category, COUNT(*) FROM documents GROUP BY category")
            categories = dict(cursor.fetchall())
        return {
            "total_chunks": total_chunks,
            "total_sources": total_sources,
            "categories": categories
        }
