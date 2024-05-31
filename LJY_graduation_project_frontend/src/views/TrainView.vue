<template>
  <div style="display: flex; justify-content: center; align-items: center; margin-top: 50px">
    <div>
      <el-steps style="min-width: 900px" :active="active" finish-status="success">
        <el-step title="Step 1" description="上传数据集" icon="UploadFilled"></el-step>
        <el-step title="Step 2" description="设定模型训练任务" icon="Setting"></el-step>
        <el-step title="Step 3" description="开始训练" icon="Loading"></el-step>
      </el-steps>

      <el-button style="margin-top: 12px" @click="next">Next step</el-button>
      <div style="margin-top: 20px">
        <el-upload
          v-if="active === 0"
          class="upload-demo"
          drag
          :before-upload="handleUpload"
          multiple
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
          <template #tip>
            <div class="el-upload__tip">情上传csv表格文件</div>
          </template>
        </el-upload>
      </div>

      <div style="margin-top: 20px">
        <el-form v-if="active === 1" label-position="right" label-width="100px">
          <el-form-item label="所用数据集">
            <el-select v-model="selectedDataset" placeholder="请选择数据集">
              <el-option v-for="item in datasets" :key="item" :label="item" :value="item">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="选用模型">
            <el-select v-model="selectedModel" placeholder="请选择模型">
              <el-option label="BERT" value="bert"></el-option>
              <el-option label="XLNet" value="xlnet"></el-option>
              <el-option label="GPT-2" value="gpt2"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="检查点路径">
            <el-input v-model="checkpointPath" placeholder="Bert_Eclipse.pth"></el-input>
          </el-form-item>
          <el-form-item label="实验编号">
            <el-input-number
              v-model="experimentNum"
              :min="1"
              :max="100"
              label="实验编号"
              :default="13"
            ></el-input-number>
          </el-form-item>
          <el-form-item label="可选特征">
            <el-input v-model="optionalFeature" placeholder="abstract+description"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <h1 v-if="active === 2">
        <el-text class="mx-1" type="primary" style="font-size: xx-large">训练中</el-text>
      </h1>
      <TrainingProgress v-if="active === 2" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import axios from 'axios'
import { API_BASE_URL } from '@/api/apiConfig' // 根据实际路径导入API_BASE_URL
import TrainingProgress from '@/components/TrainingProgress.vue'

const active = ref(0)
const uploadSuccess = ref(false) // 用于跟踪上传是否成功

const selectedDataset = ref(null)
const selectedModel = ref(null)
const checkpointPath = ref('Bert_Eclipse.pth')
const experimentNum = ref(13)
const optionalFeature = ref('abstract+description')
const datasets = ref([])
onMounted(async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/datasets/`)
    datasets.value = response.data
  } catch (error) {
    console.error('Failed to fetch datasets:', error)
  }
})

const next = async () => {
  if (active.value === 1) {
    selectedModel.value === 'bert'
    // 当 active 为 1 且 selectedModel 为 'bert' 时发送请求
    const data = {
      dataset: selectedDataset.value,
      model: selectedModel.value,
      checkpointPath: checkpointPath.value,
      experimentNum: experimentNum.value,
      optionalFeature: optionalFeature.value
    }
    try {
      const response = axios.post(`${API_BASE_URL}/api/trainbert`, data)
      console.log('Training started:', response.data)
      active.value++
    } catch (error) {
      console.error('Error starting training:', error)
    }
  } else if (active.value <= 2) {
    active.value++
  } else if (active.value > 2) {
    active.value = 0
  }
}

const handleUpload = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  const token = localStorage.getItem('access_token') // 获取存储的token
  try {
    const response = await axios.post(`${API_BASE_URL}/upload/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${token}` // 添加授权头
      }
    })
    if (response.status === 200) {
      uploadSuccess.value = true
      return true // 表示上传成功
    }
  } catch (error) {
    console.error('Upload failed:', error)
    return false // 表示上传失败
  }
}
</script>
