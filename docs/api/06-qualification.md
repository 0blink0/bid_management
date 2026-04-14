# 资质核验 (Qualification Verification)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/qualification/check | 开始资质核验 |
| GET | /api/qualification/results | 获取核验结果 |
| GET | /api/qualification/bidders/{bidderId} | 获取投标方资质详情 |

## 6.1 开始资质核验

```
POST /api/qualification/check
```

**请求参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectId | string | 是 | 项目ID |

## 6.2 获取核验结果

```
GET /api/qualification/results
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
    "bidders": [
      {
        "bidderId": "b001",
        "name": "A公司",
        "validQualifications": 8,
        "expiredQualifications": 1,
        "riskStatus": "warning"
      }
    ]
  }
}
```

## 6.3 获取投标方资质详情

```
GET /api/qualification/bidders/{bidderId}
```
