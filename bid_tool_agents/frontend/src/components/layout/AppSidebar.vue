<template>
  <nav class="sidebar">
    <div class="sidebar-nav">
      <!-- 首页 -->
      <div class="sidebar-section">
        <router-link to="/home" class="sidebar-item" :class="{ active: isActive('/home') }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
          </svg>
          <span class="sidebar-item-text">首页</span>
        </router-link>
      </div>

      <!-- 智能审查 -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">智能审查</div>
        <router-link to="/workspace/new" class="sidebar-item" :class="{ active: isActive('/workspace') }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
          </svg>
          <span class="sidebar-item-text">新建审查</span>
        </router-link>
        <router-link to="/qualification-verify" class="sidebar-item" :class="{ active: isActive('/qualification') }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>
          </svg>
          <span class="sidebar-item-text">资质核验</span>
        </router-link>
        <router-link to="/responses" class="sidebar-item" :class="{ active: isActive('/responses') }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
          </svg>
          <span class="sidebar-item-text">响应比对分析</span>
        </router-link>
        <router-link to="/risk-detection" class="sidebar-item" :class="{ active: isActive('/risk-detection') }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
          </svg>
          <span class="sidebar-item-text">围串标检测</span>
        </router-link>
      </div>

      <!-- 项目中心 -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">项目中心</div>
        <router-link to="/projects" class="sidebar-item" :class="{ active: isActive('/projects') }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/>
          </svg>
          <span class="sidebar-item-text">项目列表</span>
        </router-link>
        <router-link to="/project/1" class="sidebar-item" :class="{ active: isActive('/project') }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          <span class="sidebar-item-text">项目详情</span>
        </router-link>
      </div>

      <!-- 综合审核报告 -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">综合审核报告</div>
        <router-link to="/reports" class="sidebar-item" :class="{ active: isActive('/reports') }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          <span class="sidebar-item-text">报告列表</span>
        </router-link>
        <router-link to="/report/1/full" class="sidebar-item" :class="{ active: isActive('/report') && route.path.includes('/full') }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          <span class="sidebar-item-text">报告详情</span>
        </router-link>
      </div>

      <!-- 辅助功能 -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">辅助功能 <span class="phase-tag">二期</span></div>
        <router-link to="/evaluation-assist" class="sidebar-item" :class="{ active: isActive('/evaluation-assist') }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/>
          </svg>
          <span class="sidebar-item-text">辅助评标</span>
        </router-link>
        <router-link to="/expert-selection" class="sidebar-item" :class="{ active: isActive('/expert-selection') }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
          </svg>
          <span class="sidebar-item-text">专家抽取</span>
        </router-link>
        <router-link to="/archive-management" class="sidebar-item" :class="{ active: isActive('/archive-management') }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
          </svg>
          <span class="sidebar-item-text">档案管理</span>
        </router-link>
      </div>

      <!-- 统计分析 -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">统计分析 <span class="phase-tag">二期</span></div>
        <router-link to="/statistics" class="sidebar-item" :class="{ active: isActive('/statistics') }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
          </svg>
          <span class="sidebar-item-text">数据统计</span>
        </router-link>
      </div>

      <!-- 系统 -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">系统设置</div>
        <router-link to="/users" class="sidebar-item" :class="{ active: isActive('/users') }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
          </svg>
          <span class="sidebar-item-text">用户管理</span>
        </router-link>
        <router-link to="/knowledge-base" class="sidebar-item" :class="{ active: isActive('/knowledge-base') }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
          </svg>
          <span class="sidebar-item-text">知识库配置</span>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()

const isActive = (path: string) => {
  if (path === '/home') {
    return route.path === '/home'
  }
  if (path === '/project/1') {
    return route.path.startsWith('/project/') && route.path !== '/projects'
  }
  if (path === '/report/1/full') {
    return route.path.startsWith('/report/') && route.path.endsWith('/full')
  }
  if (path === '/workspace/new') {
    return route.path === '/workspace/new'
  }
  return route.path.startsWith(path)
}
</script>

<style scoped lang="scss">
.sidebar {
  position: fixed;
  top: var(--topbar-height);
  left: 0;
  bottom: 0;
  width: var(--sidebar-width);
  background: var(--white);
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.06);
  overflow-y: auto;
  z-index: 90;
}

.sidebar-nav {
  padding: 16px 0;
}

.sidebar-section {
  margin-bottom: 4px;
}

.sidebar-section-title {
  padding: 16px 20px 6px;
  font-size: 12px;
  font-weight: 500;
  color: var(--gray-500);
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  color: var(--gray-600);
  transition: all 0.2s ease;
  cursor: pointer;
  font-size: 14px;
  text-decoration: none;

  &:hover {
    background: var(--gray-100);
    color: var(--primary-color);
  }

  &.active {
    background: rgba(30, 90, 168, 0.08);
    color: var(--primary-color);
    font-weight: 500;
  }

  svg {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
  }
}

.sidebar-item-text {
  flex: 1;
  font-size: 14px;
}

.phase-tag {
  padding: 1px 6px;
  background: var(--gray-200);
  color: var(--gray-500);
  border-radius: 4px;
  font-size: 10px;
  font-weight: 500;
  margin-left: 4px;
}
</style>
