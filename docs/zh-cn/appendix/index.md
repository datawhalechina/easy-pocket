---
title: '附录 —— 软件工程知识参考'
description: '涵盖计算机基础、开发工具、前后端、数据、架构、运维、AI、工程素养九大领域的参考资料。'
---

# 附录（Appendix）

> 本附录来自 Datawhale [Easy-Vibe](https://github.com/datawhalechina/easy-vibe) 项目，涵盖软件工程九大领域的基础知识。学习 PocketFlow 过程中遇到不熟悉的概念时，可以在这里查阅。

<div class="appendix-grid">
  <a href="https://datawhalechina.github.io/easy-vibe/zh-cn/appendix#一、计算机是怎么回事" target="_blank" class="appendix-card">
    <div class="appendix-icon">💻</div>
    <div class="appendix-name">计算机基础</div>
    <div class="appendix-desc">CPU、操作系统、数据编码、网络、数据结构与算法、编程语言与类型系统</div>
    <span class="appendix-link">前往阅读 ↗</span>
  </a>
  <a href="https://datawhalechina.github.io/easy-vibe/zh-cn/appendix#二、开发环境与工具" target="_blank" class="appendix-card">
    <div class="appendix-icon">🛠️</div>
    <div class="appendix-name">开发工具</div>
    <div class="appendix-desc">IDE、命令行、Git 版本控制、环境变量、包管理器、调试技巧、正则表达式</div>
    <span class="appendix-link">前往阅读 ↗</span>
  </a>
  <a href="https://datawhalechina.github.io/easy-vibe/zh-cn/appendix#三、浏览器与前端" target="_blank" class="appendix-card">
    <div class="appendix-icon">🌐</div>
    <div class="appendix-name">浏览器与前端</div>
    <div class="appendix-desc">JavaScript/TypeScript、前端框架、浏览器原理、渲染管线、状态管理、性能优化</div>
    <span class="appendix-link">前往阅读 ↗</span>
  </a>
  <a href="https://datawhalechina.github.io/easy-vibe/zh-cn/appendix#四、服务器与后端" target="_blank" class="appendix-card">
    <div class="appendix-icon">🖥️</div>
    <div class="appendix-name">服务器与后端</div>
    <div class="appendix-desc">HTTP 协议、Web 框架、API 设计、认证授权、并发模式、缓存策略、消息队列</div>
    <span class="appendix-link">前往阅读 ↗</span>
  </a>
  <a href="https://datawhalechina.github.io/easy-vibe/zh-cn/appendix#五、数据" target="_blank" class="appendix-card">
    <div class="appendix-icon">📊</div>
    <div class="appendix-name">数据</div>
    <div class="appendix-desc">数据库基础、数据模型、用户行为追踪、数据分析、A/B 测试、数据可视化</div>
    <span class="appendix-link">前往阅读 ↗</span>
  </a>
  <a href="https://datawhalechina.github.io/easy-vibe/zh-cn/appendix#六、架构与系统设计" target="_blank" class="appendix-card">
    <div class="appendix-icon">🏗️</div>
    <div class="appendix-name">架构与系统设计</div>
    <div class="appendix-desc">单体到微服务演进、分布式系统挑战、高可用设计、系统设计方法论</div>
    <span class="appendix-link">前往阅读 ↗</span>
  </a>
  <a href="https://datawhalechina.github.io/easy-vibe/zh-cn/appendix#七、基础设施与运维" target="_blank" class="appendix-card">
    <div class="appendix-icon">☁️</div>
    <div class="appendix-name">基础设施与运维</div>
    <div class="appendix-desc">Linux、Docker、Kubernetes、CI/CD、DNS/HTTPS、负载均衡、云平台、监控</div>
    <span class="appendix-link">前往阅读 ↗</span>
  </a>
  <a href="https://datawhalechina.github.io/easy-vibe/zh-cn/appendix#八、人工智能" target="_blank" class="appendix-card">
    <div class="appendix-icon">🤖</div>
    <div class="appendix-name">人工智能</div>
    <div class="appendix-desc">AI 发展史、神经网络、Transformer、大语言模型、Prompt 工程、RAG、AI Agent</div>
    <span class="appendix-link">前往阅读 ↗</span>
  </a>
  <a href="https://datawhalechina.github.io/easy-vibe/zh-cn/appendix#九、工程素养" target="_blank" class="appendix-card">
    <div class="appendix-icon">📐</div>
    <div class="appendix-name">工程素养</div>
    <div class="appendix-desc">代码质量、测试策略、设计模式、安全意识、技术写作、开源协作</div>
    <span class="appendix-link">前往阅读 ↗</span>
  </a>
</div>

::: tip 使用建议
- 按需查阅，不必从头到尾读完
- 学习 PocketFlow 时遇到不熟悉的概念（如 HTTP、异步、API 设计等），直接跳转对应章节
:::

<style>
.appendix-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
  margin: 24px 0;
}

.appendix-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-bg-soft);
  border-radius: 12px;
  padding: 20px;
  text-decoration: none;
  transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
  display: flex;
  flex-direction: column;
}

.appendix-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  border-color: var(--vp-c-brand);
}

.appendix-icon {
  font-size: 1.8rem;
  margin-bottom: 8px;
}

.appendix-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin-bottom: 6px;
}

.appendix-desc {
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
  line-height: 1.5;
  flex: 1;
}

.appendix-link {
  font-size: 0.85rem;
  color: var(--vp-c-brand);
  margin-top: 12px;
  font-weight: 500;
}
</style>
