# 认证模块 (Authentication)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/auth/login | 用户登录 |
| POST | /api/auth/logout | 用户退出 |

## 1.1 用户登录

```
POST /api/auth/login
```

**请求参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "1",
      "username": "zhangsan",
      "name": "张三",
      "role": "admin"
    }
  }
}
```

## 1.2 用户退出

```
POST /api/auth/logout
```

**响应示例：**

```json
{
  "code": 0,
  "message": "success"
}
```
