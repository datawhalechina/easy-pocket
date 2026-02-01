import DefaultTheme from 'vitepress/theme'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { onMounted, watch, nextTick } from 'vue'
import { useRoute } from 'vitepress'
import './style.css'

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

    onMounted(() => {
      optimizeImages()
    })

    watch(
      () => route.path,
      () =>
        nextTick(() => {
          optimizeImages()
        })
    )
  }
}
