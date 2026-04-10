# Agent测试指南

## 快速开始

### 1. 安装测试依赖

```bash
cd backend
pip install -r requirements-dev.txt
```

### 2. 运行单个Agent测试

#### 方式一：使用Python脚本（推荐）

```bash
# 运行parser测试
python run_agent_test.py parser

# 运行compliance测试
python run_agent_test.py compliance

# 运行risk测试
python run_agent_test.py risk

# 列出所有可测试的Agent
python run_agent_test.py --list

# 运行所有Agent测试
python run_agent_test.py all

# 详细输出
python run_agent_test.py parser -v
```

#### 方式二：使用pytest直接运行

```bash
# 运行parser测试
pytest tests/agents/test_parser.py -v

# 运行compliance测试
pytest tests/agents/test_compliance.py -v

# 运行所有Agent测试
pytest tests/agents/ -v

# 运行带标记的测试
pytest tests/ -m agent -v
```

## 测试文件结构

```
tests/
├── agents/
│   ├── conftest.py              # Agent测试fixture
│   ├── test_parser.py           # 文档解析Agent测试
│   ├── test_compliance.py        # 合规审查Agent测试
│   ├── test_comparison.py        # 比对分析Agent测试
│   ├── test_qualification.py     # 资质核验Agent测试
│   ├── test_risk.py              # 风险识别Agent测试
│   ├── test_evaluation.py        # 辅助评标Agent测试
│   ├── test_expert.py            # 专家抽取Agent测试
│   ├── test_archive.py           # 档案管理Agent测试
│   └── test_statistics.py        # 统计分析Agent测试
└── conftest.py                  # 全局fixture
```

## 测试用例设计

每个Agent的测试包含：

1. **初始化测试** - 验证Agent能正确初始化
2. **记忆测试** - 验证四层记忆机制
3. **处理测试** - 验证核心处理逻辑
4. **边界测试** - 验证职责边界

## Mock LLM调用

测试时默认Mock了LLM调用，避免真实API请求：

```python
# tests/agents/conftest.py

@pytest.fixture
def mock_llm_response():
    async def mock_chat(messages, **kwargs):
        return "这是Mock LLM的响应"

    async def mock_embeddings(texts):
        return [[0.1, 0.2, 0.3] for _ in texts]

    return mock_chat, mock_embeddings
```

## 编写新测试

```python
# tests/agents/test_new_agent.py

import pytest
from unittest.mock import patch

class TestNewAgent:
    """新Agent测试"""

    @pytest.fixture
    def agent(self):
        from app.agents.new_agent.agent import NewAgent
        return NewAgent()

    def test_initialization(self, agent):
        """测试初始化"""
        assert agent.agent_id == "new"
        assert agent.name == "新Agent"

    @pytest.mark.asyncio
    async def test_process(self, agent):
        """测试处理逻辑"""
        with patch.object(agent.llm, 'chat', return_value="mocked"):
            result = await agent.process({"input": "test"})
            assert result is not None
```

## 持续集成

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          pytest tests/agents/ -v
```

## 常见问题

### Q: 测试报 "ModuleNotFoundError"
```bash
# 确保在backend目录下运行
cd backend
export PYTHONPATH=$PWD
pytest tests/agents/test_parser.py -v
```

### Q: 如何只运行特定Agent的测试？
```bash
# 使用pytest -k 参数
pytest tests/agents/ -k "parser" -v
```

### Q: 如何跳过需要真实API的测试？
```python
@pytest.mark.skip(reason="需要真实API")
async def test_with_real_api(self, agent):
    ...
```
