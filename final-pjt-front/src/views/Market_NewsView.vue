<template>
  <div class="container">
    <div class="box market-box">
      <h2>세계 증시 현황</h2>
      <div v-if="marketData.length">
        <div v-for="(market, index) in marketData" :key="index" class="market-item">
          <span>{{ market.name }}</span>
          <span :class="{ up: market.change > 0, down: market.change < 0 }">
            {{ market.value }} ({{ market.change > 0 ? "▲" : "▼" }} {{ market.change }}%)
          </span>
        </div>
      </div>
      <div v-else>
        <p>증시 데이터를 불러오는 중...</p>
      </div>
    </div>

    <div class="box news-box">
      <h2>최신 금융 뉴스</h2>
      <div v-if="newsData.length">
        <div v-for="(news, index) in newsData" :key="index" class="news-item">
          <h3>{{ news.title }}</h3>
          <p>{{ news.summary }}</p>
          <a :href="news.link" target="_blank">자세히 보기</a>
        </div>
      </div>
      <div v-else>
        <p>뉴스를 불러오는 중...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const marketData = ref([]);
const newsData = ref([]);

// 백 api key
const fetchMarketData = function () {
  axios({
    method: "get",
    url: "/api/market-data/",
  })
    .then((res) => {
      marketData.value = res.data;
    })
    .catch((err) => {
      console.error("증시 데이터 가져오기 실패:", err);
      marketData.value = [];
    });
};

// 프론트 .env apikey
const fetchNewsData = function () {
  axios({
    method: "get",
    url: `https://example-api.com/news?apikey=${import.meta.env.VITE_NEWS_API_KEY}`,
  })
    .then((res) => {
      newsData.value = res.data;
    })
    .catch((err) => {
      console.error("뉴스 데이터 가져오기 실패:", err);
      newsData.value = [];
    });
};

onMounted(() => {
  fetchMarketData();
  fetchNewsData();
});
</script>

<style>
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.box {
  background: rgba(255, 255, 255, 0.8); /* 반투명 효과 */
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
  backdrop-filter: blur(10px); /* 배경 흐림 효과 */
}

.market-box h2,
.news-box h2 {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.market-item,
.news-item {
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.market-item span {
  font-size: 14px;
}

.market-item .up {
  color: green;
}

.market-item .down {
  color: red;
}

.news-item h3 {
  font-size: 16px;
  margin: 0;
}

.news-item p {
  font-size: 14px;
  color: #555;
}

.news-item a {
  font-size: 12px;
  color: #007bff;
  text-decoration: none;
}

.news-item a:hover {
  text-decoration: underline;
}
</style>
