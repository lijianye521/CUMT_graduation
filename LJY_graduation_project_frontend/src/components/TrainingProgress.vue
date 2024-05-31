<template>
  <div class="demo-progress">
    <el-progress type="dashboard" :percentage="percentage2" :color="colors" />
    <div>{{ remainingTime }}</div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'

const totalDuration = 4 * 60 * 60 * 1000 // 4 hours in milliseconds
const updateInterval = 1000 // update every second
const percentage2 = ref(0)
const startTime = Date.now()
const currentTime = ref(Date.now()) // 添加一个响应式引用来存储当前时间

const colors = [
  { color: '#f56c6c', percentage: 20 },
  { color: '#e6a23c', percentage: 40 },
  { color: '#5cb87a', percentage: 60 },
  { color: '#1989fa', percentage: 80 },
  { color: '#6f7ad3', percentage: 100 }
]

const remainingTime = computed(() => {
  const elapsed = currentTime.value - startTime // 使用 currentTime 替代 Date.now()
  const remaining = totalDuration - elapsed
  return remaining > 0
    ? `${Math.floor(remaining / 3600000)}小时${Math.floor((remaining % 3600000) / 60000)}分钟${Math.floor((remaining % 60000) / 1000)}秒`
    : '完成'
})

onMounted(() => {
  const interval = setInterval(() => {
    currentTime.value = Date.now() // 更新 currentTime
    const elapsed = currentTime.value - startTime
    percentage2.value = ((elapsed / totalDuration) * 100).toFixed(3) // 保留三位小数
    if (elapsed >= totalDuration) {
      clearInterval(interval)
      percentage2.value = 100
    }
  }, updateInterval)
})
</script>
