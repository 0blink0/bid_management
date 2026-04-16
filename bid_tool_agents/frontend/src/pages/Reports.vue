<template>
  <AppLayout>
    <div class="reports-page">
      <PageHeader
        title="审查报告列表"
        subtitle="查看所有审查项目的报告汇总"
      />

      <div class="reports-content">
        <n-card>
          <n-table :columns="columns" :data="reports" :pagination="false">
            <template #empty>
              <n-empty description="暂无报告" />
            </template>
          </n-table>

          <Pagination
            :total="total"
            :current-page="currentPage"
            @change="handlePageChange"
          />
        </n-card>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, h } from 'vue'
import { useRouter } from 'vue-router'
import { NCard, NTable, NTag, NIcon, NEmpty } from 'naive-ui'
import AppLayout from '@/components/layout/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import Pagination from '@/components/common/Pagination.vue'

const router = useRouter()

const total = ref(8)
const currentPage = ref(1)

const reports = ref([
  {
    id: 1,
    name: '某市政府云平台建设项目',
    budget: '¥500万',
    biddingUnit: '某市政府采购中心',
    reviews: ['招标文件', '资质', '围串标', '响应'],
    bidders: 3,
    time: '2024-03-15 14:30',
    risk: '通过'
  },
  {
    id: 2,
    name: '某高校智慧校园项目',
    budget: '¥280万',
    biddingUnit: '某大学信息中心',
    reviews: ['招标文件', '响应'],
    bidders: 5,
    time: '2024-03-14 10:20',
    risk: '2项预警'
  },
  {
    id: 3,
    name: '某医院信息化建设项目',
    budget: '¥350万',
    biddingUnit: '某医院后勤部',
    reviews: ['招标文件', '资质'],
    bidders: 4,
    time: '2024-03-13 16:45',
    risk: '严重'
  }
])

const columns = [
  {
    title: '项目名称 / 预算',
    key: 'name',
    render(row) {
      return h('div', { class: 'project-cell' }, [
        h('div', { class: 'project-name' }, row.name),
        h('div', { class: 'project-budget' }, row.budget)
      ])
    }
  },
  {
    title: '招标单位',
    key: 'biddingUnit'
  },
  {
    title: '审核事项',
    key: 'reviews',
    render(row) {
      return h('div', { class: 'tags-cell' },
        row.reviews.map(tag => {
          const colorMap: Record<string, string> = {
            '招标文件': 'info',
            '资质': 'success',
            '围串标': 'error',
            '响应': 'warning'
          }
          return h(NTag, { type: colorMap[tag] || 'default', size: 'small' }, () => tag)
        })
      )
    }
  },
  {
    title: '投标单位',
    key: 'bidders',
    render(row) {
      return h('span', { class: 'bidders-count' }, `${row.bidders} 家`)
    }
  },
  {
    title: '审查时间',
    key: 'time'
  },
  {
    title: '风险',
    key: 'risk',
    render(row) {
      const typeMap: Record<string, string> = {
        '通过': 'success',
        '2项预警': 'warning',
        '严重': 'error'
      }
      return h(NTag, { type: typeMap[row.risk] || 'default', size: 'small' }, () => row.risk)
    }
  },
  {
    title: '操作',
    key: 'actions',
    render(row) {
      return h('a', {
        class: 'action-link',
        onClick: () => router.push(`/report/${row.id}/full`)
      }, '查看详情')
    }
  }
]

const handlePageChange = (page: number) => {
  currentPage.value = page
}
</script>

<style scoped lang="scss">
.reports-page {
  max-width: 1200px;
  margin: 0 auto;
}

.project-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.project-name {
  font-weight: 500;
  color: var(--gray-800);
}

.project-budget {
  font-size: 12px;
  color: var(--gray-500);
}

.tags-cell {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.bidders-count {
  font-size: 16px;
  font-weight: 500;
  color: var(--primary-color);
}

.action-link {
  color: var(--primary-color);
  cursor: pointer;

  &:hover {
    text-decoration: underline;
  }
}
</style>
