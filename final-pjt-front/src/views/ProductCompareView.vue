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
        v-for="product in filteredProducts"
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
      v-if="showingChart && labels.length && datasets.length"
      :labels="labels"
      :datasets="datasets"
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
const datasets = ref([]);

// 페이지네이션
const currentPage = ref(1);
const itemsPerPage = 5; // 한 페이지에 표시할 상품 수

// 현재 탭의 상품 목록
const filteredProducts = computed(() => {
  const products =
    activeTab.value === "deposit" ? deposits.value : savings.value;

  const searchFiltered = products.filter((product) =>
    product.fin_prdt_nm.includes(searchTerm.value)
  );

  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return searchFiltered.slice(start, end);
});

// 총 페이지 수
const totalPages = computed(() => {
  const products =
    activeTab.value === "deposit" ? deposits.value : savings.value;

  const searchFiltered = products.filter((product) =>
    product.fin_prdt_nm.includes(searchTerm.value)
  );

  return Math.ceil(searchFiltered.length / itemsPerPage);
});

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
  currentPage.value = 1; // 페이지 초기화
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
  if (!selectedProducts.value.length) {
    console.warn("선택된 상품이 없습니다.");
    return;
  }

  // 선택된 상품의 데이터 유효성 확인 및 필터링
  const validProducts = selectedProducts.value.filter(
    (product) => product.options && product.options.length
  );

  if (!validProducts.length) {
    console.warn("유효한 상품 데이터가 없습니다.");
    labels.value = [];
    datasets.value = [];
    return;
  }

  // 차트 라벨 생성
  labels.value = validProducts[0].options.map((option) => `${option.save_trm}개월`);

  // 데이터셋 생성
  datasets.value = validProducts.map((product, index) => ({
    label: product.fin_prdt_nm,
    data: product.options.map((option) => {
      const term = parseInt(option.save_trm, 10);
      const rate = option.intr_rate2 || option.intr_rate || 0;
      const returns =
        activeTab.value === "deposit"
          ? 1000000 * (1 + (rate / 100) * (term / 12)) // 예금 계산
          : 1000000 * (Math.pow(1 + rate / 1200, term) - 1); // 적금 계산
      return Math.round(returns);
    }),
    backgroundColor: `rgba(${index * 60}, 99, 132, 0.7)`,
  }));
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
.compare-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 16px;
}

/* 상품 목록 탭 스타일 */
.product-tab {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}

.product-tab button {
  background-color: #f8e5c3;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  margin: 0 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.product-tab button.active {
  background-color: #e4c089;
}

.product-tab button:hover {
  background-color: #e4c089;
}

/* 상품 목록 */
.product-list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.product-card {
  background-color: #f8ecd5;
  border-radius: 12px;
  padding: 8px;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.product-card.selected {
  background-color: #e4c089;
}

.product-card:hover {
  background-color: #f4d4a5;
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 16px 0;
}

.pagination button {
  background-color: #b57230;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* 비교 버튼 */
.compare-button {
  width: 100%;
  padding: 10px;
  background-color: #8b572a;
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  margin-top: 16px;
}

.compare-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
