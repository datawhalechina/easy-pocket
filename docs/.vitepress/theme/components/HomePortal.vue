<script setup>
import { withBase } from 'vitepress'
import { onMounted, ref } from 'vue'
import TextType from './TextType.vue'

// ── Typing Taglines ──
const taglines = [
  'Node 做事，Flow 调度，shared 通信。',
  '100 行代码，构建 LLM 应用的一切。',
  '极简设计，让 AI 也能理解和生成代码。',
  '从聊天机器人到多智能体协作。',
  '人类设计架构，AI 写实现代码。'
]

// ── Feature Highlights (4 cards) ──
const features = [
  {
    icon: '⚡',
    title: '极简核心',
    desc: '仅 100 行 Python 代码，零依赖。Node + Flow 两个抽象，覆盖 LLM 应用开发的所有主流模式。',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  },
  {
    icon: '🎯',
    title: '交互式教学',
    desc: '每个核心概念都配有交互式可视化演示，动手实验中就能理解 Node 生命周期和 Flow 图执行。',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
  },
  {
    icon: '🚀',
    title: '案例驱动',
    desc: '9 个实战案例，从聊天机器人到多智能体协作，从 RAG 到并行批处理，覆盖入门到进阶。',
    gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
  },
  {
    icon: '🤖',
    title: 'Agentic Coding',
    desc: '人类设计架构，AI 写实现代码。PocketFlow 的极简设计让 AI 也能顺畅地理解和生成代码。',
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
  }
]

// ── Stats ──
const stats = [
  { value: '100', label: '行核心代码' },
  { value: '0', label: '外部依赖' },
  { value: '12', label: '实战案例' }
]

// ── Three Sections ──
const sections = [
  {
    title: '原理篇',
    subtitle: '深入理解核心设计',
    desc: 'Node 三阶段模型、Flow 图执行、Batch 批处理与 Async 异步并发。',
    action: '开始学习',
    link: '/zh-cn/pocketflow-intro/',
    accent: 'linear-gradient(135deg, #FF9A9E 0%, #FECFEF 100%)',
    iconBg: 'linear-gradient(135deg, #FF9A9E 0%, #FAD0C4 100%)',
    icon: '📖'
  },
  {
    title: '案例篇',
    subtitle: '12 个实战案例',
    desc: '聊天机器人、RAG、写作工作流、搜索智能体、多智能体协作、批处理等。',
    action: '查看案例',
    link: '/zh-cn/pocketflow-cases/',
    accent: 'linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%)',
    iconBg: 'linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)',
    icon: '🔬'
  },
  {
    title: '附录',
    subtitle: '九大领域知识参考',
    desc: '计算机基础、开发工具、前后端、数据、架构、运维、AI、工程素养。',
    action: '查看附录',
    link: '/zh-cn/appendix/',
    accent: 'linear-gradient(135deg, #96E6A1 0%, #D4FC79 100%)',
    iconBg: 'linear-gradient(135deg, #96E6A1 0%, #D4FC79 100%)',
    icon: '📚'
  }
]

// ── Scroll Reveal ──
const portalRef = ref(null)

onMounted(() => {
  const el = portalRef.value
  if (!el) return
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed')
        }
      })
    },
    { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
  )
  el.querySelectorAll('.reveal').forEach((child) => observer.observe(child))
})
</script>

