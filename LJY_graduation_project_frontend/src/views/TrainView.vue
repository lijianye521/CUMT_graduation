<template>
  <div style="display: flex; justify-content: center; align-items: center; margin-top: 50px">
    <div>
      <el-steps style="min-width: 900px" :active="active" finish-status="success">
        <el-step title="Step 1" description="上传数据集" icon="UploadFilled"></el-step>
        <el-step title="Step 2" description="设定模型训练任务" icon="Setting"></el-step>
        <el-step title="Step 3" description="开始训练" icon="Loading"></el-step>
      </el-steps>

      <el-button style="margin-top: 12px" :disabled="active === 1 && !uploadSuccess" @click="next"
        >Next step</el-button
      >
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
            <div class="el-upload__tip">jpg/png files with a size less than 500kb</div>
          </template>
        </el-upload>
      </div>

      <div style="margin-top: 20px">
        <el-form v-if="active === 1" label-position="right" label-width="100px">
          <el-form-item label="实验编号">
            <el-input v-model="experimentId"></el-input>
          </el-form-item>
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
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import axios from 'axios'
import { API_BASE_URL } from '@/api/apiConfig' // 根据实际路径导入API_BASE_URL

const active = ref(0)
const uploadSuccess = ref(false) // 用于跟踪上传是否成功
const datasets = ref([])
const experimentId = ref('') // 初始化实验编号
const selectedDataset = ref(null) // 初始化所选数据集
const selectedModel = ref(null) // 初始化所选模型

onMounted(async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/datasets/`)
    datasets.value = response.data
  } catch (error) {
    console.error('Failed to fetch datasets:', error)
  }
})

const next = () => {
  if (active.value < 2 && uploadSuccess.value) active.value++
  else if (active.value >= 2) active.value = 0
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
