<template>
  <AppLayout>
    <div class="response-list-page">
      <PageHeader title="响应文件列表" />

      <n-card>
        <div class="filters">
          <SearchInput v-model="searchKey" placeholder="搜索文件名称" />
        </div>

        <n-table :columns="columns" :data="responses" :pagination="false">
          <template #empty>
            <n-empty description="暂无响应文件" />
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
import { NCard, NTable, NTag, NIcon, NEmpty } from 'naive-ui'
import AppLayout from '@/components/layout/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import Pagination from '@/components/common/Pagination.vue'
import { DocumentTextOutline } from '@vicons/ionicons5'

const router = useRouter()

const searchKey = ref('')
const total = ref(6)
const currentPage = ref(1)

const responses = ref([
  { id: 1, name: '华夏科技_技术方案.pdf', company: '华夏科技有限公司', uploadTime: '2024-03-14 10:00', status: 'complete' },
  { id: 2, name: '华夏科技_报价文件.pdf', company: '华夏科技有限公司', uploadTime: '2024-03-14 10:05', status: 'complete' },
  { id: 3, name: '中兴系统_技术方案.pdf', company: '中兴系统集成有限公司', uploadTime: '2024-03-14 11:00', status: 'partial' },
  { id: 4, name: '云端科技_技术方案.pdf', company: '云端科技股份有限公司', uploadTime: '2024-03-14 14:00', status: 'complete' }
])

const columns = [
  {
    title: '文件名称',
    key: 'name',
    render(row) {
      return h('div', { class: 'file-cell' }, [
        h(NIcon, { size: 20, color: '#ff4d4f' }, () => h(DocumentTextOutline)),
        h('span', null, row.name)
      ])
    }
  },
  { title: '投标单位', key: 'company' },
  { title: '上传时间', key: 'uploadTime' },
  {
    title: '状态',
    key: 'status',
    render(row) {
      return h(NTag, { type: row.status === 'complete' ? 'success' : 'warning', size: 'small' }, () => row.status === 'complete' ? '完整' : '部分')
    }
  },
  {
    title: '操作',
    key: 'actions',
    render(row) {
      return h('a', {
        class: 'action-link',
        onClick: () => router.push('/comparison')
      }, '查看比对')
    }
  }
]

const handlePageChange = (page: number) => {
  currentPage.value = page
}
</script>

<style scoped lang="scss">
.response-list-page {
  max-width: 1200px;
  margin: 0 auto;
}

.filters {
  margin-bottom: 16px;
}

.file-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.action-link {
  color: var(--primary-color);
  cursor: pointer;

  &:hover {
    text-decoration: underline;
  }
}
</style>
