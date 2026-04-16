<template>
  <Transition name="fade">
    <div v-if="visible" class="typing-indicator">
      <div class="typing-avatar">
        <n-icon size="20" color="#52c41a">
          <BotOutline />
        </n-icon>
      </div>
      <div class="typing-content">
        <div class="typing-text">AI 正在输入</div>
        <div class="typing-dots">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { BotOutline } from '@vicons/ionicons5'

defineProps<{
  visible: boolean
}>()
</script>

<style scoped lang="scss">
.typing-indicator {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  margin-bottom: 12px;
}

.typing-avatar {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.typing-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-top: 4px;
}

.typing-text {
  font-size: 13px;
  color: #8c8c8c;
}

.typing-dots {
  display: flex;
  align-items: center;
  gap: 4px;
  height: 20px;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--primary-color, #1E5AA8);
  animation: bounce 1.4s infinite ease-in-out;

  &:nth-child(1) {
    animation-delay: 0s;
  }

  &:nth-child(2) {
    animation-delay: 0.2s;
  }

  &:nth-child(3) {
    animation-delay: 0.4s;
  }
}

@keyframes bounce {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  30% {
    transform: translateY(-6px);
    opacity: 1;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 200ms ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
