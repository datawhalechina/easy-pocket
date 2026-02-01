<!--
  PocketFlowQuickStart.vue
  PocketFlow 快速体验组件

  用途：
  让读者在文章开头就能直观理解 PocketFlow 的核心概念 ——
  通过交互式演示，展示 Node 的三阶段执行模型 (prep → exec → post)
  和 Flow 的图执行流程

  交互功能：
  - 选择不同的场景（聊天机器人、RAG、工作流）
  - 可视化展示 Node 执行过程
  - 动态展示 Flow 图的遍历
-->
<template>
  <div class="pf-quick-start">
    <div class="header">
      <div class="title-row">
        <span class="icon">🚀</span>
        <span class="title">PocketFlow 快速体验</span>
      </div>
      <div class="subtitle">选择一个场景，看看 100 行代码如何驱动 LLM 应用</div>
    </div>

    <div class="scene-selector">
      <button
        v-for="scene in scenes"
        :key="scene.id"
        :class="['scene-btn', { active: currentScene === scene.id }]"
        @click="selectScene(scene.id)"
      >
        <span class="scene-icon">{{ scene.icon }}</span>
        <span class="scene-label">{{ scene.label }}</span>
      </button>
    </div>

    <div class="flow-visualization">
      <div class="flow-title">{{ activeScene.flowTitle }}</div>
      <div class="nodes-container">
        <div
          v-for="(node, index) in activeScene.nodes"
          :key="index"
          :class="['node-card', { active: activeNodeIndex === index, done: index < activeNodeIndex }]"
        >
          <div class="node-header">
            <span class="node-icon">{{ node.icon }}</span>
            <span class="node-name">{{ node.name }}</span>
          </div>
          <div class="node-phases">
            <div
              v-for="(phase, pi) in ['prep', 'exec', 'post']"
              :key="pi"
              :class="['phase', { highlight: activeNodeIndex === index && activePhase === pi }]"
            >
              <span class="phase-label">{{ phase }}</span>
              <span class="phase-desc">{{ node.phases[pi] }}</span>
            </div>
          </div>
          <div v-if="index < activeScene.nodes.length - 1" class="arrow">→</div>
        </div>
      </div>

      <div class="control-bar">
        <button class="run-btn" @click="runFlow" :disabled="isRunning">
          {{ isRunning ? '⏳ 执行中...' : '▶ 运行 Flow' }}
        </button>
        <button class="reset-btn" @click="resetFlow" :disabled="!hasRun">
          ↺ 重置
        </button>
      </div>

      <div class="output-area" v-if="outputs.length > 0">
        <div class="output-title">执行日志</div>
        <div class="output-log">
          <div v-for="(log, i) in outputs" :key="i" class="log-line">
            <span class="log-prefix">{{ log.prefix }}</span>
            <span class="log-text">{{ log.text }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="info-box">
      <p>
        <span class="info-icon">💡</span>
        <strong>核心洞察：</strong>PocketFlow 的全部魔力来自两个抽象 ——
        <strong>Node</strong>（节点，执行 prep→exec→post 三阶段）和
        <strong>Flow</strong>（流程，串联多个 Node 的有向图）。
        仅此而已，100 行代码，零依赖。
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const scenes = [
  { id: 'chat', icon: '💬', label: '聊天机器人' },
  { id: 'rag', icon: '📚', label: 'RAG 检索增强' },
  { id: 'workflow', icon: '📝', label: '写作工作流' }
]

const sceneData = {
  chat: {
    flowTitle: 'ChatBot Flow：接收输入 → 调用 LLM → 返回回复',
    nodes: [
      {
        icon: '📥',
        name: 'GetInput',
        phases: ['从 shared 读取对话历史', '拼接用户消息为 prompt', '将回复存回 shared']
      },
      {
        icon: '🤖',
        name: 'CallLLM',
        phases: ['读取 prompt', '调用大模型 API', '返回 action 决定是否继续']
      },
      {
        icon: '📤',
        name: 'SendReply',
        phases: ['读取 LLM 输出', '格式化回复内容', '输出给用户，返回 "continue"']
      }
    ]
  },
  rag: {
    flowTitle: 'RAG Flow：问题理解 → 检索文档 → 增强生成',
    nodes: [
      {
        icon: '❓',
        name: 'ParseQuery',
        phases: ['读取用户问题', '提取关键词 & 意图', '存储解析结果']
      },
      {
        icon: '🔍',
        name: 'Retrieve',
        phases: ['读取关键词', '向量搜索知识库', '返回 Top-K 文档片段']
      },
      {
        icon: '✨',
        name: 'Generate',
        phases: ['拼接 context + question', '调用 LLM 生成回答', '存储最终答案']
      }
    ]
  },
  workflow: {
    flowTitle: 'Writing Flow：大纲 → 撰写 → 润色',
    nodes: [
      {
        icon: '📋',
        name: 'Outline',
        phases: ['读取写作主题', 'LLM 生成大纲', '存储大纲结构']
      },
      {
        icon: '✍️',
        name: 'Write',
        phases: ['读取大纲', 'LLM 逐章节撰写', '拼接完整草稿']
      },
      {
        icon: '💎',
        name: 'Polish',
        phases: ['读取草稿', 'LLM 润色语言风格', '输出最终文章']
      }
    ]
  }
}

const currentScene = ref('chat')
const activeNodeIndex = ref(-1)
const activePhase = ref(-1)
const isRunning = ref(false)
const hasRun = ref(false)
const outputs = ref([])

const activeScene = computed(() => sceneData[currentScene.value])

const selectScene = (id) => {
  currentScene.value = id
  resetFlow()
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms))

