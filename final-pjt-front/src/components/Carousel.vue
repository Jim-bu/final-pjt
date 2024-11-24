<template>
  <v-carousel
    cycle
    hide-delimiters
    show-arrows="hover"
    height="400"
    class="custom-carousel"
  >
    <v-carousel-item v-for="(slide, index) in slides" :key="index">
      <div class="caro-item-container">
        <!-- 흐릿한 배경 로고 -->
        <img src="@/assets/logo.jpg" alt="Background Logo" class="background-logo" />
        
        <!-- 오른쪽 상단 텍스트 -->
        <div class="caro-item-text">
          <div class="title">{{ slide.title }}</div>
          <p class="description">{{ slide.description }}</p>
        </div>
        
        <!-- 오른쪽 버튼 -->
        <v-btn
          rounded="lg"
          class="caro-item-btn"
          @click="slide.action"
        >
          {{ slide.buttonText }} <span class="arrow">↗</span>
        </v-btn>
      </div>
    </v-carousel-item>
  </v-carousel>
</template>


<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const slides = [
  {
    title: "환율 정보 바로가기",
    description: "최신 환율 정보를 확인하세요!",
    buttonText: "환율 보기",
    action: () => {
      console.log("Navigate to exchange page");
      router.push("/exchange");
    },
  },
  {
    title: "평가 게시판 구경하기",
    description: "금융 상품에 대한 사용자 리뷰를 확인해보세요!",
    buttonText: "게시판 구경하기",
    action: () => {
      console.log("Navigate to community page");
      router.push("/community");
    },
  },
  {
    title: "상품 추천 받기",
    description: "당신에게 딱 맞는 금융 상품을 추천해드립니다!",
    buttonText: "추천받기",
    action: () => {
      console.log("Navigate to recommendation page");
      router.push("/recommendation");
    },
  },
];
</script>


<style scoped>
/* 캐러셀 컨테이너 */
.custom-carousel {
  border-radius: 16px;
  overflow: hidden;
  background-color: #ffffff; /* 대비를 위한 밝은 배경 */
  height: 400px;
  position: relative;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* 입체감 */
}

/* 흐릿한 배경 로고 */
.background-logo {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%; /* 로고 크기 */
  height: auto;
  opacity: 0.4; /* 흐릿하게 */
  z-index: 0;
  object-fit: cover;
}

/* 캐러셀 콘텐츠 컨테이너 */
.caro-item-container {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  padding: 20px;
}

/* 오른쪽 상단 텍스트 */
.caro-item-text {
  position: absolute;
  top: 20px;
  right: 20px;
  text-align: right;
  color: #333333;
}

.title {
  font-size: 26px;
  font-weight: 700;
  color: #2e2e2e;
  margin-bottom: 8px;
}

.description {
  font-size: 16px;
  font-weight: 500;
  color: #555555;
  line-height: 1.6;
}

/* 오른쪽 버튼 */
.caro-item-btn {
  position: absolute;
  bottom: 20px;
  right: 20px; /* 오른쪽으로 버튼 이동 */
  width: 300px; /* 버튼 가로 크기 */
  height: 70px; /* 버튼 세로 크기 증가 */
  background-color: #70533a; /* 버튼 배경 */
  color: #ffffff; /* 버튼 텍스트 */
  font-size: 18px;
  font-weight: 700;
  text-align: center;
  border-radius: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.caro-item-btn:hover {
  background-color: #8c735b; /* 호버 색상 */
  transform: translateY(-3px); /* 호버 애니메이션 */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

/* 화살표 스타일 */
.arrow {
  font-size: 20px;
  margin-left: 8px;
}

/* 캐러셀 화살표 스타일 */
.v-carousel .v-btn {
  background-color: #f5f5f5;
  color: #333333;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.v-carousel .v-btn:hover {
  background-color: #e0e0e0;
}
</style>
