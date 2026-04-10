<template>
  <div class="task-progress">
    <!-- 状态概览 -->
    <div class="progress-header">
      <div class="task-info">
        <h3 class="task-title">{{ task.name }}</h3>
        <n-tag :type="statusType" size="small">{{ statusText }}</n-tag>
      </div>
      <div class="task-actions">
        <n-button
          v-if="task.status === 'running'"
          size="small"
          type="error"
          @click="handleStop"
        >
          终止
        </n-button>
        <n-button
          v-if="task.status === 'completed'"
          size="small"
          type="primary"
          @click="handleView"
        >
          查看结果
        </n-button>
      </div>
    </div>

    <!-- 步骤进度 -->
    <div class="steps-container">
      <n-steps :current="currentStep" size="small" vertical>
        <n-step
          v-for="step in task.steps"
          :key="step.key"
          :title="step.title"
          :description="step.description"
          :status="getStepStatus(step)"
        />
      </n-steps>
    </div>

    <!-- 进度条 -->
    <div v-if="task.status === 'running'" class="progress-bar-container">
      <n-progress
        type="line"
        :percentage="task.progress"
        :indicator-placement="'inside'"
        :status="progressStatus"
      />
      <span class="progress-text">
        {{ task.current || '' }} {{ task.eta ? `预计剩余 ${task.eta}` : '' }}
      </span>
    </div>

    <!-- 结果统计 -->
    <div v-if="task.result" class="result-summary">
      <n-grid :cols="4" x-gap="12">
        <n-gi v-for="(stat, key) in task.result.summary" :key="key">
          <div class="stat-card" :class="`stat-${key}`">
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </n-gi>
      </n-grid>
    </div>

    <!-- 错误信息 -->
    <div v-if="task.error" class="error-info">
      <n-alert type="error" :title="task.error.title">
        {{ task.error.message }}
      </n-alert>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Task, TaskStep } from '@/types/task'

const props = defineProps<{
  task: Task
}>()

const emit = defineEmits<{
  stop: []
  view: []
}>()

const statusText = computed(() => {
  const map: Record<string, string> = {
    pending: '等待中',
    running: '执行中',
    completed: '已完成',
    failed: '失败',
    cancelled: '已取消'
  }
  return map[props.task.status] || props.task.status
})

const statusType = computed(() => {
  const map: Record<string, any> = {
    pending: 'default',
    running: 'info',
    completed: 'success',
    failed: 'error',
    cancelled: 'warning'
  }
  return map[props.task.status] || 'default'
})

const progressStatus = computed(() => {
  if (props.task.progress >= 100) return 'success'
  if (props.task.status === 'failed') return 'error'
  return 'active'
})

const currentStep = computed(() => {
  const idx = props.task.steps.findIndex(s => s.status === 'running')
  return idx >= 0 ? idx : props.task.steps.length
})

const getStepStatus = (step: TaskStep) => {
  if (step.status === 'completed') return 'finish'
  if (step.status === 'running') return 'process'
  if (step.status === 'error') return 'error'
  return 'wait'
}

const handleStop = () => emit('stop')
const handleView = () => emit('view')
</script>

<style scoped lang="scss">
.task-progress {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;

  .task-title {
    margin: 0 0 4px 0;
    font-size: 16px;
  }

  .task-actions {
    display: flex;
    gap: 8px;
  }
}

.steps-container {
  margin-bottom: 16px;
  padding-left: 8px;
}

.progress-bar-container {
  margin-bottom: 16px;

  .progress-text {
    display: block;
    text-align: center;
    margin-top: 4px;
    font-size: 12px;
    color: #999;
  }
}

.result-summary {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.stat-card {
  padding: 12px;
  border-radius: 8px;
  text-align: center;

  &.stat-success {
    background: #f6ffed;
    .stat-value { color: #52c41a; }
  }

  &.stat-warning {
    background: #fffbe6;
    .stat-value { color: #faad14; }
  }

  &.stat-error {
    background: #fff2f0;
    .stat-value { color: #ff4d4f; }
  }

  &.stat-info {
    background: #e6f7ff;
    .stat-value { color: #1890ff; }
  }

  .stat-value {
    font-size: 24px;
    font-weight: 600;
  }

  .stat-label {
    font-size: 12px;
    color: #666;
    margin-top: 4px;
  }
}

.error-info {
  margin-top: 16px;
}
</style>
