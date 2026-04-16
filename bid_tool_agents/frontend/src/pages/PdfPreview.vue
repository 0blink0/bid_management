<template>
  <AppLayout>
    <div class="pdf-preview-page">
      <PageHeader
        title="PDF 原文定位"
        back-link="/report/1"
      />

      <div class="pdf-layout">
        <!-- PDF Viewer -->
        <div class="pdf-viewer">
          <div class="pdf-toolbar">
            <n-button size="small" @click="prevPage">
              <template #icon>
                <n-icon><ChevronBackOutline /></n-icon>
              </template>
              上一页
            </n-button>
            <div class="page-indicator">
              <span>第</span>
              <n-input-number
                v-model:value="currentPage"
                :min="1"
                :max="totalPages"
                size="small"
                @blur="goToPage"
              />
              <span>页，共 {{ totalPages }} 页</span>
            </div>
            <n-button size="small" @click="nextPage">
              下一页
              <template #icon>
                <n-icon><ChevronForwardOutline /></n-icon>
              </template>
            </n-button>
          </div>

          <div class="pdf-content">
            <div class="pdf-page">
              <!-- Mock PDF content -->
              <div class="pdf-text">
                <h2>投标文件 - 资质证书</h2>
                <p>
                  <span class="highlight">根据招标文件要求，投标人须具备以下资质：</span>
                </p>
                <p>1. 企业法人营业执照（有效期内）</p>
                <p>2. 信息系统集成一级资质</p>
                <p>3. ISO9001质量管理体系认证</p>
                <p>4. <span class="warning-bg">安全生产许可证（将于2024年6月到期）</span></p>
                <p>5. 软件企业认定证书</p>
              </div>

              <!-- Problem annotation -->
              <div class="problem-annotation">
                <div class="annotation-marker">
                  <n-icon :size="16"><AlertCircleOutline /></n-icon>
                </div>
                <div class="annotation-content">
                  <div class="annotation-title">资质证书即将过期</div>
                  <div class="annotation-desc">安全生产许可证有效期至2024年6月，建议提前续期</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Problem Sidebar -->
        <div class="problem-sidebar">
          <div class="sidebar-header">问题详情</div>

          <div class="problem-info">
            <div class="info-item">
              <span class="info-label">问题标题</span>
              <span class="info-value">资质证书即将过期</span>
            </div>
            <div class="info-item">
              <span class="info-label">文件名称</span>
              <span class="info-value">投标文件_B.pdf</span>
            </div>
            <div class="info-item">
              <span class="info-label">位置</span>
              <span class="info-value">第 8 页</span>
            </div>
            <div class="info-item">
              <span class="info-label">法律依据</span>
              <span class="info-value">《招投标法》第34条</span>
            </div>
          </div>

          <n-button type="primary" block>添加到整改清单</n-button>

          <div class="other-issues">
            <div class="other-issues-title">其他问题</div>
            <div v-for="issue in otherIssues" :key="issue.page" class="issue-link">
              <n-tag :type="issue.severity" size="small">
                {{ issue.severity === 'error' ? '严重' : '警告' }}
              </n-tag>
              <span class="issue-page">第{{ issue.page }}页</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NButton, NIcon, NInputNumber, NTag } from 'naive-ui'
import AppLayout from '@/components/layout/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import {
  ChevronBackOutline,
  ChevronForwardOutline,
  AlertCircleOutline
} from '@vicons/ionicons5'

const currentPage = ref(8)
const totalPages = ref(156)

const otherIssues = ref([
  { page: 12, severity: 'error' as const },
  { page: 30, severity: 'warning' as const },
  { page: 45, severity: 'warning' as const }
])

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const goToPage = () => {
  // Navigate to page
}
</script>

<style scoped lang="scss">
.pdf-preview-page {
  height: 100%;
}

.pdf-layout {
  display: flex;
  gap: 24px;
  height: calc(100% - 100px);
}

.pdf-viewer {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
}

.pdf-toolbar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  padding: 12px;
  background: var(--gray-100);
  border-bottom: 1px solid var(--gray-200);
}

.page-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--gray-600);
}

.pdf-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: var(--gray-200);
}

.pdf-page {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  padding: 48px;
  background: #fff;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.pdf-text {
  font-size: 14px;
  line-height: 2;
  color: var(--gray-800);

  h2 {
    font-size: 18px;
    margin-bottom: 16px;
  }

  p {
    margin: 8px 0;
  }
}

.highlight {
  background: rgba(255, 217, 61, 0.3);
}

.warning-bg {
  background: rgba(255, 77, 79, 0.1);
  padding: 2px 4px;
  border-radius: 2px;
}

.problem-annotation {
  position: absolute;
  right: 80px;
  top: 200px;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 12px;
  background: rgba(250, 173, 20, 0.1);
  border: 1px solid var(--warning-color);
  border-radius: 8px;
}

.annotation-marker {
  color: var(--warning-color);
}

.annotation-title {
  font-size: 13px;
  font-weight: 500;
  color: var(--gray-800);
}

.annotation-desc {
  font-size: 12px;
  color: var(--gray-600);
  margin-top: 4px;
}

.problem-sidebar {
  width: 320px;
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-header {
  font-size: 16px;
  font-weight: 600;
  color: var(--gray-800);
}

.problem-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 12px;
  color: var(--gray-500);
}

.info-value {
  font-size: 14px;
  color: var(--gray-800);
}

.other-issues {
  margin-top: auto;
}

.other-issues-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--gray-700);
  margin-bottom: 12px;
}

.issue-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  border-bottom: 1px solid var(--gray-100);

  &:last-child {
    border-bottom: none;
  }
}

.issue-page {
  font-size: 13px;
  color: var(--gray-600);
}
</style>
