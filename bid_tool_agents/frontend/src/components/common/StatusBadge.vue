<template>
  <span :class="['status-badge', `status-${status}`]">
    <span class="status-dot"></span>
    <span class="status-text">{{ statusText }}</span>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

type StatusType = 'success' | 'warning' | 'danger' | 'info' | 'default'

const props = defineProps<{
  status: StatusType
  text?: string
}>()

const statusText = computed(() => {
  if (props.text) return props.text

  const textMap: Record<StatusType, string> = {
    success: '通过',
    warning: '警告',
    danger: '危险',
    info: '进行中',
    default: '默认'
  }
  return textMap[props.status] || props.status
})
</script>

<style scoped lang="scss">
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-success {
  background-color: var(--success-bg);
  color: var(--success-color);

  .status-dot {
    background-color: var(--success-color);
  }
}

.status-warning {
  background-color: var(--warning-bg);
  color: var(--warning-color);

  .status-dot {
    background-color: var(--warning-color);
  }
}

.status-danger {
  background-color: var(--danger-bg);
  color: var(--danger-color);

  .status-dot {
    background-color: var(--danger-color);
  }
}

.status-info {
  background-color: var(--primary-bg);
  color: var(--primary-color);

  .status-dot {
    background-color: var(--primary-color);
  }
}

.status-default {
  background-color: var(--gray-200);
  color: var(--gray-600);

  .status-dot {
    background-color: var(--gray-500);
  }
}
</style>
