<template>
  <div class="progress-steps">
    <div
      v-for="(step, index) in steps"
      :key="index"
      :class="[
        'step-item',
        {
          'step-active': index === currentStep,
          'step-completed': index < currentStep,
          'step-pending': index > currentStep
        }
      ]"
    >
      <div class="step-indicator">
        <div class="step-icon">
          <n-icon v-if="index < currentStep"><CheckmarkOutline /></n-icon>
          <span v-else>{{ index + 1 }}</span>
        </div>
        <div v-if="index < steps.length - 1" class="step-line"></div>
      </div>
      <div class="step-content">
        <div class="step-title">{{ step.title }}</div>
        <div v-if="step.description" class="step-description">{{ step.description }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { NIcon } from 'naive-ui'
import { CheckmarkOutline } from '@vicons/ionicons5'

defineProps<{
  steps: Array<{
    title: string
    description?: string
  }>
  currentStep: number
}>()
</script>

<style scoped lang="scss">
.progress-steps {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.step-item {
  display: flex;
  gap: 16px;
}

.step-indicator {
  display: flex;
  align-items: flex-start;
}

.step-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
}

.step-line {
  width: 2px;
  height: 40px;
  margin: 4px 13px;
  background-color: var(--gray-300);
}

.step-completed {
  .step-icon {
    background-color: var(--success-color);
    color: #fff;
  }

  .step-line {
    background-color: var(--success-color);
  }
}

.step-active {
  .step-icon {
    background-color: var(--primary-color);
    color: #fff;
  }
}

.step-pending {
  .step-icon {
    background-color: var(--gray-200);
    color: var(--gray-500);
  }
}

.step-content {
  padding-bottom: 24px;
}

.step-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--gray-800);
}

.step-pending .step-title {
  color: var(--gray-500);
}

.step-description {
  font-size: 12px;
  color: var(--gray-500);
  margin-top: 4px;
}
</style>
