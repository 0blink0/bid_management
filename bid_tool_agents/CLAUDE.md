# 项目配置

## 项目概览
- **名称**：智能招投标审查平台

## 架构
@docs/技术设计文档.md

## 开发规范

### 代码风格
- 使用 Prettier 格式化
- 使用带 airbnb 配置的 ESLint
- 最大行长度：100 字符
- 使用 2 空格缩进

### 命名规范
- **文件**：kebab-case（`user-controller.js`）
- **类**：PascalCase（`UserService`）
- **函数 / 变量**：camelCase（`getUserById`）
- **常量**：UPPER_SNAKE_CASE（`API_BASE_URL`）
- **数据库表**：snake_case（`user_accounts`）

### Git 工作流
- 分支命名：`feature/description` 或 `fix/description`
- 提交信息：遵循 conventional commits
- 合并前必须有 PR
- 至少需要 1 个 approval

### 测试要求
- 最低 80% 代码覆盖率
- 所有关键路径都必须有测试

### API 规范
- 只允许 RESTful 端点
- 请求 / 响应都使用 JSON
- 正确使用 HTTP 状态码
- API 版本路径：`/api/v1/`
- 所有端点都要带示例文档

### 数据库
- schema 变更使用 migrations
- 绝不硬编码凭据
- 使用连接池
- 开发环境启用查询日志
- 需要定期备份

### 部署
- 基于 Docker 的部署
- 使用 Kubernetes 编排
- 蓝绿部署策略
- 失败时自动回滚
- 部署前先执行数据库迁移

## 常用命令

| 命令 | 作用 |
|---------|---------|
| `npm run dev` | 启动开发服务器 |
| `npm test` | 运行测试套件 |
| `npm run lint` | 检查代码风格 |
| `npm run build` | 构建生产版本 |
| `npm run migrate` | 执行数据库迁移 |

## 已知问题与解决方案

## 关联项目