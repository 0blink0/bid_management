# 统计分析 (Statistics)

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/statistics/overview | 获取统计概览 |
| GET | /api/statistics/reviews | 获取审查统计 |
| GET | /api/statistics/risks | 获取风险统计 |

## 16.1 获取统计概览

```
GET /api/statistics/overview
```

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "totalProjects": 50,
    "totalReviews": 120,
    "riskProjects": 15,
    "averageScore": 85.5
  }
}
```

## 16.2 获取审查统计

```
GET /api/statistics/reviews
```

## 16.3 获取风险统计

```
GET /api/statistics/risks
```
