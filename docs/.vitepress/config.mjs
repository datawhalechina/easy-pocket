import { defineConfig } from 'vitepress'

const base = process.env.BASE || '/easy-pocket/'

export default defineConfig({
  base: base,
  // outline（页面导航）保持右侧默认位置，左侧放 sidebar 章节导航
  locales: {
    'zh-cn': {
      label: '简体中文',
      lang: 'zh-CN',
      link: '/zh-cn/',
      title: 'Easy-Pocket 教程',
      description:
        '从零掌握 PocketFlow —— 100 行代码的极简 LLM 框架',
      head: [
        ['link', { rel: 'icon', href: `${base}logo.png`.replace('//', '/') }],
        [
          'meta',
          {
            name: 'keywords',
            content:
              'PocketFlow,LLM,Agent,框架,教程,AI编程,Node,Flow,RAG,工作流'
          }
        ]
      ],
      themeConfig: {
        logo: `${base}logo.png`.replace('//', '/'),
        search: {
          provider: 'local'
        },
        outline: {
          level: [1, 6],
          label: '页面导航'
        },
        nav: [
          { text: 'GitHub', link: 'https://github.com/datawhalechina/easy-pocket' },
        ],
        sidebar: {
          '/zh-cn/': [
            {
              text: '原理篇',
              items: [
                { text: '引言：为什么需要 LLM 框架', link: '/zh-cn/pocketflow-intro/' },
                { text: '快速上手', link: '/zh-cn/pocketflow-intro/quickstart' },
                { text: '核心抽象：Node 与 Flow', link: '/zh-cn/pocketflow-intro/core-abstractions' },
                { text: '通信机制与设计模式', link: '/zh-cn/pocketflow-intro/communication-and-patterns' },
                { text: '深入源码', link: '/zh-cn/pocketflow-intro/source-code' },
                { text: '工具函数与开发范式', link: '/zh-cn/pocketflow-intro/tools-and-dev' },
              ]
            },
            {
              text: '案例篇',
              items: [
                { text: '案例地图', link: '/zh-cn/pocketflow-cases/' },
                { text: '入门：聊天机器人 / 写作 / RAG', link: '/zh-cn/pocketflow-cases/beginner' },
                { text: '智能体：搜索 / 多智能体', link: '/zh-cn/pocketflow-cases/agents' },
                { text: '批处理与并行', link: '/zh-cn/pocketflow-cases/batch-and-parallel' },
                { text: '输出质量：结构化 / 思维链', link: '/zh-cn/pocketflow-cases/output-quality' },
                { text: '高级智能体：MCP / 技能', link: '/zh-cn/pocketflow-cases/advanced-agents' },
                { text: '智能体编程', link: '/zh-cn/pocketflow-cases/agentic-coding' },
              ]
            },
            {
              text: '附录',
              items: [
                { text: '软件工程知识参考', link: '/zh-cn/appendix/' },
              ]
            }
          ]
        },
        footer: {
          message: 'Easy-Pocket —— 从零掌握 PocketFlow',
          copyright:
            '本作品采用 <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank">CC BY-NC-SA 4.0</a> 许可'
        }
      }
    }
  }
})
