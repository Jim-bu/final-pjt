<template>
  <div class="compare-page">
    <h1>상품 비교</h1>

    <!-- 검색 필드 -->
    <div class="search-container">
      <input
        v-model="searchTerm"
        class="search-input"
        type="text"
        placeholder="상품명을 검색하세요..."
      />
    </div>

    <!-- 상품 탭 -->
    <div class="product-tab">
      <button
        :class="{ active: activeTab === 'deposit' }"
        @click="changeTab('deposit')"
      >
        예금
      </button>
      <button
        :class="{ active: activeTab === 'saving' }"
        @click="changeTab('saving')"
      >
        적금
      </button>
    </div>

    <!-- 상품 목록 -->
    <div class="product-list">
      <div
        v-for="product in paginatedProducts"
        :key="product.fin_prdt_cd"
        class="product-card"
        @click="toggleSelection(product)"
        :class="{ selected: selectedProducts.includes(product) }"
      >
        <span>{{ product.fin_prdt_nm }}</span>
      </div>
    </div>

    <!-- 페이지네이션 -->
    <div class="pagination">
      <button :disabled="currentPage === 1" @click="prevPage">이전</button>
      <span>페이지 {{ currentPage }} / {{ totalPages }}</span>
      <button :disabled="currentPage === totalPages" @click="nextPage">다음</button>
    </div>

    <!-- 비교 버튼 -->
    <button
      class="compare-button"
      :disabled="selectedProducts.length < 2"
      @click="showChart"
    >
      선택 상품 비교
    </button>

    <!-- 차트 -->
    <BarChart
      v-if="showingChart"
      :labels="labels"
      :intrRate="intrRate"
      :intrRate2="intrRate2"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useProductStore } from "../stores/product";
import BarChart from "@/components/BarChart.vue";

// Store 및 데이터 선언
const productStore = useProductStore();
const deposits = ref([]);
const savings = ref([]);
const selectedProducts = ref([]);
const searchTerm = ref("");
const activeTab = ref("deposit");
const showingChart = ref(false);
const labels = ref([]);
const intrRate = ref([]);
const intrRate2 = ref([]);

// 페이지네이션
const currentPage = ref(1);
const itemsPerPage = 6;

// 상품 목록 필터링 및 페이지네이션
const filteredProducts = computed(() => {
  const products = activeTab.value === "deposit" ? deposits.value : savings.value;

  return products.filter((product) =>
    product.fin_prdt_nm.toLowerCase().includes(searchTerm.value.toLowerCase())
  );
});

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return filteredProducts.value.slice(start, start + itemsPerPage);
});

const totalPages = computed(() => Math.ceil(filteredProducts.value.length / itemsPerPage));

// 페이지 이동
const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};

// 탭 변경
const changeTab = (tab) => {
  activeTab.value = tab;
  currentPage.value = 1;
};

// 상품 선택 토글
const toggleSelection = (product) => {
  const index = selectedProducts.value.indexOf(product);
  if (index === -1) {
    selectedProducts.value.push(product);
  } else {
    selectedProducts.value.splice(index, 1);
  }
};

// 차트 데이터 생성
const prepareChartData = () => {
  if (!selectedProducts.value.length) return;

  // 유효한 상품 데이터만 필터링
  const validProducts = selectedProducts.value.filter(
    (product) => product.options && product.options.length > 0
  );

  if (!validProducts.length) {
    console.warn("유효한 상품 데이터가 없습니다.");
    labels.value = [];
    intrRate.value = [];
    intrRate2.value = [];
    return;
  }

  labels.value = validProducts[0]?.options.map((option) => `${option.save_trm}개월`);
  intrRate.value = validProducts.map((product) =>
    product.options.map((option) => option.intr_rate || 0)
  );
  intrRate2.value = validProducts.map((product) =>
    product.options.map((option) => option.intr_rate2 || 0)
  );
};

// 차트 표시
const showChart = () => {
  prepareChartData();
  showingChart.value = true;
};

// 데이터 로드
onMounted(async () => {
  await productStore.saveDeposits();
  await productStore.saveSavings();
  await productStore.fetchDeposits();
  await productStore.fetchSavings();
  deposits.value = productStore.deposits;
  savings.value = productStore.savings;
});
</script>

<style scoped>
/* 페이지 스타일 */
.compare-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 16px;
  background-color: #fdf6e3;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 검색창 스타일 */
.search-container {
  margin-bottom: 16px;
}

.search-input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 2px solid #d1c4b2;
  border-radius: 8px;
  background-color: #fffaf3;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 탭 스타일 */
.product-tab {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.product-tab button {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  background-color: #f8e5c3;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.product-tab button.active {
  background-color: #e4c089;
  color: #fff;
  font-weight: bold;
}

.product-tab button:hover {
  background-color: #d8b679;
}

/* 상품 카드 스타일 */
.product-list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.product-card {
  background-color: #fffaf3;
  border: 1px solid #d1c4b2;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s, background-color 0.3s;
}

.product-card.selected {
  background-color: #e4c089;
  border-color: #c69a5d;
  transform: scale(1.05);
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: space-between;
  margin: 20px 0;
}

.pagination button {
  padding: 10px 20px;
  font-size: 14px;
  border: none;
  border-radius: 8px;
  background-color: #c69a5d;
  color: white;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #ddd;
  color: #aaa;
  cursor: not-allowed;
}

/* 비교 버튼 */
.compare-button {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  background-color: #8b572a;
  color: white;
  margin-top: 20px;
  cursor: pointer;
}

.compare-button:disabled {
  background-color: #ddd;
  color: #aaa;
  cursor: not-allowed;
}
</style>
