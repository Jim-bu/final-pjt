<template>
  <div class="product-list-container">
    <!-- 탭 구성 -->
    <div class="tabs">
      <button
        class="tab"
        :class="{ active: activeTab === 'deposit' }"
        @click="activeTab = 'deposit'"
      >
        예금
      </button>
      <button
        class="tab"
        :class="{ active: activeTab === 'saving' }"
        @click="activeTab = 'saving'"
      >
        적금
      </button>
    </div>

    <!-- 상품 목록 -->
    <div>
      <div
        v-for="product in paginatedProducts"
        :key="product.fin_prdt_cd"
        class="product-card"
        @click="showDetail(product)"
      >
        <div class="product-header">
          <span class="product-type">
            상품 형태: {{ activeTab === 'deposit' ? "예금" : "적금" }}
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
    </div>

    <!-- 페이지네이션 -->
    <div class="pagination">
      <button
        v-for="page in totalPages"
        :key="page"
        :class="{ active: currentPage === page }"
        @click="currentPage = page"
      >
        {{ page }}
      </button>
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
import { ref, computed, onMounted } from "vue";
import { useProductStore } from "../stores/product";

const productStore = useProductStore();

// 데이터 로드
onMounted(async () => {
  await productStore.saveDeposits();
  await productStore.saveSavings();
  await productStore.fetchDeposits();
  await productStore.fetchSavings();
});



// 탭 상태
const activeTab = ref("deposit");

// 페이지네이션 상태
const currentPage = ref(1);
const itemsPerPage = 10; // 페이지당 항목 수

// 상품 목록
const products = computed(() =>
  activeTab.value === "deposit"
    ? productStore.deposits
    : productStore.savings
);

// 페이지네이션 처리
const totalPages = computed(() => Math.ceil(products.value.length / itemsPerPage));
const paginatedProducts = computed(() =>
  products.value.slice(
    (currentPage.value - 1) * itemsPerPage,
    currentPage.value * itemsPerPage
  )
);

// 상세 보기
const selectedProduct = ref(null);
const showDetail = (product) => {
  selectedProduct.value = product;
};

// 팝업 닫기
const closeDetail = () => {
  selectedProduct.value = null;
};

// 가입기간 추출 유틸리티 함수
const extractJoinPeriod = (note) => {
  const match = note?.match(/가입기간: (.+?)\n/);
  return match ? match[1] : "정보 없음";
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

/* 탭 스타일 */
.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}
.tab {
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  background-color: #f2f2f2;
  margin: 0 5px;
  border-radius: 8px;
}
.tab.active {
  background-color: #424530;
  color: #ffefcd;
}

/* 페이지네이션 스타일 */
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 16px;
}
.pagination button {
  padding: 8px 12px;
  margin: 0 4px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #f2f2f2;
}
.pagination button.active {
  background-color: #424530;
  color: #ffefcd;
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
</style>
