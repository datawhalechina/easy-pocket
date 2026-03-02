import DefaultTheme from 'vitepress/theme'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { onMounted, watch, nextTick } from 'vue'
import { useRoute } from 'vitepress'
import './style.css'
import './custom.css'

// Base Components
import StepBar from './components/base/StepBar.vue'

// PocketFlow Components
import PocketFlowQuickStart from './components/pocketflow/PocketFlowQuickStart.vue'
import CoreCodeDemo from './components/pocketflow/CoreCodeDemo.vue'
import NodeLifecycleDemo from './components/pocketflow/NodeLifecycleDemo.vue'
import FlowGraphDemo from './components/pocketflow/FlowGraphDemo.vue'
import FrameworkCompareDemo from './components/pocketflow/FrameworkCompareDemo.vue'
import CaseShowcase from './components/pocketflow/CaseShowcase.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.use(ElementPlus)

    // Base Components
    app.component('StepBar', StepBar)

    // PocketFlow Components
    app.component('PocketFlowQuickStart', PocketFlowQuickStart)
    app.component('CoreCodeDemo', CoreCodeDemo)
    app.component('NodeLifecycleDemo', NodeLifecycleDemo)
    app.component('FlowGraphDemo', FlowGraphDemo)
    app.component('FrameworkCompareDemo', FrameworkCompareDemo)
    app.component('CaseShowcase', CaseShowcase)
  },
  setup() {
    const route = useRoute()

    const optimizeImages = () => {
      const images = document.querySelectorAll('.vp-doc img')
      images.forEach((img) => {
        if (img.complete) {
          applyImageStyle(img)
        } else {
          img.onload = () => applyImageStyle(img)
        }
      })
    }

    const applyImageStyle = (img) => {
      const { naturalWidth, naturalHeight } = img
      if (!naturalWidth || !naturalHeight) return

      const ratio = naturalHeight / naturalWidth
      img.classList.remove(
        'img-tall',
        'img-very-tall',
        'img-ultra-tall',
        'img-limit-width'
      )

      if (ratio <= 1) {
        img.classList.add('img-limit-width')
        return
      }

      img.classList.add('img-tall')
      if (ratio > 2.2) {
        img.classList.add('img-ultra-tall')
      } else if (ratio > 1.3) {
        img.classList.add('img-very-tall')
      }
    }

    // 自动测量侧边栏/目录文字宽度，动态设置到刚好不换行
    const autoFitSidebars = () => {
      // --- 左侧边栏 ---
      const sidebarTexts = document.querySelectorAll('.VPSidebar .VPSidebarItem .text')
      if (sidebarTexts.length) {
        let maxW = 0
        sidebarTexts.forEach((el) => {
          // scrollWidth 是内容的完整宽度（不截断）
          maxW = Math.max(maxW, el.scrollWidth)
        })
        // 加上 padding(8+4) + 缩进余量(24) + 安全边距(8)
        const sidebarW = Math.max(160, Math.min(maxW + 44, 280))
        document.documentElement.style.setProperty('--vp-sidebar-width', sidebarW + 'px')
      }

      // --- 右侧目录 ---
      const outlineLinks = document.querySelectorAll('.VPDoc .outline-link')
      if (outlineLinks.length) {
        let maxW = 0
        outlineLinks.forEach((el) => {
          maxW = Math.max(maxW, el.scrollWidth)
        })
        // 加上 padding(8) + marker(16) + 安全边距(8)
        const asideW = Math.max(140, Math.min(maxW + 32, 280))
        document.querySelectorAll('.VPDoc .aside').forEach((el) => {
          el.style.setProperty('width', asideW + 'px', 'important')
          el.style.setProperty('max-width', asideW + 'px', 'important')
        })
        document.querySelectorAll('.VPDoc .aside-container').forEach((el) => {
          el.style.setProperty('width', (asideW - 8) + 'px', 'important')
        })
      }
    }

    onMounted(() => {
      optimizeImages()
      // 等 DOM 完全渲染后测量
      setTimeout(autoFitSidebars, 100)
    })

    watch(
      () => route.path,
      () =>
        nextTick(() => {
          optimizeImages()
          setTimeout(autoFitSidebars, 100)
        })
    )
  }
}
