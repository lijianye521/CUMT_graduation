<template>
  <div>
    <h2>实验的精准度随epoch变化</h2>
    <div class="selector-container">
      <el-select
        v-model="selectedExperimentNum"
        placeholder="请选择实验编号"
        @change="updateChartData"
        style="width: 240px"
      >
        <el-option
          v-for="num in experimentNums"
          :key="num"
          :label="'实验 ' + num"
          :value="num"
        ></el-option>
      </el-select>
      <el-select
        v-model="selectedTopValue"
        placeholder="请选择Top值"
        @change="updateChartData"
        style="width: 240px"
      >
        <el-option
          v-for="top in topValues"
          :key="top"
          :label="'Top ' + top"
          :value="top"
        ></el-option>
      </el-select>
    </div>
    <div class="chart-container" ref="chartContainer"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import * as echarts from 'echarts'
import { fetchAndStoreData, sharedData } from '@/api/training_info'

const chartContainer = ref(null)
let myChart = null
const selectedExperimentNum = ref(null)
const selectedTopValue = ref(null)
const topValues = ref([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

const experimentNums = computed(() => {
  if (!sharedData.value) return [] // 确保 sharedData.value 不是 null
  return Array.from(new Set(sharedData.value.map((item) => item.experiment_num))).sort(
    (a, b) => a - b
  )
})

const updateChartData = () => {
  if (myChart && chartContainer.value) {
    const filteredData = sharedData.value.filter(
      (item) => item.experiment_num === selectedExperimentNum.value
    )
    const seriesData = filteredData.map((item) => ({
      value: item[`top${selectedTopValue.value}_accuracy`],
      name: `Epoch ${item.epoch}`
    }))

    const option = {
      tooltip: {
        trigger: 'axis'
      },
      xAxis: {
        type: 'category',
        data: filteredData.map((item) => `Epoch ${item.epoch}`)
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: '{value} %'
        }
      },
      series: [
        {
          data: seriesData,
          type: 'line',
          smooth: true
        }
      ],
      grid: {
        bottom: 80 // 调整底部的间距以容纳 dataZoom 控件
      },
      dataZoom: [
        {
          type: 'slider', // 使用滑动条形式的 dataZoom
          start: 0, // 初始时，滑动条覆盖的起始位置（0%）
          end: 100 // 初始时，滑动条覆盖的结束位置（100%）
        }
      ]
    }

    myChart.setOption(option)
  }
}

onMounted(async () => {
  await fetchAndStoreData()
  if (chartContainer.value) {
    myChart = echarts.init(chartContainer.value)
  }
})

watch(
  () => [selectedExperimentNum.value, selectedTopValue.value],
  () => {
    updateChartData()
  }
)
</script>

<style>
.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 500px;
}
.selector-container {
  display: flex;
  justify-content: center;
  align-items: center; /* 确保内容垂直居中 */
  margin-bottom: 20px;
}
</style>
