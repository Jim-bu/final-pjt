<template>
  <div class="news-container">
    <h1>최신 금융 뉴스</h1>

    <!-- 뉴스 카드 -->
    <div class="news-card" v-for="news in newsList" :key="news.id">
      <h2>{{ news.title }}</h2>
      <p>{{ news.summary }}</p>
      <a :href="news.link" target="_blank">자세히 보기</a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/'; // API URL
const token = localStorage.getItem('token'); // 토큰 가져오기
const newsList = ref([]); // 뉴스 데이터 저장

const fetchNews = function () {
  axios({
    method: 'get',
    url: `${API_URL}/news/`,
    headers: {
      Authorization: `Token ${token}`,
    },
  })
    .then((res) => {
      newsList.value = res.data;
    })
    .catch((err) => {
      console.error('뉴스 데이터 가져오기 실패:', err.response?.data || err.message);
    });
};

onMounted(() => {
  fetchNews();
});
</script>

<style scoped>
.news-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.news-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.news-card h2 {
  font-size: 18px;
  margin-bottom: 8px;
}

.news-card p {
  font-size: 14px;
  color: #555;
}

.news-card a {
  font-size: 12px;
  color: #3366cc;
  text-decoration: none;
}

.news-card a:hover {
  text-decoration: underline;
}
</style>
