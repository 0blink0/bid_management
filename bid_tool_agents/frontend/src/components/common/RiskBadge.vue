<template>
  <span :class="['risk-badge', `risk-${level}`]">
    <n-icon :size="12">
      <AlertCircleOutline v-if="level === 'high'" />
      <WarningOutline v-else-if="level === 'medium'" />
      <CheckmarkCircleOutline v-else />
    </n-icon>
    <span>{{ levelText }}</span>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { NIcon } from 'naive-ui'
import { AlertCircleOutline, WarningOutline, CheckmarkCircleOutline } from '@vicons/ionicons5'

type RiskLevel = 'high' | 'medium' | 'low' | 'none'

const props = defineProps<{
  level: RiskLevel
}>()

const levelText = computed(() => {
  const textMap: Record<RiskLevel, string> = {
    high: '高风险',
    medium: '中风险',
    low: '低风险',
    none: '无风险'
  }
  return textMap[props.level] || props.level
})
</script>

<style scoped lang="scss">
.risk-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.risk-high {
  background-color: var(--danger-bg);
  color: var(--danger-color);
}

.risk-medium {
  background-color: var(--warning-bg);
  color: var(--warning-color);
}

.risk-low {
  background-color: rgba(24, 144, 255, 0.1);
  color: #1890ff;
}

.risk-none {
  background-color: var(--success-bg);
  color: var(--success-color);
}
</style>
