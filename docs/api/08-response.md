# 响应比对 (Response Comparison)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/response/compare | 开始响应比对 |
| GET | /api/response/results | 获取比对结果 |
| GET | /api/response/clauses | 获取条款比对详情 |

## 8.1 开始响应比对

```
POST /api/response/compare
```

**请求参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectId | string | 是 | 项目ID |

## 8.2 获取比对结果

```
GET /api/response/results
```

**查询参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectId | string | 是 | 项目ID |

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "projectId": "1",
    "totalClauses": 56,
    "overallPassRate": 80,
    "riskCount": 2
  }
}
```

## 8.3 获取条款比对详情

```
GET /api/response/clauses
```
