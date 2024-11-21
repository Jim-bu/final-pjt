<template>
  <div class="product-list-container">
    <!-- 상품 목록 -->
    <div v-for="product in products" :key="product.fin_prdt_cd" class="product-card" @click="showDetail(product)">
      <div class="product-header">
        <span class="product-type">상품 형태: {{ product.join_way.includes("예금") ? "예금" : "적금" }}</span>
      </div>
      <div class="product-body">
        <h3 class="product-name">{{ product.fin_prdt_nm }}</h3>
        <p class="product-period">가입기간: {{ extractJoinPeriod(product.etc_note) }}</p>
      </div>
      <button class="detail-button">상세 보기</button>
    </div>

    <!-- 상세 페이지 팝업 -->
    <div v-if="selectedProduct" class="popup-overlay" @click.self="closeDetail">
      <div class="popup-content">
        <h2>{{ selectedProduct.fin_prdt_nm }}</h2>
        <p><strong>상품 형태:</strong> {{ selectedProduct.join_way }}</p>
        <p><strong>가입 조건:</strong> {{ selectedProduct.join_member }}</p>
        <p><strong>특이 사항:</strong> {{ selectedProduct.spcl_cnd }}</p>
        <p><strong>만기 이율:</strong> {{ selectedProduct.mtrt_int }}</p>
        <p><strong>기타 사항:</strong> {{ selectedProduct.etc_note }}</p>
        <button class="close-button" @click="closeDetail">닫기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const products = ref([]); // 상품 목록 저장
const selectedProduct = ref(null); // 선택된 상품 저장

// 가입기간 추출 유틸리티 함수
const extractJoinPeriod = (note) => {
  const match = note.match(/가입기간: (.+?)\n/);
  return match ? match[1] : "정보 없음";
};

// 상품 상세 보기
const showDetail = (product) => {
  selectedProduct.value = product;
};

// 팝업 닫기
const closeDetail = () => {
  selectedProduct.value = null;
};

// API에서 상품 목록 가져오기
const fetchProducts = async () => {
  try {
    // Django API URL을 직접 입력
    const response = await axios.get("http://127.0.0.1:8000/bankings/deposit-products/");
    products.value = response.data;
  } catch (error) {
    console.error("API 호출 실패:", error);
    products.value = []; // 오류 시 빈 배열로 초기화
  }
};

// 컴포넌트 마운트 시 데이터 가져오기
onMounted(() => {
  fetchProducts();
});
</script>

<style scoped>
.product-list-container {
  max-width: 600px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.product-card {
  background-color: #d4a373; /* 베이지 */
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: transform 0.2s;
}

.product-card:hover {
  transform: scale(1.05);
}

.product-header {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 8px;
}

.product-body {
  font-size: 16px;
}

.detail-button {
  margin-top: 12px;
  background-color: #6a4c93;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
}

.detail-button:hover {
  background-color: #5b3b83;
}

/* 팝업 스타일 */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background-color: #fff;
  padding: 24px;
  border-radius: 12px;
  max-width: 90%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.popup-content h2 {
  font-size: 24px;
  margin-bottom: 16px;
}

.popup-content p {
  font-size: 16px;
  margin: 8px 0;
}

.close-button {
  margin-top: 16px;
  background-color: #6a4c93;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
}

.close-button:hover {
  background-color: #5b3b83;
}
</style>
