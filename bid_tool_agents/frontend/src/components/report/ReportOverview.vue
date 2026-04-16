<template>
  <div class="report-overview">
    <div class="overview-header">
      <div class="score-section">
        <div class="score-ring" :class="statusClass">
          <svg viewBox="0 0 100 100">
            <circle
              class="ring-bg"
              cx="50"
              cy="50"
              r="45"
              fill="none"
              stroke-width="10"
            />
            <circle
              class="ring-progress"
              cx="50"
              cy="50"
              r="45"
              fill="none"
              stroke-width="10"
              :stroke-dasharray="circumference"
              :stroke-dashoffset="progressOffset"
            />
          </svg>
          <div class="score-content">
            <span class="score-value">{{ score }}</span>
            <span class="score-label">分</span>
          </div>
        </div>
        <div class="status-badge" :class="statusClass">
          <n-icon :size="16">
            <CheckmarkCircleOutline v-if="status === 'pass'" />
            <WarningOutline v-else-if="status === 'warning'" />
            <AlertCircleOutline v-else />
          </n-icon>
          <span>{{ statusText }}</span>
        </div>
      </div>

      <div class="breakdown-section" v-if="breakdown && Object.keys(breakdown).length">
        <h4>分项得分</h4>
        <div class="breakdown-list">
          <div
            v-for="(item, key) in breakdown"
            :key="key"
            class="breakdown-item"
          >
            <div class="item-header">
              <span class="item-name">{{ getItemName(key) }}</span>
              <span class="item-score">{{ item.score ?? item }}</span>
            </div>
            <div class="progress-bar">
              <div
                class="progress-fill"
                :class="getProgressClass(item.score ?? item)"
                :style="{ width: getProgressWidth(item.score ?? item) + '%' }"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="overview-footer" v-if="summary">
      <div class="summary-item" v-for="(value, key) in summary" :key="key">
        <span class="summary-label">{{ getSummaryLabel(key) }}</span>
        <span class="summary-value">{{ value }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { NIcon } from 'naive-ui'
import {
  CheckmarkCircleOutline,
  WarningOutline,
  AlertCircleOutline
} from '@vicons/ionicons5'

interface Breakdown {
  [key: string]: {
    score: number
    maxScore?: number
  } | number
}

interface Summary {
  totalIssues?: number
  criticalIssues?: number
  highIssues?: number
  mediumIssues?: number
  lowIssues?: number
}

const props = withDefaults(defineProps<{
  score: number
  breakdown?: Breakdown
  status?: 'pass' | 'warning' | 'fail'
  summary?: Summary
}>(), {
  score: 0,
  status: 'warning'
})

const circumference = 2 * Math.PI * 45

const progressOffset = computed(() => {
  const progress = Math.min(Math.max(props.score, 0), 100) / 100
  return circumference * (1 - progress)
})

const statusClass = computed(() => `status-${props.status}`)

const statusText = computed(() => {
  const textMap = {
    pass: '通过',
    warning: '警告',
    fail: '不合格'
  }
  return textMap[props.status] || props.status
})

const getItemName = (key: string): string => {
  const nameMap: Record<string, string> = {
    compliance: '合规性',
    completeness: '完整性',
    accuracy: '准确性',
    consistency: '一致性',
    responsiveness: '响应性',
    qualification: '资质核验',
    risk: '风险评估'
  }
  return nameMap[key] || key
}

const getProgressClass = (value: number): string => {
  if (value >= 80) return 'progress-high'
  if (value >= 60) return 'progress-medium'
  return 'progress-low'
}

const getProgressWidth = (value: number): number => {
  return Math.min(Math.max(value, 0), 100)
}

const getSummaryLabel = (key: string): string => {
  const labelMap: Record<string, string> = {
    totalIssues: '问题总数',
    criticalIssues: '严重问题',
    highIssues: '高风险问题',
    mediumIssues: '中风险问题',
    lowIssues: '低风险问题'
  }
  return labelMap[key] || key
}
</script>

<style scoped lang="scss">
.report-overview {
  background: #fff;
  border-radius: $radius-lg;
  padding: $spacing-xl;
  box-shadow: $shadow-sm;
}

.overview-header {
  display: flex;
  gap: $spacing-2xl;
}

.score-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $spacing-md;
}

.score-ring {
  position: relative;
  width: 160px;
  height: 160px;

  svg {
    transform: rotate(-90deg);
    width: 100%;
    height: 100%;
  }

  .ring-bg {
    stroke: $gray-200;
  }

  .ring-progress {
    stroke: $gray-400;
    transition: stroke-dashoffset 0.6s ease;
  }

  &.status-pass .ring-progress {
    stroke: $success-color;
  }

  &.status-warning .ring-progress {
    stroke: $warning-color;
  }

  &.status-fail .ring-progress {
    stroke: $danger-color;
  }
}

.score-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;

  .score-value {
    font-size: $font-size-3xl;
    font-weight: $font-weight-bold;
    color: $gray-800;
  }

  .score-label {
    font-size: $font-size-sm;
    color: $gray-500;
    margin-left: 2px;
  }
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: $spacing-xs;
  padding: $spacing-xs $spacing-md;
  border-radius: $radius-full;
  font-size: $font-size-sm;
  font-weight: $font-weight-medium;

  &.status-pass {
    background: $success-bg;
    color: $success-color;
  }

  &.status-warning {
    background: $warning-bg;
    color: $warning-color;
  }

  &.status-fail {
    background: $danger-bg;
    color: $danger-color;
  }
}

.breakdown-section {
  flex: 1;
  padding-left: $spacing-xl;
  border-left: 1px solid $gray-200;

  h4 {
    margin: 0 0 $spacing-lg 0;
    font-size: $font-size-base;
    font-weight: $font-weight-semibold;
    color: $gray-700;
  }
}

.breakdown-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.breakdown-item {
  .item-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: $spacing-xs;
    font-size: $font-size-sm;
  }

  .item-name {
    color: $gray-600;
  }

  .item-score {
    font-weight: $font-weight-semibold;
    color: $gray-800;
  }
}

.progress-bar {
  height: 6px;
  background: $gray-200;
  border-radius: $radius-full;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: $radius-full;
  transition: width 0.4s ease;

  &.progress-high {
    background: $success-color;
  }

  &.progress-medium {
    background: $warning-color;
  }

  &.progress-low {
    background: $danger-color;
  }
}

.overview-footer {
  display: flex;
  gap: $spacing-2xl;
  margin-top: $spacing-xl;
  padding-top: $spacing-lg;
  border-top: 1px solid $gray-200;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: $spacing-xs;

  .summary-label {
    font-size: $font-size-xs;
    color: $gray-500;
  }

  .summary-value {
    font-size: $font-size-lg;
    font-weight: $font-weight-semibold;
    color: $gray-800;
  }
}
</style>
