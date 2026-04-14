# 项目管理 (Projects)

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/projects | 获取项目列表 |
| POST | /api/projects | 创建新项目 |
| GET | /api/projects/{id} | 获取项目详情 |
| PUT | /api/projects/{id} | 更新项目信息 |
| DELETE | /api/projects/{id} | 删除项目 |

## 2.1 获取项目列表

```
GET /api/projects
```

**查询参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| page | int | 否 | 页码，默认1 |
| pageSize | int | 否 | 每页数量，默认10 |
| status | string | 否 | 项目状态筛选 |

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [
      {
        "id": "1",
        "name": "某市政府云平台建设项目",
        "tenderer": "某市人民政府",
        "bidderCount": 3,
        "status": "reviewing",
        "createTime": "2024-01-15T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "pageSize": 10,
      "total": 8
    }
  }
}
```

## 2.2 创建新项目

```
POST /api/projects
```

**请求参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| name | string | 是 | 项目名称 |
| tenderer | string | 是 | 招标单位 |
| description | string | 否 | 项目描述 |

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "9"
  }
}
```

## 2.3 获取项目详情

```
GET /api/projects/{id}
```

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "1",
    "name": "某市政府云平台建设项目",
    "tenderer": "某市人民政府",
    "description": "云平台建设采购",
    "bidderCount": 3,
    "status": "reviewing",
    "createTime": "2024-01-15T10:30:00Z",
    "reviewProgress": 65
  }
}
```

## 2.4 更新项目信息

```
PUT /api/projects/{id}
```

**请求参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| name | string | 否 | 项目名称 |
| tenderer | string | 否 | 招标单位 |
| description | string | 否 | 项目描述 |

## 2.5 删除项目

```
DELETE /api/projects/{id}
```