<template>
  <div class="portal" ref="portalRef">

    <!-- ════════ Hero ════════ -->
    <section class="hero">
      <!-- Decorative gradient orbs -->
      <div class="hero-orb hero-orb-1" />
      <div class="hero-orb hero-orb-2" />
      <div class="hero-orb hero-orb-3" />

      <div class="hero-inner">
        <h1 class="hero-name">Easy-Pocket</h1>
        <p class="hero-text">从零掌握 PocketFlow</p>
        <div class="hero-tagline">
          <ClientOnly>
            <TextType
              :text="taglines"
              :typing-speed="45"
              :initial-delay="0"
              :pause-duration="2500"
              :post-deleting-delay="500"
              :deleting-speed="18"
              :loop="true"
            />
          </ClientOnly>
        </div>
        <div class="hero-actions">
          <a class="btn-brand" :href="withBase('/zh-cn/pocketflow-intro/')">
            <span>开始学习</span>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M6 3l5 5-5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </a>
          <a class="btn-alt" href="https://github.com/The-Pocket/PocketFlow" target="_blank" rel="noreferrer">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
            <span>GitHub</span>
          </a>
        </div>
      </div>

      <!-- Scroll indicator -->
      <div class="scroll-hint">
        <span>向下探索</span>
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M10 4v12M5 11l5 5 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
    </section>

    <!-- ════════ Feature Highlights ════════ -->
    <div class="content-container">
      <div class="highlight-grid reveal">
        <div
          v-for="(f, i) in features"
          :key="i"
          class="highlight-card"
        >
          <div class="highlight-icon-wrap" :style="{ background: f.gradient }">
            <span class="highlight-icon">{{ f.icon }}</span>
          </div>
          <h3 class="highlight-title">{{ f.title }}</h3>
          <p class="highlight-desc">{{ f.desc }}</p>
        </div>
      </div>

      <!-- ════════ 什么是 PocketFlow？ ════════ -->
      <section class="what-section reveal">
        <h2 class="what-heading">什么是 PocketFlow？</h2>

        <div class="stats-bar">
          <div v-for="(s, i) in stats" :key="i" class="stat-item">
            <span class="stat-value">{{ s.value }}</span>
            <span class="stat-label">{{ s.label }}</span>
          </div>
        </div>

        <p class="what-desc">
          用 Node 和 Flow 两个极简抽象，构建聊天机器人、RAG、智能体、工作流等主流 LLM 应用。
        </p>

        <p class="what-tagline">
          Node 做事，Flow 调度，shared 通信 —— 三个概念，构建一切。
        </p>
      </section>

      <!-- ════════ 三大板块 ════════ -->
      <div class="section-grid reveal">
        <a
          v-for="(sec, i) in sections"
          :key="i"
          :href="withBase(sec.link)"
          class="section-card"
        >
          <div class="section-accent" :style="{ background: sec.accent }" />
          <div class="section-body">
            <div class="section-icon-wrap" :style="{ background: sec.iconBg }">
              <span class="section-icon">{{ sec.icon }}</span>
            </div>
            <h3 class="section-title">{{ sec.title }}</h3>
            <p class="section-subtitle">{{ sec.subtitle }}</p>
            <p class="section-desc">{{ sec.desc }}</p>
            <span class="section-action">
              {{ sec.action }}
              <svg width="14" height="14" viewBox="0 0 16 16" fill="none"><path d="M6 3l5 5-5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </span>
          </div>
        </a>
      </div>

      <!-- ════════ Footer CTA ════════ -->
      <div class="footer-callout reveal">
        <div class="footer-callout-inner">
          <h2>少即是多，<br>代码如此，框架亦然。</h2>
          <p>打开编辑器，写下你的第一个 Node。</p>
          <a class="cta-btn" :href="withBase('/zh-cn/pocketflow-intro/')">
            <span class="cta-cursor">&gt;_</span> Start
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ============================================================================
   Scroll Reveal Animation
   ============================================================================ */
.reveal {
  opacity: 0;
  transform: translateY(32px);
  transition: opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}
.reveal.revealed {
  opacity: 1;
  transform: translateY(0);
}

/* Staggered children inside highlight-grid */
.highlight-grid.revealed .highlight-card:nth-child(1) { transition-delay: 0s; }
.highlight-grid.revealed .highlight-card:nth-child(2) { transition-delay: 0.08s; }
.highlight-grid.revealed .highlight-card:nth-child(3) { transition-delay: 0.16s; }
.highlight-grid.revealed .highlight-card:nth-child(4) { transition-delay: 0.24s; }

.highlight-card {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.6s cubic-bezier(0.16, 1, 0.3, 1),
              box-shadow 0.3s ease;
}
.highlight-grid.revealed .highlight-card {
  opacity: 1;
  transform: translateY(0);
}

