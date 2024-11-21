<template>
  <div class="home-page">
    <!-- 캐러샐 섹션 -->
    <div class="carousel-container">
      <Carousel />
    </div>

    <!-- 날짜, 세계 증시, 금융 뉴스 -->
    <div class="info-box">
      <p class="date">{{ currentDate }}</p>
      <Market_NewsView />
    </div>

    <!-- 환율 정보 바로가기 -->
    <div class="buttons-box">
      <button class="action-button" @click="goToPage('exchangeRates')">환율 정보 바로가기</button>
    </div>

    <!-- 지도 섹션 -->
    <div class="map-box">
        <Mapcopy />
    </div>
  </div>
</template>



<script setup>
import { ref } from "vue";
import { useUserStore } from "@/stores/users";
import Map from "@/components/Map.vue";
import GoBack from "@/components/GoBack.vue";
import Market_NewsView from "./Market_NewsView.vue"
import Carousel from "@/components/Carousel.vue";
import Mapcopy from "@/components/Mapcopy.vue"

const userStore = useUserStore();


const formatDate = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}.${month}.${day}`;
};

const currentDate = ref(formatDate(new Date())); // 현재 날짜를 포맷하여 초기화

const goToPage = (page) => {
  window.location.href = `/${page}`;
};
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
  background-color: rgba(0, 0, 0, 0.8);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

/* 날짜, 증시, 금융 뉴스 박스 */
.info-box {
  background-color: rgba(240, 240, 240, 0.9); /* 밝은 회색 */
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.date {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 16px;
  text-align: left;
}

/* 버튼 박스 */
.buttons-box {
  display: flex;
  justify-content: center;
}

.action-button {
  padding: 12px 24px;
  font-size: 16px;
  color: #fff;
  background-color: #3a3a3a; /* 어두운 회색 */
  border: none;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.action-button:hover {
  background-color: #2b2b2b;
}

/* 지도 박스 */
.map-box {
  background-color: rgba(240, 240, 240, 0.9);
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  position: relative;
}

</style>
