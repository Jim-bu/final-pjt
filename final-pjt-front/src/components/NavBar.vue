<template>
  <div class="navbar-container">
    <!-- 첫 번째 줄 -->
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

    <!-- 세 번째 줄 (Sticky) -->
    <div class="navbar-bottom">
      <button class="nav-btn" @click="goToPage('productList')">상품목록</button>
      <button class="nav-btn" @click="goToPage('productcompare')">상품비교</button>
      <button class="nav-btn" @click="goToPage('recommendation')">상품추천</button>
      <button class="nav-btn" @click="goToPage('nearBank')">근처은행</button>
    </div>

    <!-- 하단 네비게이션 -->
    <div class="bottom-navbar">
      <button class="bottom-btn" @click="toggleModal">
        <svg xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 0 24 24" width="40px" fill="#5f6368"><path d="M0 0h24v24H0z" fill="none"/><path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm0-8h2V7H3v2zm4 4h14v-2H7v2zm0 4h14v-2H7v2zM7 7v2h14V7H7z"/></svg>      </button>
      <div class="chatbot-button-container">
        <button class="chatbot-button" @click="toggleChatbot">
          <v-icon>mdi-robot</v-icon>
        </button>
      </div>
      <button class="bottom-btn" @click="goBack">
      <v-icon>mdi-arrow-left</v-icon>
    </button>
<!-- 모달창 -->
<div
      v-if="isModalOpen"
      class="modal-overlay"
      @click="closeModalOnOutsideClick"
    >
      <div class="modal-content">
        <h3>목록</h3>
        <div class="menu-section">
          <h4>My-</h4>
          <ul>
            <li><button @click="goToPage('')">설문조사 하러 가기</button></li>
            <li><button @click="goToPage('bank-map')">근처 은행 찾기</button></li>
          </ul>
        </div>
        <div class="menu-section">
          <h4>금융정보</h4>
          <ul>
            <li><button @click="goToPage('exchange')">환율 정보 확인하기</button></li>
            <li><button @click="goToPage('news')">뉴스 페이지</button></li>
          </ul>
        </div>
        <div class="menu-section">
          <h4>금융상품</h4>
          <ul>
            <li><button @click="goToPage('product-list')">상품 목록 확인하기</button></li>
            <li><button @click="goToPage('recommendation')">상품 추천 받기</button></li>
          </ul>
        </div>
        <button class="close-button" @click="toggleModal">닫기</button>
      </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/users';

const userStore = useUserStore();
const router = useRouter();

const isLoggedIn = computed(() => userStore.isLogin);

const logout = () => {
  userStore.logOut();
};

const goToPage = (page) => {
  // 페이지 이동
  router.push(`/${page}`);
};

// 모달 상태 관리
const isModalOpen = ref(false);

const toggleModal = () => {
  isModalOpen.value = !isModalOpen.value;
};

// 모달 외부 클릭으로 닫기
const closeModalOnOutsideClick = (event) => {
  if (event.target.classList.contains('modal-overlay')) {
    isModalOpen.value = false;
  }
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
  /* position: relative; */
  z-index: 1000;
}

/* 첫 번째 줄 */
.navbar-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #85725d; /* 변경된 배경색 */
  color: #faf7f2; /* 변경된 글씨색 */
  border-bottom: 1px solid #756451;
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

/* 세 번째 줄 (Sticky) */
.navbar-bottom {
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

.custom-link {
  text-decoration: none; /* 링크 기본 스타일 제거 */
}

.custom-icon {
  color: #ffffff; /* 원하는 색상 적용 */
  font-size: 24px; /* 아이콘 크기 조정 가능 */
}

/* 하단 네비게이션 */
.bottom-navbar {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  max-width: 600px;
  background-color: #f2f2f2;
  display: flex;
  justify-content: space-between;
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

/* 챗봇 버튼 컨테이너 */
.chatbot-button-container {
  position: absolute;
  bottom: 15px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1003;
}

/* 챗봇 버튼 스타일 */
.chatbot-button {
  background-color: #336948;
  color: white;
  border: none;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  cursor: pointer;
}

.chatbot-button:hover {
  background-color: #1b3620;
}
</style>
