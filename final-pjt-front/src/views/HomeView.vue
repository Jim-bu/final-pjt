<script setup>
import { useUserStore } from '@/stores/users'
import Map from '@/components/Map.vue'
import ExchangeCalculater from '@/components/ExchangeCalculater.vue'
import ExchangeCard from '@/components/ExchangeCard.vue'
import GoBack from '@/components/GoBack.vue'

const userStore = useUserStore()
</script>

<template>
  <div class="home-page">
    <GoBack />
    <v-carousel
      cycle
      hide-delimiters
      show-arrows="hover"
      height="400"
      class="full-width-carousel"
    >
      <v-carousel-item>
        <div class="caro-item-text">
          <p><span class="color">예 ∙ 적금 금리</span>를 쉽게 비교하고</p>
          <div class="title">
            <p>나에게 맞는</p>
            <p><span class="color">금융상품</span>을 <span class="color">추천</span> 받자!</p>
          </div>
          <v-btn
            v-if="userStore.isLogin"
            block
            rounded="xl"
            size="x-large"
            color="#1089FF"
            class="caro-item-btn"
            :to="{ name: 'productRecommend', params: { username: userStore.userInfo.username }}"
            >
              회원가입하고 추천받기
          </v-btn>
        </div> 
      </v-carousel-item>

      <v-carousel-item>
        <div class="caro-item-text">
          <p>금융상품에 관한 이야기 어디서 할 수 있을까?</p>
          <div class="title">
            <p><span class="color">금융상품 자유 게시판</span>으로</p>
            <p>오세요!</p>
          </div>
          <v-btn
            block
            rounded="xl"
            size="x-large"
            color="#1089FF"
            class="caro-item-btn"
            :to="{ name: 'postList'}"
          >금융상품 자유 게시판 바로가기</v-btn>
        </div>
      </v-carousel-item>

      <v-carousel-item>
        <div class="item3">
          <p><span class="color">금융</span>과 <span class="color">나</span>를 잇다.</p>
          <div class="title">
            <p><span class="color text-h1 font-weight-bold">MYFI</span></p>
          </div>
          <v-btn
            v-if="userStore.isLogin"
            block
            rounded="xl"
            size="x-large"
            color="#1089FF"
            class="caro-item-btn"
            :to="{ name: 'productRecommend', params: { username: userStore.userInfo.username }}"
            >
              회원가입하고 추천받기
          </v-btn>
        </div> 
      </v-carousel-item>
    </v-carousel>

    <div class="exchange-section">
      <ExchangeCard
        class="exchange-card"
        :currency="'USD'"
        :name="'미국 달러'"
        elevation="5"
      />
      <ExchangeCard
        class="exchange-card"
        :currency="'JPY'"
        :name="'일본 엔'"
        elevation="5"
      />
    </div>

    <div class="calculater-section">
      <h1><span class="color">환율</span> 계산기</h1>
      <ExchangeCalculater class="elevation-4" />
    </div>

    <div class="map-section">
      <Map :width="350" :height="600" class="mt-5" />
    </div>
  </div>
</template>

<style scoped>
.home-page {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 16px;
}

.full-width-carousel {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

.v-carousel {
  border-bottom: 1px solid #DBDBDB;
}

.caro-item-text {
  position: absolute;
  top: 20%;
  left: 5vw; /* 좌측 간격을 조정 */
  width: calc(100% - 10vw); /* 좌우 5vw씩 간격을 두도록 조정 */
  text-align: center;
}

.item3 {
  position: absolute;
  top: 20%;
  left: 5vw;
  width: calc(100% - 10vw);
  text-align: center;
}

.item3 > p,
.caro-item-text > p {
  margin: 5px 0;
  font-size: 18px; /* 앱 같은 작은 화면에 맞게 줄인 폰트 크기 */
  font-weight: 600;
}

.title {
  margin: 5px 0;
  font-size: 28px; /* 좁은 화면에 맞게 폰트 크기 조정 */
  font-weight: 900;
  letter-spacing: -1px;
}

.caro-item-btn {
  font-size: 16px; /* 좁은 화면에 맞게 줄인 버튼 폰트 크기 */
  font-weight: 600;
  letter-spacing: -1px;
  margin-top: 10px;
}

.exchange-section {
  display: flex;
  flex-direction: column; /* 세로로 정렬 */
  gap: 15px;
  margin-top: 20px;
}

.exchange-card {
  width: 100%; /* 가로 크기를 100%로 설정하여 한 줄에 한 카드만 표시 */
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 8px;
}

.calculater-section {
  width: 100%;
  margin-top: 20px;
  background-color: #f8f9fa;
  padding: 16px;
  border-radius: 10px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
}

.map-section {
  width: 100%;
  margin-top: 20px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
}
</style>
