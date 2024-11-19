<script setup>
import { ref } from 'vue';

const showRemote = ref(false);

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const toggleChatbot = () => {
  // 여기에 챗봇을 활성화하거나 나타내는 로직을 추가합니다.
  console.log('챗봇 활성화!');
};
</script>

<template>
  <div class="remote-wrapper">
    <v-btn
      icon
      color="primary"
      @click="scrollToTop"
      class="remote-button"
    >
      <v-icon>mdi-arrow-up</v-icon>
    </v-btn>

    <v-btn
      icon
      color="primary"
      @click="toggleChatbot"
      class="remote-button"
    >
      <v-icon>mdi-robot</v-icon>
    </v-btn>
  </div>
</template>

<style scoped>
.remote-wrapper {
  position: fixed;
  right: 20px;
  bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  z-index: 999;
}

.remote-button {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
