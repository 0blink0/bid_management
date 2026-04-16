<template>
  <div class="filter-select">
    <n-select
      :value="modelValue"
      :options="options"
      :placeholder="placeholder"
      clearable
      @update:value="handleChange"
    />
  </div>
</template>

<script setup lang="ts">
import { NSelect, type SelectOption } from 'naive-ui'

defineProps<{
  modelValue: string | number | null
  options: SelectOption[]
  placeholder?: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | number | null): void
  (e: 'change', value: string | number | null): void
}>()

const handleChange = (value: string | number | null) => {
  emit('update:modelValue', value)
  emit('change', value)
}
</script>

<style scoped lang="scss">
.filter-select {
  width: 140px;
}
</style>
