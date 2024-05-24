<template>
  <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    :ellipsis="false"
    @select="handleSelect"
  >
    <el-menu-item index="0">
      <img style="width: 200px" src="/images/mylogo.svg" alt="Element logo" />
    </el-menu-item>
    <div class="flex-grow" />
    <el-menu-item index="1">主页</el-menu-item>
    <el-sub-menu index="2">
      <template #title>提供服务</template>
      <el-menu-item index="2-1">模型训练</el-menu-item>
      <el-menu-item index="2-2">缺陷分派</el-menu-item>
      <el-sub-menu index="2-4">
        <template #title>训练历史记录</template>
        <el-menu-item index="2-4-1">训练时间统计</el-menu-item>
        <el-menu-item index="2-4-2">训练图表</el-menu-item>
        <el-menu-item index="2-4-3">训练历史记录</el-menu-item>
      </el-sub-menu>
    </el-sub-menu>
    <el-menu-item index="3">关于本站</el-menu-item>
    <el-menu-item index="4" v-if="loginStatus === 0">
      <el-button text @click="dialog = true">登录 </el-button>
    </el-menu-item>

    <el-sub-menu index="5" v-if="loginStatus === 1">
      <template #title>
        <div class="switch-container">
          <el-avatar
            src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
          /></div
      ></template>
      <!-- <el-menu-item index="5-1">个人信息</el-menu-item> -->
      <el-menu-item index="5-2">退出登录</el-menu-item>
    </el-sub-menu>

    <el-drawer
      v-model="dialog"
      title="请输入您的登录信息!"
      :before-close="handleClose"
      direction="rtl"
      class="demo-drawer"
    >
      <div class="demo-drawer__content">
        <el-form :model="form">
          <el-form-item label="Name" :label-width="formLabelWidth">
            <el-input v-model="form.name" autocomplete="off" />
          </el-form-item>
          <el-form-item label="Password" :label-width="formLabelWidth">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入你的密码"
              show-password
            />
          </el-form-item>
        </el-form>
        <div class="demo-drawer__footer">
          <el-button @click="cancelForm">取消</el-button>
          <el-button type="primary" :loading="loading" @click="onClick">
            {{ loading ? '登录中 ...' : '登录' }}
          </el-button>
        </div>
      </div>
    </el-drawer>

    <div class="switch-container">
      <el-switch
        v-model="isDark"
        size="large"
        :active-value="Drak"
        :inactive-value="Light"
        :active-action-icon="Sunny"
        :inactive-action-icon="Moon"
      />
    </div>
  </el-menu>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDark, useToggle } from '@vueuse/core'
import { Moon, Sunny } from '@element-plus/icons-vue'
import { ElDrawer, ElMessageBox, ElMessage } from 'element-plus'
import { useUserStore } from '../stores/useUserStore'
import { API_BASE_URL } from '../api/apiConfig' // 根据实际路径导入API_BASE_URL
import { computed } from 'vue'

import axios from 'axios'
const { setLoginStatus, getLoginStatus } = useUserStore()
onMounted(() => {
  // 检查localStorage中是否有access_token
  const accessToken = localStorage.getItem('access_token')
  if (accessToken) {
    // 如果有令牌，假设用户已登录
    setLoginStatus(1)
  } else {
    // 如果没有令牌，假设用户未登录
    setLoginStatus(0)
  }
})
const formLabelWidth = '80px'
let timer
const Drak = true // 假设深色模式为true
const Light = false // 假设浅色模式为false
const isDark = useDark()
const toggleDark = useToggle(isDark)
const dialog = ref(false)
const loading = ref(false)
const loginStatus = computed(() => getLoginStatus())
const form = reactive({
  name: '',
  password: ''
})

const onClick = async () => {
  loading.value = true
  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/token/`,
      {
        username: form.name,
        password: form.password
      },
      {
        headers: {
          'Content-Type': 'application/json' // 确保发送的内容类型为application/json
        }
      }
    )
    // 登录成功，保存令牌
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)
    localStorage.setItem('username', form.name)
    setLoginStatus(1)
    ElMessage.success('登录成功')
    dialog.value = false // 关闭登录框
  } catch (error) {
    setLoginStatus(0)
    // 设置登录状态为未登录
    ElMessage.error('登录失败，请检查用户名和密码')
    console.error('登录失败：', error)
  } finally {
    loading.value = false
  }
}

const handleClose = (done) => {
  if (loading.value) {
    return
  }
  ElMessageBox.confirm('Do you want to submit?')
    .then(() => {
      loading.value = true
      timer = setTimeout(() => {
        done()
        setTimeout(() => {
          loading.value = false
        }, 400)
      }, 2000)
    })
    .catch(() => {
      // catch error
    })
}

const cancelForm = () => {
  loading.value = false
  dialog.value = false
  clearTimeout(timer)
}

// 路由相关
const router = useRouter()
const activeIndex = ref('1')
const handleSelect = (key, keyPath) => {
  console.log(key, keyPath)
  if (key === '1') {
    router.push('/') // 跳转到主页路由
  }
  if (key === '2-1') {
    router.push('/train') // 跳转到主页路由
  }
  if (key === '2-2') {
    router.push('/predict') // 跳转到主页路由
  }
  if (key === '2-4-2') {
    router.push('/diagram') // 跳转到历史记录路由
  }
  if (key === '2-4-1') {
    router.push('/time') // 跳转到历史记录路由
  }
  if (key === '2-4-3') {
    router.push('/history') // 跳转到历史记录路由
  }
  if (key === '5-2') {
    localStorage.clear() // 删除所有的localStorage数据
    setLoginStatus(0)
    // 设置登录状态为未登录
  }
}
</script>

<style>
.flex-grow {
  flex-grow: 1;
}
.switch-container {
  display: flex;
  align-items: center;
}
</style>
