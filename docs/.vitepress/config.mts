import { defineConfig } from 'vitepress'
// https://vitepress.dev/reference/site-config

// 1. 获取环境变量并判断
// 如果环境变量 EDGEONE 等于 '1'，说明在 EdgeOne 环境，使用根路径 '/'
// 否则默认是 GitHub Pages 环境，使用仓库子路径 '/easy-vecdb/'
const isEdgeOne = process.env.EDGEONE === '1'
const baseConfig = isEdgeOne ? '/' : '/easy-pocket/'

export default defineConfig({
  lang: 'zh-CN',
  title: "Datawhale开源教程",
  description: "AI前沿知识开源教程",
  base: baseConfig,
  markdown: {
    math: true
  },
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    logo: '/datawhale-logo.png',
    nav: [
      { text: 'PDF版本下载', link: 'https://github.com/datawhalechina/easy-pocket/releases' },
    ],
    search: {
      provider: 'local',
      options: {
        translations: {
          button: {
            buttonText: '搜索文档',
            buttonAriaLabel: '搜索文档'
          },
          modal: {
            noResultsText: '无法找到相关结果',
            resetButtonTitle: '清除查询条件',
            footer: {
              selectText: '选择',
              navigateText: '切换'
            }
          }
        }
      }
    },
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

    socialLinks: [
      { icon: 'github', link: 'https://github.com/datawhalechina/easy-pocket' }
    ],

    editLink: {
      pattern: 'https://github.com/datawhalechina/easy-pocket/blob/main/docs/:path'
    },

    footer: {
      message: '<a href="https://beian.miit.gov.cn/" target="_blank">京ICP备2026002630号-1</a> | <a href="https://beian.mps.gov.cn/#/query/webSearch?code=11010602202215" rel="noreferrer" target="_blank">京公网安备11010602202215号</a>',
      copyright: '本作品采用 <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议（CC BY-NC-SA 4.0）</a> 进行许可'
    }
  }
})
