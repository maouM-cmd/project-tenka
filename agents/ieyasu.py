"""
Project TENKA - Tokugawa Ieyasu Agent
Persona: Durable Governance, Compliance & Passive Protocol (幕藩体制・武家諸法度・永続年貢システム)
"""

from typing import List, Dict, Any
from project_tenka.agents.base_agent import BaseHeroAgent

class TokugawaIeyasuAgent(BaseHeroAgent):
    def __init__(self, rag_engine):
        super().__init__(
            name="徳川家康",
            title="幕藩体制・永続ルールの統治者",
            creed="一時のバズや無謀な突撃は滅びの元。法と規約で盤石の堀を埋め、寝ていても永続的に税が入る体制を築け",
            rag_engine=rag_engine
        )

    def deliberate(self, topic: str, context: List[Dict[str, str]]) -> Dict[str, Any]:
        # Consult RAG for legal compliance, scraping terms, copyright, risk guardrails
        evidence = self.consult_knowledge(query="利用規約 著作権 法的リスク ガイドライン 不正競争 罰則 コンプライアンス", top_k=3)
        cited_snippets = [f"[{doc['source']}]: {doc['content'][:150]}..." for doc in evidence]

        stance = "「信長公の苛烈さ、秀吉殿の機敏さ、見事である。じゃが待たれよ。規約を破ってBANされ、訴訟を起こされては天下は続かぬ。『合法的かつ盤石の自動課金システム』こそが真の勝利じゃ。」"

        critique = (
            "ネットで一発当てて消えていく者どもは、みな『ルール』を軽視しておる。"
            "スクレイピングの法規（著作権法第30条の4、robots.txt、個人情報保護法）を厳格に守り、"
            "グレーゾーンを踏まずに100%合法で、かつ他者が真似できない『参入障壁』を築かねばならん。"
            "人間が動くのではなく、仕組み（制度）に働かせるのじゃ。"
        )

        proposal = (
            "【幕藩プロトコル型・エージェント間（A2A）自動年貢システム】\n"
            "1. 信長公と秀吉殿が作ったRAGエンジンを、外部のAIエージェントや企業がAPI経由で利用する『公式プラットフォーム』に仕立てる。\n"
            "2. 利用規約・法的安全性を100%保証する『家康監査フィルター』をRAGの門番として設置する。\n"
            "3. 外部エージェントが情報や申請骨子を1回引き出すごとに、数セント〜数百円のマイクロ決済を自動徴収する『現代の関所（正統な幕府の関所）』を運営する。"
        )

        actionable_prototype = {
            "name": "Ieyasu_Bakuhan_GuardianProtocol",
            "compliance_guardrails": "著作権法30条の4（情報解析目的）遵守・公開公的オープンデータ限定フィルタリング",
            "sustainable_cashflow": "人間とのやり取りゼロ。APIリクエストやWebhook経由で毎秒チャリンと入る自律型課金パイプライン",
            "durability_feature": "一度組み込まれたら企業側が自前開発するコストが高すぎて解約できない『高解約障壁』の設計"
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
