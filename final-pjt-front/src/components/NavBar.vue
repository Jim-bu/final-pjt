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
      </div>
    </div>

    <!-- 두 번째 줄 -->
    <div class="navbar-search">
      <input
        type="text"
        placeholder=" 검색어를 입력하세요..."
        class="search-input"
      />
    </div>

    <!-- 세 번째 줄 (Sticky) -->
    <div class="navbar-bottom sticky">
      <button class="nav-btn" @click="goToPage('productList')">상품목록</button>
      <button class="nav-btn" @click="goToPage('recommendation')">상품추천</button>
      <button class="nav-btn" @click="goToPage('nearBank')">근처은행</button>
      <button class="nav-btn" @click="goToPage('community')">커뮤니티</button>
    </div>

    <!-- 하단 네비게이션 -->
    <div class="bottom-navbar">
      <button class="bottom-btn" @click="goToPage('list')">목록</button>
      <button class="bottom-btn" @click="goToPage('Main')">홈</button>
      <RouterLink to="/mypage" exact-active-class="active">
        <v-icon>mdi-account</v-icon>
      </RouterLink>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import { useUserStore } from '@/stores/users';

export default {
  name: "Navbar",
  setup() {
    const userStore = useUserStore();

    const isLoggedIn = computed(() => userStore.isLogin);

    const logout = () => {
      userStore.logOut();
    };

    const goToPage = (page) => {
      // 페이지 이동
      window.location.href = `/${page}`;
    };

    return {
      isLoggedIn,
      logout,
      goToPage,
    };
  },
};
</script>

<style scoped>
/* 전체 컨테이너 */
.navbar-container {
  width: 100%;
  max-width: 600px; /* 최대 너비 */
  margin: 0 auto;
  background-color: #000;
  color: #fff;
  box-sizing: border-box;
  position: relative;
  z-index: 1000; /* 최우선적으로 화면에 표시 */
}

/* 첫 번째 줄 */
.navbar-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  border-bottom: 1px solid #444;
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
  color: #fff;
  cursor: pointer;
  text-decoration: underline;
}

/* 두 번째 줄 */
.navbar-search {
  padding: 10px 20px;
  border-bottom: 1px solid #444;
}

.search-input {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
  color: #000;
  outline: none;
}

/* 세 번째 줄 (Sticky) */
.navbar-bottom {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 10px 0;
  background-color: #000;
  border-top: 1px solid #444;
}

.sticky {
  position: sticky;
  top: 0;
  z-index: 1001; /* 최우선적으로 화면에 표시 */
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.5);
}

/* 네비게이션 버튼 */
.nav-btn {
  background-color: transparent;
  color: #fff;
  border: none;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
}

.nav-btn:hover {
  text-decoration: underline;
}

/* 하단 네비게이션 */
.bottom-navbar {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%); /* 가운데 정렬 */
  width: 100%;
  max-width: 600px; /* 최대 너비 */
  background-color: #f2f2f2; /* 연한 회색 */
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 10px 0;
  box-shadow: 0px -2px 5px rgba(0, 0, 0, 0.1);
  z-index: 1002; /* 최우선적으로 화면에 표시 */
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
</style>
