<template>
  <div class="recommendation-page">
    <div v-if="showSurveyPopup" class="popup-overlay">
      <div class="popup">
        <h4>추천 목록을 보려면 먼저 설문조사를 완료해주세요.</h4>
        <button @click="goToSurvey">설문조사 하러 가기</button>
      </div>
    </div>

    <template v-else>
      <h1>맞춤 금융 상품 추천</h1>
      <div v-if="loading" class="loading">
        로딩 중...
      </div>
      <div v-else>
        <!-- 추천 예금 상품 -->
        <div v-if="recommendedProducts.deposits.length > 0" class="product-section">
          <h2>추천 예금 상품</h2>
          <div class="product-list">
            <div
              v-for="product in recommendedProducts.deposits"
              :key="product.fin_prdt_cd"
              class="product-card"
              @click="openDetailPopup(product, 'deposit')"
            >
              <h3>{{ product.fin_prdt_nm }}</h3>
              <p>{{ product.kor_co_nm }}</p>
              <p>최고 금리: {{ product.intr_rate2 }}%</p>
              <button class="detail-button">자세히 보기</button>
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
              @click="openDetailPopup(product, 'saving')"
            >
              <h3>{{ product.fin_prdt_nm }}</h3>
              <p>{{ product.kor_co_nm }}</p>
              <p>최고 금리: {{ product.intr_rate2 }}%</p>
              <button class="detail-button">자세히 보기</button>
            </div>
          </div>
        </div>

        <!-- 상세 정보 팝업 -->
        <div v-if="selectedProduct" class="popup-overlay" @click.self="closeDetailPopup">
          <div class="popup-content">
            <h2>{{ selectedProduct.fin_prdt_nm }}</h2>
            <p><strong>은행명:</strong> {{ selectedProduct.kor_co_nm || "정보 없음" }}</p>
            <p><strong>가입 방법:</strong> {{ selectedProduct.join_way || "정보 없음" }}</p>
            <p><strong>가입 대상:</strong> {{ selectedProduct.join_member || "정보 없음" }}</p>
            <p><strong>우대 조건:</strong> {{ selectedProduct.spcl_cnd || "정보 없음" }}</p>
            <p><strong>만기 후 이율:</strong> {{ selectedProduct.mtrt_int || "정보 없음" }}</p>
            <p><strong>기타 정보:</strong> {{ selectedProduct.etc_note || "정보 없음" }}</p>
            <button class="close-button" @click="closeDetailPopup">닫기</button>
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
import { useProductStore } from "@/stores/product";

const userStore = useUserStore();
const router = useRouter();
const productStore = useProductStore();

const loading = ref(true);
const recommendedProducts = ref({
  deposits: [],
  savings: [],
});
const showSurveyPopup = ref(false);
const selectedProduct = ref(null);
const selectedProductType = ref("");

// 설문 페이지로 이동
function goToSurvey() {
  router.push("/survey");
}

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
  } catch (error) {
    console.error("Recommendation fetch failed:", error.response || error.message);
    alert("추천 데이터를 가져오는 중 문제가 발생했습니다.");
  } finally {
    loading.value = false;
  }
};

// 상세 정보 팝업 열기
const openDetailPopup = async (product, type) => {
  try {
    await productStore.fetchProductById(product.fin_prdt_cd, type);
    selectedProduct.value = productStore.selectedProduct;
  } catch (error) {
    console.error("상품 상세 정보 로드 실패:", error);
    alert("상품 상세 정보를 가져오는 중 오류가 발생했습니다.");
    selectedProduct.value = product; // 기본값으로 추천된 데이터를 팝업에 표시
  }
};

// 상세 정보 팝업 닫기
const closeDetailPopup = () => {
  selectedProduct.value = null;
  selectedProductType.value = "";
};

// 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  const isAuthenticated = localStorage.getItem("token") !== null; // 로그인 여부 확인

  if (!isAuthenticated) {
    console.log("User not authenticated. Showing popup...");
    showSurveyPopup.value = true; // 팝업 표시
  } else {
    loading.value = true;
    const surveyCompletedFromStorage = localStorage.getItem("surveyCompleted") === "true";
    
    if (!surveyCompletedFromStorage) {
      showSurveyPopup.value = true;
      loading.value = false;
    } else {
      userStore.surveyCompleted = true;
      fetchRecommendations();
    }
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
  flex-wrap: wrap;
  gap: 20px;
}

.product-card {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  flex: 1 1 calc(50% - 20px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 300px;
}

.product-card:hover {
  transform: scale(1.02);
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

.product-card button {
  margin-top: 10px;
  padding: 10px 15px;
  background-color: #2a5552;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.product-card button:hover {
  background-color: #2a5552;
}

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* 반투명 배경 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* 팝업을 위에 표시 */
}

.popup {
  background: white;
  padding: 20px 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.popup h4 {
  margin-bottom: 20px;
  font-size: 1.2rem;
  color: #333; /* 텍스트 색상 */
}

.popup button {
  padding: 10px 20px;
  font-size: 1rem;
  background-color: #2a5552; /* 어두운 초록색 */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.popup button:hover {
  background-color: #1d3e3c; /* 버튼 hover 시 더 어두운 초록색 */
  transform: scale(1.05); /* 버튼 살짝 확대 */
}
</style>

