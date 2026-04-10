/**
 * 公共侧边栏组件
 * 自动根据当前页面URL设置active状态
 */
function renderSidebar(currentPage) {
  const sidebarHTML = `
    <nav class="sidebar">
      <div class="sidebar-nav">
        <!-- 首页 -->
        <div class="sidebar-section">
          <a href="index.html" class="sidebar-item ${currentPage === 'index.html' ? 'active' : ''}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
            </svg>
            <span class="sidebar-item-text">首页</span>
          </a>
        </div>

        <!-- 智能审查 -->
        <div class="sidebar-section">
          <div class="sidebar-section-title">智能审查</div>
          <a href="02-workspace.html" class="sidebar-item ${currentPage === '02-workspace.html' ? 'active' : ''}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
            </svg>
            <span class="sidebar-item-text">新建审查</span>
          </a>
          <a href="qualification-list.html" class="sidebar-item ${currentPage === 'qualification-list.html' ? 'active' : ''}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>
            </svg>
            <span class="sidebar-item-text">资质核验</span>
          </a>
          <a href="response-list.html" class="sidebar-item ${currentPage === 'response-list.html' ? 'active' : ''}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
            <span class="sidebar-item-text">响应比对分析</span>
          </a>
          <a href="detection-list.html" class="sidebar-item ${currentPage === 'detection-list.html' ? 'active' : ''}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
            </svg>
            <span class="sidebar-item-text">围串标检测</span>
          </a>
        </div>

        <!-- 项目中心 -->
        <div class="sidebar-section">
          <div class="sidebar-section-title">项目中心</div>
          <a href="project-list.html" class="sidebar-item ${currentPage === 'project-list.html' ? 'active' : ''}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/>
            </svg>
            <span class="sidebar-item-text">项目列表</span>
          </a>
          <a href="project-detail.html" class="sidebar-item ${currentPage === 'project-detail.html' ? 'active' : ''}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <span class="sidebar-item-text">项目详情</span>
          </a>
        </div>

        <!-- 综合审核报告 -->
        <div class="sidebar-section">
          <div class="sidebar-section-title">综合审核报告</div>
          <a href="06-report.html" class="sidebar-item ${currentPage === '06-report.html' ? 'active' : ''}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <span class="sidebar-item-text">报告列表</span>
          </a>
          <a href="06b-report-detail.html" class="sidebar-item ${currentPage === '06b-report-detail.html' ? 'active' : ''}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <span class="sidebar-item-text">报告详情</span>
          </a>
        </div>

        <!-- 辅助功能 -->
        <div class="sidebar-section">
          <div class="sidebar-section-title">辅助功能 <span class="phase-tag">二期</span></div>
          <a href="scoring-assist.html" class="sidebar-item ${currentPage === 'scoring-assist.html' ? 'active' : ''}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/>
            </svg>
            <span class="sidebar-item-text">辅助评标</span>
          </a>
          <a href="expert-selection.html" class="sidebar-item ${currentPage === 'expert-selection.html' ? 'active' : ''}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
            </svg>
            <span class="sidebar-item-text">专家抽取</span>
          </a>
          <a href="archive-management.html" class="sidebar-item ${currentPage === 'archive-management.html' ? 'active' : ''}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
            </svg>
            <span class="sidebar-item-text">档案管理</span>
          </a>
        </div>

        <!-- 统计分析 -->
        <div class="sidebar-section">
          <div class="sidebar-section-title">统计分析 <span class="phase-tag">二期</span></div>
          <a href="statistics.html" class="sidebar-item ${currentPage === 'statistics.html' ? 'active' : ''}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
            <span class="sidebar-item-text">数据统计</span>
          </a>
        </div>

        <!-- 系统 -->
        <div class="sidebar-section">
          <div class="sidebar-section-title">系统设置</div>
          <a href="08-admin.html" class="sidebar-item ${currentPage === '08-admin.html' ? 'active' : ''}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
            <span class="sidebar-item-text">用户管理</span>
          </a>
          <a href="10-knowledge-base.html" class="sidebar-item ${currentPage === '10-knowledge-base.html' ? 'active' : ''}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
            </svg>
            <span class="sidebar-item-text">知识库配置</span>
          </a>
        </div>
      </div>
    </nav>
  `;

  // 插入到页面中
  document.body.insertAdjacentHTML('afterbegin', sidebarHTML);
}

// 获取当前页面文件名
function getCurrentPage() {
  const path = window.location.pathname;
  const filename = path.substring(path.lastIndexOf('/') + 1);
  return filename || 'index.html';
}

// 页面加载完成后渲染侧边栏
document.addEventListener('DOMContentLoaded', function() {
  const currentPage = getCurrentPage();
  renderSidebar(currentPage);
});