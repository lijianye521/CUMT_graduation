<template>
  <div>
    <h2>实验的精准度变化对比</h2>
    <div class="selector-container">
      <div v-for="(selection, index) in selections" :key="index" class="selection-group">
        <el-select
          v-model="selection.experimentNum"
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
          v-model="selection.topValue"
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
        <el-button @click="addSelection" v-if="index === selections.length - 1">+</el-button>
        <el-button @click="removeSelection(index)" v-if="selections.length > 1">-</el-button>
      </div>
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
const topValues = ref([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
const selections = ref([{ experimentNum: null, topValue: null }])

const experimentNums = computed(() => {
  if (!sharedData.value) return []
  return Array.from(new Set(sharedData.value.map((item) => item.experiment_num))).sort(
    (a, b) => a - b
  )
})

const colors = [
  '#1f77b4',
  '#ff7f0e',
  '#2ca02c',
  '#d62728',
  '#9467bd',
  '#8c564b',
  '#e377c2',
  '#7f7f7f',
  '#bcbd22',
  '#17becf'
]

const updateChartData = () => {
  if (myChart && chartContainer.value) {
    const series = selections.value.map((selection, index) => {
      const filteredData = sharedData.value.filter(
        (item) => item.experiment_num === selection.experimentNum
      )
      return {
        data: filteredData.map((item) => ({
          value: item[`top${selection.topValue}_accuracy`],
          name: `Epoch ${item.epoch}`
        })),
        type: 'line',
        smooth: true,
        name: `实验 ${selection.experimentNum} Top ${selection.topValue}`,
        itemStyle: { color: colors[index % colors.length] }
      }
    })

    // 找到最大的 epoch 数
    const maxEpochs = Math.max(...sharedData.value.map((item) => item.epoch))

    const option = {
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        // 生成从 1 到 maxEpochs 的数组作为 xAxis 数据
        data: Array.from({ length: maxEpochs }, (_, i) => `Epoch ${i + 1}`)
      },
      yAxis: { type: 'value', axisLabel: { formatter: '{value} %' } },
      series: series,
      grid: { bottom: 80 },
      dataZoom: [
        {
          type: 'slider',
          start: 0,
          end: 100
        }
      ]
    }

    myChart.setOption(option, true)
  }
}
const addSelection = () => {
  selections.value.push({ experimentNum: null, topValue: null })
}

const removeSelection = (index) => {
  selections.value.splice(index, 1)
  updateChartData()
}

onMounted(async () => {
  await fetchAndStoreData()
  if (chartContainer.value) {
    myChart = echarts.init(chartContainer.value)
    updateChartData()
  }
})

watch(selections, updateChartData, { deep: true })
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
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}
.selection-group {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}
</style>
