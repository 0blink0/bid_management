# 评分辅助 (Scoring Assist)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/scoring/assist | 获取评分辅助建议 |
| GET | /api/scoring/criteria | 获取评分标准 |

## 15.1 获取评分辅助建议

```
POST /api/scoring/assist
```

**请求参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectId | string | 是 | 项目ID |
| bidderId | string | 是 | 投标方ID |

## 15.2 获取评分标准

```
GET /api/scoring/criteria
```
