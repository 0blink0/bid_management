<template>
  <AppLayout>
    <div class="report-detail-page">
      <div class="report-layout">
        <!-- Main Content -->
        <div class="report-main">
          <PageHeader
            title="审查报告"
            back-link="/reports"
          >
            <template #actions>
              <n-button @click="toggleView">标准视图</n-button>
              <n-button type="primary">导出 PDF</n-button>
            </template>
          </PageHeader>

          <!-- Overview Cards -->
          <n-grid :cols="4" :x-gap="16" :y-gap="16">
            <n-gi>
              <div class="overview-card">
                <div class="overview-label">合规检测</div>
                <div class="overview-value primary">92%</div>
              </div>
            </n-gi>
            <n-gi>
              <div class="overview-card">
                <div class="overview-label">风险识别</div>
                <div class="overview-value danger">85%</div>
              </div>
            </n-gi>
            <n-gi>
              <div class="overview-card">
                <div class="overview-label">资质核验</div>
                <div class="overview-value success">95%</div>
              </div>
            </n-gi>
            <n-gi>
              <div class="overview-card">
                <div class="overview-label">响应比对</div>
                <div class="overview-value warning">78%</div>
              </div>
            </n-gi>
          </n-grid>

          <!-- Issues Section -->
          <n-card class="issues-section" title="需要关注的问题">
            <div class="issue-list">
              <div v-for="issue in issues" :key="issue.id" class="issue-item">
                <div class="issue-indicator" :class="issue.severity"></div>
                <div class="issue-content">
                  <div class="issue-header">
                    <n-tag :type="issue.severity === 'danger' ? 'error' : 'warning'" size="small">
                      {{ issue.type }}
                    </n-tag>
                    <span class="issue-location">[{{ issue.location }}]</span>
                  </div>
                  <div class="issue-title">{{ issue.title }}</div>
                  <div class="issue-reference">{{ issue.reference }}</div>
                </div>
              </div>
            </div>
          </n-card>
        </div>

        <!-- Chat Sidebar -->
        <ChatSidebar />
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NGrid, NGi, NCard, NTag, NButton } from 'naive-ui'
import AppLayout from '@/components/layout/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import ChatSidebar from '@/components/chat/ChatSidebar.vue'

const toggleView = () => {}

const issues = ref([
  {
    id: 1,
    severity: 'danger',
    type: '招标文件',
    location: '第12页',
    title: '存在错敏词问题',
    reference: '《政府采购法》第22条'
  },
  {
    id: 2,
    severity: 'warning',
    type: '投标文件',
    location: '第8页',
    title: '资质证书即将过期',
    reference: '《招投标法》第34条'
  },
  {
    id: 3,
    severity: 'warning',
    type: '响应文件',
    location: '第15页',
    title: '技术方案响应不完整',
    reference: '《招投标法》第36条'
  }
])
</script>

<style scoped lang="scss">
.report-detail-page {
  height: 100%;
}

.report-layout {
  display: flex;
  gap: 24px;
  height: 100%;
}

.report-main {
  flex: 1;
  min-width: 0;
}

.overview-card {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.overview-label {
  font-size: 13px;
  color: var(--gray-500);
  margin-bottom: 8px;
}

.overview-value {
  font-size: 32px;
  font-weight: 700;

  &.primary {
    color: var(--primary-color);
  }

  &.danger {
    color: var(--danger-color);
  }

  &.success {
    color: var(--success-color);
  }

  &.warning {
    color: var(--warning-color);
  }
}

.issues-section {
  margin-top: 24px;
}

.issue-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.issue-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: var(--gray-100);
  border-radius: 8px;
}

.issue-indicator {
  width: 4px;
  border-radius: 2px;
  flex-shrink: 0;

  &.danger {
    background: var(--danger-color);
  }

  &.warning {
    background: var(--warning-color);
  }
}

.issue-content {
  flex: 1;
}

.issue-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.issue-location {
  font-size: 12px;
  color: var(--gray-500);
}

.issue-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--gray-800);
  margin-bottom: 4px;
}

.issue-reference {
  font-size: 12px;
  color: var(--gray-500);
}
</style>
