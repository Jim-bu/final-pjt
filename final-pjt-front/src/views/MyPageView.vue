<script setup>
import { ref, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/users'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'

const userStore = useUserStore()
const router = useRouter()
const { userInfo } = storeToRefs(userStore)

onMounted(() => {
  checkAuth()
})

const checkAuth = () => {
  if (!userStore.isLogin) {
    router.push({
      name: 'login',
      query: { redirect: router.currentRoute.value.fullPath }
    })
  }
}

// userStore.isLogin 상태 변화 감지
watch(() => userStore.isLogin, (newValue) => {
  if (!newValue) {
    checkAuth()
  }
})
</script>

<template>
  <div v-if="userStore.isLogin" class="container">
    <header class="d-flex align-center mb-7">
      <RouterLink 
        :to="{ name: 'myPage', params: { username: userStore.userInfo?.username }}" 
        exact-active-class="active"
      >
        회원 정보 관리
      </RouterLink>
      <p>|</p>
      <div class="button-container">
        <RouterLink 
          :to="{ name: 'userUpdate' }" 
          class="edit-button"
        >
          회원 정보 수정
        </RouterLink>
      </div>
    </header>
    <RouterView />
  </div>
  <div v-else class="loading-container">
    <div class="loading-message">
      <p>로그인이 필요한 서비스입니다</p>
      <RouterLink :to="{ name: 'login' }" class="login-link">로그인 하기</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.container {
  width: 600px;
  margin: 2rem auto;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50vh;
}

.loading-message {
  text-align: center;
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.loading-message p {
  color: #666;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.login-link {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  background-color: #e4c089;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.login-link:hover {
  background-color: #d8b679;
}

header {
  gap: 10px;
  font-size: 17px;
}

header a {
  font-weight: 600;
  font-size: 20px;
  letter-spacing: -1px;
  color: #222;
  text-decoration: none;
}

a.active {
  color: #5c5c4e;
}
</style>