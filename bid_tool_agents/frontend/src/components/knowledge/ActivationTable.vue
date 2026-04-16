<template>
  <div class="activation-table">
    <div class="table-header">
      <div class="header-left">
        <search-input
          v-model="searchValue"
          placeholder="搜索规则名称"
          @search="handleSearch"
        />
        <filter-select
          v-model="scopeFilter"
          :options="scopeOptions"
          placeholder="适用范围"
          @change="handleScopeChange"
        />
        <filter-select
          v-model="statusFilter"
          :options="statusOptions"
          placeholder="状态"
          @change="handleStatusChange"
        />
      </div>
      <div class="header-right">
        <n-button @click="handleHistory">生效历史</n-button>
        <n-button type="primary" @click="handleActivate">
          <template #icon>
            <n-icon><play-outline /></n-icon>
          </template>
          激活规则
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
import { NButton, NIcon, NSwitch, NTag } from 'naive-ui'
import { PlayOutline, TimeOutline, PauseOutline } from '@vicons/ionicons5'
import DataTable from '@/components/common/DataTable.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import FilterSelect from '@/components/common/FilterSelect.vue'
import type { TableColumn } from '@/components/common/DataTable.vue'

interface ActivationRule {
  id: string
  ruleId: string
  ruleName: string
  ruleType: string
  effectiveTime: string
  expireTime: string | null
  scope: 'all' | 'government' | 'engineering' | 'service'
  status: 'active' | 'inactive' | 'pending'
  activatedBy: string
  activatedAt: string
}

const loading = ref(false)
const searchValue = ref('')
const scopeFilter = ref<string | number | null>(null)
const statusFilter = ref<string | number | null>(null)

const paginationConfig = ref({
  page: 1,
  pageSize: 10,
  total: 0
})

const scopeOptions = [
  { label: '全部项目', value: 'all' },
  { label: '政府采购', value: 'government' },
  { label: '工程建设', value: 'engineering' },
  { label: '服务类', value: 'service' }
]

const statusOptions = [
  { label: '已激活', value: 'active' },
  { label: '已停用', value: 'inactive' },
  { label: '待生效', value: 'pending' }
]

const rowKey = (row: ActivationRule) => row.id

const scopeText = (scope: ActivationRule['scope']): string => {
  const textMap: Record<ActivationRule['scope'], string> = {
    all: '全部项目',
    government: '政府采购',
    engineering: '工程建设',
    service: '服务类'
  }
  return textMap[scope]
}

const statusTagType = (status: ActivationRule['status']): 'success' | 'warning' | 'default' => {
  const typeMap: Record<ActivationRule['status'], 'success' | 'warning' | 'default'> = {
    active: 'success',
    inactive: 'default',
    pending: 'warning'
  }
  return typeMap[status]
}

const statusText = (status: ActivationRule['status']): string => {
  const textMap: Record<ActivationRule['status'], string> = {
    active: '已激活',
    inactive: '已停用',
    pending: '待生效'
  }
  return textMap[status]
}

const columns = computed<TableColumn[]>(() => [
  {
    key: 'ruleName',
    title: '规则名称',
    dataIndex: 'ruleName',
    minWidth: 180,
    ellipsis: true
  },
  {
    key: 'ruleType',
    title: '规则类型',
    dataIndex: 'ruleType',
    width: 120
  },
  {
    key: 'effectiveTime',
    title: '生效时间',
    dataIndex: 'effectiveTime',
    width: 160,
    sortable: true
  },
  {
    key: 'expireTime',
    title: '失效时间',
    dataIndex: 'expireTime',
    width: 160,
    render: (row: ActivationRule) => row.expireTime || '永久有效'
  },
  {
    key: 'scope',
    title: '适用范围',
    dataIndex: 'scope',
    width: 100,
    render: (row: ActivationRule) => scopeText(row.scope)
  },
  {
    key: 'status',
    title: '状态',
    dataIndex: 'status',
    width: 100,
    render: (row: ActivationRule) => {
      return h(
        NTag,
        {
          type: statusTagType(row.status),
          size: 'small',
          round: true
        },
        () => statusText(row.status)
      )
    }
  },
  {
    key: 'activatedBy',
    title: '激活人',
    dataIndex: 'activatedBy',
    width: 100
  },
  {
    key: 'activatedAt',
    title: '激活时间',
    dataIndex: 'activatedAt',
    width: 160
  },
  {
    key: 'actions',
    title: '操作',
    width: 150,
    fixed: 'right',
    render: (row: ActivationRule) => {
      return h('div', { class: 'action-buttons' }, [
        h(
          NSwitch,
          {
            size: 'small',
            value: row.status === 'active',
            onUpdateValue: () => handleToggle(row)
          }
        ),
        h(
          NButton,
          {
            size: 'small',
            text: true,
            onClick: () => handleViewHistory(row)
          },
          () => h(NIcon, () => h(TimeOutline))
        )
      ])
    }
  }
])

const tableData = ref<ActivationRule[]>([
  {
    id: '1',
    ruleId: 'R001',
    ruleName: '敏感词检测规则',
    ruleType: '错敏词',
    effectiveTime: '2026-01-01 00:00:00',
    expireTime: null,
    scope: 'all',
    status: 'active',
    activatedBy: '张三',
    activatedAt: '2025-12-20 14:30:00'
  },
  {
    id: '2',
    ruleId: 'R002',
    ruleName: '法规引用完整性检查',
    ruleType: '合规性',
    effectiveTime: '2026-03-01 00:00:00',
    expireTime: '2026-12-31 23:59:59',
    scope: 'government',
    status: 'active',
    activatedBy: '李四',
    activatedAt: '2026-02-25 10:00:00'
  },
  {
    id: '3',
    ruleId: 'R003',
    ruleName: '围串标检测规则',
    ruleType: '风险检测',
    effectiveTime: '2026-04-01 00:00:00',
    expireTime: null,
    scope: 'engineering',
    status: 'pending',
    activatedBy: '王五',
    activatedAt: '2026-03-15 09:00:00'
  }
])

const emit = defineEmits<{
  (e: 'toggle', rule: ActivationRule): void
  (e: 'view-history', rule: ActivationRule): void
  (e: 'activate'): void
  (e: 'history'): void
  (e: 'search', keyword: string): void
  (e: 'filter-change', filters: { scope?: string; status?: string }): void
  (e: 'page-change', page: number): void
}>()

const handleSearch = (keyword: string) => {
  emit('search', keyword)
}

const handleScopeChange = (value: string | number | null) => {
  emit('filter-change', { scope: value as string | undefined })
}

const handleStatusChange = (value: string | number | null) => {
  emit('filter-change', { status: value as string | undefined })
}

const handlePageChange = (page: number) => {
  paginationConfig.value.page = page
  emit('page-change', page)
}

const handleToggle = (rule: ActivationRule) => {
  emit('toggle', rule)
}

const handleViewHistory = (rule: ActivationRule) => {
  emit('view-history', rule)
}

const handleActivate = () => {
  emit('activate')
}

const handleHistory = () => {
  emit('history')
}
</script>

<style scoped lang="scss">
.activation-table {
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
    gap: 12px;
    align-items: center;
  }
}
</style>
