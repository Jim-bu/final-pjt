<template>
  <div class="chat-bot">
    <div v-for="(message, index) in messages" :key="index" class="chat-message">
      <p>{{ message.text }}</p>
    </div>
    <div v-if="currentQuestion">
      <p>{{ currentQuestion.text }}</p>
      <button
        v-for="(option, index) in currentQuestion.options"
        :key="index"
        @click="handleResponse(option)"
      >
        {{ option }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const messages = ref([{ text: '안녕하세요! 금융 상품 추천을 원하시나요?' }]);
const userResponses = ref([]);

const questions = [
  {
    id: 0,
    text: '금융 상품 추천을 원하시나요?',
    options: ['네, 원합니다', '아니요, 괜찮습니다'],
  },
  {
    id: 1,
    text: '어떤 종류의 금융 상품을 찾고 계신가요?',
    options: ['예금', '적금', '투자', '카드'],
  },
  {
    id: 2,
    text: '주로 사용하는 은행이 어디인가요?',
    options: ['국민은행', '신한은행', '하나은행', '우리은행', '상관없음'],
  },
];

const currentQuestion = ref(questions[0]);

function handleResponse(option) {
  messages.value.push({ text: `사용자: ${option}` });
  userResponses.value.push(option);

  if (currentQuestion.value.id === 0) {
    if (option === '네, 원합니다') {
      currentQuestion.value = questions[1];
    } else {
      currentQuestion.value = null;
      messages.value.push({ text: '감사합니다! 다음에 또 이용해주세요.' });
    }
  } else if (currentQuestion.value.id === 1) {
    currentQuestion.value = questions[2];
  } else if (currentQuestion.value.id === 2) {
    submitSurvey();
  }
}

// 설문조사 응답 제출 후 추천 페이지로 이동
async function submitSurvey() {
  try {
    const response = await fetch('/api/submit-survey/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ responses: userResponses.value }),
    });

    const data = await response.json();
    if (data.status === 'success') {
      messages.value.push({ text: '설문이 완료되었습니다! 추천 페이지로 이동합니다.' });
      router.push('/recommendation'); // 추천 페이지로 이동
    }
  } catch (error) {
    console.error('설문조사 제출 오류:', error);
    messages.value.push({ text: '오류가 발생했습니다. 다시 시도해주세요.' });
  }
}

// API 요청 함수
async function submitSurveyAPI() {
  try {
    const response = await fetch('/api/submit-survey/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ responses: userResponses.value }),
    });

    const data = await response.json();
    if (data.status === 'success') {
      router.push('/recommendation'); // 추천 페이지로 이동
    }
  } catch (error) {
    console.error('설문조사 제출 오류:', error);
  }
}
</script>

<style>
.chat-bot {
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 10px;
  width: 300px;
  margin: 0 auto;
}

.chat-message {
  margin-bottom: 10px;
}

button {
  margin: 5px;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #007bff;
  color: white;
}

button:hover {
  background-color: #0056b3;
}
</style>
