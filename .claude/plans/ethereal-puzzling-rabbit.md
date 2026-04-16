# Vue 3 实现计划：将 HTML 设计页面转换为 Vue 3 组件

## 项目概述

将 `docs/html/` 目录下的 25 个 HTML 设计页面实现为 Vue 3 + TypeScript 页面组件。

**前端位置**: `bid_tool_agents/frontend/`
**技术栈**: Vue 3.4+ / TypeScript 5.x / Vite 5.x / Vue Router 4.x / Pinia 2.x / Naive UI 2.x / SCSS

---

## 1. HTML 到 Vue 路由映射

| HTML 文件 | Vue 路由 | Vue 页面组件 | 优先级 |
|-----------|----------|--------------|--------|
| 01-login.html | `/login` | `Login.vue` (新建) | P0 |
| 02-workspace.html | `/workspace/new` | `WorkspaceNew.vue` (新建) | P0 |
| 03-workspace-step2.html | `/workspace/progress` | `WorkspaceProgress.vue` (新建) | P0 |
| 04b-duplicate-detection.html | `/workspace/processing` | `WorkspaceProcessing.vue` (新建) | P1 |
| 05-reviewing.html | `/reports` | `Reports.vue` (新建) | P0 |
| 06-report.html | `/report/:id` | `ReportDetail.vue` (新建) | P0 |
| 06b-report-chat.html | `/report/:id/chat` | `ReportChat.vue` (新建) | P1 |
| 06b-report-detail.html | `/report/:id/full` | `ReportFull.vue` (新建) | P0 |
| 07-pdf-preview.html | `/pdf/:id` | `PdfPreview.vue` (新建) | P1 |
| 08-admin.html | `/admin` | `Admin.vue` (新建) | P0 |
| 09-user-management.html | `/users` | `UserManagement.vue` (新建) | P1 |
| 10-knowledge-base.html | `/knowledge-base` | 增强现有 `KnowledgeBase.vue` | P0 |
| archive-management.html | `/archive` | 增强现有 `ArchiveManagement.vue` | P0 |
| detection-list.html | `/risk-detection` | 增强现有 `RiskDetection.vue` | P0 |
| expert-selection.html | `/expert-selection` | 增强现有 `ExpertSelection.vue` | P0 |
| index.html | `/home` | 增强现有 `Home.vue` | P0 |
| project-detail.html | `/project/:id` | `ProjectDetail.vue` (新建) | P1 |
| project-list.html | `/projects` | `ProjectList.vue` (新建) | P1 |
| qualification-check.html | `/qualification/:id` | `QualificationCheck.vue` (新建) | P1 |
| qualification-list.html | `/qualification` | 增强现有 `QualificationVerify.vue` | P0 |
| response-compare.html | `/comparison` | 增强现有 `Comparison.vue` | P0 |
| response-list.html | `/responses` | `ResponseList.vue` (新建) | P2 |
| scoring-assist.html | `/evaluation-assist` | 增强现有 `EvaluationAssist.vue` | P0 |
| statistics.html | `/statistics` | 增强现有 `Statistics.vue` | P0 |

---

## 2. 需要创建的公共组件

### 布局组件 (`src/components/layout/`)
- `AppLayout.vue` - 主布局（顶部栏 + 侧边栏）
- `AppTopbar.vue` - 顶部导航
- `AppSidebar.vue` - 侧边导航菜单
- `PageHeader.vue` - 页面头部（标题 + 面包屑 + 操作按钮）

### 通用组件 (`src/components/common/`)
- `StatusBadge.vue` - 状态徽章（成功/警告/危险）
- `DataTable.vue` - 数据表格（排序、分页）
- `Pagination.vue` - 分页控件
- `FileCard.vue` - 文件卡片
- `FileUploader.vue` - 拖拽上传（增强现有）
- `ProgressSteps.vue` - 步骤进度指示器
- `StatCard.vue` - 统计卡片
- `RiskBadge.vue` - 风险等级徽章
- `RoleBadge.vue` - 用户角色徽章
- `Modal.vue` - 模态框
- `ConfirmModal.vue` - 确认对话框
- `SearchInput.vue` - 搜索输入框
- `FilterSelect.vue` - 筛选下拉框

### 聊天组件 (`src/components/chat/`)
- `ChatSidebar.vue` - AI 聊天侧边栏
- `ChatMessage.vue` - 聊天消息气泡（现有 - 增强）
- `QuickQuestions.vue` - 快捷问题按钮
- `TypingIndicator.vue` - AI 打字指示器

### 报告组件 (`src/components/report/`)
- `ReportOverview.vue` - 报告得分概览
- `IssueList.vue` - 问题列表
- `IssueCard.vue` - 问题卡片
- `BidderCard.vue` - 投标方信息卡片
- `HeatMap.vue` - 围串标热力图
- `PdfViewer.vue` - PDF 查看器

