<template>
  <div class="stat-card">
    <div class="stat-icon" :style="{ backgroundColor: iconBgColor }">
      <n-icon :size="24" :color="iconColor">
        <component :is="icon" />
      </n-icon>
    </div>
    <div class="stat-content">
      <div class="stat-value">{{ value }}</div>
      <div class="stat-label">{{ label }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { NIcon } from 'naive-ui'
import type { Component } from 'vue'

const props = defineProps<{
  value: string | number
  label: string
  icon: Component
  color?: 'primary' | 'success' | 'warning' | 'danger' | 'purple'
}>()

const colorMap = {
  primary: { bg: 'rgba(30, 90, 168, 0.1)', color: '#1E5AA8' },
  success: { bg: 'rgba(82, 196, 26, 0.1)', color: '#52c41a' },
  warning: { bg: 'rgba(250, 173, 20, 0.1)', color: '#faad14' },
  danger: { bg: 'rgba(255, 77, 79, 0.1)', color: '#ff4d4f' },
  purple: { bg: 'rgba(114, 46, 209, 0.1)', color: '#722ed1' }
}

const iconBgColor = computed(() => colorMap[props.color || 'primary'].bg)
const iconColor = computed(() => colorMap[props.color || 'primary'].color)
</script>

<style scoped lang="scss">
.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 8px;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--gray-800);
  line-height: 1;
}

.stat-label {
  font-size: 13px;
  color: var(--gray-500);
}
</style>