const runFlow = async () => {
  isRunning.value = true
  hasRun.value = true
  outputs.value = []
  const nodes = activeScene.value.nodes

  outputs.value.push({ prefix: '[Flow]', text: '开始执行...' })

  for (let i = 0; i < nodes.length; i++) {
    activeNodeIndex.value = i
    const node = nodes[i]

    for (let p = 0; p < 3; p++) {
      activePhase.value = p
      const phaseName = ['prep', 'exec', 'post'][p]
      outputs.value.push({
        prefix: `[${node.name}]`,
        text: `${phaseName}() → ${node.phases[p]}`
      })
      await sleep(600)
    }
  }

  activeNodeIndex.value = nodes.length
  outputs.value.push({ prefix: '[Flow]', text: '✅ 执行完毕！' })
  isRunning.value = false
}

const resetFlow = () => {
  activeNodeIndex.value = -1
  activePhase.value = -1
  isRunning.value = false
  hasRun.value = false
  outputs.value = []
}
</script>

<style scoped>
.pf-quick-start {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
  padding: 1.5rem;
  margin: 1.5rem 0;
}

.header {
  margin-bottom: 1.25rem;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.icon {
  font-size: 1.5rem;
}

.title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--vp-c-text-1);
}

.subtitle {
  color: var(--vp-c-text-3);
  font-size: 0.9rem;
}

.scene-selector {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
  flex-wrap: wrap;
}

.scene-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: var(--vp-c-bg);
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
  color: var(--vp-c-text-2);
}

.scene-btn:hover {
  border-color: var(--vp-c-brand);
  color: var(--vp-c-brand);
}

.scene-btn.active {
  background: var(--vp-c-brand);
  color: #fff;
  border-color: var(--vp-c-brand);
}

.flow-visualization {
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 1.25rem;
  margin-bottom: 1rem;
}

.flow-title {
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.nodes-container {
  display: flex;
  gap: 0.5rem;
  align-items: stretch;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.node-card {
  flex: 1;
  min-width: 180px;
  border: 2px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 0.75rem;
  position: relative;
  transition: all 0.3s;
  background: var(--vp-c-bg);
}

.node-card.active {
  border-color: var(--vp-c-brand);
  box-shadow: 0 0 12px rgba(66, 133, 244, 0.15);
}

.node-card.done {
  border-color: #67c23a;
  opacity: 0.75;
}

.node-header {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  font-size: 0.95rem;
}

.node-icon {
  font-size: 1.2rem;
}

.node-phases {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.phase {
  display: flex;
  align-items: baseline;
  gap: 0.4rem;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-size: 0.8rem;
  transition: all 0.2s;
}

.phase.highlight {
  background: rgba(66, 133, 244, 0.1);
  color: var(--vp-c-brand);
}

.phase-label {
  font-family: var(--vp-font-family-mono);
  font-weight: 600;
  min-width: 32px;
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
}

.phase.highlight .phase-label {
  color: var(--vp-c-brand);
}

.phase-desc {
  color: var(--vp-c-text-3);
  font-size: 0.78rem;
}

.phase.highlight .phase-desc {
  color: var(--vp-c-text-1);
}

.arrow {
  position: absolute;
  right: -18px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
  color: var(--vp-c-text-3);
  z-index: 1;
}

.control-bar {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.run-btn,
.reset-btn {
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s;
}

.run-btn {
  background: var(--vp-c-brand);
  color: #fff;
}

.run-btn:hover:not(:disabled) {
  opacity: 0.85;
}

.run-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.reset-btn {
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-2);
  border: 1px solid var(--vp-c-divider);
}

.reset-btn:hover:not(:disabled) {
  border-color: var(--vp-c-brand);
  color: var(--vp-c-brand);
}

.reset-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.output-area {
  margin-top: 1rem;
  border-top: 1px solid var(--vp-c-divider);
  padding-top: 0.75rem;
}

.output-title {
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
  margin-bottom: 0.5rem;
}

.output-log {
  background: var(--vp-c-bg-alt);
  border-radius: 6px;
  padding: 0.75rem;
  max-height: 200px;
  overflow-y: auto;
  font-family: var(--vp-font-family-mono);
  font-size: 0.8rem;
}

.log-line {
  padding: 0.15rem 0;
}

.log-prefix {
  color: var(--vp-c-brand);
  font-weight: 600;
  margin-right: 0.5rem;
}

.log-text {
  color: var(--vp-c-text-2);
}

.info-box {
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-left: 3px solid var(--vp-c-brand);
  border-radius: 6px;
  padding: 0.75rem 1rem;
}

.info-box p {
  margin: 0;
  font-size: 0.88rem;
  line-height: 1.6;
  color: var(--vp-c-text-2);
}

.info-icon {
  margin-right: 0.25rem;
}

@media (max-width: 640px) {
  .nodes-container {
    flex-direction: column;
  }

  .arrow {
    position: static;
    text-align: center;
    transform: rotate(90deg);
    margin: 0.25rem 0;
  }

  .node-card {
    min-width: unset;
  }
}
</style>
