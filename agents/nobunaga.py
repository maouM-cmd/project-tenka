"""
Project TENKA - Oda Nobunaga Agent
Persona: Disruption of Monopoly Barriers (楽市楽座・関所破壊・鉄砲隊運用)
"""

from typing import List, Dict, Any
from project_tenka.agents.base_agent import BaseHeroAgent

class OdaNobunagaAgent(BaseHeroAgent):
    def __init__(self, rag_engine):
        super().__init__(
            name="織田信長",
            title="関所破壊・市場解放の覇王",
            creed="既存の関所（中抜き・高額独占）を焼き討ちにし、テクノロジーの集中砲火で市場の富を強奪せよ",
            rag_engine=rag_engine
        )

    def deliberate(self, topic: str, context: List[Dict[str, str]]) -> Dict[str, Any]:
        # Consult RAG for high-barrier, monopoly-heavy regulatory/subsidy data
        evidence = self.consult_knowledge(query="助成金 補助金 独占 手数料 申請要件 ブラックボックス 審査基準", top_k=3)
        cited_snippets = [f"[{doc['source']}]: {doc['content'][:150]}..." for doc in evidence]

        stance = "「チマチマした受託や下請けなど虫唾が走る！専門コンサルが『難解さ』を盾に数十万〜数百万を着服する関所を丸ごと焼き払え！」"

        critique = (
            "世の凡百どもは『コミュ力がない』『スキルがない』と嘆きながら、既存のプラットフォームで奴隷のように搾取されている。"
            "なぜ彼らに頭を下げる？関所の通行手形（難解な申請書や専門知識）を、我らのRAGで秒で完全自動生成し、"
            "タダ同然で世にバラ撒けば、既存の独占業者は干上がり、利用者は一網打尽に我らに平伏す。"
        )

        proposal = (
            "【関所破壊型・逆張りフリーミアム戦略】\n"
            "1. 専門士業が独占する『超高額な公的申請・制度マッチング・減点回避ロジック』をRAGで丸裸にする。\n"
            "2. 本来50万円〜100万円かかる診断・書類作成プロトタイプをAIエージェントが0円〜数千円で即時発行する仕組みを作る。\n"
            "3. 業界の既存勢力をパニックに陥れ、集まった莫大なトラフィックに対し『最終採択率99%保証の特急シミュレーション』を高単価で刈り取る。"
        )

        actionable_prototype = {
            "name": "Nobunaga_BarrierBreaker_Engine",
            "target_monopoly": "公的補助金・事業再構築・DX導入の難解申請と高額中抜き",
            "disruption_mechanism": "審査基準PDF・過去の採択事例・不採択理由をRAGで全解読し、合格確率スコアと最適申請文を即時出力",
            "monetization_hook": "基本判定は完全無料開放でシェア独占、エージェントによる『自動修正・加点ブースト』で成果報酬型課金"
        }

        return {
            "speaker": self.name,
            "title": self.title,
            "stance": stance,
            "cited_facts": cited_snippets,
            "critique": critique,
            "proposal": proposal,
            "actionable_prototype": actionable_prototype
        }
