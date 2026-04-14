# 知识库管理 (Knowledge Base)

## 11.1 法规库

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/knowledge/regulations | 获取法规库 |
| POST | /api/knowledge/regulations | 添加法规 |
| PUT | /api/knowledge/regulations/{id} | 更新法规 |
| DELETE | /api/knowledge/regulations/{id} | 删除法规 |

## 11.2 规则库

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/knowledge/rules | 获取规则库 |
| POST | /api/knowledge/rules | 添加规则 |
| PUT | /api/knowledge/rules/{id} | 更新规则 |
| DELETE | /api/knowledge/rules/{id} | 删除规则 |

## 11.3 错敏词库

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/knowledge/sensitive-words | 获取错敏词库 |
| POST | /api/knowledge/sensitive-words | 添加错敏词 |
| PUT | /api/knowledge/sensitive-words/{id} | 更新错敏词 |
| DELETE | /api/knowledge/sensitive-words/{id} | 删除错敏词 |

## 11.4 其他知识库

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/knowledge/templates | 获取模板库 |
| GET | /api/knowledge/cases | 获取案例库 |
| GET | /api/knowledge/activation | 获取规则生效配置 |
| PUT | /api/knowledge/activation/{id} | 更新规则生效状态 |
