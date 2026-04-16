<template>
  <AppLayout>
    <div class="workspace-progress-page">
      <PageHeader
        title="正在审查中"
        :subtitle="progressSubtitle"
        back-link="/workspace/new"
      />

      <div class="progress-container">
        <!-- Loading State -->
        <div v-if="!isComplete" class="progress-card">
          <div class="spinner-wrapper">
            <div class="spinner"></div>
          </div>

          <div class="review-items">
            <div
              v-for="(item, index) in reviewItems"
              :key="item.key"
              class="review-item"
              :class="{ completed: index < currentStep, active: index === currentStep }"
            >
              <div class="item-indicator">
                <div v-if="index < currentStep" class="indicator-check">
                  <n-icon><CheckmarkOutline /></n-icon>
                </div>
                <div v-else-if="index === currentStep" class="indicator-spin">
                  <div class="mini-spinner"></div>
                </div>
                <div v-else class="indicator-pending"></div>
              </div>
              <div class="item-info">
                <span class="item-name">{{ item.name }}</span>
                <span v-if="index === currentStep" class="item-status">处理中...</span>
                <span v-else-if="index < currentStep" class="item-status">已完成</span>
                <span v-else class="item-status">等待中</span>
              </div>
            </div>
          </div>

          <div class="file-info-badge">
            <n-icon><DocumentTextOutline /></n-icon>
            <span>{{ fileCount }} 个文件</span>
          </div>
        </div>

        <!-- Complete State -->
        <div v-else class="complete-card">
          <div class="success-icon">
            <n-icon :size="48"><CheckmarkCircleOutline /></n-icon>
          </div>
          <h2>审查完成</h2>
          <p>已完成所有审查项目，发现 {{ issueCount }} 个问题</p>

          <div class="result-summary">
            <div class="summary-item">
              <span class="summary-value">{{ issueCount }}</span>
              <span class="summary-label">发现问题</span>
            </div>
            <div class="summary-item">
              <span class="summary-value">{{ riskCount }}</span>
              <span class="summary-label">风险预警</span>
            </div>
            <div class="summary-item">
              <span class="summary-value">{{ companyCount }}</span>
              <span class="summary-label">投标公司</span>
            </div>
          </div>

          <div class="action-buttons">
            <n-button @click="goToProject">查看项目详情</n-button>
            <n-button type="primary" @click="goToReport">查看审查报告</n-button>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { NIcon, NButton } from 'naive-ui'
import AppLayout from '@/components/layout/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import {
  CheckmarkOutline,
  DocumentTextOutline,
  CheckmarkCircleOutline
} from '@vicons/ionicons5'

const router = useRouter()

const currentStep = ref(0)
const isComplete = ref(false)
const fileCount = ref(3)
const issueCount = ref(12)
const riskCount = ref(2)
const companyCount = ref(3)

const reviewItems = [
  { key: 'parse', name: '文件解析' },
  { key: 'compliance', name: '合规检测' },
  { key: 'comparison', name: '响应比对' },
  { key: 'qualification', name: '资质核验' },
  { key: 'risk', name: '风险识别' },
  { key: 'report', name: '生成报告' }
]

const progressSubtitle = computed(() => {
  if (isComplete.value) return '所有审查项目已完成'
  return `${reviewItems[currentStep.value].name} - AI正在对文件进行多维度分析`
})

const simulateProgress = () => {
  const interval = setInterval(() => {
    if (currentStep.value < reviewItems.length - 1) {
      currentStep.value++
    } else {
      clearInterval(interval)
      setTimeout(() => {
        isComplete.value = true
      }, 500)
    }
  }, 800)
}

const goToProject = () => {
  router.push('/project/1')
}

const goToReport = () => {
  router.push('/report/1/full')
}

onMounted(() => {
  simulateProgress()
})
</script>

<style scoped lang="scss">
.workspace-progress-page {
  max-width: 600px;
  margin: 0 auto;
}

.progress-container {
  margin-top: 24px;
}

.progress-card,
.complete-card {
  background: #fff;
  border-radius: 12px;
  padding: 48px;
  text-align: center;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.spinner-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 32px;
}

.spinner {
  width: 80px;
  height: 80px;
  border: 4px solid var(--gray-200);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.mini-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid var(--gray-200);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.review-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
  text-align: left;
  max-width: 300px;
  margin: 0 auto 32px;
}

.review-item {
  display: flex;
  align-items: center;
  gap: 12px;
  opacity: 0.5;

  &.active {
    opacity: 1;
  }

  &.completed {
    opacity: 1;

    .item-name {
      color: var(--success-color);
    }
  }
}

.item-indicator {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.indicator-check {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--success-color);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.indicator-pending {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--gray-300);
}

.item-info {
  display: flex;
  flex-direction: column;
}

.item-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--gray-800);
}

.item-status {
  font-size: 12px;
  color: var(--gray-500);
}

.file-info-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: var(--gray-100);
  border-radius: 20px;
  font-size: 13px;
  color: var(--gray-600);
}

.success-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--success-bg);
  color: var(--success-color);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
}

.complete-card h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: var(--gray-800);
}

.complete-card p {
  margin: 8px 0 32px;
  font-size: 14px;
  color: var(--gray-500);
}

.result-summary {
  display: flex;
  justify-content: center;
  gap: 48px;
  margin-bottom: 32px;
  padding: 24px;
  background: var(--gray-100);
  border-radius: 12px;
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.summary-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--gray-800);
}

.summary-label {
  font-size: 13px;
  color: var(--gray-500);
  margin-top: 4px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
}
</style>
