<template>
  <div class="rules-table">
    <div class="table-header">
      <div class="header-left">
        <search-input
          v-model="searchValue"
          placeholder="搜索规则名称"
          @search="handleSearch"
        />
        <filter-select
          v-model="typeFilter"
          :options="typeOptions"
          placeholder="规则类型"
          @change="handleTypeChange"
        />
        <filter-select
          v-model="severityFilter"
          :options="severityOptions"
          placeholder="严重程度"
          @change="handleSeverityChange"
        />
        <filter-select
          v-model="statusFilter"
          :options="statusOptions"
          placeholder="状态"
          @change="handleStatusChange"
        />
      </div>
      <div class="header-right">
        <n-button @click="handleImport">导入</n-button>
        <n-button type="primary" @click="handleAdd">
          <template #icon>
            <n-icon><add-outline /></n-icon>
          </template>
          新增规则
        </n-button>
      </div>
    </div>

    <data-table
      :columns="columns"
      :data="tableData"
      :loading="loading"
      :pagination="paginationConfig"
      :row-key="rowKey"
      @page-change="handlePageChange"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, h } from 'vue'
import { NButton, NIcon, NTag } from 'naive-ui'
import { AddOutline, EyeOutline, PencilOutline, Toggle } from '@vicons/ionicons5'
import DataTable from '@/components/common/DataTable.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import FilterSelect from '@/components/common/FilterSelect.vue'
import type { TableColumn } from '@/components/common/DataTable.vue'

interface Rule {
  id: string
  name: string
  type: 'sensitive_words' | 'compliance' | 'completeness' | 'evaluation_method' | 'consistency'
  severity: 'critical' | 'high' | 'medium' | 'low'
  status: 'enabled' | 'disabled'
  checkTypes: string[]
  description: string
  updatedAt: string
}

const loading = ref(false)
const searchValue = ref('')
const typeFilter = ref<string | number | null>(null)
const severityFilter = ref<string | number | null>(null)
const statusFilter = ref<string | number | null>(null)

const paginationConfig = ref({
  page: 1,
  pageSize: 10,
  total: 0
})

const typeOptions = [
  { label: '错敏词', value: 'sensitive_words' },
  { label: '合规性', value: 'compliance' },
  { label: '完整性', value: 'completeness' },
  { label: '评标办法', value: 'evaluation_method' },
  { label: '一致性', value: 'consistency' }
]

const severityOptions = [
  { label: '严重', value: 'critical' },
  { label: '高', value: 'high' },
  { label: '中', value: 'medium' },
  { label: '低', value: 'low' }
]

const statusOptions = [
  { label: '已启用', value: 'enabled' },
  { label: '已禁用', value: 'disabled' }
]

const rowKey = (row: Rule) => row.id

const typeText = (type: Rule['type']): string => {
  const textMap: Record<Rule['type'], string> = {
    sensitive_words: '错敏词',
    compliance: '合规性',
    completeness: '完整性',
    evaluation_method: '评标办法',
    consistency: '一致性'
  }
  return textMap[type]
}

const severityTagType = (severity: Rule['severity']): 'error' | 'warning' | 'info' | 'default' => {
  const typeMap: Record<Rule['severity'], 'error' | 'warning' | 'info' | 'default'> = {
    critical: 'error',
    high: 'warning',
    medium: 'info',
    low: 'default'
  }
  return typeMap[severity]
}

const severityText = (severity: Rule['severity']): string => {
  const textMap: Record<Rule['severity'], string> = {
    critical: '严重',
    high: '高',
    medium: '中',
    low: '低'
  }
  return textMap[severity]
}

