<template>
  <div class="quick-questions">
    <div class="questions-header" v-if="showHeader">
      <span class="header-text">快捷问题</span>
    </div>
    <div class="questions-list">
      <n-button
        v-for="(question, index) in questions"
        :key="index"
        class="question-btn"
        :loading="loading && selectedIndex === index"
        :disabled="loading"
        @click="handleSelect(question, index)"
      >
        <template #icon v-if="selectedIndex !== index">
          <n-icon><ChatbubblesOutline /></n-icon>
        </template>
        <span class="question-text">{{ question }}</span>
      </n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ChatbubblesOutline } from '@vicons/ionicons5'

const props = withDefaults(defineProps<{
  questions: string[]
  loading?: boolean
  showHeader?: boolean
}>(), {
  loading: false,
  showHeader: true
})

const emit = defineEmits<{
  select: [question: string]
}>()

const selectedIndex = ref<number>(-1)

const handleSelect = (question: string, index: number) => {
  selectedIndex.value = index
  emit('select', question)
}
</script>

<style scoped lang="scss">
.quick-questions {
  padding: 12px 16px;
  background: var(--gray-100, #fafafa);
  border-radius: 8px;
  margin-bottom: 12px;
}

.questions-header {
  margin-bottom: 12px;

  .header-text {
    font-size: 13px;
    font-weight: 500;
    color: var(--gray-600, #595959);
  }
}

.questions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.question-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  font-size: 13px;
  border-radius: 6px;
  background: var(--primary-bg, rgba(30, 90, 168, 0.1));
  color: var(--primary-color, #1E5AA8);
  border: 1px solid transparent;
  transition: all 200ms ease;

  &:hover:not(:disabled) {
    background: var(--primary-color, #1E5AA8);
    color: #fff;
    border-color: var(--primary-color, #1E5AA8);
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(30, 90, 168, 0.2);
  }

  &:active:not(:disabled) {
    transform: translateY(0);
    box-shadow: none;
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  :deep(.n-icon) {
    font-size: 14px;
  }

  .question-text {
    line-height: 1.4;
    word-break: break-word;
  }
}
</style>
