"""
比对分析Agent
"""
from typing import Any, Dict
from app.agents.base.agent import BaseAgent


class ComparisonAgent(BaseAgent):
    """比对分析Agent"""

    def __init__(self):
        super().__init__(
            agent_id="comparison",
            name="比对分析Agent",
            description="负责招投标文件的一致性比对"
        )
        self.skills = ["similarity_analysis", "graph_query"]
        self.boundaries = ["不做合规性判断"]

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "success"}
