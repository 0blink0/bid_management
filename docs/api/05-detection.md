# 招标文件检测 (Bidding Document Detection)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/detection/bidding | 招标文件检测 |
| GET | /api/detection/bidding/{id} | 获取检测结果 |
| GET | /api/detection/bidding/{id}/issues | 获取问题列表 |

## 5.1 招标文件检测

```
POST /api/detection/bidding
```

**请求参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectId | string | 是 | 项目ID |
| fileId | string | 是 | 招标文件ID |

## 5.2 获取检测结果

```
GET /api/detection/bidding/{id}
```

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "resultId": "det_001",
    "status": "completed",
    "summary": {
      "totalIssues": 5,
      "critical": 1,
      "warning": 2,
      "info": 2
    }
  }
}
```

## 5.3 获取问题列表

```
GET /api/detection/bidding/{id}/issues
```
