<template>
  <AppLayout>
    <div class="project-list-page">
      <PageHeader title="项目管理" />

      <n-card>
        <div class="filters">
          <SearchInput v-model="searchKey" placeholder="搜索项目名称" />
          <FilterSelect
            v-model="statusFilter"
            :options="statusOptions"
            placeholder="全部状态"
          />
        </div>

        <n-table :columns="columns" :data="projects" :pagination="false">
          <template #empty>
            <n-empty description="暂无项目" />
          </template>
        </n-table>

        <Pagination
          :total="total"
          :current-page="currentPage"
          @change="handlePageChange"
        />
      </n-card>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, h } from 'vue'
import { useRouter } from 'vue-router'
import { NCard, NTable, NTag, NEmpty } from 'naive-ui'
import AppLayout from '@/components/layout/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import FilterSelect from '@/components/common/FilterSelect.vue'
import Pagination from '@/components/common/Pagination.vue'
import type { SelectOption } from 'naive-ui'

const router = useRouter()

const searchKey = ref('')
const statusFilter = ref(null)
const total = ref(8)
const currentPage = ref(1)

const statusOptions: SelectOption[] = [
  { label: '全部状态', value: null },
  { label: '已完成', value: 'completed' },
  { label: '进行中', value: 'in_progress' }
]

const projects = ref([
  { id: 1, name: '某市政府云平台建设项目', budget: '¥500万', status: 'completed', createTime: '2024-03-10' },
  { id: 2, name: '某高校智慧校园项目', budget: '¥280万', status: 'in_progress', createTime: '2024-03-12' },
  { id: 3, name: '某医院信息化建设项目', budget: '¥350万', status: 'completed', createTime: '2024-03-08' }
])

const columns = [
  { title: '项目名称', key: 'name' },
  { title: '预算', key: 'budget' },
  {
    title: '状态',
    key: 'status',
    render(row) {
      return h(NTag, { type: row.status === 'completed' ? 'success' : 'warning', size: 'small' }, () => row.status === 'completed' ? '已完成' : '进行中')
    }
  },
  { title: '创建时间', key: 'createTime' },
  {
    title: '操作',
    key: 'actions',
    render(row) {
      return h('a', {
        class: 'action-link',
        onClick: () => router.push(`/project/${row.id}`)
      }, '查看详情')
    }
  }
]

const handlePageChange = (page: number) => {
  currentPage.value = page
}
</script>

<style scoped lang="scss">
.project-list-page {
  max-width: 1200px;
  margin: 0 auto;
}

.filters {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.action-link {
  color: var(--primary-color);
  cursor: pointer;

  &:hover {
    text-decoration: underline;
  }
}
</style>
