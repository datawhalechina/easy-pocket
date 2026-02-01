<!--
  NodeLifecycleDemo.vue
  Node 三阶段生命周期可视化

  用途：
  直观展示 PocketFlow 节点的 prep → exec → post 三阶段模型，
  让读者输入自定义数据，观察数据如何在三个阶段之间流转

  交互功能：
  - 输入框编辑 shared 数据
  - 动画展示三阶段执行过程
  - 实时显示每个阶段的输入和输出
-->
<template>
  <div class="lifecycle-demo">
    <div class="header">
      <span class="icon">🔄</span>
      <span class="title">Node 三阶段生命周期</span>
    </div>

    <div class="lifecycle-flow">
      <div class="shared-store">
        <div class="store-label">shared（共享存储）</div>
        <div class="store-content">
          <code>{{ sharedDisplay }}</code>
        </div>
      </div>

      <div class="phases-row">
        <div
          v-for="(phase, index) in phases"
          :key="phase.name"
          :class="['phase-card', { active: activePhase === index, done: index < activePhase }]"
        >
          <div class="phase-num">{{ index + 1 }}</div>
          <div class="phase-name">{{ phase.name }}()</div>
          <div class="phase-desc">{{ phase.desc }}</div>
          <div class="phase-io">
            <div class="io-in">
              <span class="io-label">输入</span>
              <code class="io-val">{{ phase.input }}</code>
            </div>
            <div class="io-arrow">→</div>
            <div class="io-out">
              <span class="io-label">输出</span>
              <code class="io-val">{{ phase.output }}</code>
            </div>
          </div>
          <div v-if="index < 2" class="phase-connector">→</div>
        </div>
      </div>

      <div class="action-result" v-if="actionResult">
        <span class="action-label">post() 返回的 action：</span>
        <code class="action-value">{{ actionResult }}</code>
        <span class="action-desc">→ Flow 据此决定执行哪个后继节点</span>
      </div>
    </div>

    <div class="controls">
      <button class="run-btn" @click="runLifecycle" :disabled="isRunning">
        {{ isRunning ? '⏳ 执行中...' : '▶ 执行 _run(shared)' }}
      </button>
      <button class="reset-btn" @click="reset">↺ 重置</button>
    </div>

    <div class="info-box">
      <p>
        <span class="info-icon">💡</span>
        <strong>关键理解：</strong>
        <strong>prep</strong> 从 shared 读数据 →
        <strong>exec</strong> 执行核心逻辑（如调用 LLM）→
        <strong>post</strong> 将结果写回 shared 并返回 action。
        三个阶段职责分明，互不耦合。
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const activePhase = ref(-1)
const isRunning = ref(false)
const actionResult = ref('')
const sharedData = ref({ question: '什么是 PocketFlow？', answer: '' })

const sharedDisplay = computed(() => JSON.stringify(sharedData.value, null, 2))

const phases = computed(() => [
  {
    name: 'prep',
    desc: '从 shared 中读取所需数据',
    input: 'shared',
    output: activePhase.value >= 0 ? `"${sharedData.value.question}"` : '...'
  },
  {
    name: 'exec',
    desc: '执行核心业务逻辑',
    input: activePhase.value >= 1 ? `"${sharedData.value.question}"` : '...',
    output:
      activePhase.value >= 1
        ? '"PocketFlow 是一个 100 行的 LLM 框架"'
        : '...'
  },
  {
    name: 'post',
    desc: '将结果写回 shared，返回 action',
    input: activePhase.value >= 2 ? 'shared + exec_res' : '...',
    output: activePhase.value >= 2 ? '"default"' : '...'
  }
])

const sleep = (ms) => new Promise((r) => setTimeout(r, ms))

const runLifecycle = async () => {
  isRunning.value = true
  actionResult.value = ''
  sharedData.value = { question: '什么是 PocketFlow？', answer: '' }

  // Phase 0: prep
  activePhase.value = 0
  await sleep(1000)

  // Phase 1: exec
  activePhase.value = 1
  await sleep(1200)

  // Phase 2: post
  activePhase.value = 2
  sharedData.value = {
    question: '什么是 PocketFlow？',
    answer: 'PocketFlow 是一个 100 行的 LLM 框架'
  }
  await sleep(800)

  actionResult.value = '"default"'
  activePhase.value = 3
  isRunning.value = false
}

const reset = () => {
  activePhase.value = -1
  isRunning.value = false
  actionResult.value = ''
  sharedData.value = { question: '什么是 PocketFlow？', answer: '' }
}
</script>

<style scoped>
.lifecycle-demo {
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

.shared-store {
  background: var(--vp-c-bg);
  border: 1px dashed var(--vp-c-brand);
  border-radius: 8px;
  padding: 0.75rem;
  margin-bottom: 1rem;
}

.store-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--vp-c-brand);
  margin-bottom: 0.25rem;
}

.store-content code {
  font-size: 0.8rem;
  color: var(--vp-c-text-2);
  white-space: pre;
}

.phases-row {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.phase-card {
  flex: 1;
  border: 2px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 0.75rem;
  background: var(--vp-c-bg);
  position: relative;
  transition: all 0.3s;
}

.phase-card.active {
  border-color: var(--vp-c-brand);
  box-shadow: 0 0 12px rgba(66, 133, 244, 0.12);
}

.phase-card.done {
  border-color: #67c23a;
  opacity: 0.7;
}

.phase-num {
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--vp-c-brand);
  color: #fff;
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: 700;
  margin-bottom: 0.35rem;
}

.phase-name {
  font-family: var(--vp-font-family-mono);
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--vp-c-text-1);
  margin-bottom: 0.2rem;
}

.phase-desc {
  font-size: 0.8rem;
  color: var(--vp-c-text-3);
  margin-bottom: 0.5rem;
}

.phase-io {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.75rem;
}

.io-label {
  color: var(--vp-c-text-3);
  font-size: 0.7rem;
}

.io-val {
  font-size: 0.72rem;
  color: var(--vp-c-text-2);
  word-break: break-all;
}

.io-arrow {
  color: var(--vp-c-text-3);
  flex-shrink: 0;
}

.phase-connector {
  position: absolute;
  right: -16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
  color: var(--vp-c-text-3);
  z-index: 1;
}

.action-result {
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  font-size: 0.83rem;
  color: var(--vp-c-text-2);
  margin-bottom: 1rem;
}

.action-label { font-weight: 600; }
.action-value { color: var(--vp-c-brand); font-weight: 600; margin: 0 0.25rem; }
.action-desc { color: var(--vp-c-text-3); }

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

.run-btn {
  background: var(--vp-c-brand);
  color: #fff;
}

.run-btn:hover:not(:disabled) { opacity: 0.85; }
.run-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.reset-btn {
  background: var(--vp-c-bg);
  color: var(--vp-c-text-2);
  border: 1px solid var(--vp-c-divider);
}

.reset-btn:hover { border-color: var(--vp-c-brand); color: var(--vp-c-brand); }

.info-box {
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-left: 3px solid var(--vp-c-brand);
  border-radius: 6px;
  padding: 0.75rem 1rem;
}

.info-box p {
  margin: 0;
  font-size: 0.85rem;
  line-height: 1.6;
  color: var(--vp-c-text-2);
}

.info-icon { margin-right: 0.25rem; }

@media (max-width: 640px) {
  .phases-row { flex-direction: column; }
  .phase-connector {
    position: static;
    text-align: center;
    transform: rotate(90deg);
    margin: 0.2rem 0;
  }
}
</style>