### 知识库组件 (`src/components/knowledge/`)
- `KnowledgeTabs.vue` - 知识库 6 个标签页
- `RegulationTable.vue` - 法规库表格
- `RulesTable.vue` - 规则库表格
- `SensitiveWordsTable.vue` - 错敏词库表格
- `TemplateTable.vue` - 模板库表格
- `CasesTable.vue` - 案例库表格
- `ActivationTable.vue` - 规则生效表格

---

## 3. 实施步骤

### Phase 1: 基础设施
1. 创建 CSS 变量文件 `src/styles/variables.scss`（匹配设计颜色）
2. 创建布局组件：`AppLayout`、`AppTopbar`、`AppSidebar`
3. 创建通用组件：`StatusBadge`、`DataTable`、`Pagination`、`StatCard` 等
4. 更新路由配置 `src/router/index.ts`

### Phase 2: 核心页面 (P0)
5. 实现 `Login.vue` - 登录页面
6. 增强 `Home.vue` - 首页仪表盘
7. 创建工作流页面：`WorkspaceNew`、`WorkspaceProgress`、`WorkspaceProcessing`
8. 创建报告页面：`Reports`、`ReportDetail`、`ReportFull`
9. 实现 `Admin.vue` - 用户管理

### Phase 3: 支持页面 (P1)
10. 增强知识库页面（6 个标签页）
11. 实现 `PdfPreview.vue` - PDF 预览
12. 创建项目页面：`ProjectList`、`ProjectDetail`
13. 实现 `QualificationCheck.vue` - 资质检查
14. 增强其他现有页面

### Phase 4: 完善 (P2)
15. 实现聊天功能组件
16. 添加图表可视化（热力图等）
17. 响应式调整

---

## 4. 关键修改文件

### 需要修改的文件
- `src/router/index.ts` - 添加新路由
- `src/App.vue` - 集成布局组件
- `src/styles/variables.scss` - CSS 变量
- `src/pages/Home.vue` - 增强首页

### 需要创建的页面组件
- `src/pages/Login.vue`
- `src/pages/WorkspaceNew.vue`
- `src/pages/WorkspaceProgress.vue`
- `src/pages/WorkspaceProcessing.vue`
- `src/pages/Reports.vue`
- `src/pages/ReportDetail.vue`
- `src/pages/ReportChat.vue`
- `src/pages/ReportFull.vue`
- `src/pages/PdfPreview.vue`
- `src/pages/Admin.vue`
- `src/pages/UserManagement.vue`
- `src/pages/ProjectDetail.vue`
- `src/pages/ProjectList.vue`
- `src/pages/QualificationCheck.vue`
- `src/pages/ResponseList.vue`

### 需要创建的公共组件
- `src/components/layout/AppLayout.vue`
- `src/components/layout/AppTopbar.vue`
- `src/components/layout/AppSidebar.vue`
- `src/components/layout/PageHeader.vue`
- `src/components/common/StatusBadge.vue`
- `src/components/common/DataTable.vue`
- `src/components/common/Pagination.vue`
- `src/components/common/StatCard.vue`
- `src/components/common/ProgressSteps.vue`
- `src/components/common/FileCard.vue`
- `src/components/common/Modal.vue`
- `src/components/common/ConfirmModal.vue`
- `src/components/common/SearchInput.vue`
- `src/components/common/FilterSelect.vue`
- `src/components/common/RiskBadge.vue`
- `src/components/common/RoleBadge.vue`
- `src/components/chat/ChatSidebar.vue`
- `src/components/chat/QuickQuestions.vue`
- `src/components/chat/TypingIndicator.vue`
- `src/components/report/ReportOverview.vue`
- `src/components/report/IssueList.vue`
- `src/components/report/IssueCard.vue`
- `src/components/report/BidderCard.vue`
- `src/components/report/HeatMap.vue`
- `src/components/report/PdfViewer.vue`
- `src/components/knowledge/KnowledgeTabs.vue`
- `src/components/knowledge/RegulationTable.vue`
- `src/components/knowledge/RulesTable.vue`
- `src/components/knowledge/SensitiveWordsTable.vue`
- `src/components/knowledge/TemplateTable.vue`
- `src/components/knowledge/CasesTable.vue`
- `src/components/knowledge/ActivationTable.vue`

---

## 5. 验证方式

1. **运行开发服务器**: `cd bid_tool_agents/frontend && npm run dev`
2. **手动测试**: 访问各页面验证 UI 效果
3. **路由测试**: 验证所有新路由正常跳转
4. **组件测试**: 验证各公共组件正确渲染

---

## 6. 设计系统变量

```scss
// 颜色主题（匹配 HTML 设计）
$primary-color: #1E5AA8;
$primary-light: #2C7BE5;
$success-color: #52c41a;
$warning-color: #faad14;
$danger-color: #ff4d4f;
$purple-color: #722ed1;

// 灰色系
$gray-100: #fafafa;
$gray-200: #f5f5f5;
$gray-300: #e8e8e8;
$gray-400: #d9d9d9;
$gray-500: #8c8c8c;
$gray-600: #595959;
$gray-700: #434343;
$gray-800: #1f1f1f;

// 字体
$font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
```
