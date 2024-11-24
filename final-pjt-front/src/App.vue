<template>
  <v-app>
    <NavBar v-if="!isLoadingScreen" />
    <chatbotModal v-if="!isLoadingScreen" />
    <div class="centered-content">
      <router-view />
      <div class="content-padding"></div>
    </div>
    <Remote />
  </v-app>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import NavBar from './components/NavBar.vue';
import Remote from './components/Remote.vue';
import chatbotModal from './components/chatbotModal.vue';

const route = useRoute(); // 현재 라우트를 가져옵니다.
const isLoadingScreen = ref(false);

// 라우트 이름을 감지하여 NavBar 표시 여부를 업데이트
watch(
  () => route.name,
  (newRouteName) => {
    isLoadingScreen.value = newRouteName === 'LoadingScreen';
  },
  { immediate: true } // 컴포넌트가 로드될 때 바로 실행
);
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  width: 100%;
  height: 100%;
}

.v-app {
  display: flex;
  flex-direction: column; /* 위에서 아래로 정렬 */
  align-items: center; /* 수평 중앙 정렬 */
  min-height: 100vh; /* 화면 전체 높이 채움 */
  background-color: #f5f5f5; /* 배경 색상 */
  overflow-x: hidden;
}

.centered-content {
  width: 100%;
  max-width: 600px; /* 콘텐츠 너비를 600px로 제한 */
  margin: 0 auto; /* 가운데 정렬 */
  padding: 16px;
  box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
  background-color: white; /* 흰색 배경 */
  border-radius: 10px; /* 모서리를 둥글게 설정 */
  flex-grow: 1; /* 남는 공간 채우기 */
}

.content-padding {
  height: 100px; /* 추가 여백 높이 */
  background-color: transparent; /* 투명 배경 */
}

@media (max-width: 600px) {
  .centered-content {
    width: 100%;
    max-width: 100%;
    margin: 0;
    border-radius: 0;
  }
}

footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100px; /* 네비게이션 바 높이 */
  background-color: #424530; /* Fern 색상 */
  color: #FFEFCD; /* Warm Ivory 색상 */
  text-align: center;
  line-height: 60px;
  z-index: 10;
}
</style>
