<template>
  <div class="popup-menu-overlay" @click.self="closePopup">
    <div class="popup-menu">
      <h3>목록</h3>
      <div class="menu-section">
        <h4>My-</h4>
        <ul>
          <li class="menu-item level-1"><button @click="navigateTo('/')">설문조사 하러 가기</button></li>
          <li class="menu-item level-1"><button @click="navigateTo('/bank-map')">  근처 은행 찾기</button></li>
        </ul>
      </div>
      <div class="menu-section">
        <h4>금융정보</h4>
        <ul>
          <li class="menu-item level-1"><button @click="navigateTo('/exchange')">  환율 정보 확인하기</button></li>
          <li class="menu-item level-1"><button @click="navigateTo('/news')">  뉴스 페이지</button></li>
        </ul>
      </div>
      <div class="menu-section">
        <h4>금융상품</h4>
        <ul>
          <li class="menu-item level-1"><button @click="navigateTo('/product-list')">  상품 목록 확인하기</button></li>
          <li class="menu-item level-1"><button @click="navigateTo('/recommendation')">  상품 추천 받기</button></li>
        </ul>
      </div>
      <button class="close-button" @click="closePopup">닫기</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const closePopup = () => {
  router.back(); // 팝업창 닫기
};

const navigateTo = (path) => {
  router.push(path);
};
</script>

<style scoped>
.popup-menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 200;
}

.popup-menu {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.menu-section {
  margin-bottom: 20px;
}

.menu-section h4 {
  font-size: 18px;
  margin-bottom: 10px;
}

.menu-item.level-1 {
  padding-left: 10px; /* 1단계 들여쓰기 */
}

.menu-section ul {
  list-style: none;
  padding: 0;
}

.menu-section ul li {
  margin-bottom: 10px;
}

.menu-section ul li button {
  background: none;
  border: none;
  color: #424530;
  font-size: 16px;
  cursor: pointer;
  text-align: left;
  width: 100%;
}

.menu-section ul li button:hover {
  color: #ff7f50;
}

.close-button {
  background: #ff7f50;
  border: none;
  color: #fff;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
  text-align: center;
}

.close-button:hover {
  background: #ff4500;
}
</style>
