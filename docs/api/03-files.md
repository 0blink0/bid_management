# 文件管理 (Files)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/files/upload/preview | 上传文件预览（识别文件类型，不写入数据库） |
| POST | /api/files/upload/confirm | 确认提交（用户确认后写入数据库） |
| GET | /api/files | 获取项目文件列表（按类型筛选） |
| GET | /api/files/{id} | 获取文件信息 |
| GET | /api/files/{id}/preview | 获取PDF预览 |
| DELETE | /api/files/{id} | 删除文件 |

**文件类型说明：**

| 文件类型 | type值 | 描述 |
|----------|--------|------|
| 招标文件 | bidding_document | 招标方发布的招标文件 |
| 投标文件 | bidder_response | 投标方提交的响应文件 |

## 3.1 上传文件预览

```
POST /api/files/upload/preview
```

**请求参数 (multipart/form-data)：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| files | File[] | 是 | 上传的文件（支持多个文件同时上传） |

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "project": {
      "name": "某市政府云平台建设项目",
      "tenderer": "某市人民政府"
    },
    "files": [
      {
        "name": "招标文件.pdf",
        "size": 2048576,
        "type": "bidding_document",
        "identified": true
      },
      {
        "name": "投标文件-A公司.pdf",
        "size": 1536000,
        "type": "bidder_response",
        "identified": true
      }
    ],
    "confirmToken": "temp_abc123"
  }
}
```

**说明：**
- 系统自动识别文件内容，判定文件类型（仅识别，不写入数据库）
- 返回识别结果和 `confirmToken` 用于后续确认提交
- 用户确认识别结果无误后，调用确认接口提交

## 3.2 确认提交

```
POST /api/files/upload/confirm
```

**请求参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| confirmToken | string | 是 | 预览接口返回的确认令牌 |

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "project": {
      "id": "1",
      "name": "某市政府云平台建设项目",
      "tenderer": "某市人民政府"
    },
    "files": [
      {
        "id": "file_001",
        "name": "招标文件.pdf",
        "size": 2048576,
        "type": "bidding_document",
        "uploadTime": "2024-01-15T10:35:00Z"
      },
      {
        "id": "file_002",
        "name": "投标文件-A公司.pdf",
        "size": 1536000,
        "type": "bidder_response",
        "uploadTime": "2024-01-15T10:35:00Z"
      }
    ]
  }
}
```

## 3.3 获取项目文件列表

```
GET /api/files
```

**查询参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectId | string | 是 | 项目ID |
| type | string | 否 | 文件类型筛选（bidding_document/bidder_response） |

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "biddingDocuments": [
      {
        "id": "file_001",
        "name": "招标文件.pdf",
        "size": 2048576,
        "uploadTime": "2024-01-15T10:35:00Z"
      }
    ],
    "bidderResponses": [
      {
        "id": "file_002",
        "name": "投标文件-A公司.pdf",
        "size": 1536000,
        "bidderName": "A公司",
        "uploadTime": "2024-01-15T10:35:00Z"
      }
    ]
  }
}
```

## 3.4 获取文件信息

```
GET /api/files/{id}
```

## 3.5 获取PDF预览

```
GET /api/files/{id}/preview
```

## 3.6 删除文件

```
DELETE /api/files/{id}
```
