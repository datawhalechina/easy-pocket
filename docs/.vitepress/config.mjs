import { defineConfig } from 'vitepress'

const base = process.env.BASE || '/easy-pocket/'

export default defineConfig({
  base: base,
  transformPageData(pageData) {
    // 将页面导航（outline）移到左侧，非首页生效
    if (pageData.frontmatter.layout !== 'home') {
      pageData.frontmatter.aside = 'left'
    }
  },
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
          {
            text: 'PocketFlow 原理',
            link: '/zh-cn/pocketflow-intro/'
          },
          {
            text: '应用案例',
            link: '/zh-cn/pocketflow-cases/'
          },
          {
            text: '附录',
            link: '/zh-cn/appendix/'
          }
        ],
        sidebar: {},
        footer: {
          message: 'Easy-Pocket —— 从零掌握 PocketFlow',
          copyright:
            '本作品采用 <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank">CC BY-NC-SA 4.0</a> 许可'
        }
      }
    }
  }
})
