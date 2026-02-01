---
layout: page
---

<script setup>
import { onMounted } from 'vue'
import { useRouter, useData } from 'vitepress'

onMounted(() => {
  const { site } = useData()
  const router = useRouter()
  router.go(site.value.base + 'zh-cn/')
})
</script>

<div style="display: flex; align-items: center; justify-content: center; min-height: 50vh;">
  <p style="color: var(--vp-c-text-3);">正在跳转...</p>
</div>
