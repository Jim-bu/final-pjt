<template>
  <div class="compare-page">
    <h1>상품 비교</h1>

    <!-- 상품 목록 -->
    <div class="product-list">
      <h2>상품 목록</h2>
      <div
        v-for="product in products"
        :key="product.fin_prdt_cd"
        class="product-card"
      >
        <input
          type="checkbox"
          :value="product"
          v-model="selectedProducts"
        />
        <span>{{ product.fin_prdt_nm }}</span>
      </div>
    </div>

    <!-- 선택한 상품 비교 버튼 -->
    <button
      class="compare-button"
      :disabled="selectedProducts.length < 2"
      @click="compareProducts"
    >
      선택 상품 비교
    </button>

    <!-- 차트 -->
    <div v-if="chartData.length" class="chart-container">
      <BarChart :chart-data="chartData" />
    </div>

    <!-- 게시판 -->
    <div class="board">
      <h2>상품 의견 게시판</h2>
      <form @submit.prevent="addPost">
        <textarea
          v-model="newPost"
          placeholder="여기에 의견을 작성하세요..."
        ></textarea>
        <button type="submit">게시</button>
      </form>
      <ul class="posts">
        <li v-for="(post, index) in posts" :key="index">
          <p>{{ post }}</p>
          <!-- 댓글 -->
          <div class="comments">
            <form @submit.prevent="addComment(index)">
              <input
                v-model="newComments[index]"
                placeholder="댓글을 작성하세요..."
              />
              <button type="submit">댓글 추가</button>
            </form>
            <ul>
              <li v-for="(comment, idx) in comments[index] || []" :key="idx">
                {{ comment }}
              </li>
            </ul>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from 'axios';
import BarChart from "@/components/BarChart.vue";

// 상품 데이터
const products = ref([]); // 백엔드에서 가져올 상품 목록
const selectedProducts = ref([]); // 선택된 상품
const chartData = ref([]); // 차트 데이터

// 수익 계산 로직
const calculateReturns = (product) => {
  const periods = product.mtrt_int.match(/- (.+?): (.+?)%/g) || [];
  return periods.map((period) => {
    const [label, percentage] = period.match(/(.+?): (.+?)%/).slice(1);
    const returnAmount = (parseFloat(percentage) / 100) * 1000000; // 가상의 기준 금액 1,000,000원
    return { label, value: returnAmount };
  });
};

// 상품 비교
const compareProducts = () => {
  chartData.value = selectedProducts.value.map((product) => {
    const returns = calculateReturns(product);
    return {
      name: product.fin_prdt_nm,
      returns: returns.map((r) => r.value),
      labels: returns.map((r) => r.label),
    };
  });
};

// 게시판 데이터
const posts = ref([]); // 게시글
const newPost = ref(""); // 새 게시글
const comments = ref([]); // 댓글 데이터
const newComments = ref({}); // 새 댓글

// 게시글 추가
const addPost = () => {
  if (newPost.value.trim()) {
    posts.value.push(newPost.value.trim());
    newPost.value = "";
    comments.value.push([]); // 댓글 초기화
  }
};

// 댓글 추가
const addComment = (postIndex) => {
  if (!newComments.value[postIndex]?.trim()) return;

  if (!comments.value[postIndex]) {
    comments.value[postIndex] = [];
  }

  comments.value[postIndex].push(newComments.value[postIndex]);
  newComments.value[postIndex] = "";
};

// 데이터 가져오기
const fetchProducts = async () => {
  try {
    const response = await axios.get("/api/products/");
    products.value = response.data;
  } catch (error) {
    console.error("상품 데이터를 가져오는 중 오류 발생:", error);
    // 더미 데이터로 대체
    products.value = [
      {
        fin_prdt_cd: "PRD001",
        fin_prdt_nm: "WON플러스예금",
        mtrt_int: "만기 후\n- 1개월이내: 50%\n- 1개월초과 6개월이내: 30%\n- 6개월초과: 20%",
      },
      {
        fin_prdt_cd: "PRD002",
        fin_prdt_nm: "SMART 적금",
        mtrt_int: "만기 후\n- 6개월이내: 70%\n- 6개월초과 12개월이내: 50%",
      },
      {
        fin_prdt_cd: "PRD003",
        fin_prdt_nm: "GOLD 정기예금",
        mtrt_int: "만기 후\n- 12개월: 100%",
      },
    ];
  }
};

onMounted(() => {
  fetchProducts();
});
</script>

<style scoped>
.compare-page {
  max-width: 600px;
  margin: 0 auto;
  padding: 16px;
}

.product-list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.product-card {
  background-color: #d4a373;
  border-radius: 12px;
  padding: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.compare-button {
  width: 100%;
  padding: 10px;
  background-color: #8b572a;
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
}

.compare-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.chart-container {
  margin: 20px 0;
}

.board {
  margin-top: 20px;
  padding: 16px;
  border-top: 2px solid #333; /* 구분선 추가 */
}

.board h2 {
  font-size: 20px;
  font-weight: bold;
  color: #333; /* 검은색 텍스트 */
  margin-bottom: 16px;
  border-bottom: 2px solid #333; /* 제목 구분선 */
  padding-bottom: 8px;
}

textarea {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  margin-bottom: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: none;
  background-color: #f9f9f9; /* 연한 회색 배경 */
}

button {
  padding: 10px 16px;
  font-size: 14px;
  color: #fff;
  background-color: #333; /* 검은색 버튼 */
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #555; /* 버튼 hover 효과 */
}

.posts {
  margin-top: 16px;
}

.posts li {
  padding: 16px;
  border: 1px solid #ddd; /* 구분선 */
  border-radius: 8px;
  margin-bottom: 16px;
  background-color: #fdfdfd; /* 밝은 배경 */
}

.posts li p {
  font-size: 14px;
  color: #333; /* 검은 텍스트 */
  margin-bottom: 8px;
}

.comments {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #ccc; /* 댓글 구분선 */
}

.comments form {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.comments form input {
  flex: 1;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.comments form button {
  padding: 8px 12px;
  font-size: 14px;
  color: #fff;
  background-color: #333;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.comments form button:hover {
  background-color: #555;
}

.comments ul {
  margin-top: 8px;
}

.comments ul li {
  font-size: 14px;
  color: #333;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  margin-bottom: 8px;
}


</style>