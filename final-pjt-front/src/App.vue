<template>
  <v-app>
    <NavBar />
    <div class="centered-content">
      <router-view /> <!-- 각 페이지의 콘텐츠가 여기에 표시됨 -->
    </div>
    <Remote />
  </v-app>
</template>

<script setup>
import NavBar from './components/NavBar.vue';
import Remote from './components/Remote.vue';
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
  overflow: visible
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

@media (max-width: 600px) {
  .centered-content {
    width: 100%;
    max-width: 100%;
    margin: 0;
    border-radius: 0;
  }
}
</style>
