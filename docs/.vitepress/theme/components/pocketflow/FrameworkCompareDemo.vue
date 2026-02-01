<!--
  FrameworkCompareDemo.vue
  PocketFlow 与其他框架对比组件

  用途：
  通过数据卡片对比 PocketFlow 和 LangChain、CrewAI 等框架，
  让读者直观理解 PocketFlow "极简"的定位

  交互功能：
  - 滑动对比不同维度（代码量、依赖、学习曲线等）
  - 高亮 PocketFlow 的优势指标
-->
<template>
  <div class="framework-compare">
    <div class="header">
      <span class="icon">⚖️</span>
      <span class="title">框架对比：为什么选择 PocketFlow？</span>
    </div>

    <div class="compare-table">
      <div class="table-header">
        <div class="th dimension">维度</div>
        <div class="th pf">PocketFlow</div>
        <div class="th other">LangChain</div>
        <div class="th other">CrewAI</div>
        <div class="th other">AutoGen</div>
      </div>

      <div v-for="row in rows" :key="row.dim" class="table-row">
        <div class="td dimension">
          <span class="dim-icon">{{ row.icon }}</span>
          <span>{{ row.dim }}</span>
        </div>
        <div :class="['td', 'pf', { best: row.pfBest }]">
          <span>{{ row.pf }}</span>
        </div>
        <div class="td other">{{ row.lc }}</div>
        <div class="td other">{{ row.crew }}</div>
        <div class="td other">{{ row.auto }}</div>
      </div>
    </div>

    <div class="insight-cards">
      <div class="insight" v-for="insight in insights" :key="insight.title">
        <div class="insight-icon">{{ insight.icon }}</div>
        <div class="insight-content">
          <div class="insight-title">{{ insight.title }}</div>
          <div class="insight-text">{{ insight.text }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const rows = [
  { icon: '📏', dim: '核心代码量', pf: '~100 行', lc: '~405K 行', crew: '~18K 行', auto: '~7K 行', pfBest: true },
  { icon: '📦', dim: '依赖数量', pf: '0', lc: '大量', crew: '中等', auto: '中等', pfBest: true },
  { icon: '🔒', dim: '供应商锁定', pf: '无', lc: '部分', crew: '部分', auto: '部分', pfBest: true },
  { icon: '📈', dim: '学习曲线', pf: '极低', lc: '陡峭', crew: '中等', auto: '中等', pfBest: true },
  { icon: '🧩', dim: '设计模式', pf: 'Node + Flow 图', lc: 'Chain / Agent', crew: 'Role-based', auto: 'Conversation', pfBest: false },
  { icon: '🔄', dim: '异步支持', pf: '内置', lc: '部分', crew: '内置', auto: '内置', pfBest: false },
  { icon: '🔀', dim: '并行批处理', pf: '内置', lc: '需扩展', crew: '内置', auto: '内置', pfBest: false },
  { icon: '🎯', dim: '适用场景', pf: '通用 LLM 应用', lc: '通用 LLM 应用', crew: '多 Agent', auto: '多 Agent', pfBest: false }
]

const insights = [
  {
    icon: '💡',
    title: '极简不等于简陋',
    text: '100 行代码覆盖了 Node、Flow、Batch、Async 四大核心抽象，足以构建 RAG、Agent、工作流等所有主流模式。'
  },
  {
    icon: '🔧',
    title: '零依赖 = 完全掌控',
    text: '没有第三方库意味着你可以完整理解框架的每一行代码，也不会被供应商版本升级所绑定。'
  },
  {
    icon: '🤖',
    title: 'Agentic Coding 友好',
    text: 'PocketFlow 鼓励"人类设计架构，AI 写实现代码"的开发模式，其极简核心让 AI 也能轻松理解和生成代码。'
  }
]
</script>

<style scoped>
.framework-compare {
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
.title { font-size: 1.15rem; font-weight: 700; color: var(--vp-c-text-1); }

.compare-table {
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 1.25rem;
  overflow-x: auto;
}

.table-header, .table-row {
  display: grid;
  grid-template-columns: 1.2fr 1fr 1fr 1fr 1fr;
  min-width: 550px;
}

.table-header {
  background: var(--vp-c-bg);
  border-bottom: 2px solid var(--vp-c-divider);
}

.th, .td {
  padding: 0.5rem 0.65rem;
  font-size: 0.82rem;
}

.th {
  font-weight: 700;
  color: var(--vp-c-text-1);
}

.th.pf { color: var(--vp-c-brand); }

.table-row {
  border-bottom: 1px solid var(--vp-c-divider);
}

.table-row:last-child { border-bottom: none; }

.td {
  color: var(--vp-c-text-2);
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.td.pf { font-weight: 600; }
.td.pf.best {
  color: var(--vp-c-brand);
  background: rgba(66, 133, 244, 0.05);
}

.td.dimension { font-weight: 500; color: var(--vp-c-text-1); }
.dim-icon { font-size: 1rem; }

.td.other { color: var(--vp-c-text-3); }

.insight-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
}

.insight {
  display: flex;
  gap: 0.65rem;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 0.75rem;
}

.insight-icon { font-size: 1.5rem; flex-shrink: 0; }
.insight-title { font-weight: 700; font-size: 0.88rem; color: var(--vp-c-text-1); margin-bottom: 0.2rem; }
.insight-text { font-size: 0.8rem; color: var(--vp-c-text-3); line-height: 1.5; }
</style>
