<template>
  <el-steps :active="active" align-center>
    <el-step
      v-for="(item, index) in items"
      :key="index"
      :title="item.title"
      :description="item.description"
    />
  </el-steps>
</template>

<script setup>
defineProps({
  active: {
    type: Number,
    default: 0
  },
  items: {
    type: Array,
    default: () => []
  }
})
</script>
