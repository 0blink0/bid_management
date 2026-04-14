# 围串标检测 (Collusion Detection)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/collusion/detect | 开始围串标检测 |
| GET | /api/collusion/results | 获取检测结果 |
| GET | /api/collusion/matrix | 获取关联度矩阵 |
| GET | /api/collusion/suspicious | 获取可疑组合列表 |

## 7.1 开始围串标检测

```
POST /api/collusion/detect
```

**请求参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectId | string | 是 | 项目ID |

## 7.2 获取检测结果

```
GET /api/collusion/results
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
    "totalBidders": 3,
    "suspiciousPairs": 2,
    "status": "completed"
  }
}
```

## 7.3 获取关联度矩阵

```
GET /api/collusion/matrix
```

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "bidders": ["A公司", "B公司", "C公司"],
    "matrix": [
      [0, 0.85, 0.32],
      [0.85, 0, 0.45],
      [0.32, 0.45, 0]
    ]
  }
}
```

## 7.4 获取可疑组合列表

```
GET /api/collusion/suspicious
```
