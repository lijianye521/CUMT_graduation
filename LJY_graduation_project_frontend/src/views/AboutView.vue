<template>
  <div class="profile-view">
    <el-container>
      <el-header>
        <h1 class="custom-title">网站简介</h1>
      </el-header>
      <el-main>
        <p>
          本网站为个人毕业设计工作量和前端工作能力的体现。 代码仓库地址：<a
            href="https://github.com/lijianye521/CUMT_graduation"
          ></a
          >https://github.com/lijianye521/CUMT_graduation
        </p>
        <div>
          <h1 class="custom-title">系统功能</h1>

          <el-timeline>
            <el-timeline-item
              v-for="(item, index) in timelineItems"
              :key="index"
              :timestamp="item.timestamp"
              :color="item.color"
              :icon="item.icon"
            >
              <el-card shadow="hover">
                <h3>{{ item.title }}</h3>
                <p>{{ item.description }}</p>
              </el-card>
            </el-timeline-item>
          </el-timeline>
          <p>
            通过清晰的布局和设计，本系统不仅展示个人信息和工作经历，还确保了界面的一致性和响应性，同时展示了模型的高效性和准确性。
          </p>
        </div>
        <h1 class="custom-title">技术栈</h1>

        <el-row>
          <el-col :span="24">
            <el-card shadow="hover">
              <strong>Vue.js:</strong>
              一个渐进式的JavaScript框架，用于构建用户界面。Vue的核心库只关注视图层，易于学习且易于与其他库或已有项目整合。
            </el-card>
          </el-col>

          <el-col :span="24">
            <el-card shadow="hover">
              <strong>Element UI:</strong> 一套为开发者、设计师和产品经理准备的基于 Vue 3.0
              的桌面端组件库，提供了丰富的组件选择，使得开发更加快捷。
            </el-card>
          </el-col>

          <el-col :span="24">
            <el-card shadow="hover">
              <strong>Django:</strong>
              一个高级的 Python Web 框架，鼓励快速开发和干净、实用的设计。Django 遵循 "不要重复自己"
              的原则，旨在简化数据库驱动网站的开发。
            </el-card>
          </el-col>

          <el-col :span="24">
            <el-card shadow="hover">
              <strong>Transformer:</strong>
              一种基于自注意力机制的深度学习模型架构，广泛用于处理序列到序列的任务，如机器翻译和文本摘要。Transformer
              模型的设计支持并行处理和有效地学习长距离依赖。
            </el-card>
          </el-col>
        </el-row>

        <h1 class="custom-title">作者个人简介</h1>
        <p>
          李建业，一名具备广泛技术背景的软件工程师，拥有丰富的前端和后端开发经验。精通多种编程语言和框架，包括但不限于
          PHP、HTML5、CSS、JavaScript、C++ 和 Python。在前端方面，李建业精通使用 Vue.js 和 React
          等现代 JavaScript 框架，能够创建用户友好的界面和交互体验。
        </p>
        <el-link :underline="false" href="https://www.lijianye.work/" target="_blank"
          >访问李建业的个人网站</el-link
        >
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const timelineItems = ref([
  {
    timestamp: '预处理阶段',
    title: '软件缺陷报告预处理',
    description: '对输入的缺陷报告进行清洗和格式化，为后续处理阶段准备数据。',
    color: 'green',
    icon: 'el-icon-s-check'
  },
  {
    timestamp: '提取阶段',
    title: '语义信息提取',
    description: '使用如Bert模型等先进的深度学习技术提取报告中的关键语义信息。',
    color: 'blue',
    icon: 'el-icon-s-data'
  },
  {
    timestamp: '整合阶段',
    title: '整合语义信息',
    description: '通过深度学习模型如Bert，整合提取的语义信息，为分类提供准确的输入。',
    color: 'purple',
    icon: 'el-icon-s-operation'
  },
  {
    timestamp: '分类阶段',
    title: '分类',
    description: '基于提取和整合的信息，对缺陷报告进行准确分类。',
    color: 'red',
    icon: 'el-icon-s-marketing'
  },
  {
    timestamp: '评估阶段',
    title: '模型训练、校验、测试',
    description: '系统支持模型的全面训练、校验以及测试，确保模型的有效性和准确性。',
    color: 'orange',
    icon: 'el-icon-s-flag'
  }
])

// 这里可以保持空白，因为已经移除了表格相关的数据
</script>

<style scoped>
.profile-view {
  font-family: Arial, sans-serif;
}
.custom-title {
  font-size: 28px;
  color: #409eff; /* Element UI primary color */
  font-weight: bold;
  padding: 10px 0;
  border-bottom: 2px solid #409eff;
}
</style>
