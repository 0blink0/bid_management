<template>
  <n-modal
    v-model:show="visibleSync"
    :mask-closable="!loading"
    :close-on-esc="!loading"
    :style="{ width: width }"
    preset="dialog"
    :title="title"
    :positive-text="confirmText"
    :negative-text="cancelText"
    :positive-button-props="confirmButtonProps"
    :negative-button-props="cancelButtonProps"
    :action-type="danger ? 'error' : 'primary'"
    @positive-click="handleConfirm"
    @negative-click="handleCancel"
    @close="handleClose"
  >
    <template #icon v-if="danger">
      <n-icon size="24" color="var(--danger-color)">
        <AlertCircleOutline />
      </n-icon>
    </template>
    <div class="confirm-modal-content" :class="{ 'has-icon': danger }">
      <n-icon v-if="danger" size="48" color="var(--danger-color)" class="warning-icon">
        <AlertCircleOutline />
      </n-icon>
      <p class="confirm-message">{{ message }}</p>
    </div>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { NModal, NIcon } from 'naive-ui'
import { AlertCircleOutline } from '@vicons/ionicons5'

const props = defineProps<{
  visible: boolean
  title: string
  message: string
  confirmText?: string
  cancelText?: string
  danger?: boolean
  loading?: boolean
  width?: string
}>()

const emit = defineEmits<{
  (e: 'confirm'): void
  (e: 'cancel'): void
  (e: 'close'): void
  (e: 'update:visible', value: boolean): void
}>()

const visibleSync = ref(props.visible)

watch(() => props.visible, (val) => {
  visibleSync.value = val
})

watch(visibleSync, (val) => {
  emit('update:visible', val)
})

const width = computed(() => props.width || '420px')

const confirmText = computed(() => props.confirmText || '确定')
const cancelText = computed(() => props.cancelText || '取消')

const confirmButtonProps = computed(() => ({
  type: props.danger ? 'error' : 'primary',
  loading: props.loading,
  disabled: props.loading
}))

const cancelButtonProps = computed(() => ({
  disabled: props.loading
}))

const handleConfirm = () => {
  if (props.loading) return false
  emit('confirm')
  return false
}

const handleCancel = () => {
  if (props.loading) return
  emit('cancel')
}

const handleClose = () => {
  emit('close')
}
</script>

<style scoped lang="scss">
.confirm-modal-content {
  padding: 16px 0;
  text-align: center;

  &.has-icon {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
  }
}

.warning-icon {
  flex-shrink: 0;
}

.confirm-message {
  margin: 0;
  font-size: 14px;
  color: var(--gray-700);
  line-height: 1.6;
  text-align: left;
}

:deep(.n-dialog) {
  .n-dialog__icon {
    display: none;
  }
}
</style>
