<template>
  <div class="pagination">
    <span class="pagination-info">
      共 {{ total }} 条记录，第 {{ currentPage }}/{{ totalPages }} 页
    </span>
    <div class="pagination-controls">
      <n-button
        size="small"
        :disabled="currentPage === 1"
        @click="goToPage(1)"
      >
        首页
      </n-button>
      <n-button
        size="small"
        :disabled="currentPage === 1"
        @click="goToPage(currentPage - 1)"
      >
        上一页
      </n-button>
      <n-button
        v-for="page in visiblePages"
        :key="page"
        size="small"
        :type="page === currentPage ? 'primary' : 'default'"
        @click="goToPage(page)"
      >
        {{ page }}
      </n-button>
      <n-button
        size="small"
        :disabled="currentPage === totalPages"
        @click="goToPage(currentPage + 1)"
      >
        下一页
      </n-button>
      <n-button
        size="small"
        :disabled="currentPage === totalPages"
        @click="goToPage(totalPages)"
      >
        末页
      </n-button>
    </div>
    <div class="pagination-jump">
      跳至
      <n-input-number
        v-model:value="jumpPage"
        :min="1"
        :max="totalPages"
        size="small"
        style="width: 60px"
        @blur="handleJump"
      />
      页
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { NButton, NInputNumber } from 'naive-ui'

const props = defineProps<{
  total: number
  currentPage: number
  pageSize?: number
}>()

const emit = defineEmits<{
  (e: 'update:currentPage', page: number): void
  (e: 'change', page: number): void
}>()

const pageSize = computed(() => props.pageSize || 10)
const totalPages = computed(() => Math.ceil(props.total / pageSize.value))
const jumpPage = ref(props.currentPage)

const visiblePages = computed(() => {
  const pages: number[] = []
  const total = totalPages.value
  const current = props.currentPage
  const range = 2

  for (let i = 1; i <= total; i++) {
    if (i === 1 || i === total || (i >= current - range && i <= current + range)) {
      pages.push(i)
    }
  }

  // Add ellipsis markers would require more complex logic
  return pages
})

const goToPage = (page: number) => {
  if (page < 1 || page > totalPages.value || page === props.currentPage) return
  emit('update:currentPage', page)
  emit('change', page)
}

const handleJump = () => {
  if (jumpPage.value >= 1 && jumpPage.value <= totalPages.value) {
    goToPage(jumpPage.value)
  }
}
</script>

<style scoped lang="scss">
.pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0;
}

.pagination-info {
  font-size: 13px;
  color: var(--gray-500);
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pagination-jump {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--gray-600);
}
</style>
