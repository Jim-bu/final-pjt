<template>
  <div class="survey-container">
    <div v-if="!surveyCompleted" class="survey-bot">
      <div class="survey-header">
        <h2>맞춤형 금융 상품 추천을 위한 설문조사</h2>
        <p>{{ currentSection.title }}</p>
      </div>

      <div class="survey-progress">
        <div class="progress-bar">
          <div :style="{ width: `${progressPercentage}%` }" class="progress-fill"></div>
        </div>
        <span>{{ currentQuestionIndex + 1 }} / {{ totalQuestions }}</span>
      </div>

      <div class="survey-content">
        <div class="question-container">
          <h3>{{ currentQuestion.text }}</h3>
          <div class="options-container">
            <button
              v-for="option in currentQuestion.options"
              :key="option.value"
              :class="['option-button', { selected: selectedOption === option.value }]"
              @click="selectOption(option.value)"
            >
              {{ option.label }}
            </button>
          </div>
        </div>

        <div class="navigation-buttons">
          <button 
            v-if="currentQuestionIndex > 0" 
            @click="previousQuestion" 
            class="nav-button"
          >
            이전
          </button>
          <button 
            v-if="currentQuestionIndex < totalQuestions - 1" 
            @click="nextQuestion" 
            class="nav-button"
            :disabled="!selectedOption"
          >
            다음
          </button>
          <button 
            v-else 
            @click="submitSurvey" 
            class="submit-button"
            :disabled="!selectedOption"
          >
            제출하기
          </button>
        </div>
      </div>
    </div>

    <div v-else class="survey-completion">
      <h2>설문이 완료되었습니다!</h2>
      <p>맞춤형 금융 상품 추천 결과를 확인하시겠습니까?</p>
      <button @click="goToRecommendations" class="recommendation-button">
        추천 결과 보기
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/users'
import axios from 'axios'

const router = useRouter()
const userStore = useUserStore()

// 상태 관리
const currentQuestionIndex = ref(0)
const selectedOption = ref(null)
const surveyResponses = ref({})
const surveyCompleted = ref(false)

// 설문 섹션과 질문 정의
const surveyStructure = {
  basicInfo: {
    title: '기본 정보',
    questions: [
      {
        id: 'age_group',
        text: '연령대를 선택해주세요.',
        options: [
          { value: '20대', label: '20대' },
          { value: '30대', label: '30대' },
          { value: '40대', label: '40대' },
          { value: '50대', label: '50대' },
          { value: '60대_이상', label: '60대 이상' }
        ]
      },
      {
        id: 'income_source',
        text: '현재 주요 소득원은 무엇인가요?',
        options: [
          { value: '직장', label: '직장' },
          { value: '자영업', label: '자영업' },
          { value: '프리랜서', label: '프리랜서' },
          { value: '기타', label: '기타' }
        ]
      },
      {
        id: 'asset_size',
        text: '자산 규모를 선택해주세요.',
        options: [
          { value: '1000만원_이하', label: '1000만원 이하' },
          { value: '1000만원_5000만원', label: '1000만원 ~ 5000만원' },
          { value: '5000만원_이상', label: '5000만원 이상' }
        ]
      }
    ]
  },
  financialGoals: {
    title: '금융 목표',
    questions: [
      {
        id: 'financial_purpose',
        text: '금융 상품을 이용하는 주요 목적은 무엇인가요?',
        options: [
          { value: '단기_수익', label: '단기 수익' },
          { value: '장기_자산관리', label: '장기 자산 관리' },
          { value: '리스크_회피', label: '리스크 회피' },
          { value: '재산_증식', label: '재산 증식' }
        ]
      },
      {
        id: 'important_factor',
        text: '금융 상품에서 가장 중요하게 생각하는 요소는 무엇인가요?',
        options: [
          { value: '이율', label: '이율' },
          { value: '안정성', label: '안정성' },
          { value: '유동성', label: '유동성' },
          { value: '브랜드_신뢰도', label: '브랜드 신뢰도' }
        ]
      },
      {
        id: "recent_investment",
        text: "최근 투자 경험이 있나요?",
        options: [
          { value: true, label: "예" },
          { value: false, label: "아니오" }
        ]
      },
    ]
  },
  financialExperience: {
    title: '금융 이용 경험',
    questions: [
      {
        id: 'financial_products',
        text: '이용한 적이 있는 금융 상품은 무엇인가요?',
        options: [
          { value: '예금', label: '예금' },
          { value: '적금', label: '적금' },
          { value: '펀드', label: '펀드' },
          { value: '주식', label: '주식' },
          { value: '없음', label: '없음' }
        ]
      },
      {
        id: 'preferred_bank',
        text: '주로 사용하는 은행은 어디인가요?',
        options: [
          { value: '국민은행', label: '국민은행' },
          { value: '신한은행', label: '신한은행' },
          { value: '우리은행', label: '우리은행' },
          { value: '하나은행', label: '하나은행' },
          { value: '기타', label: '기타' }
        ]
      }
    ]
  }
}

