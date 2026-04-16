<template>
  <div class="issue-list">
    <div class="list-header">
      <div class="header-left">
        <h3>问题列表</h3>
        <span class="issue-count" v-if="!loading">
          共 {{ filteredIssues.length }} 项
        </span>
      </div>

      <div class="header-right">
        <n-button
          v-if="severityFilter !== 'all'"
          text
          size="small"
          @click="$emit('clear-filter')"
        >
          清除筛选
        </n-button>
        <n-select
          v-model="localSeverityFilter"
          :options="severityOptions"
          size="small"
          style="width: 120px"
          @update:value="handleFilterChange"
        />
      </div>
    </div>

    <div class="list-content" v-loading="loading">
      <template v-if="filteredIssues.length > 0">
        <IssueCard
          v-for="issue in filteredIssues"
          :key="issue.id"
          :issue="issue"
          @click="$emit('issue-click', issue)"
        />
      </template>

      <div v-else-if="!loading" class="empty-state">
        <n-icon :size="48" depth="3">
          <CheckmarkCircleOutline />
        </n-icon>
        <p>暂无问题</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { NButton, NIcon, NSelect } from 'naive-ui'
import { CheckmarkCircleOutline } from '@vicons/ionicons5'
import IssueCard from './IssueCard.vue'

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

const props = withDefaults(defineProps<{
  issues: Issue[]
  loading?: boolean
  severityFilter?: string
}>(), {
  issues: () => [],
  loading: false,
  severityFilter: 'all'
})

const emit = defineEmits<{
  'issue-click': [issue: Issue]
  'clear-filter': []
  'filter-change': [severity: string]
}>()

const severityOptions = [
  { label: '全部', value: 'all' },
  { label: '严重', value: 'critical' },
  { label: '高风险', value: 'high' },
  { label: '中风险', value: 'medium' },
  { label: '低风险', value: 'low' }
]

const localSeverityFilter = ref(props.severityFilter)

watch(() => props.severityFilter, (newVal) => {
  localSeverityFilter.value = newVal
})

const filteredIssues = computed(() => {
  if (localSeverityFilter.value === 'all') {
    return props.issues
  }
  return props.issues.filter(
    issue => issue.severity === localSeverityFilter.value
  )
})

const handleFilterChange = (value: string) => {
  emit('filter-change', value)
}
</script>

<style scoped lang="scss">
.issue-list {
  background: #fff;
  border-radius: $radius-lg;
  overflow: hidden;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-lg $spacing-xl;
  border-bottom: 1px solid $gray-200;
}

.header-left {
  display: flex;
  align-items: center;
  gap: $spacing-md;

  h3 {
    margin: 0;
    font-size: $font-size-lg;
    font-weight: $font-weight-semibold;
    color: $gray-800;
  }

  .issue-count {
    font-size: $font-size-sm;
    color: $gray-500;
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
}

.list-content {
  padding: $spacing-lg;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $spacing-3xl;
  color: $gray-500;

  p {
    margin: $spacing-md 0 0 0;
    font-size: $font-size-sm;
  }
}
</style>
