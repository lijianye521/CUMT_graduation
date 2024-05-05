<template>
  <div>
    <h2>每一轮次的精准度图表</h2>
    <div class="selector-container">
      <el-select
        v-model="selectedExperimentNum"
        placeholder="请选择实验编号"
        @change="updateChartData"
        style="width: 240px"
      >
        <el-option v-for="num in experimentNums" :key="num" :label="'实验 ' + num" :value="num">
        </el-option>
      </el-select>
      <el-select
        v-model="selectedEpoch"
        placeholder="请选择Epoch"
        @change="updateChartData"
        style="width: 240px"
      >
        <el-option v-for="epoch in epochs" :key="epoch" :label="'Epoch ' + epoch" :value="epoch">
        </el-option>
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
const selectedEpoch = ref(null)

const experimentNums = computed(() => {
  if (!sharedData.value) return [] // 确保 sharedData.value 不是 null
  return Array.from(new Set(sharedData.value.map((item) => item.experiment_num))).sort(
    (a, b) => a - b
  )
})

const epochs = computed(() => {
  if (!selectedExperimentNum.value || !sharedData.value) return [] // 同样确保 sharedData.value 不是 null
  return Array.from(
    new Set(
      sharedData.value
        .filter((item) => item.experiment_num === selectedExperimentNum.value)
        .map((item) => item.epoch)
    )
  ).sort((a, b) => a - b)
})

const updateChartData = () => {
  if (myChart && chartContainer.value) {
    const selectedData = sharedData.value.find(
      (item) =>
        item.experiment_num === selectedExperimentNum.value && item.epoch === selectedEpoch.value
    )

    if (selectedData) {
      const data = [
        { name: 'Top 1', value: selectedData.top1_accuracy },
        { name: 'Top 2', value: selectedData.top2_accuracy },
        { name: 'Top 3', value: selectedData.top3_accuracy },
        { name: 'Top 4', value: selectedData.top4_accuracy },
        { name: 'Top 5', value: selectedData.top5_accuracy },
        { name: 'Top 6', value: selectedData.top6_accuracy },
        { name: 'Top 7', value: selectedData.top7_accuracy },
        { name: 'Top 8', value: selectedData.top8_accuracy },
        { name: 'Top 9', value: selectedData.top9_accuracy },
        { name: 'Top 10', value: selectedData.top10_accuracy }
      ]

      const option = {
        tooltip: {
          trigger: 'item', // 或者 'axis'
          formatter: '{b} : {c} %'
        },
        xAxis: {
          type: 'category',
          data: data.map((d) => d.name)
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value} %'
          }
        },
        series: [
          {
            data: data.map((d) => d.value),
            type: 'bar'
          }
        ]
      }

      myChart.setOption(option)
    }
  }
}

onMounted(async () => {
  await fetchAndStoreData()
  if (chartContainer.value) {
    myChart = echarts.init(chartContainer.value)
  }
})

watch(
  () => [selectedExperimentNum.value, selectedEpoch.value],
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