const columns = computed<TableColumn[]>(() => [
  {
    key: 'name',
    title: '规则名称',
    dataIndex: 'name',
    minWidth: 180,
    ellipsis: true
  },
  {
    key: 'type',
    title: '规则类型',
    dataIndex: 'type',
    width: 100,
    render: (row: Rule) => typeText(row.type)
  },
  {
    key: 'severity',
    title: '严重程度',
    dataIndex: 'severity',
    width: 100,
    render: (row: Rule) => {
      return h(
        NTag,
        {
          type: severityTagType(row.severity),
          size: 'small',
          round: true
        },
        () => severityText(row.severity)
      )
    }
  },
  {
    key: 'status',
    title: '状态',
    dataIndex: 'status',
    width: 90,
    render: (row: Rule) => {
      return h(
        NTag,
        {
          type: row.status === 'enabled' ? 'success' : 'default',
          size: 'small',
          round: true
        },
        () => row.status === 'enabled' ? '启用' : '禁用'
      )
    }
  },
  {
    key: 'description',
    title: '规则描述',
    dataIndex: 'description',
    minWidth: 200,
    ellipsis: true
  },
  {
    key: 'updatedAt',
    title: '更新时间',
    dataIndex: 'updatedAt',
    width: 120,
    sortable: true
  },
  {
    key: 'actions',
    title: '操作',
    width: 180,
    fixed: 'right',
    render: (row: Rule) => {
      return h('div', { class: 'action-buttons' }, [
        h(
          NButton,
          {
            size: 'small',
            text: true,
            onClick: () => handleView(row)
          },
          () => h(NIcon, () => h(EyeOutline))
        ),
        h(
          NButton,
          {
            size: 'small',
            text: true,
            onClick: () => handleEdit(row)
          },
          () => h(NIcon, () => h(PencilOutline))
        ),
        h(
          NButton,
          {
            size: 'small',
            text: true,
            onClick: () => handleToggle(row)
          },
          () => h(NIcon, () => h(Toggle))
        )
      ])
    }
  }
])

const tableData = ref<Rule[]>([
  {
    id: '1',
    name: '敏感词检测规则',
    type: 'sensitive_words',
    severity: 'critical',
    status: 'enabled',
    checkTypes: ['sensitive_words'],
    description: '检测文档中的敏感词汇',
    updatedAt: '2026-03-15'
  },
  {
    id: '2',
    name: '法规引用完整性检查',
    type: 'compliance',
    severity: 'high',
    status: 'enabled',
    checkTypes: ['compliance'],
    description: '检查法规引用是否完整准确',
    updatedAt: '2026-03-10'
  },
  {
    id: '3',
    name: '评标办法格式检查',
    type: 'evaluation_method',
    severity: 'medium',
    status: 'enabled',
    checkTypes: ['evaluation_method'],
    description: '检查评标办法格式是否符合要求',
    updatedAt: '2026-03-08'
  }
])

const emit = defineEmits<{
  (e: 'view', rule: Rule): void
  (e: 'edit', rule: Rule): void
  (e: 'add'): void
  (e: 'import'): void
  (e: 'toggle', rule: Rule): void
  (e: 'search', keyword: string): void
  (e: 'filter-change', filters: { type?: string; severity?: string; status?: string }): void
  (e: 'page-change', page: number): void
}>()

const handleSearch = (keyword: string) => {
  emit('search', keyword)
}

const handleTypeChange = (value: string | number | null) => {
  emit('filter-change', { type: value as string | undefined })
}

const handleSeverityChange = (value: string | number | null) => {
  emit('filter-change', { severity: value as string | undefined })
}

const handleStatusChange = (value: string | number | null) => {
  emit('filter-change', { status: value as string | undefined })
}

const handlePageChange = (page: number) => {
  paginationConfig.value.page = page
  emit('page-change', page)
}

const handleView = (rule: Rule) => {
  emit('view', rule)
}

const handleEdit = (rule: Rule) => {
  emit('edit', rule)
}

const handleAdd = () => {
  emit('add')
}

const handleImport = () => {
  emit('import')
}

const handleToggle = (rule: Rule) => {
  emit('toggle', rule)
}
</script>

<style scoped lang="scss">
.rules-table {
  .table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    flex-wrap: wrap;
    gap: 12px;

    .header-left {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }

    .header-right {
      display: flex;
      gap: 8px;
    }
  }

  :deep(.action-buttons) {
    display: flex;
    gap: 8px;
  }
}
</style>
