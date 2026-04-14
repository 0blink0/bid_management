# 报告管理 (Reports)

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/reports | 获取报告列表 |
| GET | /api/reports/{id} | 获取报告详情 |
| POST | /api/reports/{id}/export | 导出报告(PDF) |
| GET | /api/reports/{id}/summary | 获取报告摘要 |

## 9.1 获取报告列表

```
GET /api/reports
```

**查询参数：**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| page | int | 否 | 页码 |
| pageSize | int | 否 | 每页数量 |
| projectId | string | 否 | 项目ID筛选 |

## 9.2 获取报告详情

```
GET /api/reports/{id}
```

## 9.3 导出报告(PDF)

```
POST /api/reports/{id}/export
```

## 9.4 获取报告摘要

```
GET /api/reports/{id}/summary
```
