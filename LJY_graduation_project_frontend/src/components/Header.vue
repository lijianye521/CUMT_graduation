<template>
  <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    :ellipsis="false"
    @select="handleSelect"
  >
    <el-menu-item index="0">
      <img
        style="width: 200px"
        src="/images/mylogo.svg"
        alt="Element logo"
      /> 
    </el-menu-item>
    <div class="flex-grow" />
    <el-menu-item index="1">主页</el-menu-item>
    <el-sub-menu index="2">
      <template #title>提供服务</template>
      <el-menu-item index="2-1">模型训练</el-menu-item>
      <el-menu-item index="2-2">item two</el-menu-item>
      <el-menu-item index="2-3">item three</el-menu-item>
      <el-sub-menu index="2-4">
        <template #title>模型情况对比</template>
        <el-menu-item index="2-4-1">精确度对比</el-menu-item>
        <el-menu-item index="2-4-2">item two</el-menu-item>
        <el-menu-item index="2-4-3">item three</el-menu-item>
      </el-sub-menu>
    </el-sub-menu>
    <el-menu-item index="3">关于本站</el-menu-item>
    
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
import { ref } from 'vue'
import { useRouter } from 'vue-router' // 引入useRouter
import { useDark, useToggle } from '@vueuse/core'
import { Moon, Sunny } from '@element-plus/icons-vue'

const isDark = useDark()
const toggleDark = useToggle(isDark)
const value1 = ref(true)
//路由相关
const router = useRouter() // 使用useRouter
const activeIndex = ref('1')
const handleSelect = (key, keyPath) => {
  console.log(key, keyPath)
  if (key === '1') { // 检查是否点击的是“主页”菜单项
    router.push('/') // 跳转到/about路由
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