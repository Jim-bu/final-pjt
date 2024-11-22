<template>
  <div class="community-page">
    <h1>상품 평가 게시판</h1>

    <!-- 의견 작성 폼 -->
    <div class="opinion-form">
      <h2>상품 평가 작성</h2>

      <!-- 상품 유형 선택 -->
      <div class="product-type">
        <label>상품 유형:</label>
        <select v-model="newOpinion.productType" class="product-select">
          <option value="deposit">예금</option>
          <option value="saving">적금</option>
        </select>
      </div>

      <!-- 상품 선택 -->
      <div class="product-select-container">
        <label>상품 선택:</label>
        <select v-model="newOpinion.productName" class="product-select">
          <option disabled value="">상품을 선택하세요</option>
          <option
            v-for="product in getProductList(newOpinion.productType)"
            :key="product.fin_prdt_cd"
            :value="product.fin_prdt_nm"
          >
            {{ product.fin_prdt_nm }}
          </option>
        </select>
      </div>

      <input
        v-model="newOpinion.title"
        class="input-title"
        type="text"
        placeholder="제목을 입력하세요"
      />
      <textarea
        v-model="newOpinion.content"
        class="textarea-content"
        placeholder="상품에 대한 의견을 작성하세요"
      ></textarea>

      <!-- 별점 선택 -->
      <div class="rating-container">
        <label>별점:</label>
        <div class="stars">
          <span
            v-for="star in 5"
            :key="star"
            class="star"
            :class="{ filled: star <= newOpinion.rating }"
            @click="newOpinion.rating = star"
          >
            ★
          </span>
        </div>
      </div>

      <button class="submit-button" @click="addOpinion">작성하기</button>
    </div>

    <!-- 게시물 목록 -->
    <div class="opinion-list">
      <h2>사용자 평가</h2>
      <div
        v-for="(opinion, index) in opinions"
        :key="index"
        class="opinion-card"
      >
        <h3>{{ opinion.title }}</h3>
        <p class="product-info">
          {{ opinion.productType === "deposit" ? "예금" : "적금" }} - {{ opinion.productName }}
        </p>
        <p class="content">{{ opinion.content }}</p>
        <p class="rating">별점: {{ opinion.rating }}점</p>
        <button class="comment-toggle" @click="toggleComments(index)">
          댓글 보기
        </button>

        <!-- 댓글 목록 -->
        <div v-if="opinion.showComments" class="comment-section">
          <ul class="comment-list">
            <li
              v-for="(comment, idx) in opinion.comments"
              :key="idx"
              class="comment-item"
            >
              {{ comment }}
            </li>
          </ul>
          <div class="comment-form">
            <input
              v-model="newComments[index]"
              class="input-comment"
              type="text"
              placeholder="댓글을 입력하세요"
            />
            <button @click="addComment(index)">댓글 추가</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useProductStore } from "../stores/product";

// 상품 데이터 가져오기
const productStore = useProductStore();
const deposits = ref([]);
const savings = ref([]);

// 의견 및 댓글 관련 상태
const opinions = ref([]);
const newOpinion = ref({
  productType: "deposit",
  productName: "",
  title: "",
  content: "",
  rating: 0,
  comments: [],
  showComments: false,
});
const newComments = ref({});

// 데이터 로드
onMounted(async () => {
  await productStore.saveDeposits();
  await productStore.saveSavings();
  await productStore.fetchDeposits();
  await productStore.fetchSavings();
  deposits.value = productStore.deposits;
  savings.value = productStore.savings;
});

// 상품 목록 가져오기
const getProductList = (type) => {
  return type === "deposit" ? deposits.value : savings.value;
};

// 의견 추가
const addOpinion = () => {
  if (
    !newOpinion.value.title ||
    !newOpinion.value.content ||
    !newOpinion.value.productName
  ) {
    alert("모든 필드를 입력하세요.");
    return;
  }
  opinions.value.push({
    ...newOpinion.value,
    comments: [],
    showComments: false,
  });
  newOpinion.value = {
    productType: "deposit",
    productName: "",
    title: "",
    content: "",
    rating: 0,
    comments: [],
    showComments: false,
  };
};

// 댓글 토글
const toggleComments = (index) => {
  opinions.value[index].showComments = !opinions.value[index].showComments;
};

// 댓글 추가
const addComment = (index) => {
  if (!newComments.value[index]?.trim()) {
    alert("댓글을 입력하세요.");
    return;
  }
  opinions.value[index].comments.push(newComments.value[index]);
  newComments.value[index] = "";
};
</script>

<style scoped>
/* 기존 스타일 유지 및 일부 개선 */
.community-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 16px;
  background: #f9f5ee;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  font-size: 24px;
  color: #333;
  margin-bottom: 16px;
}

.opinion-form {
  margin-bottom: 24px;
  padding: 16px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.input-title,
.textarea-content,
.input-comment,
.product-select {
  width: 100%;
  margin-bottom: 12px;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
}

.stars {
  display: flex;
  gap: 4px;
  font-size: 24px;
  cursor: pointer;
}

.star {
  color: #ccc;
  transition: color 0.3s;
}

.star.filled {
  color: #ffd700;
}

.submit-button {
  padding: 10px 16px;
  background: #5a9;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s;
}

.submit-button:hover {
  background: #47a;
}
</style>
