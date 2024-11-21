<template>
  <v-carousel
    cycle
    hide-delimiters
    show-arrows="hover"
    height="400"
  >
    <v-carousel-item v-for="(slide, index) in slides" :key="index">
      <div class="caro-item-text">
        <p>{{ slide.description }}</p>
        <div class="title">
          <p>{{ slide.title }}</p>
        </div>
        <v-btn
          block
          rounded="xl"
          size="x-large"
          color="#1089FF"
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
/* 캐러샐 전체 컨테이너 */
.v-carousel {
  border-radius: 12px;
  overflow: hidden;
  background-color: #f5e5cc;
}

.caro-item-text {
  flex: 1;
  text-align: left;
  padding: 30px 40px; /* 왼쪽 위로 이동 */
  line-height: 1.8; /* 줄 간격 확대 */
}

.caro-item-text .description {
  margin-bottom: 20px;
  font-size: 18px; /* 글씨 크기 확대 */
  color: #555;
}

.caro-item-text .title {
  font-size: 28px; /* 글씨 크기 확대 */
  font-weight: bold;
  color: #333;
  margin-bottom: 30px;
}

.caro-item-btn {
  margin-top: 10px;
  padding: 12px 24px;
  font-size: 18px; /* 버튼 글씨 크기 확대 */
  background-color: #70533a; /* 갈색 계열 */
  color: white;
  border-radius: 24px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.caro-item-btn:hover {
  background-color: #7a4e26; /* 호버 시 조금 더 어두운 갈색 */
}


</style>
