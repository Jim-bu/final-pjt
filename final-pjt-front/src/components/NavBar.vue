<template>
  <div class="navbar-container">
    <!-- 첫 번째 줄 -->
    <div class="navbar-top">
      <div class="navbar-logo">WWW</div>
      <div class="navbar-user-actions">
        <span @click="goToPage('mypage')" class="icon-link">
          <img :src="mypageIcon" alt="mypage" class="icon-image" />
        </span>
        <span @click="goToPage('wishlist')" class="icon-link">
          <img :src="jjimlistIcon" alt="jjimlist" class="icon-image" />
        </span>
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
    <div class="navbar-bottom">
      <button class="nav-btn" @click="goToPage('productList')">상품목록</button>
      <button class="nav-btn" @click="goToPage('recommendation')">상품추천</button>
      <button class="nav-btn" @click="goToPage('nearBank')">근처은행</button>
      <button class="nav-btn" @click="goToPage('community')">커뮤니티</button>
    </div>
  </div>
</template>

<script>
import mypageIcon from "@/assets/mypage.png";
import jjimlistIcon from "@/assets/jjimlist.png";

export default {
  name: "Navbar",
  data() {
    return {
      mypageIcon,
      jjimlistIcon,
    };
  },
  methods: {
    goToPage(page) {
      this.$router.push({ name: page });
    },
  },
};
</script>

<style scoped>
.navbar-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  background-color: #000;
  color: #fff;
  box-sizing: border-box;
  position: relative; /* Sticky를 지원 */
}

.navbar-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  border-bottom: 1px solid #444;
}

.icon-image {
  width: 20px;
  height: 20px;
  object-fit: cover;
}

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

.navbar-bottom {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 10px 0;
  border-top: 1px solid #444;
  background-color: #000;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.5);
}
</style>
