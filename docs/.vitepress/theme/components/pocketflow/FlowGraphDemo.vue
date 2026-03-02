<!--
  FlowGraphDemo.vue
  Flow 有向图可视化组件

  用途：
  交互式展示 PocketFlow 的核心 Flow 编排机制 ——
  用户可以通过点击按钮构建自己的 Node 图，
  并观察 Flow 如何沿 action 遍历执行

  交互功能：
  - 预设多种经典 Flow 模式（链式、分支、循环）
  - 可视化图遍历动画
  - 展示 shared 数据在节点间的传递
-->
<template>
  <div class="flow-graph-demo">
    <div class="header">
      <span class="icon">🗺️</span>
      <span class="title">Flow 图执行可视化</span>
    </div>

    <div class="pattern-selector">
      <button
        v-for="p in patterns"
        :key="p.id"
        :class="['pattern-btn', { active: currentPattern === p.id }]"
        @click="selectPattern(p.id)"
      >
        {{ p.icon }} {{ p.label }}
      </button>
    </div>

    <div class="graph-area">
      <div class="graph-desc">{{ activePattern.desc }}</div>

      <div class="graph-canvas">
        <div
          v-for="(node, i) in activePattern.nodes"
          :key="i"
          :class="['graph-node', { active: visitIndex === i, done: i < visitIndex }]"
          :style="node.style"
        >
          <div class="gn-icon">{{ node.icon }}</div>
          <div class="gn-name">{{ node.name }}</div>
        </div>

        <svg class="graph-edges" viewBox="0 0 600 200">
          <defs>
            <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
              <polygon points="0 0, 8 3, 0 6" fill="var(--vp-c-text-3)" />
            </marker>
          </defs>
          <path
            v-for="(edge, i) in activePattern.edges"
            :key="i"
            :d="edge.d"
            fill="none"
            :stroke="getEdgeColor(edge, i)"
            stroke-width="2"
            marker-end="url(#arrowhead)"
          />
          <text
            v-for="(edge, i) in activePattern.edges"
            :key="'t' + i"
            :x="edge.labelX"
            :y="edge.labelY"
            font-size="11"
            fill="var(--vp-c-text-3)"
            text-anchor="middle"
          >
            {{ edge.label }}
          </text>
        </svg>
      </div>

      <div class="code-snippet">
        <pre><code>{{ activePattern.code }}</code></pre>
      </div>
    </div>

    <div class="controls">
      <button class="run-btn" @click="runGraph" :disabled="isRunning">
        {{ isRunning ? '⏳ 遍历中...' : '▶ 运行 Flow' }}
      </button>
      <button class="reset-btn" @click="resetGraph">↺ 重置</button>
    </div>

    <div class="visit-log" v-if="visitLog.length > 0">
      <div class="log-title">遍历路径</div>
      <div class="log-path">
        <span v-for="(entry, i) in visitLog" :key="i" class="log-entry">
          <span class="log-node">{{ entry }}</span>
          <span v-if="i < visitLog.length - 1" class="log-sep">→</span>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const patterns = [
  { id: 'chain', icon: '⛓️', label: '链式' },
  { id: 'branch', icon: '🔀', label: '条件分支' },
  { id: 'loop', icon: '🔁', label: '循环' }
]

const patternData = {
  chain: {
    desc: '最基本的模式：Node 依次执行，每个 post() 返回 "default"',
    nodes: [
      { icon: 'A', name: 'NodeA', style: 'left: 30px; top: 70px;' },
      { icon: 'B', name: 'NodeB', style: 'left: 230px; top: 70px;' },
      { icon: 'C', name: 'NodeC', style: 'left: 430px; top: 70px;' }
    ],
    edges: [
      { d: 'M 105 100 L 230 100', label: 'default', labelX: 167, labelY: 90 },
      { d: 'M 305 100 L 430 100', label: 'default', labelX: 367, labelY: 90 }
    ],
    sequence: [0, 1, 2],
    code: `a, b, c = NodeA(), NodeB(), NodeC()
a >> b >> c          # 链式连接
flow = Flow(start=a)
flow.run(shared)     # A → B → C`
  },
  branch: {
    desc: '条件分支：post() 返回不同 action，走向不同的后继节点',
    nodes: [
      { icon: '?', name: 'Check', style: 'left: 30px; top: 70px;' },
      { icon: '✓', name: 'Approve', style: 'left: 280px; top: 20px;' },
      { icon: '✗', name: 'Reject', style: 'left: 280px; top: 120px;' }
    ],
    edges: [
      { d: 'M 105 90 L 280 50', label: '"approve"', labelX: 190, labelY: 58 },
      { d: 'M 105 110 L 280 140', label: '"reject"', labelX: 190, labelY: 140 }
    ],
    sequence: [0, 1],
    code: `check = Check()
approve = Approve()
reject = Reject()
check - "approve" >> approve
check - "reject" >> reject
flow = Flow(start=check)  # Check → Approve 或 Reject`
  },
  loop: {
    desc: '循环模式：post() 返回 "retry" 回到自身，返回 "done" 结束',
    nodes: [
      { icon: '📝', name: 'Draft', style: 'left: 30px; top: 70px;' },
      { icon: '🔍', name: 'Review', style: 'left: 230px; top: 70px;' },
      { icon: '✅', name: 'Done', style: 'left: 430px; top: 70px;' }
    ],
    edges: [
      { d: 'M 105 100 L 230 100', label: 'default', labelX: 167, labelY: 90 },
      { d: 'M 305 100 L 430 100', label: '"done"', labelX: 367, labelY: 90 },
      { d: 'M 280 75 C 280 20, 80 20, 80 75', label: '"retry"', labelX: 180, labelY: 20 }
    ],
    sequence: [0, 1, 0, 1, 2],
    code: `draft = Draft()
review = Review()
done = Done()
draft >> review
review - "retry" >> draft   # 不满意则重写
review - "done" >> done     # 满意则完成`
  }
}

