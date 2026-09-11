"""
Project TENKA - Autonomous Monetization Auto-Pilot Pipeline
(天下統一 完全自律巡回エンジン)
Runs every cycle:
1. Harvests new open data (Hideyoshi)
2. Updates RAG knowledge base
3. Synthesizes new niche templates & competitive alerts (Shotoku & Nobunaga)
4. Deploys live updates to GitHub Pages (Ieyasu)
"""

import os
import sys
import subprocess
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, "C:/Users/haruki/.gemini/antigravity/scratch")
from project_tenka.harvester.real_crawler import harvest_tokyo_opendata, ingest_to_rag
from project_tenka.core.rag_engine import HybridRAGEngine

def run_cycle():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n========================================================")
    print(f"【Project TENKA: 自律収益化巡回サイクル開始】 {timestamp}")
    print(f"========================================================")

    db_path = "C:/Users/haruki/.gemini/antigravity/scratch/project_tenka/data/indexed/tenka_rag.db"
    rag = HybridRAGEngine(db_path=db_path)

    # 1. 秀吉の太閤検地（オープンデータ拡充）
    queries = ["公募", "入札", "DX推進", "省力化", "地域創生", "助成金"]
    datasets = harvest_tokyo_opendata(queries=queries)
    if datasets:
        ingest_to_rag(datasets, rag)

    stats = rag.get_stats()
    print(f"[RAG最新状態]: 総チャンク={stats['total_chunks']}, ソース数={stats['total_sources']}")

    # 2. 家康の自動デプロイ（Git commit & push）
    try:
        project_dir = "C:/Users/haruki/.gemini/antigravity/scratch/project_tenka"
        subprocess.run(["git", "add", "."], cwd=project_dir, check=True)
        commit_msg = f"auto(pilot): autonomous crawl & knowledge refresh at {timestamp}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=project_dir)
        subprocess.run(["git", "push", "origin", "main"], cwd=project_dir, check=True)
        print(f"  [OK] GitHub Pagesへ自律デプロイ完了！")
    except Exception as e:
        print(f"  [Notice] Git同期状況: {e}")

    print(f"========================================================")
    print(f"【自律巡回サイクル完了】 次の巡回まで待機します。")
    print(f"========================================================\n")

if __name__ == "__main__":
    run_cycle()
