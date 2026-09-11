"""
Project TENKA - Main Runner (天下統一評定 起動スクリプト)
Indexes raw knowledge, summons Nobunaga, Hideyoshi, Ieyasu, and Shotoku Taishi,
and runs an autonomous multi-agent strategy council.
"""

import os
import sys

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Ensure project root is in sys.path
sys.path.insert(0, "C:/Users/haruki/.gemini/antigravity/scratch")

from project_tenka.core.rag_engine import HybridRAGEngine
from project_tenka.core.council import TenkaCouncil

def main():
    print("================================================================")
    print("【Project TENKA: 天下統一マルチエージェントRAG基盤 起動】")
    print("織田信長 × 豊臣秀吉 × 徳川家康 × 聖徳太子 による未踏戦略サミット")
    print("================================================================")

    db_path = "C:/Users/haruki/.gemini/antigravity/scratch/project_tenka/data/indexed/tenka_rag.db"
    rag = HybridRAGEngine(db_path=db_path)

    # 1. Ingest raw data into RAG
    raw_dir = "C:/Users/haruki/.gemini/antigravity/scratch/project_tenka/data/raw"
    files = [f for f in os.listdir(raw_dir) if f.endswith(".txt")]
    
    print(f"\n[1] 未電子化・生データの太閤検地（RAGインデックス化開始）: {len(files)} ファイル")
    for filename in files:
        filepath = os.path.join(raw_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        category = filename.replace(".txt", "")
        rag.add_document(source=filename, category=category, content=content)
        print(f"  [OK] 検地完了: {filename} (カテゴリ: {category})")

    stats = rag.get_stats()
    print(f"\n[RAGインデックス完了]: 総蓄積チャンク数 = {stats['total_chunks']}")

    # 2. Summon the Council
    council = TenkaCouncil(rag_engine=rag)

    # 3. Deliberate on the ultimate prompt
    topic = "「スキルもコミュ力もない個人が、既存のありきたりな副業を一切やらず、RAGとマルチエージェントで未踏の領域を切り拓いて最速かつ永続的にお金を稼ぐための具体的作戦」"
    
    result = council.run_session(topic=topic)
    print("\n【評定完了】天下統一の青写真が描かれました。")

if __name__ == "__main__":
    main()
