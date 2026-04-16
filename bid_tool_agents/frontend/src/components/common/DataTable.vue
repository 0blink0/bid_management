<template>
  <div class="data-table">
    <n-data-table
      :columns="processedColumns"
      :data="data"
      :loading="loading"
      :pagination="paginationConfig"
      :row-key="rowKey"
      :row-props="rowProps"
      :bordered="bordered"
      :single-line="!bordered"
      @update:sorter="handleSorterChange"
      @update:filters="handleFilterChange"
      @update:page="handlePageChange"
      @update:checked-row-keys="handleSelectionChange"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { NDataTable } from 'naive-ui'
import type { DataTableColumns, DataTableSortState, DataTableFilterState, PaginationProps } from 'naive-ui'

export interface TableColumn {
  key: string
  title: string
  dataIndex?: string | string[]
  width?: number | string
  minWidth?: number | string
  fixed?: 'left' | 'right'
  align?: 'left' | 'center' | 'right'
  sortable?: boolean
  filterable?: boolean | {
    filter?: (value: any, row: any) => boolean
    filterMode?: 'or' | 'and'
    format?: (value: any) => any
    choices?: Array<{ label: string; value: any }>
  }
  render?: (row: any, column: TableColumn, index: number) => any
  ellipsis?: boolean
}

export interface SelectionOption {
  label: string
  value: string | number
}

const props = defineProps<{
  columns: TableColumn[]
  data: any[]
  loading?: boolean
  pagination?: false | Partial<PaginationProps>
  sortable?: boolean
  filterable?: boolean
  rowKey?: string | ((row: any) => string | number)
  selectionType?: 'single' | 'multiple'
  bordered?: boolean
  rowProps?: (row: any, index: number) => Record<string, any>
}>()

const emit = defineEmits<{
  (e: 'sort', sorter: { columnKey: string; order: 'ascend' | 'descend' | false }): void
  (e: 'filter', filters: Record<string, any>): void
  (e: 'page-change', page: number): void
  (e: 'selection-change', keys: (string | number)[]): void
}>()

const rowKey = computed(() => props.rowKey || 'id')

const processedColumns = computed<DataTableColumns[]>(() => {
  return props.columns.map((col) => {
    const processed: DataTableColumns = {
      key: col.key,
      title: col.title,
      dataIndex: col.dataIndex || col.key,
      width: col.width,
      minWidth: col.minWidth,
      fixed: col.fixed,
      align: col.align,
      ellipsis: col.ellipsis ?? true,
      sorter: props.sortable !== false && col.sortable ? col.sortable : undefined,
      filter: props.filterable !== false && col.filterable
        ? typeof col.filterable === 'object' ? col.filterable.filter : undefined
        : undefined,
      render: col.render
    }
    return processed
  })
})

const paginationConfig = computed(() => {
  if (props.pagination === false) {
    return false
  }

  const defaultPagination: PaginationProps = {
    pageSize: 10,
    pageSizes: [10, 20, 50, 100],
    showSizePicker: true,
    showQuickJumper: true,
    prefix: ({ total }) => `共 ${total} 条`
  }

  return { ...defaultPagination, ...props.pagination }
})

const handleSorterChange = (sorter: DataTableSortState | DataTableSortState[]) => {
  const singleSorter = Array.isArray(sorter) ? sorter[0] : sorter
  if (singleSorter && 'columnKey' in singleSorter) {
    emit('sort', {
      columnKey: singleSorter.columnKey,
      order: singleSorter.order
    })
  } else if (singleSorter === false) {
    emit('sort', { columnKey: '', order: false })
  }
}

const handleFilterChange = (filters: DataTableFilterState) => {
  emit('filter', filters as Record<string, any>)
}

const handlePageChange = (page: number) => {
  emit('page-change', page)
}

const handleSelectionChange = (keys: (string | number)[]) => {
  emit('selection-change', keys)
}
</script>

<style scoped lang="scss">
.data-table {
  width: 100%;

  :deep(.n-data-table-th) {
    background-color: var(--gray-100);
    color: var(--gray-700);
    font-weight: 600;
    font-size: 13px;
  }

  :deep(.n-data-table-td) {
    font-size: 13px;
    color: var(--gray-800);
  }

  :deep(.n-data-table-tr:hover) {
    background-color: var(--primary-bg);
  }

  :deep(.n-pagination) {
    margin-top: 16px;
  }
}
</style>
