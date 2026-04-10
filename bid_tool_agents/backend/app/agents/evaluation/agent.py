"""
辅助评标Agent
"""
from typing import Any, Dict
from app.agents.base.agent import BaseAgent


class EvaluationAgent(BaseAgent):
    """辅助评标Agent"""

    def __init__(self):
        super().__init__(
            agent_id="evaluation",
            name="辅助评标Agent",
            description="负责辅助评标和评分建议"
        )
        self.skills = ["scoring_config", "objective_analysis"]
        self.boundaries = ["提供评分建议", "不替代专家评审"]

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "success"}
