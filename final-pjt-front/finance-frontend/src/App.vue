<template>
  <div>
    <h1>금융 상품 추천 챗봇</h1>
    <SurveyBot v-if="showChat" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import SurveyBot from './components/SurveyBot.vue';

const showChat = ref(false);

onMounted(() => {
  // 컴포넌트가 마운트된 후 대화창 표시
  showChat.value = true;
});
</script>

<style>
h1 {
  text-align: center;
  margin-top: 20px;
}
</style>
