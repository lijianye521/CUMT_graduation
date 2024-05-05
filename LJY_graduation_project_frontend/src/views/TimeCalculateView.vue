<template>
  <div class="chart-container" ref="pieChartContainer"></div>
  <div style="margin-top: 20px; font-size: 20px" class="table-container">
    总共训练时间：<span id="totalDuration">{{ totalDuration }}</span> 小时
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import * as echarts from 'echarts'
import { fetchAndStoreData, sharedData } from '@/api/training_info'

const pieChartContainer = ref(null)
let pieChart = null

const experimentDurations = computed(() => {
  const durationSum = {}
  if (sharedData.value) {
    sharedData.value.forEach((item) => {
      if (durationSum[item.experiment_num]) {
        durationSum[item.experiment_num] += item.duration
      } else {
        durationSum[item.experiment_num] = item.duration
      }
    })
  }
  return Object.keys(durationSum).map((key) => ({
    name: `实验 ${key}`,
    value: (durationSum[key] / 60.0).toFixed(2)
  }))
})
const totalDuration = ref(0)

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
const initPieChart = () => {
  if (pieChartContainer.value) {
    pieChart = echarts.init(pieChartContainer.value)
    const option = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b} : {c} 小时 ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left',
        data: experimentDurations.value.map((item) => item.name)
      },
      series: [
        {
          name: '实验时间',
          type: 'pie',
          radius: '55%',
          center: ['50%', '60%'],
          data: experimentDurations.value,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    }
    pieChart.setOption(option)
  }
}

onMounted(async () => {
  await fetchAndStoreData()
  calculateTotalDuration() // 然后计算总时长
  initPieChart()
})
</script>

<style>
.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 500px;
}
.table-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 如果需要垂直居中也可以加上这个 */
}
</style>
