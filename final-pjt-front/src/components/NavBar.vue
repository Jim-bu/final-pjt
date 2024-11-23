<template>
  <div class="navbar-container">
    <!-- 상단 네비게이션 -->
    <div class="navbar-top">
      <div class="navbar-logo" @click="goToPage('Main')">WWW</div>
      <div class="navbar-user-actions">
        <template v-if="isLoggedIn">
          <span class="action-link" @click="logout">로그아웃</span>
        </template>
        <template v-else>
          <span class="action-link" @click="goToPage('login')">로그인</span>
          <span class="action-link" @click="goToPage('signup')">회원가입</span>
        </template>
        <RouterLink
          to="/mypage"
          exact-active-class="active"
          class="custom-link"
        >
          <v-icon class="custom-icon">mdi-account</v-icon>
        </RouterLink>
      </div>
    </div>

    <div class="navbar-bottom">
      <button class="nav-btn" @click="goToPage('productList')">상품목록</button>
      <button class="nav-btn" @click="goToPage('productcompare')">상품비교</button>
      <button class="nav-btn" @click="goToPage('recommendation')">상품추천</button>
      <button class="nav-btn" @click="goToPage('nearBank')">근처은행</button>
    </div>

    <!-- 하단 네비게이션 -->
    <div class="bottom-navbar">
      <!-- 메뉴 버튼 -->
      <button class="bottom-btn" @click="openPopup">
        <v-icon>mdi-menu</v-icon>
      </button>

      <!-- 뒤로 가기 버튼 -->
      <button class="bottom-btn" @click="router.back">
        <v-icon>mdi-arrow-left</v-icon>
      </button>
    </div>
      <!-- 챗봇 버튼 -->
    <button class="chatbot-button" @click="chatbotStore.openModal">
      <v-icon>mdi-robot</v-icon>
    </button>

  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/users";
import { useChatbotStore } from "@/stores/chatbot";

const chatbotStore = useChatbotStore();

const openChatbot = () => {
  chatbotStore.openModal();
};

const userStore = useUserStore();
const router = useRouter();
const chatbotModal = ref(null);

const isLoggedIn = computed(() => userStore.isLogin);

const logout = () => {
  userStore.logOut();
};

const goToPage = (page) => {
  router.push(`/${page}`);
};

const openPopup = () => {
  router.push({ name: "PopupMenu" });
};

</script>

<style scoped>
/* 전체 컨테이너 */
.navbar-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  background-color: #85725d;
  color: #fff;
  z-index: 1000;
}

/* 상단 네비게이션 */
.navbar-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #85725d;
  color: #faf7f2;
  border-bottom: 1px solid #756451;
}

.navbar-bottom {
  position: sticky;
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 10px 0;
  background-color: #85725d; /* 변경된 배경색 */
  color: #faf7f2;
  border-top: 1px solid #756451;
  position: sticky;
  top: 0;
  z-index: 1001;
}

.navbar-logo {
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
}

.navbar-user-actions {
  display: flex;
  gap: 15px;
}

.action-link {
  color: #faf7f2;
  cursor: pointer;
  text-decoration: underline;
}

.custom-link {
  text-decoration: none;
}

.custom-icon {
  color: #ffffff;
  font-size: 24px;
}

/* 하단 네비게이션 */
.bottom-navbar {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 600px;
  background-color: #f2f2f2;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  padding: 10px 0;
  box-shadow: 0px -2px 5px rgba(0, 0, 0, 0.1);
  z-index: 1002;
}

.bottom-btn {
  background-color: transparent;
  color: #000;
  border: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
}

.bottom-btn:hover {
  text-decoration: underline;
}

/* 챗봇 버튼 */
.chatbot-button {
  position: fixed; /* 네비게이션 바와 독립적으로 고정 */
  bottom: 5px; /* 화면 하단 기준 위치 */
  left: 50%; /* 화면 중앙에 위치 */
  transform: translateX(-50%); /* X축 중앙 정렬 */
  background-color: #336948;
  color: white;
  border: none;
  border-radius: 50%;
  width: 64px;
  height: 64px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  z-index: 1003;
}

.chatbot-button:hover {
  background-color: #1b3620;
}
</style>
