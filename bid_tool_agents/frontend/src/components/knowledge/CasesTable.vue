<template>
  <div class="cases-table">
    <div class="table-header">
      <div class="header-left">
        <search-input
          v-model="searchValue"
          placeholder="搜索案例名称"
          @search="handleSearch"
        />
        <filter-select
          v-model="typeFilter"
          :options="typeOptions"
          placeholder="案例类型"
          @change="handleTypeChange"
        />
        <filter-select
          v-model="riskLevelFilter"
          :options="riskLevelOptions"
          placeholder="风险等级"
          @change="handleRiskLevelChange"
        />
      </div>
      <div class="header-right">
        <n-button type="primary" @click="handleAdd">
          <template #icon>
            <n-icon><add-outline /></n-icon>
          </template>
          新增案例
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
import { AddOutline, EyeOutline, PencilOutline } from '@vicons/ionicons5'
import DataTable from '@/components/common/DataTable.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import FilterSelect from '@/components/common/FilterSelect.vue'
import type { TableColumn } from '@/components/common/DataTable.vue'

interface Case {
  id: string
  name: string
  type: '违规' | '处罚' | '整改' | '典型'
  riskLevel: 'critical' | 'high' | 'medium' | 'low'
  relatedBidSections: string[]
  description: string
  outcome: string
  caseDate: string
  source: string
}

const loading = ref(false)
const searchValue = ref('')
const typeFilter = ref<string | number | null>(null)
const riskLevelFilter = ref<string | number | null>(null)

const paginationConfig = ref({
  page: 1,
  pageSize: 10,
  total: 0
})

const typeOptions = [
  { label: '违规案例', value: '违规' },
  { label: '处罚案例', value: '处罚' },
  { label: '整改案例', value: '整改' },
  { label: '典型案例', value: '典型' }
]

const riskLevelOptions = [
  { label: '严重', value: 'critical' },
  { label: '高', value: 'high' },
  { label: '中', value: 'medium' },
  { label: '低', value: 'low' }
]

const rowKey = (row: Case) => row.id

const riskLevelTagType = (level: Case['riskLevel']): 'error' | 'warning' | 'info' | 'default' => {
  const typeMap: Record<Case['riskLevel'], 'error' | 'warning' | 'info' | 'default'> = {
    critical: 'error',
    high: 'warning',
    medium: 'info',
    low: 'default'
  }
  return typeMap[level]
}

const riskLevelText = (level: Case['riskLevel']): string => {
  const textMap: Record<Case['riskLevel'], string> = {
    critical: '严重',
    high: '高',
    medium: '中',
    low: '低'
  }
  return textMap[level]
}

const columns = computed<TableColumn[]>(() => [
  {
    key: 'name',
    title: '案例名称',
    dataIndex: 'name',
    minWidth: 200,
    ellipsis: true
  },
  {
    key: 'type',
    title: '类型',
    dataIndex: 'type',
    width: 100,
    render: (row: Case) => {
      return h(
        NTag,
        {
          type: row.type === '处罚' ? 'error' : row.type === '典型' ? 'success' : 'info',
          size: 'small',
          round: true
        },
        () => row.type
      )
    }
  },
  {
    key: 'riskLevel',
    title: '风险等级',
    dataIndex: 'riskLevel',
    width: 100,
    render: (row: Case) => {
      return h(
        NTag,
        {
          type: riskLevelTagType(row.riskLevel),
          size: 'small',
          round: true
        },
        () => riskLevelText(row.riskLevel)
      )
    }
  },
  {
    key: 'relatedBidSections',
    title: '相关标段',
    dataIndex: 'relatedBidSections',
    width: 150,
    ellipsis: true,
    render: (row: Case) => row.relatedBidSections.join(', ') || '-'
  },
  {
    key: 'description',
    title: '案例描述',
    dataIndex: 'description',
    minWidth: 200,
    ellipsis: true
  },
  {
    key: 'outcome',
    title: '处理结果',
    dataIndex: 'outcome',
    minWidth: 150,
    ellipsis: true
  },
  {
    key: 'caseDate',
    title: '案例日期',
    dataIndex: 'caseDate',
    width: 120,
    sortable: true
  },
  {
    key: 'actions',
    title: '操作',
    width: 120,
    fixed: 'right',
    render: (row: Case) => {
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
        )
      ])
    }
  }
])

const tableData = ref<Case[]>([
  {
    id: '1',
    name: '某公司串通投标案',
    type: '违规',
    riskLevel: 'critical',
    relatedBidSections: ['标段A', '标段B'],
    description: '经查实，三家投标单位存在串通投标行为',
    outcome: '取消中标资格，罚款50万元',
    caseDate: '2025-12-15',
    source: '市公共资源交易中心'
  },
  {
    id: '2',
    name: '专家评分异常案',
    type: '典型',
    riskLevel: 'high',
    relatedBidSections: ['标段C'],
    description: '专家打分偏离正常范围，涉嫌违规操作',
    outcome: '重新组织评审',
    caseDate: '2025-11-20',
    source: '省政府采购中心'
  },
  {
    id: '3',
    name: '资质造假处罚案',
    type: '处罚',
    riskLevel: 'critical',
    relatedBidSections: ['标段D'],
    description: '投标单位伪造资质证书',
    outcome: '三年内禁止参与政府采购活动',
    caseDate: '2025-10-08',
    source: '财政部'
  }
])

const emit = defineEmits<{
  (e: 'view', caseItem: Case): void
  (e: 'edit', caseItem: Case): void
  (e: 'add'): void
  (e: 'search', keyword: string): void
  (e: 'filter-change', filters: { type?: string; riskLevel?: string }): void
  (e: 'page-change', page: number): void
}>()

const handleSearch = (keyword: string) => {
  emit('search', keyword)
}

const handleTypeChange = (value: string | number | null) => {
  emit('filter-change', { type: value as string | undefined })
}

const handleRiskLevelChange = (value: string | number | null) => {
  emit('filter-change', { riskLevel: value as string | undefined })
}

const handlePageChange = (page: number) => {
  paginationConfig.value.page = page
  emit('page-change', page)
}

const handleView = (caseItem: Case) => {
  emit('view', caseItem)
}

const handleEdit = (caseItem: Case) => {
  emit('edit', caseItem)
}

const handleAdd = () => {
  emit('add')
}
</script>

<style scoped lang="scss">
.cases-table {
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
