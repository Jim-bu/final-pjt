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
      
        <button class="delete-button" @click="handleDeleteAccount">
          회원 탈퇴
        </button>
      </div>
    </header>

    <!-- MyPage 컴포넌트 -->
    <MyPage />

    <!-- 가입한 금융 상품 리스트 -->
    <section class="subscriptions">
      <h2>내가 가입한 금융 상품</h2>
      <ul v-if="subscriptions.length > 0">
        <li v-for="subscription in subscriptions" :key="subscription.id">
          {{ subscription.product_name }} (가입일: {{ subscription.subscribed_at }})
          <button @click="cancelSubscription(subscription)">구독 취소</button>
        </li>
      </ul>
      <p v-else>가입한 금융 상품이 없습니다.</p>
    </section>
  </div>

  <div v-else class="loading-container">
    <div class="loading-message">
      <p>로그인이 필요한 서비스입니다</p>
      <RouterLink :to="{ name: 'login' }" class="login-link">로그인 하기</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useProductStore } from "@/stores/product";
import { useUserStore } from "@/stores/users";
import { useRouter } from "vue-router";
import MyPage from "@/components/MyPage.vue";

const userStore = useUserStore();
const productStore = useProductStore();
const router = useRouter();

const subscriptions = ref([]);

// Fetch 구독 리스트 및 프로필 정보
onMounted(async () => {
  if (userStore.isLogin) {
    await productStore.fetchSubscriptions();
    subscriptions.value = productStore.subscriptions;
  }
});

// 구독 취소 처리
const cancelSubscription = async (subscription) => {
  const response = await productStore.toggleSubscription(subscription);
  alert(response.message);
  subscriptions.value = productStore.subscriptions; // 갱신
};

// 회원 탈퇴 처리
const handleDeleteAccount = async () => {
  if (confirm("정말로 회원 탈퇴를 진행하시겠습니까? 이 작업은 되돌릴 수 없습니다.")) {
    try {
      await userStore.deleteAccount();
      alert("회원 탈퇴가 완료되었습니다.");
      router.push({ name: "Main" });
    } catch (error) {
      console.error("회원 탈퇴 실패:", error);
      alert("회원 탈퇴 중 문제가 발생했습니다. 다시 시도해주세요.");
    }
  }
};
</script>

<style scoped>
.container {
  width: 800px;
  margin: 2rem auto;
}

.subscriptions {
  margin-top: 2rem;
}

.subscriptions h2 {
  margin-bottom: 1rem;
}

button {
  margin-left: 1rem;
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #c0392b;
}

.delete-button {
  margin-left: 10px;
  background-color: #c0392b;
  color: white;
  border: none;
  padding: 5px 15px;
  border-radius: 5px;
  cursor: pointer;
}

.delete-button:hover {
  background-color: #a93226;
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
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
