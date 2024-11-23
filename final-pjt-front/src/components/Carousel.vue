<template>
  <v-carousel
    cycle
    hide-delimiters
    show-arrows="hover"
    height="300"
    class="custom-carousel"
  >
    <v-carousel-item v-for="(slide, index) in slides" :key="index">
      <div class="caro-item-text">
        <div class="title">{{ slide.title }}</div>
        <p class="description">{{ slide.description }}</p>
        <v-btn
          rounded="xl"
          class="caro-item-btn"
          @click="slide.action"
        >
          {{ slide.buttonText }}
        </v-btn>
      </div>
    </v-carousel-item>
  </v-carousel>
</template>

<script setup>
const slides = [
  {
    title: "AI 맞춤형 금융 상품",
    description: "AI가 추천하는 최적의 금융 상품을 확인해보세요!",
    buttonText: "나에게 맞는 상품 보기",
    action: () => {
      console.log("Navigate to 추천 페이지");
    },
  },
  {
    title: "고금리 예적금 상품 비교",
    description: "높은 금리를 제공하는 상품을 비교해보세요!",
    buttonText: "최고 금리 보기",
    action: () => {
      console.log("Navigate to 예적금 비교 페이지");
    },
  },
  {
    title: "맞춤형 카드 혜택 추천",
    description: "당신의 소비 패턴에 맞는 최고의 카드를 추천받으세요!",
    buttonText: "추천받기",
    action: () => {
      console.log("Navigate to 카드 추천 페이지");
    },
  },
];
</script>

<style scoped>
/* 캐러셀 컨테이너 */
.custom-carousel {
  border-radius: 12px;
  overflow: hidden;
  background-color: #f9f5f0;
  height: 300px;
}

/* 캐러셀 아이템 텍스트 */
.caro-item-text {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
  text-align: left;
  position: relative;
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #333333;
  margin-bottom: 16px;
}

.description {
  font-size: 16px;
  color: #555555;
  margin-bottom: 20px;
  line-height: 1.6;
}

/* 캐러셀 버튼 */
.caro-item-btn {
  position: absolute;
  bottom: 20px;
  right: 25%; /* 오른쪽 25% 지점 */
  transform: translateX(50%);
  width: 250px; /* 버튼 고정 가로 길이 */
  height: 100px; /* 버튼 고정 세로 길이 */
  background-color: #70533a; /* 갈색 계열 */
  color: #ffffff;
  font-size: 20px; /* 글씨 크기 */
  padding: 0; /* 기본 패딩 제거 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: background-color 0.3s ease;
  line-height: 40px; /* 버튼 세로 정렬 */
}

.caro-item-btn:hover {
  background-color: #8c735b;
}
</style>
