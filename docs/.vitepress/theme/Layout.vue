<script setup>
import DefaultTheme from 'vitepress/theme'
</script>

<template>
  <DefaultTheme.Layout />
</template>

<style>
/* Hide default VitePress hero — replaced by HomePortal's built-in hero */
.VPHomeHero {
  display: none !important;
}
</style>
