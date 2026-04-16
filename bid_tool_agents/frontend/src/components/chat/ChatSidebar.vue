<template>
  <div class="chat-sidebar">
    <div class="chat-header">
      <n-icon :size="20"><ChatbubblesOutline /></n-icon>
      <span>智能助手</span>
    </div>

    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message', msg.type]"
      >
        <div class="message-avatar">
          <n-icon v-if="msg.type === 'assistant'" :size="20"><SparklesOutline /></n-icon>
          <span v-else>我</span>
        </div>
        <div class="message-content">
          <div class="message-bubble">{{ msg.content }}</div>
          <div class="message-time">{{ msg.time }}</div>
        </div>
      </div>
      <div v-if="isTyping" class="message assistant">
        <div class="message-avatar">
          <n-icon :size="20"><SparklesOutline /></n-icon>
        </div>
        <div class="message-content">
          <div class="message-bubble typing">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="quick-questions">
      <button
        v-for="q in quickQuestions"
        :key="q"
        class="quick-btn"
        @click="askQuestion(q)"
      >
        {{ q }}
      </button>
    </div>

    <div class="chat-input">
      <n-input
        v-model:value="inputMessage"
        placeholder="输入问题..."
        @keyup.enter="sendMessage"
      />
      <n-button type="primary" @click="sendMessage">
        <template #icon>
          <n-icon><SendOutline /></n-icon>
        </template>
      </n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { NIcon, NInput, NButton } from 'naive-ui'
import { ChatbubblesOutline, SparklesOutline, SendOutline } from '@vicons/ionicons5'

const messagesContainer = ref<HTMLElement | null>(null)
const inputMessage = ref('')
const isTyping = ref(false)

const messages = ref([
  {
    type: 'assistant',
    content: '您好！我是智能审查助手，可以帮您解答关于审查报告的问题。',
    time: '14:30'
  }
])

const quickQuestions = [
  '核心风险是什么？',
  '解释第30页问题'
]

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const sendMessage = () => {
  if (!inputMessage.value.trim()) return

  messages.value.push({
    type: 'user',
    content: inputMessage.value,
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  })

  const question = inputMessage.value
  inputMessage.value = ''
  scrollToBottom()

  // Simulate typing
  isTyping.value = true
  setTimeout(() => {
    isTyping.value = false
    messages.value.push({
      type: 'assistant',
      content: `关于"${question}"，我正在分析中...`,
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
    })
    scrollToBottom()
  }, 1500)
}

const askQuestion = (q: string) => {
  inputMessage.value = q
  sendMessage()
}
</script>

<style scoped lang="scss">
.chat-sidebar {
  width: 380px;
  height: calc(100vh - 120px);
  background: #fff;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--gray-200);
  font-weight: 600;
  color: var(--gray-800);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
  gap: 8px;

  &.user {
    flex-direction: row-reverse;
  }
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--gray-200);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: var(--gray-600);
  flex-shrink: 0;

  .assistant & {
    background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
    color: #fff;
  }
}

.message-content {
  max-width: 80%;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;

  .user & {
    background: var(--primary-color);
    color: #fff;
    border-bottom-right-radius: 4px;
  }

  .assistant & {
    background: var(--gray-100);
    color: var(--gray-800);
    border-bottom-left-radius: 4px;
  }

  &.typing {
    padding: 16px 20px;
  }
}

.message-time {
  font-size: 11px;
  color: var(--gray-500);
  margin-top: 4px;

  .user & {
    text-align: right;
  }
}

.typing-indicator {
  display: flex;
  gap: 4px;

  span {
    width: 8px;
    height: 8px;
    background: var(--gray-400);
    border-radius: 50%;
    animation: typing 1.4s infinite;

    &:nth-child(2) {
      animation-delay: 0.2s;
    }

    &:nth-child(3) {
      animation-delay: 0.4s;
    }
  }
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-4px);
  }
}

.quick-questions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 0 20px 16px;
}

.quick-btn {
  padding: 6px 12px;
  background: var(--gray-100);
  border: none;
  border-radius: 16px;
  font-size: 12px;
  color: var(--gray-600);
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: var(--primary-bg);
    color: var(--primary-color);
  }
}

.chat-input {
  display: flex;
  gap: 8px;
  padding: 16px 20px;
  border-top: 1px solid var(--gray-200);
}
</style>
