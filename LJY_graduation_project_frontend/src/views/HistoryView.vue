<template>
  <div class="table-container">
    <el-table :data="sharedData" stripe style="width: 100%" height="750">
      <el-table-column prop="id" label="ID" width="100" sortable></el-table-column>
      <el-table-column prop="epoch" label="Epoch" width="90"></el-table-column>
      <el-table-column prop="start_time" label="Start Time" width="180" sortable>
        <template #default="{ row }">
          {{ formatDate(row.start_time) }}
        </template>
      </el-table-column>
      <el-table-column prop="end_time" label="End Time" width="180">
        <template #default="{ row }">
          {{ formatDate(row.end_time) }}
        </template>
      </el-table-column>
      <el-table-column prop="duration" label="Duration (min)" width="100">
        <template #default="{ row }">
          {{ formatDuration(row.duration) }}
        </template>
      </el-table-column>
      <el-table-column prop="model" label="Model" width="180"></el-table-column>
      <el-table-column prop="top1_accuracy" label="Top 1 Accuracy" width="100"></el-table-column>
      <el-table-column prop="top2_accuracy" label="Top 2 Accuracy" width="100"></el-table-column>
      <el-table-column prop="top3_accuracy" label="Top 3 Accuracy" width="100"></el-table-column>
      <el-table-column prop="top4_accuracy" label="Top 4 Accuracy" width="100"></el-table-column>
      <el-table-column prop="top5_accuracy" label="Top 5 Accuracy" width="100"></el-table-column>
      <el-table-column prop="top6_accuracy" label="Top 6 Accuracy" width="100"></el-table-column>
      <el-table-column prop="top7_accuracy" label="Top 7 Accuracy" width="100"></el-table-column>
      <el-table-column prop="top8_accuracy" label="Top 8 Accuracy" width="100"></el-table-column>
      <el-table-column prop="top9_accuracy" label="Top 9 Accuracy" width="100"></el-table-column>
      <el-table-column prop="top10_accuracy" label="Top 10 Accuracy" width="100"></el-table-column>
      <el-table-column
        prop="optional_feature"
        label="Optional Feature"
        width="180"
      ></el-table-column>
      <el-table-column prop="learning_rate" label="Learning Rate" width="130"></el-table-column>
      <el-table-column prop="dataset" label="Dataset" width="280"></el-table-column>
      <el-table-column prop="experiment_num" label="experiment_num" width="280"></el-table-column>
      <!-- 添加更多列，根据你的数据结构 -->
    </el-table>
  </div>

  <div style="margin-top: 20px; font-size: 20px" class="table-container">
    总共训练时间：<span id="totalDuration">{{ totalDuration }}</span> 小时
  </div>
</template>
<script setup>
import { onMounted, ref } from 'vue'

import { fetchAndStoreData, sharedData } from '@/api/training_info' // 确保路径正确

const totalDuration = ref(0)
console.log(sharedData)

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return (
    date.toLocaleDateString('zh-CN') + ' ' + date.toLocaleTimeString('zh-CN', { hour12: false })
  )
}

const formatDuration = (minute) => {
  return minute.toFixed(2)
}

const calculateTotalDuration = () => {
  const totalSeconds = sharedData.value.reduce((acc, cur) => acc + cur.duration, 0)
  const hours = (totalSeconds / 60).toFixed(2)
  console.log(hours)
  animateTotalDuration(0, parseFloat(hours), 3000) // 从0到计算出的总时长，持续时间3000ms
}

const animateTotalDuration = (startValue, endValue, duration) => {
  let startTimestamp = null
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp
    const progress = Math.min((timestamp - startTimestamp) / duration, 1)
    totalDuration.value = (progress * (endValue - startValue) + startValue).toFixed(2)
    if (progress < 1) {
      window.requestAnimationFrame(step)
    }
  }
  window.requestAnimationFrame(step)
}
onMounted(async () => {
  await fetchAndStoreData() // 确保数据加载完成
  calculateTotalDuration() // 然后计算总时长
})
</script>
<style>
.table-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 如果需要垂直居中也可以加上这个 */
}
.el-table {
  max-width: 90%; /* 例如，最大宽度为90% */
  /* 更多的样式调整 */
}
</style>
