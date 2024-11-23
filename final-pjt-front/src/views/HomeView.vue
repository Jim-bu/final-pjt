<template>
  <div class="home-page">
    <!-- 캐러샐 섹션 -->
    <div class="carousel-container">
      <Carousel />
    </div>

    <!-- 날짜, 세계 증시, 금융 뉴스 -->
    <div class="info-box">
      <p class="date">{{ currentDate }}</p>
      <!-- 세계 증시 -->
      <div class="stock-market">
        <h3>세계 증시</h3>
        <ul class="stock-list">
          <li v-for="(stock, index) in stockData" :key="index">
            <span>{{ stock.name }}:</span>
            <span>{{ stock.price }}</span>
            <span :class="['change-icon', stock.direction]">
              <template v-if="stock.direction === 'up'">▲</template>
              <template v-else-if="stock.direction === 'down'">▼</template>
            </span>
          </li>
        </ul>
      </div>

      <!-- 구분선 -->
      <div class="divider"></div>

      <!-- 금융 뉴스 -->
      <div class="financial-news">
        <h3>금융 뉴스</h3>
        <ul class="news-list">
          <li v-for="(news, index) in limitedNews" :key="index" class="news-item">
            <h4 v-html="news.title"></h4>
            <p>{{ truncateText(news.description, 15) }}</p>
          </li>
        </ul>
        <button class="news-button" @click="goToPage('news')">더 많은 뉴스 보기</button>
      </div>
    </div>

    <!-- 지도 섹션 -->
    <div class="map-box">
      <Mapcopy />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import Carousel from "@/components/Carousel.vue";
import Mapcopy from "@/components/Mapcopy.vue";

import { useNewsStore } from "@/stores/news";

const { limitedNews, fetchNewsData } = useNewsStore();

const router = useRouter();

const currentDate = ref(""); // 초기화된 ref 선언
const stockData = ref([]); // 초기화된 ref 선언

// 날짜 포맷 함수
const formatDate = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}.${month}.${day}`;
};

// 데이터 로드 함수
const fetchStockData = () => {
  stockData.value = [
    { name: "S&P 500", price: "4,500.00", direction: "up" },
    { name: "NASDAQ", price: "13,200.00", direction: "down" },
    { name: "KOSPI", price: "2,800.00", direction: "up" },
  ];
};

// 텍스트 자르기 함수
const truncateText = (text, maxLength) => {
  if (!text) return "";
  return text.length > maxLength ? text.slice(0, maxLength) + "..." : text;
};

// 라우팅 함수
const goToPage = (page) => {
  router.push(`/${page}`);
};

// 컴포넌트 마운트 시 실행
onMounted(() => {
  currentDate.value = formatDate(new Date()); // 날짜 초기화
  fetchStockData();
  fetchNewsData();
});
</script>

<style scoped>
/* 메인 컨테이너 */
.home-page {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 캐러샐 섹션 */
.carousel-container {
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 20px;
}

/* 날짜, 증시, 금융 뉴스 박스 */
.info-box {
  background-color: rgba(240, 240, 240, 0.9);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.date {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

/* 구분선 */
.divider {
  height: 1px;
  background-color: #ccc; /* 구분선 색상 */
  margin: 20px 0; /* 위아래 여백 */
}

/* 증시 및 뉴스 리스트 */
.stock-list {
  list-style: none;
  padding: 0;
}

.stock-list li {
  display: flex;
  align-items: center;
  gap: 10px;
}

.change-icon {
  font-size: 14px;
  font-weight: bold;
}

.change-icon.up {
  color: #3a774e; /* 초록색 */
}

.change-icon.down {
  color: #d9534f; /* 빨간색 */
}

.news-list {
  list-style: none;
  padding: 0;
}

.news-button {
  margin-top: 10px;
  padding: 12px;
  font-size: 14px;
  background-color: #3a3a3a;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.news-button:hover {
  background-color: #2b2b2b;
}

/* 지도 박스 */
.map-box {
  background-color: rgba(240, 240, 240, 0.9);
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}
</style>
