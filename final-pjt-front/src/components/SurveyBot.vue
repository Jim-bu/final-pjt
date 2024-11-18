<template>
  <div class="chat-bot">
    <h2>설문조사</h2>
    <div v-for="(message, index) in messages" :key="index" class="chat-message">
      <p>{{ message.text }}</p>
    </div>
    <div v-if="currentQuestion">
      <h3>{{ currentQuestion.text }}</h3>
      <div class="options">
        <div
          v-for="(option, index) in currentQuestion.options"
          :key="index"
          :class="['option-button', selectedOption === option ? 'selected' : '']"
          @click="handleResponse(option)"
        >
          {{ option }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();

const messages = ref([{ text: '안녕하세요! 금융 상품 추천을 원하시나요?' }]);
const userResponses = ref([]);
const selectedOption = ref(null);

const questions = reactive([
  { id: 0, text: '금융 상품 추천을 원하시나요?', options: ['네, 원합니다', '아니요, 괜찮습니다'] },
  { id: 1, text: '어떤 상품을 원하시나요?', options: ['예금', '적금', '투자', '카드'] },
  { id: 2, text: '주로 사용하는 은행이 어디인가요?', options: ['국민은행', '신한은행', '하나은행', '우리은행', '상관없음'] },
  { id: 3, text: '이용해본 경험이 있는 상품은?', options: ['예금', '적금', '펀드', '주식', '없음'] },
  { id: 4, text: '투자 자금의 기간 수준은?', options: ['6개월 미만', '6개월 이상~1년', '1년 이상~2년', '2년 이상~3년', '3년 이상'] },
  { id: 5, text: '금융상품에 가용 금액 수준은?', options: ['100만원 이하', '100만원~500만원', '500만원~1000만원', '1000만원 이상'] },
  { id: 6, text: '투자 목적은 무엇인가요?', options: ['단기 수익', '장기 투자', '위험 회피', '재산 증식'] },
  { id: 7, text: '기대하는 이익 수준은?', options: ['1% 이하', '1% ~ 3%', '3% ~ 5%', '5% 이상'] },
]);

const currentQuestion = ref(questions[0]);

function handleResponse(option) {
  selectedOption.value = option;
  messages.value.push({ text: `사용자: ${option}` });
  userResponses.value.push(option);

  if (currentQuestion.value.id === 0 && option === '아니요, 괜찮습니다') {
    console.log('사용자가 "아니요"를 선택했습니다. 메인 페이지로 이동합니다.');
    router.replace('/main').catch((err) => console.error('페이지 이동 오류:', err));
    return;
  }

  if (currentQuestion.value.id === questions.length - 1) {
    console.log('마지막 질문에 도달했습니다. 설문을 제출합니다.');
    submitSurvey();
  } else {
    currentQuestion.value = questions[currentQuestion.value.id + 1];
    selectedOption.value = null;
  }
}

async function submitSurvey() {
  try {
    const response = await axios.post('/api/submit-survey/', {
      responses: userResponses.value,
    });

    if (response.data.status === 'success') {
      console.log('설문 제출이 완료되었습니다. 추천 페이지로 이동합니다.');
      router.replace('/recommendation').catch((err) => console.error('페이지 이동 오류:', err));
      // 라우터 리셋 시도
      resetRouter();
    } else {
      messages.value.push({ text: '서버에서 오류가 발생했습니다. 다시 시도해주세요.' });
    }
  } catch (error) {
    console.error('설문조사 제출 오류:', error);
    messages.value.push({ text: '오류가 발생했습니다. 다시 시도해주세요.' });
  }
}
</script>

<style scoped>
.chat-bot {
  padding: 20px;
  max-width: 400px;
  margin: 0 auto;
  background-color: #f0f0f0;
  border-radius: 10px;
}

h2 {
  text-align: center;
}

.chat-message {
  margin-bottom: 10px;
}

.options {
  display: flex;
  flex-direction: column;
}

.option-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  margin: 5px 0;
  border: 2px solid #ccc;
  border-radius: 10px;
  cursor: pointer;
  background-color: #fff;
  transition: all 0.3s;
}

.option-button:hover {
  border-color: #90ee90;
}

.selected {
  border-color: #90ee90;
  background-color: #e6ffe6;
  color: #333;
  font-weight: bold;
}
</style>
