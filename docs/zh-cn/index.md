---
layout: home
hero:
  name: 'Easy-Pocket'
  text: '从零掌握 PocketFlow'
  tagline: '100 行代码的极简 LLM 框架 —— 零依赖，零门槛'
  actions:
    - theme: brand
      text: 开始学习
      link: /zh-cn/pocketflow-intro/
    - theme: alt
      text: GitHub
      link: https://github.com/The-Pocket/PocketFlow
features:
  - title: 极简核心
    details: 仅 100 行 Python 代码，零依赖。Node + Flow 两个抽象，覆盖 LLM 应用开发的所有主流模式。
  - title: 交互式教学
    details: 每个核心概念都配有交互式可视化演示，动手实验中就能理解 Node 生命周期和 Flow 图执行。
  - title: 案例驱动
    details: 9 个实战案例，从聊天机器人到多智能体协作，从 RAG 到并行批处理，覆盖入门到进阶。
  - title: Agentic Coding
    details: 人类设计架构，AI 写实现代码。PocketFlow 的极简设计让 AI 也能顺畅地理解和生成代码。
---

<div class="intro-section">
  <h2 class="intro-title">什么是 PocketFlow？</h2>
  <div class="stats-bar">
    <div class="stat-item">
      <div class="stat-number">100</div>
      <div class="stat-label">行核心代码</div>
    </div>
    <div class="stat-divider"></div>
    <div class="stat-item">
      <div class="stat-number">0</div>
      <div class="stat-label">外部依赖</div>
    </div>
    <div class="stat-divider"></div>
    <div class="stat-item">
      <div class="stat-number">12</div>
      <div class="stat-label">实战案例</div>
    </div>
  </div>
  <p class="intro-desc">
    用 <strong>Node</strong> 和 <strong>Flow</strong> 两个极简抽象，构建聊天机器人、RAG、智能体、工作流等主流 LLM 应用。
  </p>
  <blockquote class="intro-tagline">
    Node 做事，Flow 调度，shared 通信 —— 三个概念，构建一切。
  </blockquote>
</div>

<div class="stage-container">
  <a href="./pocketflow-intro/" class="stage-card">
    <div class="stage-icon">原理篇</div>
    <p>深入理解 PocketFlow 的核心设计：Node 三阶段模型、Flow 图执行、Batch 批处理与 Async 异步并发。</p>
    <span>开始学习 →</span>
  </a>
  <a href="./pocketflow-cases/" class="stage-card">
    <div class="stage-icon">案例篇</div>
    <p>12 个实战案例：聊天机器人、RAG、写作工作流、搜索智能体、多智能体协作、批处理、并行执行等。</p>
    <span>查看案例 →</span>
  </a>
  <a href="./appendix/" class="stage-card">
    <div class="stage-icon">附录</div>
    <p>计算机基础、开发工具、前后端、数据、架构、运维、AI、工程素养 —— 九大领域知识参考。</p>
    <span>查看附录 →</span>
  </a>
</div>

<style>
.intro-section {
  text-align: center;
  margin: 48px auto 40px;
  max-width: 800px;
  padding: 0 20px;
}

.intro-title {
  border: none;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 28px;
}

.stats-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 32px;
  margin-bottom: 24px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--vp-c-brand);
  line-height: 1.1;
}

.stat-label {
  font-size: 0.85rem;
  color: var(--vp-c-text-3);
  margin-top: 4px;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: var(--vp-c-divider);
}

.intro-desc {
  font-size: 1.1rem;
  color: var(--vp-c-text-2);
  line-height: 1.6;
  margin-bottom: 20px;
}

.intro-tagline {
  border-left: 3px solid var(--vp-c-brand);
  padding: 8px 16px;
  margin: 0 auto;
  display: inline-block;
  text-align: left;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  font-style: normal;
  background: var(--vp-c-bg-soft);
  border-radius: 0 8px 8px 0;
}

.stage-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.stage-card:nth-child(1) { --card-color: #3b82f6; }
.stage-card:nth-child(2) { --card-color: #8b5cf6; }
.stage-card:nth-child(3) { --card-color: #10b981; }

.stage-card {
  background-color: var(--vp-c-bg-soft);
  border-radius: 12px;
  padding: 24px;
  transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
  border: 1px solid var(--vp-c-bg-soft);
  position: relative;
  overflow: hidden;
  text-decoration: none;
}

.stage-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background-color: var(--card-color);
  opacity: 0.5;
  transition: opacity 0.2s;
}

.stage-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border-color: var(--card-color);
}

.stage-card:hover::before {
  opacity: 1;
}

.stage-icon {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: var(--card-color);
  opacity: 0.8;
}

.stage-card h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--vp-c-text-1);
  transition: color 0.2s;
}

.stage-card:hover h3 {
  color: var(--card-color);
}

.stage-card p {
  font-size: 0.9rem;
  color: var(--vp-c-text-2);
  margin-bottom: 16px;
  line-height: 1.5;
}
</style>

<style>
.footer-cta {
  margin-top: 80px;
  padding: 40px 24px;
  text-align: center;
  background: var(--vp-c-bg-soft);
  border-radius: 24px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 40px;
  border: 1px solid var(--vp-c-bg-soft);
  transition: border-color 0.3s;
}

.footer-cta:hover {
  border-color: var(--vp-c-brand);
}

.support-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 8px;
  color: var(--vp-c-text-1);
}

.support-text {
  font-size: 1.1rem;
  color: var(--vp-c-text-2);
}
</style>
