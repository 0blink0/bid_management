# 专家抽取 (Expert Selection)

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/experts | 获取专家列表 |
| POST | /api/experts/select | 抽取专家 |
| GET | /api/experts/selection-history | 获取抽取历史 |

## 14.1 获取专家列表

```
GET /api/experts
```

## 14.2 抽取专家

```
POST /api/experts/select
```

**请求参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectId | string | 是 | 项目ID |
| count | int | 是 | 抽取数量 |

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "selectionId": "sel_001",
    "experts": [
      {"name": "李专家", "field": "计算机", "phone": "138****1234"}
    ]
  }
}
```

## 14.3 获取抽取历史

```
GET /api/experts/selection-history
```
