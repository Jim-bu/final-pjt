<template>
  <div class="recommendation-page">
    <h1>맞춤 금융 상품 추천</h1>

    <div v-if="!userStore.isLogin">
      <div class="overlay"></div>
      <div class="login-popup">
        <h2>로그인이 필요합니다</h2>
        <p>추천 목록을 보려면 로그인 또는 회원가입이 필요합니다.</p>
        <button @click="goToLogin">로그인</button>
        <button @click="goToSignup">회원가입</button>
      </div>
    </div>

    <div v-else class="recommend-list">
      <div
        v-for="(product, index) in recommendedProducts"
        :key="index"
        class="recommend-item"
      >
        <h3>{{ product.name }}</h3>
        <p>{{ product.description }}</p>
        <strong>금리: {{ product.rate }}%</strong>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useUserStore } from '@/stores/users';

const userStore = useUserStore();
const recommendedProducts = ref([]);

onMounted(() => {
  if (userStore.isLogin) {
    recommendedProducts.value = [
      { name: '안전한 예금 상품', description: '안정적인 금리를 제공합니다.', rate: 3.5 },
      { name: '높은 금리 적금 상품', description: '높은 이율을 제공합니다.', rate: 4.2 },
    ];
  }
});

function goToLogin() {
  window.location.href = '/login';
}

function goToSignup() {
  window.location.href = '/signup';
}
</script>

<style scoped>
.recommendation-page {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  z-index: 1000;
}

.login-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #fff;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  z-index: 1001;
  text-align: center;
  animation: popup-fade-in 0.5s ease-in-out;
}

.login-popup h2 {
  margin-bottom: 15px;
  font-size: 1.5rem;
}

.login-popup button {
  display: inline-block;
  margin: 10px;
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  background-color: #007bff;
  color: #fff;
  font-weight: bold;
  transition: background-color 0.3s;
}

.login-popup button:hover {
  background-color: #0056b3;
}

.recommend-list {
  margin-top: 20px;
  filter: blur(5px);
  opacity: 0.5;
}

.recommend-item {
  padding: 15px;
  margin-bottom: 10px;
  background: linear-gradient(to right, #f5f5f5, #e0e0e0);
  border-radius: 10px;
}

@keyframes popup-fade-in {
  from {
    opacity: 0;
    transform: translate(-50%, -60%);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -50%);
  }
}
</style>
