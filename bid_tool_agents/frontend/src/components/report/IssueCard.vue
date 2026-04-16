<template>
  <div class="issue-card" :class="[`severity-${issue.severity}`, { expanded: isExpanded }]">
    <div class="card-header" @click="toggleExpand">
      <div class="header-left">
        <n-icon :size="18" :class="`severity-icon-${issue.severity}`">
          <AlertCircleOutline v-if="issue.severity === 'critical'" />
          <WarningOutline v-else-if="issue.severity === 'high'" />
          <InformationCircleOutline v-else />
        </n-icon>
        <div class="issue-info">
          <h4 class="issue-title">{{ issue.title }}</h4>
          <div class="issue-meta">
            <n-tag
              :type="getSeverityTagType(issue.severity)"
              size="small"
            >
              {{ getSeverityText(issue.severity) }}
            </n-tag>
            <span class="meta-divider" v-if="issue.location">
              <n-icon :size="12"><LocationOutline /></n-icon>
              {{ getLocationText(issue.location) }}
            </span>
          </div>
        </div>
      </div>

      <n-icon class="expand-icon" :size="20">
        <ChevronDownOutline />
      </n-icon>
    </div>

    <transition name="expand">
      <div v-if="isExpanded" class="card-body">
        <div class="section">
          <h5>问题描述</h5>
          <p>{{ issue.description }}</p>
        </div>

        <div class="section" v-if="issue.evidence">
          <h5>证据</h5>
          <div class="evidence-box">
            {{ issue.evidence }}
          </div>
        </div>

        <div class="section" v-if="issue.suggestion">
          <h5>整改建议</h5>
          <p class="suggestion">{{ issue.suggestion }}</p>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NIcon, NTag } from 'naive-ui'
import {
  AlertCircleOutline,
  WarningOutline,
  InformationCircleOutline,
  LocationOutline,
  ChevronDownOutline
} from '@vicons/ionicons5'

export interface Issue {
  id: string
  title: string
  description: string
  severity: 'critical' | 'high' | 'medium' | 'low'
  location?: {
    page?: number
    section?: string
    line?: number
  }
  suggestion?: string
  evidence?: string
}

const props = defineProps<{
  issue: Issue
}>()

const isExpanded = ref(false)

const toggleExpand = () => {
  isExpanded.value = !isExpanded.value
}

const getSeverityTagType = (severity: string): 'error' | 'warning' | 'info' | 'default' => {
  const typeMap = {
    critical: 'error',
    high: 'warning',
    medium: 'info',
    low: 'default'
  }
  return typeMap[severity] || 'default'
}

const getSeverityText = (severity: string): string => {
  const textMap = {
    critical: '严重',
    high: '高风险',
    medium: '中风险',
    low: '低风险'
  }
  return textMap[severity] || severity
}

const getLocationText = (location: Issue['location']): string => {
  if (!location) return ''
  const parts = []
  if (location.page) parts.push(`第${location.page}页`)
  if (location.section) parts.push(location.section)
  if (location.line) parts.push(`第${location.line}行`)
  return parts.join(' / ')
}
</script>

<style scoped lang="scss">
.issue-card {
  background: #fff;
  border: 1px solid $gray-200;
  border-radius: $radius-lg;
  overflow: hidden;
  transition: box-shadow $transition-base;

  &:hover {
    box-shadow: $shadow-md;
  }

  &.severity-critical {
    border-left: 3px solid $danger-color;
  }

  &.severity-high {
    border-left: 3px solid $warning-color;
  }

  &.severity-medium {
    border-left: 3px solid $primary-color;
  }

  &.severity-low {
    border-left: 3px solid $gray-400;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: $spacing-lg;
  cursor: pointer;
}

.header-left {
  display: flex;
  gap: $spacing-md;
}

.severity-icon-critical {
  color: $danger-color;
}

.severity-icon-high {
  color: $warning-color;
}

.severity-icon-medium {
  color: $primary-color;
}

.severity-icon-low {
  color: $gray-500;
}

.issue-info {
  .issue-title {
    margin: 0;
    font-size: $font-size-base;
    font-weight: $font-weight-medium;
    color: $gray-800;
  }
}

.issue-meta {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  margin-top: $spacing-xs;
}

.meta-divider {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
  font-size: $font-size-xs;
  color: $gray-500;
}

.expand-icon {
  color: $gray-400;
  transition: transform $transition-base;

  .expanded & {
    transform: rotate(180deg);
  }
}

.card-body {
  padding: 0 $spacing-lg $spacing-lg;
}

.section {
  padding-top: $spacing-md;

  h5 {
    margin: 0 0 $spacing-sm 0;
    font-size: $font-size-xs;
    font-weight: $font-weight-semibold;
    color: $gray-500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  p {
    margin: 0;
    font-size: $font-size-sm;
    color: $gray-700;
    line-height: 1.6;
  }
}

.evidence-box {
  background: $gray-100;
  padding: $spacing-md;
  border-radius: $radius-base;
  font-size: $font-size-sm;
  color: $gray-700;
  line-height: 1.6;
  font-family: monospace;
  white-space: pre-wrap;
  word-break: break-all;
}

.suggestion {
  color: $primary-color !important;
}

.expand-enter-active,
.expand-leave-active {
  transition: all $transition-base;
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
  padding-top: 0;
}

.expand-enter-to,
.expand-leave-from {
  opacity: 1;
  max-height: 500px;
}
</style>