const currentPattern = ref('chain')
const visitIndex = ref(-1)
const isRunning = ref(false)
const visitLog = ref([])

const activePattern = computed(() => patternData[currentPattern.value])

const selectPattern = (id) => {
  currentPattern.value = id
  resetGraph()
}

const getEdgeColor = (edge, i) => {
  return 'var(--vp-c-text-3)'
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms))

const runGraph = async () => {
  isRunning.value = true
  visitLog.value = []
  const seq = activePattern.value.sequence

  for (let i = 0; i < seq.length; i++) {
    visitIndex.value = seq[i]
    visitLog.value.push(activePattern.value.nodes[seq[i]].name)
    await sleep(800)
  }

  visitIndex.value = seq.length + 10
  isRunning.value = false
}

const resetGraph = () => {
  visitIndex.value = -1
  isRunning.value = false
  visitLog.value = []
}
</script>

<style scoped>
.flow-graph-demo {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
  padding: 1.5rem;
  margin: 1.5rem 0;
}

.header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}

.icon { font-size: 1.5rem; }

.title {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--vp-c-text-1);
}

.pattern-selector {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.pattern-btn {
  padding: 0.4rem 0.9rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  cursor: pointer;
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
  transition: all 0.2s;
}

.pattern-btn:hover { border-color: var(--vp-c-brand); }
.pattern-btn.active { background: var(--vp-c-brand); color: #fff; border-color: var(--vp-c-brand); }

.graph-area {
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.graph-desc {
  font-size: 0.88rem;
  color: var(--vp-c-text-2);
  margin-bottom: 0.75rem;
}

.graph-canvas {
  position: relative;
  width: 600px;
  max-width: 100%;
  height: 200px;
  margin: 0 auto 1rem;
}

.graph-edges {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.graph-node {
  position: absolute;
  width: 75px;
  height: 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg-soft);
  transition: all 0.3s;
  z-index: 2;
}

.graph-node.active {
  border-color: var(--vp-c-brand);
  box-shadow: 0 0 16px rgba(66, 133, 244, 0.2);
  transform: scale(1.08);
}

.graph-node.done {
  border-color: #67c23a;
  opacity: 0.65;
}

.gn-icon {
  font-size: 1.2rem;
  font-weight: 700;
}

.gn-name {
  font-size: 0.72rem;
  color: var(--vp-c-text-3);
  margin-top: 0.15rem;
}

.code-snippet {
  background: var(--vp-c-bg-alt);
  border-radius: 6px;
  overflow: hidden;
}

.code-snippet pre {
  margin: 0;
  padding: 0.75rem;
  font-size: 0.8rem;
  line-height: 1.5;
  font-family: var(--vp-font-family-mono);
  color: var(--vp-c-text-2);
  overflow-x: auto;
}

.controls {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.run-btn, .reset-btn {
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s;
}

.run-btn { background: var(--vp-c-brand); color: #fff; }
.run-btn:hover:not(:disabled) { opacity: 0.85; }
.run-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.reset-btn { background: var(--vp-c-bg); color: var(--vp-c-text-2); border: 1px solid var(--vp-c-divider); }
.reset-btn:hover { border-color: var(--vp-c-brand); color: var(--vp-c-brand); }

.visit-log {
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  padding: 0.75rem;
}

.log-title {
  font-weight: 600;
  font-size: 0.83rem;
  color: var(--vp-c-text-2);
  margin-bottom: 0.35rem;
}

.log-path {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.log-node {
  background: var(--vp-c-brand);
  color: #fff;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.log-sep {
  color: var(--vp-c-text-3);
  font-size: 0.9rem;
}
</style>
