<template>
    <div style="display: flex; justify-content: center; align-items: center; margin-top: 50px;">
      <div>
        <el-steps style="min-width: 900px" :active="active" finish-status="success">
          <el-step title="Step 1" description="上传数据集" icon="UploadFilled"></el-step>
          <el-step title="Step 2" description="设定模型训练任务" icon="Setting"></el-step>
          <el-step title="Step 3" description="开始训练" icon="Loading"></el-step>
        </el-steps>

        <el-button style="margin-top: 12px" :disabled="active.value === 1 && !uploadSuccess" @click="next">Next step</el-button>
        <div style="margin-top:20px">
                <!-- 仅当 active.value 为 1 时显示的上传组件 -->
        <el-upload 
        v-if="active === 0"
        class="upload-demo"
        drag
        action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
        multiple
        >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
        Drop file here or <em>click to upload</em>
        </div>
        <template #tip>
            <div class="el-upload__tip">
                jpg/png files with a size less than 500kb
            </div>
        </template>
            </el-upload>
      </div>

    </div>
      </div>

    
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { UploadFilled } from '@element-plus/icons-vue'
  
  const active = ref(0)
  const uploadSuccess = ref(false) // 用于跟踪上传是否成功
  
  const next = () => {
    if (active.value < 2 && uploadSuccess.value) active.value++
    else if (active.value >= 2) active.value = 0
  }
  
  const handleUploadSuccess = () => {
    uploadSuccess.value = true // 上传成功时更新状态
  }
  </script>