/* Staggered section cards */
.section-grid.revealed .section-card:nth-child(1) { transition-delay: 0s; }
.section-grid.revealed .section-card:nth-child(2) { transition-delay: 0.1s; }
.section-grid.revealed .section-card:nth-child(3) { transition-delay: 0.2s; }

.section-card {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.6s cubic-bezier(0.16, 1, 0.3, 1),
              box-shadow 0.3s ease;
}
.section-grid.revealed .section-card {
  opacity: 1;
  transform: translateY(0);
}

/* ============================================================================
   Hero
   ============================================================================ */
.hero {
  position: relative;
  min-height: 92vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 80px 24px 60px;
  box-sizing: border-box;
  overflow: hidden;
}

/* Decorative gradient orbs */
.hero-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.35;
  pointer-events: none;
  animation: orbFloat 8s ease-in-out infinite alternate;
}
:root.dark .hero-orb { opacity: 0.18; }

.hero-orb-1 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, #42d392 0%, transparent 70%);
  top: -80px; left: -100px;
  animation-delay: 0s;
}
.hero-orb-2 {
  width: 350px; height: 350px;
  background: radial-gradient(circle, #647eff 0%, transparent 70%);
  bottom: -60px; right: -80px;
  animation-delay: -3s;
}
.hero-orb-3 {
  width: 250px; height: 250px;
  background: radial-gradient(circle, #f093fb 0%, transparent 70%);
  top: 30%; right: 15%;
  animation-delay: -5s;
}

@keyframes orbFloat {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(30px, -20px) scale(1.1); }
}

.hero-inner {
  position: relative;
  z-index: 1;
  max-width: 680px;
  margin: 0 auto;
}

.hero-badge {
  display: inline-block;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.06em;
  color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
  padding: 6px 16px;
  border-radius: 980px;
  margin: 0 0 24px;
}

.hero-name {
  font-size: 52px;
  font-weight: 800;
  line-height: 1.08;
  letter-spacing: -0.03em;
  background: linear-gradient(135deg, #42d392 10%, #647eff 60%, #f093fb 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 0 40px rgba(66, 211, 146, 0.25));
  margin: 0 0 12px;
  padding: 0;
  border: none;
}

.hero-text {
  font-size: 34px;
  font-weight: 600;
  line-height: 1.25;
  color: var(--vp-c-text-1);
  margin: 0 0 20px;
}

.hero-tagline {
  min-height: 36px;
  font-size: 18px;
  font-weight: 500;
  color: var(--vp-c-text-2);
  margin-bottom: 36px;
  display: flex;
  justify-content: center;
}

.hero-actions {
  display: flex;
  gap: 14px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-brand {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 12px 28px;
  border-radius: 980px;
  font-size: 15px;
  font-weight: 600;
  color: #fff !important;
  background: linear-gradient(135deg, #42d392, #647eff);
  text-decoration: none;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1),
              box-shadow 0.25s ease;
  box-shadow: 0 4px 16px rgba(66, 211, 146, 0.3);
}
.btn-brand:hover {
  transform: translateY(-2px) scale(1.03);
  box-shadow: 0 8px 28px rgba(66, 211, 146, 0.4);
}
.btn-brand svg { transition: transform 0.2s; }
.btn-brand:hover svg { transform: translateX(3px); }

.btn-alt {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  border-radius: 980px;
  font-size: 15px;
  font-weight: 600;
  color: var(--vp-c-text-1) !important;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  text-decoration: none;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1),
              background 0.2s, border-color 0.2s;
  backdrop-filter: blur(12px);
}
.btn-alt:hover {
  transform: translateY(-2px) scale(1.03);
  background: var(--vp-c-bg);
  border-color: var(--vp-c-text-3);
}

/* Scroll hint */
.scroll-hint {
  position: absolute;
  bottom: 28px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  color: var(--vp-c-text-3);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.04em;
  animation: scrollBounce 2s ease-in-out infinite;
  opacity: 0.6;
}
@keyframes scrollBounce {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(6px); }
}

/* ============================================================================
   Content Container
   ============================================================================ */
.content-container {
  max-width: 1152px;
  margin: 0 auto;
  padding: 0 24px;
}

a { text-decoration: none; color: inherit; }

/* ============================================================================
   Feature Highlights (2x2 Grid)
   ============================================================================ */
.highlight-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  padding: 20px 0 24px;
}

