# 用户管理 (User Management)

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/users | 获取用户列表 |
| POST | /api/users | 创建用户 |
| PUT | /api/users/{id} | 更新用户信息 |
| DELETE | /api/users/{id} | 删除用户 |
| PUT | /api/users/{id}/status | 启用/禁用用户 |

## 12.1 获取用户列表

```
GET /api/users
```

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [
      {
        "id": "1",
        "username": "zhangsan",
        "name": "张三",
        "role": "admin",
        "status": "active",
        "createTime": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

## 12.2 创建用户

```
POST /api/users
```

**请求参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |
| name | string | 是 | 姓名 |
| role | string | 是 | 角色(admin/reviewer/viewer) |

## 12.3 更新用户信息

```
PUT /api/users/{id}
```

## 12.4 删除用户

```
DELETE /api/users/{id}
```

## 12.5 启用/禁用用户

```
PUT /api/users/{id}/status
```

**请求参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| status | string | 是 | 状态(active/disabled) |
