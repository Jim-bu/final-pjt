<template>
  <div class="recommendation-page">
    <!-- 설문조사 필요 팝업 -->
    <div v-if="showSurveyPopup" class="popup-overlay">
      <div class="popup">
        <h4>추천 목록을 보려면 먼저 설문조사를 완료해주세요.</h4>
        <button @click="goToSurvey">설문조사 하러 가기</button>
      </div>
    </div>

    <!-- 추천 목록 표시 -->
    <template v-else>
      <h1>맞춤 금융 상품 추천</h1>
      <div v-if="loading" class="loading">
        데이터를 불러오는 중입니다...
      </div>
      <div v-else>
        <!-- 추천 예금 상품 -->
        <div v-if="recommendedProducts.deposits.length > 0" class="product-section">
          <h2>추천 예금 상품</h2>
          <div class="product-list">
            <div
              v-for="product in recommendedProducts.deposits"
              :key="product.id"
              class="product-card"
            >
              <h3>{{ product.fin_prdt_nm }}</h3>
              <p>{{ product.kor_co_nm }}</p>
              <p>
                최고금리: {{ Math.max(...product.deposit_options.map(opt => opt.intr_rate2 || 0)) }}%
              </p>
              <button @click="goToDetail(product.id, 'deposit')">자세히 보기</button>
            </div>
          </div>
        </div>
        <br /><br />
        <!-- 추천 적금 상품 -->
        <div v-if="recommendedProducts.savings.length > 0" class="product-section">
          <h2>추천 적금 상품</h2>
          <div class="product-list">
            <div
              v-for="product in recommendedProducts.savings"
              :key="product.id"
              class="product-card"
            >
              <h3>{{ product.fin_prdt_nm }}</h3>
              <p>{{ product.kor_co_nm }}</p>
              <p>
                최고금리: {{ Math.max(...product.saving_options.map(opt => opt.intr_rate2 || 0)) }}%
              </p>
              <button @click="goToDetail(product.id, 'saving')">자세히 보기</button>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useUserStore } from "@/stores/users";
import { useRouter } from "vue-router";
import axios from "axios";

const userStore = useUserStore();
const router = useRouter();
const loading = ref(true);
const recommendedProducts = ref({
  deposits: [],
  savings: [],
});
const showSurveyPopup = ref(false); // 설문 팝업 표시 여부

// 설문 페이지로 이동
function goToSurvey() {
  router.push("/survey"); // Survey 페이지로 리다이렉트
}

// 추천 상품 데이터 가져오기
const fetchRecommendations = async () => {
  axios({
    method: "get",
    url: `${import.meta.env.VITE_API_URL}/recommendations/recommend/`,
    headers: {
      Authorization: `Token ${localStorage.getItem("token")}`,
    },
  })
    .then((response) => {
      recommendedProducts.value = {
        deposits: response.data.deposit_recommendations || [],
        savings: response.data.saving_recommendations || [],
      };
    })
    .catch((error) => {
      console.error("Recommendation fetch failed:", error.response || error.message);
      alert("추천 데이터를 가져오는 중 문제가 발생했습니다.");
    });
};



onMounted(() => {
  // 로컬 스토리지에서 설문 완료 상태 확인
  const surveyCompletedFromStorage = localStorage.getItem("surveyCompleted") === "true";

  if (!surveyCompletedFromStorage) {
    showSurveyPopup.value = true; // 설문조사가 완료되지 않으면 팝업 표시
  } else {
    userStore.surveyCompleted = true; // 상태 동기화
    fetchRecommendations(); // 설문조사가 완료된 경우 데이터 가져오기
  }
});
</script>


<style scoped>
/* 페이지 레이아웃 */
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

/* 로딩 상태 */
.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #666;
  margin: 50px 0;
}

/* 팝업 오버레이 */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5); /* 반투명 배경 */
  backdrop-filter: blur(5px); /* 배경 흐림 효과 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

/* 팝업 */
.popup {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  width: 300px;
}

.popup h2 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #333;
}

.popup p {
  margin-bottom: 20px;
  color: #666;
}

.popup button {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  background-color: #85725d;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}

.popup button:hover {
  background-color: #6c5a4c;
  transform: scale(1.05);
}

/* 반응형 처리 */
@media (max-width: 768px) {
  .recommendation-page {
    padding: 15px;
  }

  .popup {
    width: 90%;
  }
}
</style>
