<template>
  <div>
    <h1 class="page-title">软件缺陷分派页面</h1>

    <el-form :model="form" label-width="120px">
      <el-form-item label="数据集">
        <el-select v-model="form.dataset" placeholder="请选择数据集">
          <el-option v-for="item in datasets" :key="item" :label="item" :value="item"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="模型参数">
        <el-select v-model="form.model" placeholder="请选择数据集">
          <el-option v-for="item in models" :key="item" :label="item" :value="item"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="总结">
        <el-input
          type="textarea"
          v-model="form.summary"
          autosize
          placeholder="请输入总结"
        ></el-input>
      </el-form-item>

      <el-form-item label="描述">
        <el-input
          type="textarea"
          v-model="form.description"
          autosize
          placeholder="请输入描述"
        ></el-input>
      </el-form-item>

      <el-row :gutter="20">
        <el-col :span="6">
          <el-form-item label="产品">
            <el-input v-model="form.product" placeholder="请输入产品"></el-input>
          </el-form-item>
        </el-col>

        <el-col :span="6">
          <el-form-item label="组件">
            <el-input v-model="form.component" placeholder="请输入组件"></el-input>
          </el-form-item>
        </el-col>

        <el-col :span="6">
          <el-form-item label="严重性">
            <el-input v-model="form.severity" placeholder="请输入严重性"></el-input>
          </el-form-item>
        </el-col>

        <el-col :span="6">
          <el-form-item label="优先级">
            <el-input v-model="form.priority" placeholder="请输入优先级"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <div class="button-group">
        <el-button type="primary" @click="startAssignment">开始分派</el-button>
        <el-button @click="exit">退出</el-button>
      </div>
    </el-form>

    <!-- 分割线 -->
    <hr />

    <!-- 推荐开发者列表 -->
    <div v-if="results.length > 0">
      <h2>推荐开发者列表</h2>
      <ul>
        <li v-for="(result, index) in results" :key="index">{{ result }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { API_BASE_URL } from '@/api/apiConfig' // 根据实际路径导入API_BASE_URL

const form = ref({
  dataset: '',
  model: '',
  summary: '',
  description: '',
  product: '',
  component: '',
  severity: '',
  priority: ''
})

const datasets = ref([])
const models = ref([])
const results = ref([])

onMounted(async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/datasets/`)
    datasets.value = response.data
    console.log(datasets.value)
  } catch (error) {
    console.error('Failed to fetch datasets:', error)
  }
  try {
    const response = await axios.get(`${API_BASE_URL}/api/models/`)
    models.value = response.data
    console.log(models.value)
  } catch (error) {
    console.error('Failed to fetch models:', error)
  }
})

const startAssignment = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/predict/`, form.value)
    console.log('开始分派', response.data)

    // 检查 response.data.predictions 是否为数组并包含元素
    if (Array.isArray(response.data.predictions)) {
      results.value = response.data.predictions
    } else {
      console.error('Unexpected response format:', response.data)
      results.value = ['Unexpected response format']
    }
  } catch (error) {
    console.error('Failed to start assignment:', error)
  }
}

const exit = () => {
  // 退出的逻辑
  console.log('退出')
}
</script>

<style scoped>
.page-title {
  text-align: center;
}

.button-group {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

hr {
  margin-top: 20px;
}

h2 {
  text-align: center;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  text-align: center;
  margin: 5px 0;
}
</style>
