<template>
  <div class="news-page">
    <h1>경제 뉴스</h1>
    <div v-if="loading" class="loading">뉴스 데이터를 불러오는 중...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-else>
      <ul class="news-list">
        <li v-for="news in newsData" :key="news.id" class="news-item">
          <h3>{{ news.title }}</h3>
          <p>{{ news.description }}</p>
          <div class="news-meta">
            <span>{{ formatDate(news.pub_date) }}</span>
            <div class="news-links">
              <a :href="news.originallink" target="_blank" rel="noopener noreferrer">
                원문 보기
              </a>
              <a :href="news.link" target="_blank" rel="noopener noreferrer">
                네이버 뉴스
              </a>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useNewsStore } from "@/stores/news";

const { newsData, fetchNewsData, loading, error } = useNewsStore();

const formatDate = (dateString) => {
  try {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      weekday: 'long'
    }).format(date);
  } catch (error) {
    return dateString;
  }
};

onMounted(() => {
  fetchNewsData();
});
</script>


<style scoped>
.news-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 16px;
  font-family: Arial, sans-serif;
  background-color: #f9f1dc; /* 연한 노랑 배경 */
}

h1 {
  font-size: 28px;
  color: #5a5a5a;
  text-align: center;
  margin-bottom: 20px;
}

.news-list {
  list-style: none;
  padding: 0;
}

.news-item {
  padding: 20px;
  border: 1px solid #e5d4c0; /* 옅은 갈색 */
  border-radius: 8px;
  margin-bottom: 16px;
  background-color: #d8e7d1; /* 연한 초록 배경 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.news-item h3 {
  font-size: 20px;
  color: #70533a; /* 짙은 갈색 */
  margin-bottom: 10px;
}

.news-item p {
  font-size: 16px;
  color: #333;
  margin-bottom: 10px;
}

.news-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: #666;
}

.news-meta a {
  color: #3a774e; /* 초록 계열 */
  text-decoration: none;
}

.news-meta a:hover {
  text-decoration: underline;
}

.news-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #e5d4c0;
}

.news-links {
  display: flex;
  gap: 15px;
}

.news-links a {
  color: #3a774e;
  text-decoration: none;
  font-size: 14px;
  padding: 4px 8px;
  border-radius: 4px;
  background-color: rgba(58, 119, 78, 0.1);
}

.news-links a:hover {
  background-color: rgba(58, 119, 78, 0.2);
  text-decoration: none;
}
</style>
