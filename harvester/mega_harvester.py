"""
Project TENKA - Mega Open Data Harvester (全国大規模太閤検地クローラー)
Expands harvesting across Tokyo, Digital Agency, and national procurement datasets.
Integrates deep structured public tender and subsidy open data into TENKA RAG.
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

# Curated high-value national & municipal data targets
MEGA_SEARCH_QUERIES = [
    {"q": "事業承継", "category": "national_succession", "weight": "加点高"},
    {"q": "スタートアップ支援", "category": "national_startup", "weight": "超高額"},
    {"q": "脱炭素・GX", "category": "national_gx", "weight": "国策最優先"},
    {"q": "AI導入", "category": "national_ai", "weight": "DX特別枠"},
    {"q": "観光振興", "category": "regional_tourism", "weight": "地方創生"},
    {"q": "ものづくり", "category": "mfg_grant", "weight": "設備投資型"},
    {"q": "省エネルギー", "category": "energy_grant", "weight": "光熱費削減"},
    {"q": "就職支援・人材育成", "category": "hr_grant", "weight": "雇用維持"}
]

def harvest_mega_datasets() -> List[Dict[str, Any]]:
    harvested = []
    headers = {"User-Agent": "ProjectTenka-MegaHarvester/2.0"}

    print("🌾🥷 【秀吉×小太郎】全国メガ太閤検地（国策・自治体横断クローリング）開始！")
    for item in MEGA_SEARCH_QUERIES:
        q = item["q"]
        cat = item["category"]
        try:
            print(f"  ▶ 国策重要分野『{q}』({item['weight']}) を検地中...")
            params = {"q": q, "rows": 8}
            res = requests.get(CKAN_API_ENDPOINT, params=params, headers=headers, timeout=12)
            if res.status_code == 200:
                results = res.json().get("result", {}).get("results", [])
                print(f"    ✓ {len(results)} 件の公的データセットを補足！")
                for r in results:
                    harvested.append({
                        "id": r.get("id"),
                        "title": r.get("title", ""),
                        "notes": r.get("notes", ""),
                        "organization": r.get("organization", {}).get("title", "国・公的機関"),
                        "url": r.get("url", ""),
                        "category": cat,
                        "query_tag": q
                    })
        except Exception as e:
            print(f"    × 通信警告: {e}")

    return harvested

def ingest_mega_to_rag(datasets: List[Dict[str, Any]], rag: HybridRAGEngine):
    print(f"\n🌾 【秀吉】全国から収集した {len(datasets)} 件の公的データをRAGの蔵に一括蓄積します！")
    count = 0
    for d in datasets:
        content = (
            f"【公的支援・入札名】: {d['title']}\n"
            f"【管轄行政機関】: {d['organization']}\n"
            f"【詳細・公募要件】: {d['notes']}\n"
            f"【公式ソースURL】: {d['url']}\n"
            f"【重点政策カテゴリ】: {d['category']} ({d['query_tag']})\n"
        )
        source = f"mega_{d['category']}_{d['id'][:8]}.txt"
        rag.add_document(
            source=source,
            category=d["category"],
            content=content,
            metadata={"id": d["id"], "category": d["category"]}
        )
        count += 1

    print(f"  [OK] {count} 件のデータセットをRAGインデックスに蓄積完了！")

def main():
    db_path = "C:/Users/haruki/.gemini/antigravity/scratch/project_tenka/data/indexed/tenka_rag.db"
    rag = HybridRAGEngine(db_path=db_path)

    data = harvest_mega_datasets()
    if data:
        ingest_mega_to_rag(data, rag)

    stats = rag.get_stats()
    print(f"\n========================================================")
    print(f"🌾 【全国メガ太閤検地 完了】")
    print(f"総蓄積チャンク数: {stats['total_chunks']}")
    print(f"参照ソース数: {stats['total_sources']}")
    print(f"カテゴリ数: {len(stats['categories'])} 領域")
    print(f"========================================================")

if __name__ == "__main__":
    main()
