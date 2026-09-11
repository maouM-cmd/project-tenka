"""
Project TENKA - Council Engine (天下統一評定エンジン)
Orchestrates multi-agent deliberations among Nobunaga, Hideyoshi, Ieyasu, and Shotoku Taishi,
grounded by the Hybrid RAG Knowledge Base.
"""

import os
import sys
import json
from typing import List, Dict, Any

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from project_tenka.core.rag_engine import HybridRAGEngine
from project_tenka.agents.nobunaga import OdaNobunagaAgent
from project_tenka.agents.hideyoshi import ToyotomiHideyoshiAgent
from project_tenka.agents.ieyasu import TokugawaIeyasuAgent
from project_tenka.agents.shotoku import ShotokuTaishiAgent

class TenkaCouncil:
    def __init__(self, rag_engine: HybridRAGEngine):
        self.rag_engine = rag_engine
        self.nobunaga = OdaNobunagaAgent(rag_engine)
        self.hideyoshi = ToyotomiHideyoshiAgent(rag_engine)
        self.ieyasu = TokugawaIeyasuAgent(rag_engine)
        self.shotoku = ShotokuTaishiAgent(rag_engine)
        self.agents = [self.nobunaga, self.hideyoshi, self.ieyasu, self.shotoku]

    def run_session(self, topic: str, output_dir: str = "C:/Users/haruki/.gemini/antigravity/scratch/project_tenka/output") -> Dict[str, Any]:
        """Execute a full council session with RAG integration and consensus synthesis."""
        os.makedirs(output_dir, exist_ok=True)
        print(f"\n========================================================")
        print(f"【Project TENKA: 天下統一評定 開始】")
        print(f"評定議題: {topic}")
        print(f"========================================================\n")

        rag_stats = self.rag_engine.get_stats()
        print(f"[RAGナレッジ状況]: 総チャンク数={rag_stats['total_chunks']}, ソース数={rag_stats['total_sources']}, 分類={rag_stats['categories']}\n")

        deliberation_log = []
        context = []

        # Round 1: Individual Position & RAG retrieval
        print("--- [第壱幕: 各英雄によるRAG召喚と立論] ---")
        for agent in self.agents:
            statement = agent.deliberate(topic=topic, context=context)
            deliberation_log.append(statement)
            context.append({"speaker": statement["speaker"], "proposal": statement["proposal"]})
            print(f"\n▶ 【{statement['speaker']}】({statement['title']}):")
            print(f"   信条: {statement['stance']}")
            print(f"   RAG引用根拠: {len(statement['cited_facts'])} 件参照")
            for fact in statement['cited_facts']:
                print(f"     - {fact}")
            print(f"   提案抜粋: {statement['proposal'].splitlines()[0]}")

        # Final Synthesis by Shotoku Taishi
        final_synthesis = deliberation_log[-1]["actionable_prototype"]

        # Build Council Result
        result = {
            "topic": topic,
            "rag_stats": rag_stats,
            "deliberations": deliberation_log,
            "final_consensus_prototype": final_synthesis
        }

        # Save to JSON
        json_path = os.path.join(output_dir, "council_deliberation.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        # Save Markdown Report
        md_path = os.path.join(output_dir, "TENKA_COUNCIL_REPORT.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# 【Project TENKA 天下統一軍議 最終報告書】\n\n")
            f.write(f"**議題**: {topic}\n\n")
            f.write(f"## 1. ナレッジベース（RAG）状況\n")
            f.write(f"- 蓄積チャンク数: {rag_stats['total_chunks']}\n")
            f.write(f"- 参照ソース数: {rag_stats['total_sources']}\n\n")
            f.write(f"## 2. 四英雄の評定記録\n\n")
            for entry in deliberation_log:
                f.write(f"### ■ {entry['speaker']}（{entry['title']}）\n")
                f.write(f"> **発言**: {entry['stance']}\n\n")
                f.write(f"**【現状批判】**:\n{entry['critique']}\n\n")
                f.write(f"**【打開提案】**:\n{entry['proposal']}\n\n")
                f.write(f"**【参照したRAG知見】**:\n")
                for fact in entry['cited_facts']:
                    f.write(f"- {fact}\n")
                f.write(f"\n---\n\n")
            f.write(f"## 3. 聖徳太子による最終統合仕様書\n\n")
            f.write(f"```json\n{json.dumps(final_synthesis, ensure_ascii=False, indent=2)}\n```\n")

        print(f"\n========================================================")
        print(f"【天下統一評定 終了: 成果物を生成しました】")
        print(f"JSON: {json_path}")
        print(f"Markdown: {md_path}")
        print(f"========================================================\n")

        return result
