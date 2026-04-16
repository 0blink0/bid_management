<template>
  <n-modal
    v-model:show="showModal"
    :mask-closable="maskClosable"
    :close-on-esc="true"
    @after-leave="handleAfterLeave"
  >
    <div class="modal-container" :style="{ width: width }">
      <div class="modal-header">
        <h3 class="modal-title">{{ title }}</h3>
        <n-button quaternary circle @click="handleClose">
          <template #icon>
            <n-icon><CloseOutline /></n-icon>
          </template>
        </n-button>
      </div>
      <div class="modal-body">
        <slot />
      </div>
      <div v-if="$slots.footer" class="modal-footer">
        <slot name="footer" />
      </div>
    </div>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { NModal, NButton, NIcon } from 'naive-ui'
import { CloseOutline } from '@vicons/ionicons5'

const props = defineProps<{
  show: boolean
  title: string
  width?: string
  maskClosable?: boolean
}>()

const emit = defineEmits<{
  (e: 'update:show', value: boolean): void
  (e: 'close'): void
}>()

const showModal = ref(props.show)

watch(() => props.show, (val) => {
  showModal.value = val
})

const handleClose = () => {
  showModal.value = false
  emit('update:show', false)
  emit('close')
}

const handleAfterLeave = () => {
  emit('close')
}
</script>

<style scoped lang="scss">
.modal-container {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--gray-200);
}

.modal-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--gray-800);
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid var(--gray-200);
  background-color: var(--gray-100);
}
</style>
