<template>
  <div
    class="chat-message"
    :class="[`message-${message.role}`, { streaming: isStreaming }]"
  >
    <!-- 头像 -->
    <div class="message-avatar">
      <n-icon v-if="message.role === 'user'" size="24" color="#1890ff">
        <PersonOutline />
      </n-icon>
      <n-icon v-else size="24" color="#52c41a">
        <BotOutline />
      </n-icon>
    </div>

    <!-- 内容区 -->
    <div class="message-content">
      <!-- 角色名 -->
      <div class="message-header">
        <span class="role-name">{{ message.role === 'user' ? '用户' : 'Agent' }}</span>
        <span class="message-time">{{ formatTime(message.timestamp) }}</span>
      </div>

      <!-- 消息内容 -->
      <div class="message-body">
        <!-- 流式输出 -->
        <template v-if="isStreaming && message.role === 'assistant'">
          <div class="streaming-text">
            {{ displayText }}<span class="cursor">▋</span>
          </div>
        </template>

        <!-- 普通文本 -->
        <template v-else>
          <div class="message-text" v-html="renderMarkdown(message.content)"></div>
        </template>

        <!-- 引用原文 -->
        <template v-if="message.citations?.length">
          <div class="citations">
            <div class="citation-header">原文依据:</div>
            <div
              v-for="(cit, idx) in message.citations"
              :key="idx"
              class="citation-item"
              @click="jumpToSource(cit)"
            >
              <n-tag size="small">{{ cit.file }}</n-tag>
              <span class="citation-text">{{ cit.text }}</span>
            </div>
          </div>
        </template>

        <!-- 操作按钮 -->
        <template v-if="!isStreaming && message.actions?.length">
          <div class="message-actions">
            <n-button
              v-for="action in message.actions"
              :key="action.key"
              size="small"
              @click="handleAction(action)"
            >
              {{ action.label }}
            </n-button>
          </div>
        </template>
      </div>

      <!-- 进度条（如果有） -->
      <template v-if="message.progress !== undefined">
        <div class="message-progress">
          <n-progress
            type="line"
            :percentage="message.progress"
            :indicator-placement="'inside'"
            :status="getProgressStatus(message.progress)"
          />
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted } from 'vue'
import { PersonOutline, BotOutline } from '@vicons/ionicons5'
import type { ChatMessage as ChatMessageType } from '@/types/agent'

const props = defineProps<{
  message: ChatMessageType
}>()

const emit = defineEmits<{
  action: [action: any]
  jumpToSource: [citation: any]
}>()

// 流式文本
const displayText = ref('')
const isStreaming = computed(() => props.message.status === 'streaming')

// 监听流式更新
watch(
  () => props.message.content,
  (newContent) => {
    if (isStreaming.value) {
      displayText.value = newContent
    }
  },
  { immediate: true }
)

// 格式化时间
const formatTime = (timestamp: number) => {
  return new Date(timestamp).toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 渲染Markdown（简化版）
const renderMarkdown = (text: string) => {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br>')
}

// 获取进度状态
const getProgressStatus = (progress: number) => {
  if (progress >= 100) return 'success'
  if (progress >= 50) return 'active'
  return 'default'
}

// 处理操作
const handleAction = (action: any) => {
  emit('action', action)
}

// 跳转到原文
const jumpToSource = (citation: any) => {
  emit('jumpToSource', citation)
}
</script>

<style scoped lang="scss">
.chat-message {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 12px;

  &.message-user {
    background: #f0f7ff;
    flex-direction: row-reverse;
  }

  &.message-assistant {
    background: #fafafa;
  }

  &.streaming {
    background: #fffbe6;
  }
}

.message-avatar {
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

.message-content {
  flex: 1;
  min-width: 0;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;

  .role-name {
    font-weight: 600;
    font-size: 14px;
  }

  .message-time {
    font-size: 12px;
    color: #999;
  }
}

.message-body {
  font-size: 14px;
  line-height: 1.6;
}

.message-text {
  white-space: pre-wrap;
  word-break: break-word;
}

.streaming-text {
  font-family: monospace;
  white-space: pre-wrap;

  .cursor {
    animation: blink 1s infinite;
    color: #1890ff;
  }
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.citations {
  margin-top: 12px;
  padding: 8px;
  background: #f5f5f5;
  border-radius: 4px;
  font-size: 12px;

  .citation-header {
    font-weight: 600;
    margin-bottom: 8px;
    color: #666;
  }

  .citation-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 0;
    cursor: pointer;

    &:hover {
      color: #1890ff;
    }
  }
}

.message-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.message-progress {
  margin-top: 8px;
}
</style>
