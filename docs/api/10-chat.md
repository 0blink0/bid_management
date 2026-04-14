# 智能问答 (Chat)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/chat/query | 发送问答查询 |
| GET | /api/chat/history/{reportId} | 获取问答历史 |

## 10.1 发送问答查询

```
POST /api/chat/query
```

**请求参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| reportId | string | 是 | 报告ID |
| query | string | 是 | 问题内容 |

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "answer": "根据检测结果，A公司和B公司存在以下关联特征...",
    "sources": ["招标文件第5.2条", "资质核验报告"],
    "confidence": 0.92
  }
}
```

## 10.2 获取问答历史

```
GET /api/chat/history/{reportId}
```
