# 审查流程 (Review)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/reviews/start | 开始审查 |
| GET | /api/reviews/{id}/status | 获取审查状态 |
| GET | /api/reviews/{id}/progress | 获取审查进度 |
| POST | /api/reviews/{id}/cancel | 取消审查 |

## 4.1 开始审查

```
POST /api/reviews/start
```

**请求参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectId | string | 是 | 项目ID |

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "reviewId": "rev_001",
    "status": "running"
  }
}
```

## 4.2 获取审查状态

```
GET /api/reviews/{id}/status
```

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "reviewId": "rev_001",
    "status": "running",
    "currentStep": "qualification_check",
    "steps": [
      {"name": "文件检测", "status": "completed"},
      {"name": "资质核验", "status": "running"},
      {"name": "围串标检测", "status": "pending"},
      {"name": "响应比对", "status": "pending"}
    ]
  }
}
```

## 4.3 获取审查进度

```
GET /api/reviews/{id}/progress
```

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "reviewId": "rev_001",
    "progress": 65,
    "estimatedTime": "5分钟"
  }
}
```

## 4.4 取消审查

```
POST /api/reviews/{id}/cancel
```
