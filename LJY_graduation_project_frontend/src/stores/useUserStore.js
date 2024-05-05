import { ref } from 'vue';

// 创建一个响应式的登录状态
const loginStatus = ref(0); // 0为未登录，1为已登录

// 提供修改登录状态的函数
function setLoginStatus(status) {
    loginStatus.value = status;
}

// 提供读取登录状态的函数
function getLoginStatus() {
    return loginStatus.value;
}

// 导出函数，以便在其他组件中使用
export function useUserStore() {
    return {
        setLoginStatus,
        getLoginStatus,
    };
}