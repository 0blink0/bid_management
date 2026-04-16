<template>
  <div class="sensitive-words-table">
    <div class="table-header">
      <div class="header-left">
        <search-input
          v-model="searchValue"
          placeholder="搜索词条"
          @search="handleSearch"
        />
        <filter-select
          v-model="typeFilter"
          :options="typeOptions"
          placeholder="类型"
          @change="handleTypeChange"
        />
        <filter-select
          v-model="statusFilter"
          :options="statusOptions"
          placeholder="状态"
          @change="handleStatusChange"
        />
      </div>
      <div class="header-right">
        <n-button @click="handleExport">导出</n-button>
        <n-button @click="handleBatchImport">批量导入</n-button>
        <n-button type="primary" @click="handleAdd">
          <template #icon>
            <n-icon><add-outline /></n-icon>
          </template>
          新增词条
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
import { AddOutline, PencilOutline, TrashOutline, DownloadOutline, CloudUploadOutline } from '@vicons/ionicons5'
import DataTable from '@/components/common/DataTable.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import FilterSelect from '@/components/common/FilterSelect.vue'
import type { TableColumn } from '@/components/common/DataTable.vue'

interface SensitiveWord {
  id: string
  word: string
  type: '错别字' | '敏感词' | '不规范表述' | '禁用词'
  correctSuggestion: string
  severity: 'critical' | 'high' | 'medium'
  status: 'enabled' | 'disabled'
  category: string
  updatedAt: string
}

const loading = ref(false)
const searchValue = ref('')
const typeFilter = ref<string | number | null>(null)
const statusFilter = ref<string | number | null>(null)

const paginationConfig = ref({
  page: 1,
  pageSize: 10,
  total: 0
})

const typeOptions = [
  { label: '错别字', value: '错别字' },
  { label: '敏感词', value: '敏感词' },
  { label: '不规范表述', value: '不规范表述' },
  { label: '禁用词', value: '禁用词' }
]

const statusOptions = [
  { label: '启用', value: 'enabled' },
  { label: '禁用', value: 'disabled' }
]

const rowKey = (row: SensitiveWord) => row.id

const severityTagType = (severity: SensitiveWord['severity']): 'error' | 'warning' | 'info' => {
  const typeMap: Record<SensitiveWord['severity'], 'error' | 'warning' | 'info'> = {
    critical: 'error',
    high: 'warning',
    medium: 'info'
  }
  return typeMap[severity]
}

const severityText = (severity: SensitiveWord['severity']): string => {
  const textMap: Record<SensitiveWord['severity'], string> = {
    critical: '严重',
    high: '高',
    medium: '中'
  }
  return textMap[severity]
}

const columns = computed<TableColumn[]>(() => [
  {
    key: 'word',
    title: '词条',
    dataIndex: 'word',
    minWidth: 150,
    ellipsis: true
  },
  {
    key: 'type',
    title: '类型',
    dataIndex: 'type',
    width: 110,
    render: (row: SensitiveWord) => {
      return h(
        NTag,
        {
          type: row.type === '敏感词' ? 'error' : row.type === '禁用词' ? 'warning' : 'info',
          size: 'small',
          round: true
        },
        () => row.type
      )
    }
  },
  {
    key: 'correctSuggestion',
    title: '正确建议',
    dataIndex: 'correctSuggestion',
    minWidth: 150,
    ellipsis: true
  },
  {
    key: 'severity',
    title: '严重程度',
    dataIndex: 'severity',
    width: 100,
    render: (row: SensitiveWord) => {
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
    key: 'category',
    title: '分类',
    dataIndex: 'category',
    width: 100
  },
  {
    key: 'status',
    title: '状态',
    dataIndex: 'status',
    width: 90,
    render: (row: SensitiveWord) => {
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
    key: 'updatedAt',
    title: '更新时间',
    dataIndex: 'updatedAt',
    width: 120
  },
  {
    key: 'actions',
    title: '操作',
    width: 150,
    fixed: 'right',
    render: (row: SensitiveWord) => {
      return h('div', { class: 'action-buttons' }, [
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
            onClick: () => handleDelete(row)
          },
          () => h(NIcon, () => h(TrashOutline))
        )
      ])
    }
  }
])

const tableData = ref<SensitiveWord[]>([
  {
    id: '1',
    word: '投搞',
    type: '错别字',
    correctSuggestion: '投稿',
    severity: 'medium',
    status: 'enabled',
    category: '文字错误',
    updatedAt: '2026-03-15'
  },
  {
    id: '2',
    word: '领导',
    type: '不规范表述',
    correctSuggestion: '负责人/主管',
    severity: 'low',
    status: 'enabled',
    category: '称谓',
    updatedAt: '2026-03-10'
  },
  {
    id: '3',
    word: '必须',
    type: '敏感词',
    correctSuggestion: '应当/需要',
    severity: 'high',
    status: 'enabled',
    category: '强制性用语',
    updatedAt: '2026-03-08'
  }
])

const emit = defineEmits<{
  (e: 'edit', word: SensitiveWord): void
  (e: 'delete', word: SensitiveWord): void
  (e: 'add'): void
  (e: 'export'): void
  (e: 'batch-import'): void
  (e: 'search', keyword: string): void
  (e: 'filter-change', filters: { type?: string; status?: string }): void
  (e: 'page-change', page: number): void
}>()

const handleSearch = (keyword: string) => {
  emit('search', keyword)
}

const handleTypeChange = (value: string | number | null) => {
  emit('filter-change', { type: value as string | undefined })
}

const handleStatusChange = (value: string | number | null) => {
  emit('filter-change', { status: value as string | undefined })
}

const handlePageChange = (page: number) => {
  paginationConfig.value.page = page
  emit('page-change', page)
}

const handleEdit = (word: SensitiveWord) => {
  emit('edit', word)
}

const handleDelete = (word: SensitiveWord) => {
  emit('delete', word)
}

const handleAdd = () => {
  emit('add')
}

const handleExport = () => {
  emit('export')
}

const handleBatchImport = () => {
  emit('batch-import')
}
</script>

<style scoped lang="scss">
.sensitive-words-table {
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