.highlight-card {
  position: relative;
  background: var(--vp-c-bg-soft);
  border-radius: 20px;
  padding: 32px 28px 28px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(12px);
}
:root.dark .highlight-card {
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.04);
}
.highlight-card:hover {
  transform: translateY(-4px) !important;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.08);
}
:root.dark .highlight-card:hover {
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.3);
}

.highlight-icon-wrap {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.highlight-icon {
  font-size: 22px;
  line-height: 1;
  filter: saturate(0) brightness(10);
}

.highlight-title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 10px;
  color: var(--vp-c-text-1);
  border: none;
  padding: 0;
  letter-spacing: -0.01em;
}

.highlight-desc {
  font-size: 14px;
  line-height: 1.7;
  color: var(--vp-c-text-2);
  margin: 0;
}

/* ============================================================================
   什么是 PocketFlow？
   ============================================================================ */
.what-section {
  text-align: center;
  padding: 88px 0 72px;
}

.what-label {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--vp-c-brand-1);
  margin-bottom: 12px;
}

.what-heading {
  font-size: 40px;
  font-weight: 800;
  letter-spacing: -0.03em;
  margin-bottom: 44px;
  color: var(--vp-c-text-1);
  border: none;
  padding: 0;
  line-height: 1.15;
}

.stats-bar {
  display: flex;
  justify-content: center;
  gap: 64px;
  margin-bottom: 40px;
}

.stat-item {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  position: relative;
}
.stat-item:not(:last-child)::after {
  content: '';
  position: absolute;
  right: -32px;
  top: 50%;
  transform: translateY(-50%);
  width: 1px;
  height: 48px;
  background: var(--vp-c-divider);
}

.stat-value {
  font-size: 52px;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.03em;
  background: linear-gradient(135deg, #42d392, #647eff);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stat-label {
  font-size: 14px;
  font-weight: 600;
  color: var(--vp-c-text-3);
  letter-spacing: 0.02em;
}

.what-desc {
  font-size: 18px;
  line-height: 1.8;
  color: var(--vp-c-text-2);
  max-width: 600px;
  margin: 0 auto 24px;
}

.what-tagline {
  font-size: 17px;
  font-weight: 700;
  margin: 0;
  letter-spacing: 0.01em;
  background: linear-gradient(135deg, #42d392, #647eff);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* ============================================================================
   Section Cards (原理/案例/附录)
   ============================================================================ */
.section-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  padding-bottom: 96px;
}

.section-card {
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  background: var(--vp-c-bg-soft);
  border: 1px solid rgba(0, 0, 0, 0.06);
  text-decoration: none !important;
  backdrop-filter: blur(12px);
}
:root.dark .section-card {
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.04);
}
.section-card:hover {
  transform: translateY(-6px) !important;
  box-shadow: 0 20px 48px rgba(0, 0, 0, 0.1);
}
:root.dark .section-card:hover {
  box-shadow: 0 20px 48px rgba(0, 0, 0, 0.4);
}

.section-accent { height: 5px; width: 100%; }

.section-body {
  padding: 28px 28px 24px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.section-icon-wrap {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.section-icon {
  font-size: 20px;
  line-height: 1;
  filter: saturate(0) brightness(10);
}

.section-title {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 4px;
  color: var(--vp-c-text-1);
  border: none;
  padding: 0;
  letter-spacing: -0.01em;
}

.section-subtitle {
  font-size: 13px;
  font-weight: 600;
  color: var(--vp-c-brand-1);
  margin: 0 0 12px;
  letter-spacing: 0.01em;
}

.section-desc {
  font-size: 14px;
  line-height: 1.7;
  color: var(--vp-c-text-2);
  margin: 0 0 20px;
  flex: 1;
}

.section-action {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  font-weight: 700;
  color: var(--vp-c-brand-1);
  transition: gap 0.2s ease;
}
.section-card:hover .section-action {
  gap: 8px;
  color: var(--vp-c-brand-2);
}

/* ============================================================================
   Footer Callout
   ============================================================================ */
.footer-callout {
  margin: 0 -24px;
  padding: 0;
}

.footer-callout-inner {
  text-align: center;
  padding: 96px 32px;
  background: linear-gradient(160deg,
    rgba(66, 211, 146, 0.06) 0%,
    rgba(100, 126, 255, 0.06) 50%,
    rgba(240, 147, 251, 0.06) 100%
  );
  border-top: 1px solid var(--vp-c-divider);
  position: relative;
  overflow: hidden;
}
:root.dark .footer-callout-inner {
  background: linear-gradient(160deg,
    rgba(66, 211, 146, 0.04) 0%,
    rgba(100, 126, 255, 0.04) 50%,
    rgba(240, 147, 251, 0.04) 100%
  );
}

.footer-callout h2 {
  font-size: 44px;
  font-weight: 800;
  margin-bottom: 16px;
  line-height: 1.15;
  color: var(--vp-c-text-1);
  letter-spacing: -0.03em;
}

.footer-callout p {
  font-size: 18px;
  color: var(--vp-c-text-2);
  margin: 0 0 36px;
  line-height: 1.6;
}

.cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--vp-c-text-1);
  color: var(--vp-c-bg) !important;
  padding: 14px 36px;
  border-radius: 980px;
  font-size: 17px;
  font-weight: 600;
  font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
  text-decoration: none;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1),
              box-shadow 0.25s ease;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}
