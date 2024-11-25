<template>
  <div class="recommendation-page">
    <!-- 로그인되지 않았을 때 -->
    <div v-if="!userStore.isLogin">
      <div class="overlay"></div>
      <div class="login-popup">
        <h2>로그인이 필요합니다</h2>
        <p>추천 목록을 보려면 로그인 또는 회원가입이 필요합니다.</p>
        <button @click="goToLogin">로그인</button>
        <button @click="goToSignup">회원가입</button>
      </div>
    </div>

    <!-- 로그인된 경우 추천 목록 표시 -->
    <div v-else>
      <h1>맞춤 금융 상품 추천</h1>
      <div v-if="loading" class="loading">
        데이터를 불러오는 중입니다...
      </div>
      <div v-else>
        <!-- 추천 예금 상품 -->
        <div v-if="recommendedProducts.deposits.length > 0" class="product-section">
          <h2>추천 예금 상품</h2>
          <div class="product-list">
            <div v-for="product in recommendedProducts.deposits" :key="product.id" class="product-card">
              <h3>{{ product.fin_prdt_nm }}</h3>
              <p>{{ product.kor_co_nm }}</p>
              <p>최고금리: {{ Math.max(...product.deposit_options.map(opt => opt.intr_rate2 || 0)) }}%</p>
              <button @click="goToDetail(product.id, 'deposit')">자세히 보기</button>
            </div>
          </div>
        </div>
        <br><br>
        <!-- 추천 적금 상품 -->
        <div v-if="recommendedProducts.savings.length > 0" class="product-section">
          <h2>추천 적금 상품</h2>
          <div class="product-list">
            <div v-for="product in recommendedProducts.savings" :key="product.id" class="product-card">
              <h3>{{ product.fin_prdt_nm }}</h3>
              <p>{{ product.kor_co_nm }}</p>
              <p>최고금리: {{ Math.max(...product.saving_options.map(opt => opt.intr_rate2 || 0)) }}%</p>
              <button @click="goToDetail(product.id, 'saving')">자세히 보기</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useUserStore } from "@/stores/users";
import axios from "axios";

const userStore = useUserStore();
const loading = ref(true);
const recommendedProducts = ref({
  deposits: [],
  savings: []
});

// 로그인 페이지로 이동
function goToLogin() {
  window.location.href = "/login";
}

// 회원가입 페이지로 이동
function goToSignup() {
  window.location.href = "/signup";
}

// 설문 페이지로 이동
function goToSurvey() {
  alert("설문조사가 필요합니다."); // 팝업 알림
  window.location.href = "/survey"; // SurveyBot.vue로 이동
}

const fetchRecommendations = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/surveys/recommendations/", {
      headers: { Authorization: `Token ${userStore.token}` }
    });

    // 응답 데이터가 예상대로 오는지 검증
    if (response.data.deposit_recommendations && response.data.saving_recommendations) {
      recommendedProducts.value = {
        deposits: response.data.deposit_recommendations || [],
        savings: response.data.saving_recommendations || []
      };
    } else {
      throw new Error("Invalid response structure");
    }
  } catch (error) {
    console.error("추천 상품 조회 실패:", error);
    goToSurvey(); // 설문조사 페이지로 이동
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  if (userStore.isLogin) {
    fetchRecommendations();
  }
});
</script>

<style scoped>
/* 페이지 전체 레이아웃 */
.recommendation-page {
  padding: 20px;
  max-width: 800px; /* 더 넓은 화면을 지원 */
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

/* 섹션 제목 */
.product-section h2 {
  margin-bottom: 20px;
  font-size: 1.5rem;
  color: #85725d;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 5px;
}

/* 상품 카드 리스트 */
.product-list {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

/* 상품 카드 */
.product-card {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.product-card h3 {
  font-size: 1.2rem;
  margin-bottom: 10px;
  color: #333;
}

.product-card p {
  margin: 5px 0;
  font-size: 0.9rem;
  color: #555;
}

.product-card button {
  margin-top: 10px;
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #85725d;
  color: white;
  font-size: 0.9rem;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.product-card button:hover {
  background-color: #85725d;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* 카드 호버 효과 */
.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

/* 팝업 오버레이 */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  z-index: 999;
}

/* 팝업 창 */
.login-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #fff;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  text-align: center;
}

.login-popup h2 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #333;
}

.login-popup button {
  margin: 10px;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  background-color: #85725d;
  color: white;
  font-size: 1rem;
  transition: background-color 0.3s, transform 0.3s;
}

.login-popup button:hover {
  background-color: #85725d;
  transform: scale(1.05);
}

/* 반응형 처리 */
@media (max-width: 768px) {
  .recommendation-page {
    padding: 15px;
  }

  .product-card {
    padding: 10px;
  }

  .product-card h3 {
    font-size: 1rem;
  }

  .product-card button {
    font-size: 0.8rem;
    padding: 6px 12px;
  }
}
</style>
