# 智能招投标审查平台

基于LangGraph多Agent架构的智能招投标审查系统。

## 技术栈

- **前端**: Vue 3 + TypeScript + Vite + Naive UI
- **后端**: FastAPI + LangGraph + Pydantic
- **Agent**: LangGraph StateGraph + 四层记忆机制
- **LLM**: 阿里云API / 私有化千问 / DeepSeek
- **数据库**: PostgreSQL + Qdrant + Neo4j + Redis
- **文档解析**: GLM-ocr

## 项目结构

```
bid_tool_agents/
├── frontend/           # Vue3前端
├── backend/            # FastAPI后端
│   ├── app/
│   │   ├── agents/    # Agent核心
│   │   ├── skills/    # 共享Skills
│   │   ├── tools/     # 工具层
│   │   └── memory/    # 全局记忆
│   └── config/        # 配置文件
├── knowledge_base/     # 知识库
├── storage/           # 文件存储
└── docker-compose.yaml
```

## 快速启动

### 开发环境

```bash
# 前端
cd frontend
npm install
npm run dev

# 后端
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker Compose

```bash
docker-compose up -d
```

## 环境配置

配置文件位于 `backend/config/`:
- `development.yaml` - 开发环境
- `production.yaml` - 生产环境
- `testing.yaml` - 测试环境

通过环境变量切换:
```bash
export ENV=production
```

## LLM切换

前期使用阿里云API，后期切换到私有化部署:

```yaml
# 切换为私有化
llm:
  active: private_qwen  # 改为 private_qwen
```

## Agent四层记忆

- **瞬时记忆**: < 1分钟，原始输入 + LLM缓存
- **短期记忆**: 任务周期，任务上下文
- **长期记忆**: 月~年，经验 + 知识库
- **核心记忆**: 永久，Agent能力精华

## API文档

启动后访问: http://localhost:8000/docs
