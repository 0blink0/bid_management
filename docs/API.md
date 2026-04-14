# 智能招投标审查平台 - API接口文档

本文档描述智能招投标审查平台后端RESTful API接口。

## 目录

| 模块 | 文件 | 描述 |
|------|------|------|
| [认证模块](./api/01-auth.md) | 01-auth.md | 用户登录、退出 |
| [项目管理](./api/02-projects.md) | 02-projects.md | 项目CRUD操作 |
| [文件管理](./api/03-files.md) | 03-files.md | 文件上传、预览、删除 |
| [审查流程](./api/04-review.md) | 04-review.md | 审查开始、状态、进度 |
| [招标文件检测](./api/05-detection.md) | 05-detection.md | 招标文件问题检测 |
| [资质核验](./api/06-qualification.md) | 06-qualification.md | 企业、人员、证书核验 |
| [围串标检测](./api/07-collusion.md) | 07-collusion.md | 投标人关联分析 |
| [响应比对](./api/08-response.md) | 08-response.md | 响应文件条款比对 |
| [报告管理](./api/09-reports.md) | 09-reports.md | 审查报告查看、导出 |
| [智能问答](./api/10-chat.md) | 10-chat.md | 智能助手问答 |
| [知识库管理](./api/11-knowledge.md) | 11-knowledge.md | 法规库、规则库、错敏词库 |
| [用户管理](./api/12-users.md) | 12-users.md | 用户CRUD操作 |
| [归档管理](./api/13-archive.md) | 13-archive.md | 项目归档、恢复 |
| [专家抽取](./api/14-experts.md) | 14-experts.md | 专家列表、抽取 |
| [评分辅助](./api/15-scoring.md) | 15-scoring.md | 评分建议、标准 |
| [统计分析](./api/16-statistics.md) | 16-statistics.md | 统计概览、审查统计 |

---

## 通用说明

### 认证方式

API使用Bearer Token认证，Token通过登录接口获取。

**请求头：**

```
Authorization: Bearer <token>
```

### 通用响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

### 分页格式

列表接口支持分页，响应格式如下：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [],
    "pagination": {
      "page": 1,
      "pageSize": 10,
      "total": 100,
      "totalPages": 10
    }
  }
}
```
