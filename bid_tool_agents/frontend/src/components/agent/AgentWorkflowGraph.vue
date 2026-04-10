<template>
  <div class="agent-workflow">
    <div class="workflow-header">
      <span class="title">Agent 工作流</span>
      <n-tag :type="statusType" size="small">{{ statusText }}</n-tag>
    </div>

    <div class="workflow-graph" ref="graphRef">
      <svg :viewBox="`0 0 ${width} ${height}`">
        <!-- 连接线 -->
        <g class="edges">
          <path
            v-for="(edge, idx) in edges"
            :key="`edge-${idx}`"
            :d="getEdgePath(edge)"
            class="workflow-edge"
            :class="{ active: edge.active, completed: edge.completed }"
          />
        </g>

        <!-- 节点 -->
        <g class="nodes">
          <g
            v-for="node in nodes"
            :key="node.id"
            :transform="`translate(${node.x}, ${node.y})`"
            class="workflow-node"
            :class="{
              active: node.active,
              completed: node.completed,
              error: node.status === 'error'
            }"
            @click="handleNodeClick(node)"
          >
            <!-- 节点背景 -->
            <rect
              :width="nodeWidth"
              :height="nodeHeight"
              rx="8"
              ry="8"
              class="node-bg"
            />

            <!-- 图标 -->
            <foreignObject x="8" y="8" width="32" height="32">
              <n-icon :color="getNodeColor(node)" size="24">
                <component :is="getNodeIcon(node)" />
              </n-icon>
            </foreignObject>

            <!-- 标签 -->
            <text
              :x="nodeWidth / 2"
              :y="nodeHeight - 12"
              text-anchor="middle"
              class="node-label"
            >
              {{ node.label }}
            </text>

            <!-- 状态指示器 -->
            <circle
              v-if="node.active"
              :cx="nodeWidth - 8"
              cy="8"
              r="6"
              class="status-indicator active"
            />
            <circle
              v-else-if="node.completed"
              :cx="nodeWidth - 8"
              cy="8"
              r="6"
              class="status-indicator completed"
            />
          </g>
        </g>
      </svg>
    </div>

    <!-- 节点详情 -->
    <div v-if="selectedNode" class="node-detail">
      <div class="detail-header">
        <n-icon size="20">
          <component :is="getNodeIcon(selectedNode)" />
        </n-icon>
        <span>{{ selectedNode.label }}</span>
      </div>
      <div class="detail-content">
        <n-descriptions :column="1" size="small">
          <n-descriptions-item label="状态">
            <n-tag :type="getStatusType(selectedNode)" size="small">
              {{ getStatusText(selectedNode) }}
            </n-tag>
          </n-descriptions-item>
          <n-descriptions-item label="耗时">
            {{ selectedNode.duration || '0s' }}
          </n-descriptions-item>
          <n-descriptions-item label="输出">
            {{ selectedNode.output || '无' }}
          </n-descriptions-item>
        </n-descriptions>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  DocumentTextOutline,
  CheckmarkCircleOutline,
  AlertCircleOutline,
  PersonOutline,
  SettingsOutline,
  ShieldOutline,
  GitCompareOutline,
  BarChartOutline,
  ArchiveOutline
} from '@vicons/ionicons5'

interface WorkflowNode {
  id: string
  label: string
  x: number
  y: number
  status: 'idle' | 'active' | 'completed' | 'error'
  duration?: string
  output?: string
  agentId: string
}

interface WorkflowEdge {
  from: string
  to: string
  active?: boolean
  completed?: boolean
}

const props = withDefaults(defineProps<{
  nodes?: WorkflowNode[]
  edges?: WorkflowEdge[]
}>(), {
  nodes: () => [
    { id: 'parser', label: '文档解析', x: 100, y: 50, status: 'completed', agentId: 'parser' },
    { id: 'compliance', label: '合规审查', x: 100, y: 130, status: 'active', agentId: 'compliance' },
    { id: 'comparison', label: '比对分析', x: 200, y: 130, status: 'idle', agentId: 'comparison' },
    { id: 'risk', label: '风险识别', x: 100, y: 210, status: 'idle', agentId: 'risk' }
  ],
  edges: () => [
    { from: 'parser', to: 'compliance', completed: true },
    { from: 'compliance', to: 'comparison', active: true },
    { from: 'compliance', to: 'risk' }
  ]
})