// Computed Properties
const currentSection = computed(() => {
  const sections = Object.values(surveyStructure)
  const totalQuestions = sections.reduce((acc, section) => 
    acc + section.questions.length, 0)
  let questionCount = 0
  
  for (const section of sections) {
    questionCount += section.questions.length
    if (currentQuestionIndex.value < questionCount) {
      return section
    }
  }
  return sections[0]
})

const currentQuestion = computed(() => {
  const sections = Object.values(surveyStructure)
  let questionIndex = currentQuestionIndex.value
  
  for (const section of sections) {
    if (questionIndex < section.questions.length) {
      return section.questions[questionIndex]
    }
    questionIndex -= section.questions.length
  }
})

const totalQuestions = computed(() => {
  return Object.values(surveyStructure).reduce((acc, section) => 
    acc + section.questions.length, 0)
})

const progressPercentage = computed(() => {
  return (currentQuestionIndex.value / totalQuestions.value) * 100
})

// Methods
const selectOption = (option) => {
  selectedOption.value = option
  surveyResponses.value[currentQuestion.value.id] = option
}

const nextQuestion = () => {
  if (selectedOption.value) {
    currentQuestionIndex.value++
    selectedOption.value = surveyResponses.value[currentQuestion.value?.id] || null
  }
}

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
    selectedOption.value = surveyResponses.value[currentQuestion.value.id] || null
  }
}

const submitSurvey = async () => {
  if (!userStore.isLogin) {
    alert('로그인이 필요한 서비스입니다.')
    router.push('/login')
    return
  }

  try {
    const response = await axios.post(
      'http://127.0.0.1:8000/surveys/submit-survey/',
      surveyResponses.value,
      { headers: { Authorization: `Token ${userStore.token}` } }
    )
    surveyCompleted.value = true
  } catch (error) {
    console.error('설문 제출 실패:', error)
    alert('설문 제출 중 오류가 발생했습니다. 다시 시도해주세요.')
  }
}

const goToRecommendations = () => {
  router.push('/recommendation')
}

// 컴포넌트 마운트 시 초기화
onMounted(() => {
  if (!userStore.isLogin) {
    router.push('/login')
  }
})
</script>

<style scoped>
.survey-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.survey-header {
  text-align: center;
  margin-bottom: 2rem;
}

.survey-progress {
  margin-bottom: 2rem;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #4CAF50;
  transition: width 0.3s ease;
}

.question-container {
  margin-bottom: 2rem;
}

.options-container {
  display: grid;
  gap: 1rem;
  margin-top: 1rem;
}

.option-button {
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.option-button:hover {
  border-color: #4CAF50;
}

.option-button.selected {
  border-color: #4CAF50;
  background-color: #E8F5E9;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
}

.nav-button, .submit-button {
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 4px;
  background-color: #4CAF50;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.nav-button:disabled, .submit-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.survey-completion {
  text-align: center;
}

.recommendation-button {
  margin-top: 1rem;
  padding: 1rem 2rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.recommendation-button:hover {
  background-color: #45a049;
}
</style>