.cta-btn:hover {
  transform: translateY(-2px) scale(1.03);
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.18);
}
:root.dark .cta-btn:hover {
  background: #e0e0e0;
}

.cta-cursor {
  opacity: 0.5;
  animation: cursorBlink 1.2s step-end infinite;
}
@keyframes cursorBlink {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 0; }
}

/* ============================================================================
   Responsive
   ============================================================================ */
@media (min-width: 640px) {
  .hero-name { font-size: 60px; }
  .hero-text { font-size: 38px; }
  .hero-tagline { font-size: 20px; min-height: 36px; }
}

@media (min-width: 960px) {
  .hero-name { font-size: 72px; }
  .hero-text { font-size: 42px; }
  .hero-tagline { font-size: 22px; }
}

@media (max-width: 960px) {
  .hero { min-height: 80vh; }
  .section-grid { grid-template-columns: 1fr; }
  .what-heading { font-size: 32px; }
  .stats-bar { gap: 40px; }
  .stat-value { font-size: 44px; }
  .stat-item:not(:last-child)::after { right: -20px; height: 40px; }
  .footer-callout h2 { font-size: 36px; }
  .hero-orb-3 { display: none; }
}

@media (max-width: 640px) {
  .hero { min-height: 75vh; padding: 60px 20px 48px; }
  .hero-badge { font-size: 12px; padding: 5px 14px; margin-bottom: 20px; }
  .hero-name { font-size: 40px; }
  .hero-text { font-size: 26px; }
  .hero-tagline { font-size: 16px; min-height: 28px; }
  .highlight-grid { grid-template-columns: 1fr; }
  .highlight-card { padding: 24px; }
  .what-section { padding: 64px 0 56px; }
  .what-heading { font-size: 28px; }
  .what-desc { font-size: 16px; }
  .stats-bar { flex-wrap: wrap; gap: 28px; padding: 0 20px; }
  .stat-value { font-size: 38px; }
  .stat-item:not(:last-child)::after { display: none; }
  .footer-callout h2 { font-size: 30px; }
  .footer-callout-inner { padding: 64px 24px; }
  .hero-orb-1 { width: 250px; height: 250px; }
  .hero-orb-2 { width: 200px; height: 200px; }
  .scroll-hint { display: none; }
}
</style>
