<template>
  <div class="recommendation-page">
    <!-- 설문조사 팝업 -->
    <div v-if="showSurveyPopup" class="popup-overlay">
      <div class="popup">
        <h4>추천 목록을 보려면 먼저 설문조사를 완료해주세요.</h4>
        <button @click="goToSurvey">설문조사 하러 가기</button>
      </div>
    </div>

    <!-- 추천 목록 -->
    <div v-else>
      <h1>맞춤 금융 상품 추천</h1>

      <!-- 로딩 상태 -->
      <div v-if="loading" class="loading">
        로딩 중...
      </div>

      <!-- 추천 데이터 -->
      <div v-else>
        <!-- 추천 예금 상품 -->
        <div v-if="recommendedProducts.deposits.length > 0" class="product-section">
          <h2>추천 예금 상품</h2>
          <div class="product-list">
            <div
              v-for="product in recommendedProducts.deposits"
              :key="product.fin_prdt_cd"
              class="product-card"
            >
              <h3>{{ product.fin_prdt_nm }}</h3>
              <p>{{ product.kor_co_nm }}</p>
              <p>최고 금리: {{ product.intr_rate2 }}%</p>
            </div>
          </div>
        </div>

        <!-- 추천 적금 상품 -->
        <div v-if="recommendedProducts.savings.length > 0" class="product-section">
          <h2>추천 적금 상품</h2>
          <div class="product-list">
            <div
              v-for="product in recommendedProducts.savings"
              :key="product.fin_prdt_cd"
              class="product-card"
            >
              <h3>{{ product.fin_prdt_nm }}</h3>
              <p>{{ product.kor_co_nm }}</p>
              <p>최고 금리: {{ product.intr_rate2 }}%</p>
            </div>
          </div>
        </div>

        <!-- 상품 비교 페이지로 이동 버튼 -->
        <div class="compare-button-container">
          <button class="compare-button" @click="goToComparePage">
            상품 비교 페이지로 이동
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();

const loading = ref(true);
const recommendedProducts = ref({
  deposits: [],
  savings: [],
});
const showSurveyPopup = ref(false);

// 추천 상품 데이터 가져오기
const fetchRecommendations = async () => {
  try {
    const response = await axios({
      method: "get",
      url: `${import.meta.env.VITE_API_URL}/recommendations/recommend/`,
      headers: {
        Authorization: `Token ${localStorage.getItem("token")}`,
      },
    });

    recommendedProducts.value = {
      deposits: response.data.deposit_recommendations || [],
      savings: response.data.saving_recommendations || [],
    };

    // 추천 데이터가 없는 경우 설문조사 팝업 표시
    if (
      recommendedProducts.value.deposits.length === 0 &&
      recommendedProducts.value.savings.length === 0
    ) {
      showSurveyPopup.value = true;
    }
  } catch (error) {
    console.error("Recommendation fetch failed:", error.response || error.message);
    // alert("추천 데이터를 가져오는 중 문제가 발생했습니다.");
  } finally {
    loading.value = false;
  }
};

// 상품 비교 페이지로 이동
const goToComparePage = () => {
  const queryData = {
    deposits: JSON.stringify(recommendedProducts.value.deposits),
    savings: JSON.stringify(recommendedProducts.value.savings),
  };
  router.push({ name: "productcompare", query: queryData });
};

// 설문 페이지로 이동
const goToSurvey = () => {
  router.push("/survey");
};

// 컴포넌트 마운트 시 데이터 로드
onMounted(async () => {
  const isAuthenticated = localStorage.getItem("token") !== null; // 로그인 여부 확인

  if (!isAuthenticated) {
    console.log("User not authenticated. Showing popup...");
    showSurveyPopup.value = true; // 팝업 표시
    loading.value = false;
    return;
  }

  const surveyCompletedFromStorage = localStorage.getItem("surveyCompleted") === "true";

  if (!surveyCompletedFromStorage) {
    console.log("Survey not completed. Showing popup...");
    showSurveyPopup.value = true; // 설문조사 요청 팝업
    loading.value = false;
    return;
  }

  await fetchRecommendations();

  if (
    recommendedProducts.value.deposits.length === 0 &&
    recommendedProducts.value.savings.length === 0
  ) {
    console.log("No recommended products. Showing popup...");
    showSurveyPopup.value = true; // 추천 데이터가 없는 경우 팝업 표시
  }
});
</script>

<style scoped>
.recommendation-page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
  line-height: 1.5;
  color: #333;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #666;
  margin: 50px 0;
}

.product-section {
  margin-top: 20px;
}

.product-list {
  display: flex;
  flex-direction: column; /* 세로 정렬 */
  gap: 20px;
}

.product-card {
  background: linear-gradient(to bottom, #ffffff, #f0f0f0);
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-5px); /* 살짝 위로 올라감 */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.product-card h3 {
  margin: 0 0 10px;
  font-size: 1.2rem;
  color: #333;
}

.product-card p {
  margin: 5px 0;
  color: #666;
}

.compare-button-container {
  margin-top: 30px;
  text-align: center;
}

.compare-button {
  padding: 15px 30px;
  font-size: 1rem;
  background-color: #424530;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.compare-button:hover {
  background-color: #5a5a4a;
  transform: scale(1.05);
}
</style>