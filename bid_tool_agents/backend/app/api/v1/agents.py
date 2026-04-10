"""
Agent调用接口
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

router = APIRouter()


class AgentRequest(BaseModel):
    """Agent请求"""
    agent_id: str
    task_type: str
    input_data: Dict[str, Any]
    options: Optional[Dict[str, Any]] = None


class AgentResponse(BaseModel):
    """Agent响应"""
    success: bool
    agent_id: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class TaskStatusResponse(BaseModel):
    """任务状态响应"""
    task_id: str
    status: str
    progress: float
    result: Optional[Dict[str, Any]] = None


@router.post("/invoke", response_model=AgentResponse)
async def invoke_agent(request: AgentRequest) -> AgentResponse:
    """调用Agent"""
    try:
        # TODO: 实现Agent调用逻辑
        return AgentResponse(
            success=True,
            agent_id=request.agent_id,
            result={"message": "Agent invoked successfully"}
        )
    except Exception as e:
        return AgentResponse(
            success=False,
            agent_id=request.agent_id,
            error=str(e)
        )


@router.post("/task/{task_id}/status", response_model=TaskStatusResponse)
async def get_task_status(task_id: str) -> TaskStatusResponse:
    """获取任务状态"""
    # TODO: 实现任务状态查询
    return TaskStatusResponse(
        task_id=task_id,
        status="running",
        progress=0.5
    )


@router.get("/list")
async def list_agents() -> List[Dict[str, str]]:
    """列出所有Agent"""
    return [
        {"id": "coordinator", "name": "协调器", "description": "意图识别、任务分解"},
        {"id": "parser", "name": "文档解析", "description": "PDF解析、OCR识别"},
        {"id": "compliance", "name": "合规审查", "description": "合规性检查"},
        {"id": "comparison", "name": "比对分析", "description": "文本比对"},
        {"id": "qualification", "name": "资质核验", "description": "资质有效性核验"},
        {"id": "risk", "name": "风险识别", "description": "围串标检测"},
        {"id": "evaluation", "name": "辅助评标", "description": "评分建议"},
        {"id": "expert", "name": "专家抽取", "description": "专家随机抽取"},
        {"id": "archive", "name": "档案管理", "description": "任务跟踪、归档"},
        {"id": "statistics", "name": "统计分析", "description": "统计分析"}
    ]
