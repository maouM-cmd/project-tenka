"""
Project TENKA - Toyotomi Hideyoshi Real Data Harvester
(豊臣秀吉: 本番オープンデータ太閤検地クローラー)
Fetches live open government datasets (Tokyo Open Data Catalog CKAN API, etc.)
and ingests them directly into the TENKA Hybrid RAG Database.
"""

import os
import sys
import json
import requests
from typing import List, Dict, Any

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, "C:/Users/haruki/.gemini/antigravity/scratch")
from project_tenka.core.rag_engine import HybridRAGEngine

CKAN_API_ENDPOINT = "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_search"

def harvest_tokyo_opendata(queries: List[str] = ["補助金", "助成金", "入札", "DX"]) -> List[Dict[str, Any]]:
    """Query live Tokyo Open Data CKAN API for authentic government datasets."""
    harvested = []
    headers = {"User-Agent": "ProjectTenka-Harvester/1.0"}

    print("🌾 【秀吉】全国太閤検地（リアルオープンデータ取得）を開始いたしますぞ！")
    for q in queries:
        try:
            print(f"  ▶ キーワード『{q}』で官公庁データベースを検地中...")
            params = {"q": q, "rows": 10}
            res = requests.get(CKAN_API_ENDPOINT, params=params, headers=headers, timeout=15)
            if res.status_code == 200:
                data = res.json()
                results = data.get("result", {}).get("results", [])
                print(f"    ✓ {len(results)} 件の本物データセットを確保！")
                for item in results:
                    harvested.append({
                        "id": item.get("id"),
                        "title": item.get("title", ""),
                        "notes": item.get("notes", ""),
                        "organization": item.get("organization", {}).get("title", "東京都"),
                        "url": item.get("url", ""),
                        "resources_count": len(item.get("resources", [])),
                        "query_tag": q
                    })
            else:
                print(f"    × エラー (Status: {res.status_code})")
        except Exception as e:
            print(f"    × 通信例外: {e}")

    return harvested

def ingest_to_rag(datasets: List[Dict[str, Any]], rag: HybridRAGEngine):
    """Format harvested datasets and ingest into SQLite RAG engine."""
    print(f"\n🌾 【秀吉】検地した {len(datasets)} 件の生データをRAGナレッジの蔵（SQLite）へ運び込みます！")
    
    ingested_count = 0
    for d in datasets:
        content = (
            f"【公的データセット名】: {d['title']}\n"
            f"【管轄機関】: {d['organization']}\n"
            f"【概要・要件】: {d['notes']}\n"
            f"【関連リソース数】: {d['resources_count']}件\n"
            f"【公式URL】: {d['url']}\n"
            f"【検地分類】: {d['query_tag']}\n"
        )
        source = f"tokyo_opendata_{d['id'][:8]}.txt"
        metadata = {"id": d["id"], "organization": d["organization"], "query": d["query_tag"]}
        
        rag.add_document(
            source=source,
            category=f"live_{d['query_tag']}",
            content=content,
            metadata=metadata
        )
        ingested_count += 1

    print(f"  [OK] 合計 {ingested_count} 件のデータセットをRAGインデックスに蓄積完了！")

def main():
    db_path = "C:/Users/haruki/.gemini/antigravity/scratch/project_tenka/data/indexed/tenka_rag.db"
    rag = HybridRAGEngine(db_path=db_path)

    datasets = harvest_tokyo_opendata(queries=["補助金", "助成金", "入札", "中小企業"])
    if datasets:
        ingest_to_rag(datasets, rag)
    
    stats = rag.get_stats()
    print(f"\n========================================================")
    print(f"🌾 【太閤検地 完了報告書】")
    print(f"総蓄積チャンク数: {stats['total_chunks']}")
    print(f"参照ソース数: {stats['total_sources']}")
    print(f"カテゴリ一覧: {list(stats['categories'].keys())}")
    print(f"========================================================")

if __name__ == "__main__":
    main()
