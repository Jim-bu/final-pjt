<template>
  <div class="product-list-container">
    <!-- 상품 목록 -->
    <div
      v-for="product in products"
      :key="product.fin_prdt_cd"
      class="product-card"
      @click="showDetail(product)"
    >
      <div class="product-header">
        <span class="product-type">
          상품 형태: {{ product.join_way?.includes("예금") ? "예금" : "적금" }}
        </span>
      </div>
      <div class="product-body">
        <h3 class="product-name">{{ product.fin_prdt_nm }}</h3>
        <p class="product-period">
          가입기간: {{ extractJoinPeriod(product.etc_note) }}
        </p>
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
import { useProductStore } from "../stores/product";

const productStore = useProductStore();
const products = ref([])

// 컴포넌트 마운트 시 데이터 저장 및 가져오기
onMounted(() => {
  productStore.saveProducts(); // 데이터 저장
  productStore.fetchProducts(); // 저장된 데이터 조회
});

products.value = productStore.fetchProducts(); // 전체 상품 데이터 참조
const selectedProduct = productStore.fetchProductById(); // 선택된 상품 데이터 참조

// 가입기간 추출 유틸리티 함수
const extractJoinPeriod = (note) => {
  const match = note.match(/가입기간: (.+?)\n/);
  return match ? match[1] : "정보 없음";
};

// 상품 상세 보기
const showDetail = (product) => {
  productStore.fetchProductById(product.fin_prdt_cd); // 선택된 상품 데이터 로드
};

// 팝업 닫기
const closeDetail = () => {
  productStore.selectedProduct = null; // 선택된 상품 초기화
};


</script>

<style scoped>
.product-list-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 800px;
  margin: 0 auto;
}

.product-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  background-color: #f9f9f9;
  cursor: pointer;
  transition: transform 0.2s;
}

.product-card:hover {
  transform: scale(1.02);
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
  background-color: #424530;
  color: #ffefcd;
  border: none;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
}

.detail-button:hover {
  background-color: #2a3620;
}

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
</style>
