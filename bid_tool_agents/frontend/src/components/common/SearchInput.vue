<template>
  <div class="search-input">
    <n-input
      :value="modelValue"
      :placeholder="placeholder"
      clearable
      @update:value="handleInput"
    >
      <template #prefix>
        <n-icon><SearchOutline /></n-icon>
      </template>
    </n-input>
  </div>
</template>

<script setup lang="ts">
import { NInput, NIcon } from 'naive-ui'
import { SearchOutline } from '@vicons/ionicons5'

defineProps<{
  modelValue: string
  placeholder?: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'search', value: string): void
}>()

const handleInput = (value: string) => {
  emit('update:modelValue', value)
  emit('search', value)
}
</script>

<style scoped lang="scss">
.search-input {
  width: 100%;
  max-width: 300px;
}
</style>