const emit = defineEmits<{
  nodeClick: [node: WorkflowNode]
}>()

const width = 320
const height = 280
const nodeWidth = 100
const nodeHeight = 48
const selectedNode = ref<WorkflowNode | null>(null)

const statusText = computed(() => {
  const activeNode = props.nodes.find(n => n.status === 'active')
  return activeNode ? `执行中: ${activeNode.label}` : '等待中'
})

const statusType = computed(() => {
  const hasActive = props.nodes.some(n => n.status === 'active')
  const hasError = props.nodes.some(n => n.status === 'error')
  if (hasError) return 'error'
  if (hasActive) return 'info'
  return 'default'
})

const getNodeIcon = (node: WorkflowNode) => {
  const icons: Record<string, any> = {
    parser: DocumentTextOutline,
    compliance: ShieldOutline,
    comparison: GitCompareOutline,
    qualification: CheckmarkCircleOutline,
    risk: AlertCircleOutline,
    evaluation: BarChartOutline,
    expert: PersonOutline,
    archive: ArchiveOutline,
    statistics: BarChartOutline
  }
  return icons[node.agentId] || SettingsOutline
}

const getNodeColor = (node: WorkflowNode) => {
  if (node.status === 'completed') return '#52c41a'
  if (node.status === 'active') return '#1890ff'
  if (node.status === 'error') return '#ff4d4f'
  return '#999'
}

const getStatusType = (node: WorkflowNode) => {
  if (node.status === 'completed') return 'success'
  if (node.status === 'active') return 'info'
  if (node.status === 'error') return 'error'
  return 'default'
}

const getStatusText = (node: WorkflowNode) => {
  if (node.status === 'completed') return '已完成'
  if (node.status === 'active') return '执行中'
  if (node.status === 'error') return '失败'
  return '等待'
}

const getEdgePath = (edge: WorkflowEdge) => {
  const fromNode = props.nodes.find(n => n.id === edge.from)
  const toNode = props.nodes.find(n => n.id === edge.to)
  if (!fromNode || !toNode) return ''

  const startX = fromNode.x + nodeWidth / 2
  const startY = fromNode.y + nodeHeight
  const endX = toNode.x + nodeWidth / 2
  const endY = toNode.y

  const midY = (startY + endY) / 2

  return `M ${startX} ${startY} C ${startX} ${midY}, ${endX} ${midY}, ${endX} ${endY}`
}

const handleNodeClick = (node: WorkflowNode) => {
  selectedNode.value = node
  emit('nodeClick', node)
}
</script>

<style scoped lang="scss">
.agent-workflow {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  height: 100%;
}

.workflow-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;

  .title {
    font-weight: 600;
    font-size: 14px;
  }
}

.workflow-graph {
  svg {
    width: 100%;
    height: auto;
  }
}

.workflow-edge {
  fill: none;
  stroke: #ddd;
  stroke-width: 2;
  transition: stroke 0.3s;

  &.active {
    stroke: #1890ff;
    stroke-dasharray: 5, 5;
    animation: dash 0.5s linear infinite;
  }

  &.completed {
    stroke: #52c41a;
  }
}

@keyframes dash {
  to {
    stroke-dashoffset: -10;
  }
}

.workflow-node {
  cursor: pointer;
  transition: transform 0.2s;

  &:hover {
    transform: scale(1.02);
  }

  .node-bg {
    fill: #fff;
    stroke: #e8e8e8;
    stroke-width: 2;
    transition: all 0.3s;
  }

  &.active .node-bg {
    fill: #e6f7ff;
    stroke: #1890ff;
  }

  &.completed .node-bg {
    fill: #f6ffed;
    stroke: #52c41a;
  }

  &.error .node-bg {
    fill: #fff2f0;
    stroke: #ff4d4f;
  }

  .node-label {
    font-size: 12px;
    fill: #333;
  }
}

.status-indicator {
  &.active {
    fill: #1890ff;
    animation: pulse 1s infinite;
  }

  &.completed {
    fill: #52c41a;
  }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.node-detail {
  margin-top: 16px;
  padding: 12px;
  background: #fafafa;
  border-radius: 4px;

  .detail-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    margin-bottom: 8px;
  }
}
</style>
