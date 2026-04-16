<template>
  <div class="regulation-table">
    <div class="table-header">
      <div class="header-left">
        <search-input
          v-model="searchValue"
          placeholder="搜索法规名称或编号"
          @search="handleSearch"
        />
      </div>
      <div class="header-right">
        <n-button type="primary" @click="handleAdd">
          <template #icon>
            <n-icon><add-outline /></n-icon>
          </template>
          新增法规
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
import type { TableColumn } from '@/components/common/DataTable.vue'

interface Regulation {
  id: string
  name: string
  code: string
  publishDate: string
  effectiveDate: string
  status: 'effective' | 'pending' | 'abolished'
  category: string
  source: string
}

const loading = ref(false)
const searchValue = ref('')
const paginationConfig = ref({
  page: 1,
  pageSize: 10,
  total: 0
})

const rowKey = (row: Regulation) => row.id

const statusTagType = (status: Regulation['status']): 'success' | 'warning' | 'default' => {
  const typeMap: Record<Regulation['status'], 'success' | 'warning' | 'default'> = {
    effective: 'success',
    pending: 'warning',
    abolished: 'default'
  }
  return typeMap[status]
}

const statusText = (status: Regulation['status']): string => {
  const textMap: Record<Regulation['status'], string> = {
    effective: '已生效',
    pending: '待生效',
    abolished: '已废止'
  }
  return textMap[status]
}

const columns = computed<TableColumn[]>(() => [
  {
    key: 'name',
    title: '法规名称',
    dataIndex: 'name',
    minWidth: 200,
    ellipsis: true
  },
  {
    key: 'code',
    title: '法规编号',
    dataIndex: 'code',
    width: 160
  },
  {
    key: 'category',
    title: '分类',
    dataIndex: 'category',
    width: 120
  },
  {
    key: 'publishDate',
    title: '发布日期',
    dataIndex: 'publishDate',
    width: 120,
    sortable: true
  },
  {
    key: 'effectiveDate',
    title: '生效日期',
    dataIndex: 'effectiveDate',
    width: 120,
    sortable: true
  },
  {
    key: 'status',
    title: '状态',
    dataIndex: 'status',
    width: 100,
    render: (row: Regulation) => {
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
    key: 'source',
    title: '来源',
    dataIndex: 'source',
    width: 150,
    ellipsis: true
  },
  {
    key: 'actions',
    title: '操作',
    width: 150,
    fixed: 'right',
    render: (row: Regulation) => {
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

const tableData = ref<Regulation[]>([
  {
    id: '1',
    name: '中华人民共和国招标投标法',
    code: '主席令第21号',
    publishDate: '1999-08-30',
    effectiveDate: '2000-01-01',
    status: 'effective',
    category: '法律',
    source: '全国人民代表大会'
  },
  {
    id: '2',
    name: '中华人民共和国政府采购法',
    code: '主席令第68号',
    publishDate: '2002-06-29',
    effectiveDate: '2003-01-01',
    status: 'effective',
    category: '法律',
    source: '全国人民代表大会'
  },
  {
    id: '3',
    name: '招标投标法实施条例',
    code: '国务院令第613号',
    publishDate: '2011-11-30',
    effectiveDate: '2012-02-01',
    status: 'effective',
    category: '行政法规',
    source: '国务院'
  }
])

const emit = defineEmits<{
  (e: 'view', regulation: Regulation): void
  (e: 'edit', regulation: Regulation): void
  (e: 'add'): void
  (e: 'search', keyword: string): void
  (e: 'page-change', page: number): void
}>()

const handleSearch = (keyword: string) => {
  emit('search', keyword)
}

const handlePageChange = (page: number) => {
  paginationConfig.value.page = page
  emit('page-change', page)
}

const handleView = (regulation: Regulation) => {
  emit('view', regulation)
}

const handleEdit = (regulation: Regulation) => {
  emit('edit', regulation)
}

const handleAdd = () => {
  emit('add')
}
</script>

<style scoped lang="scss">
.regulation-table {
  .table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;

    .header-left {
      display: flex;
      gap: 12px;
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
