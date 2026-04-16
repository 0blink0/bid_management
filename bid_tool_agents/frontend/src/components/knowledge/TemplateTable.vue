<template>
  <div class="template-table">
    <div class="table-header">
      <div class="header-left">
        <search-input
          v-model="searchValue"
          placeholder="搜索模板名称"
          @search="handleSearch"
        />
        <filter-select
          v-model="typeFilter"
          :options="typeOptions"
          placeholder="模板类型"
          @change="handleTypeChange"
        />
        <filter-select
          v-model="sceneFilter"
          :options="sceneOptions"
          placeholder="适用场景"
          @change="handleSceneChange"
        />
      </div>
      <div class="header-right">
        <n-button @click="handleUpload">上传模板</n-button>
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
import { NButton, NIcon } from 'naive-ui'
import { CloudUploadOutline, EyeOutline, DownloadOutline, PencilOutline } from '@vicons/ionicons5'
import DataTable from '@/components/common/DataTable.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import FilterSelect from '@/components/common/FilterSelect.vue'
import type { TableColumn } from '@/components/common/DataTable.vue'

interface Template {
  id: string
  name: string
  type: 'word' | 'excel' | 'pdf' | 'other'
  scene: string
  description: string
  fileSize: string
  downloadCount: number
  updatedAt: string
  updatedBy: string
}

const loading = ref(false)
const searchValue = ref('')
const typeFilter = ref<string | number | null>(null)
const sceneFilter = ref<string | number | null>(null)

const paginationConfig = ref({
  page: 1,
  pageSize: 10,
  total: 0
})

const typeOptions = [
  { label: 'Word文档', value: 'word' },
  { label: 'Excel表格', value: 'excel' },
  { label: 'PDF文档', value: 'pdf' },
  { label: '其他', value: 'other' }
]

const sceneOptions = [
  { label: '招标文件', value: '招标文件' },
  { label: '投标文件', value: '投标文件' },
  { label: '评标报告', value: '评标报告' },
  { label: '合同模板', value: '合同模板' }
]

const rowKey = (row: Template) => row.id

const typeText = (type: Template['type']): string => {
  const textMap: Record<Template['type'], string> = {
    word: 'Word',
    excel: 'Excel',
    pdf: 'PDF',
    other: '其他'
  }
  return textMap[type]
}

const typeTagType = (type: Template['type']): 'success' | 'warning' | 'error' | 'default' => {
  const typeMap: Record<Template['type'], 'success' | 'warning' | 'error' | 'default'> = {
    word: 'success',
    excel: 'warning',
    pdf: 'error',
    other: 'default'
  }
  return typeMap[type]
}

const columns = computed<TableColumn[]>(() => [
  {
    key: 'name',
    title: '模板名称',
    dataIndex: 'name',
    minWidth: 200,
    ellipsis: true
  },
  {
    key: 'type',
    title: '类型',
    dataIndex: 'type',
    width: 100,
    render: (row: Template) => {
      return h(
        'span',
        { class: `type-badge type-${row.type}` },
        typeText(row.type)
      )
    }
  },
  {
    key: 'scene',
    title: '适用场景',
    dataIndex: 'scene',
    width: 120
  },
  {
    key: 'description',
    title: '描述',
    dataIndex: 'description',
    minWidth: 180,
    ellipsis: true
  },
  {
    key: 'fileSize',
    title: '文件大小',
    dataIndex: 'fileSize',
    width: 100
  },
  {
    key: 'downloadCount',
    title: '下载次数',
    dataIndex: 'downloadCount',
    width: 100
  },
  {
    key: 'updatedAt',
    title: '更新时间',
    dataIndex: 'updatedAt',
    width: 120,
    sortable: true
  },
  {
    key: 'updatedBy',
    title: '更新人',
    dataIndex: 'updatedBy',
    width: 100
  },
  {
    key: 'actions',
    title: '操作',
    width: 180,
    fixed: 'right',
    render: (row: Template) => {
      return h('div', { class: 'action-buttons' }, [
        h(
          NButton,
          {
            size: 'small',
            text: true,
            onClick: () => handlePreview(row)
          },
          () => h(NIcon, () => h(EyeOutline))
        ),
        h(
          NButton,
          {
            size: 'small',
            text: true,
            onClick: () => handleDownload(row)
          },
          () => h(NIcon, () => h(DownloadOutline))
        ),
        h(
          NButton,
          {
            size: 'small',
            text: true,
            onClick: () => handleEdit(row)
          },
          () => h(NIcon, () => h(PencilOutline))
        )
      ])
    }
  }
])

const tableData = ref<Template[]>([
  {
    id: '1',
    name: '标准招标文件模板',
    type: 'word',
    scene: '招标文件',
    description: '适用于一般政府采购项目的标准招标文件模板',
    fileSize: '2.5MB',
    downloadCount: 156,
    updatedAt: '2026-03-15',
    updatedBy: '张三'
  },
  {
    id: '2',
    name: '投标函模板',
    type: 'word',
    scene: '投标文件',
    description: '标准投标函格式模板',
    fileSize: '156KB',
    downloadCount: 89,
    updatedAt: '2026-03-10',
    updatedBy: '李四'
  },
  {
    id: '3',
    name: '评标打分表',
    type: 'excel',
    scene: '评标报告',
    description: '综合评分法打分表模板',
    fileSize: '320KB',
    downloadCount: 45,
    updatedAt: '2026-03-08',
    updatedBy: '王五'
  }
])

const emit = defineEmits<{
  (e: 'preview', template: Template): void
  (e: 'download', template: Template): void
  (e: 'edit', template: Template): void
  (e: 'upload'): void
  (e: 'search', keyword: string): void
  (e: 'filter-change', filters: { type?: string; scene?: string }): void
  (e: 'page-change', page: number): void
}>()

const handleSearch = (keyword: string) => {
  emit('search', keyword)
}

const handleTypeChange = (value: string | number | null) => {
  emit('filter-change', { type: value as string | undefined })
}

const handleSceneChange = (value: string | number | null) => {
  emit('filter-change', { scene: value as string | undefined })
}

const handlePageChange = (page: number) => {
  paginationConfig.value.page = page
  emit('page-change', page)
}

const handlePreview = (template: Template) => {
  emit('preview', template)
}

const handleDownload = (template: Template) => {
  emit('download', template)
}

const handleEdit = (template: Template) => {
  emit('edit', template)
}

const handleUpload = () => {
  emit('upload')
}
</script>

<style scoped lang="scss">
.template-table {
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

  :deep(.type-badge) {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 12px;

    &.type-word {
      background-color: var(--primary-bg);
      color: var(--primary-color);
    }

    &.type-excel {
      background-color: var(--success-bg);
      color: var(--success-color);
    }

    &.type-pdf {
      background-color: var(--danger-bg);
      color: var(--danger-color);
    }

    &.type-other {
      background-color: var(--gray-200);
      color: var(--gray-600);
    }
  }
}
</style>
