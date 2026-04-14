# 归档管理 (Archive)

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/archive | 获取归档列表 |
| POST | /api/archive | 项目归档 |
| GET | /api/archive/{id} | 获取归档详情 |
| POST | /api/archive/{id}/restore | 恢复归档项目 |

## 13.1 获取归档列表

```
GET /api/archive
```

## 13.2 项目归档

```
POST /api/archive
```

**请求参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectId | string | 是 | 项目ID |

## 13.3 获取归档详情

```
GET /api/archive/{id}
```

## 13.4 恢复归档项目

```
POST /api/archive/{id}/restore
```
