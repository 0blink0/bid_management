<template>
  <AppLayout>
    <div class="workspace-processing-page">
      <PageHeader
        title="正在智能审查中"
        subtitle="预计需要 3 分钟左右"
        back-link="/workspace/new"
      />

      <div class="processing-container">
        <div class="progress-card">
          <div class="progress-steps">
            <div
              v-for="(step, index) in steps"
              :key="step.key"
              class="step-item"
            >
              <div class="step-label">{{ step.label }}</div>
              <div class="step-bar-wrapper">
                <div
                  class="step-bar"
                  :style="{ width: getStepProgress(index) + '%' }"
                ></div>
              </div>
              <div class="step-status">
                <span v-if="index < currentStep" class="status-complete">完成</span>
                <span v-else-if="index === currentStep" class="status-processing">
                  {{ currentProgress }}%
                </span>
                <span v-else class="status-pending">等待</span>
              </div>
            </div>
          </div>

          <div class="action-buttons">
            <n-button @click="goToReport">查看报告</n-button>
            <n-button type="error" @click="showCancelModal = true">取消审查</n-button>
          </div>
        </div>
      </div>

      <!-- Cancel Modal -->
      <Modal
        v-model:show="showCancelModal"
        title="确认取消"
        width="400px"
        :mask-closable="true"
      >
        <div class="cancel-modal-content">
          <div class="warning-icon">
            <n-icon :size="48"><AlertCircleOutline /></n-icon>
          </div>
          <p>确认取消本次审查？</p>
          <p class="hint">取消后可在草稿箱中继续编辑</p>
        </div>
        <template #footer>
          <n-button @click="showCancelModal = false">继续审查</n-button>
          <n-button type="error" @click="confirmCancel">确认取消</n-button>
        </template>
      </Modal>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { NButton, NIcon } from 'naive-ui'
import AppLayout from '@/components/layout/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import Modal from '@/components/common/Modal.vue'
import { AlertCircleOutline } from '@vicons/ionicons5'

const router = useRouter()

const showCancelModal = ref(false)

const steps = [
  { key: 'parse', label: '文件解析' },
  { key: 'compliance', label: '合规检测' },
  { key: 'comparison', label: '响应比对' },
  { key: 'qualification', label: '资质核验' },
  { key: 'risk', label: '风险识别' },
  { key: 'report', label: '生成报告' }
]

const currentStep = ref(1)
const currentProgress = ref(78)

const getStepProgress = (index: number) => {
  if (index < currentStep.value) return 100
  if (index === currentStep.value) return currentProgress.value
  return 0
}

const goToReport = () => {
  router.push('/report/1')
}

const confirmCancel = () => {
  showCancelModal.value = false
  router.push('/workspace/new')
}
</script>

<style scoped lang="scss">
.workspace-processing-page {
  max-width: 600px;
  margin: 0 auto;
}

.processing-container {
  margin-top: 24px;
}

.progress-card {
  background: #fff;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.progress-steps {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.step-label {
  width: 80px;
  font-size: 13px;
  color: var(--gray-700);
}

.step-bar-wrapper {
  flex: 1;
  height: 8px;
  background: var(--gray-200);
  border-radius: 4px;
  overflow: hidden;
}

.step-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
  border-radius: 4px;
  transition: width 0.3s ease;
}

.step-status {
  width: 60px;
  text-align: right;
  font-size: 12px;
}

.status-complete {
  color: var(--success-color);
}

.status-processing {
  color: var(--primary-color);
  font-weight: 500;
}

.status-pending {
  color: var(--gray-400);
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--gray-200);
}

.cancel-modal-content {
  text-align: center;
  padding: 16px 0;
}

.warning-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--danger-bg);
  color: var(--danger-color);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.cancel-modal-content p {
  margin: 0;
  font-size: 16px;
  color: var(--gray-800);
}

.cancel-modal-content .hint {
  font-size: 13px;
  color: var(--gray-500);
  margin-top: 8px;
}
</style>
