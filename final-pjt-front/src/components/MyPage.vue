<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/accounts/user_info/";
const userFields = ref(null);

// 금액 포맷팅 함수
const formatCurrency = (value) => {
  if (value === null || value === undefined) return '미입력';
  return new Intl.NumberFormat('ko-KR', { 
    style: 'currency', 
    currency: 'KRW',
    maximumFractionDigits: 0 
  }).format(value);
};

// 기간 포맷팅 함수
const formatPeriod = (months) => {
  if (!months) return '미입력';
  return `${months}개월`;
};

// 사용자 정보 가져오기
const fetchUserFields = async () => {
  try {
    const token = localStorage.getItem("token");
    if (!token) {
      console.error("로그인 토큰이 없습니다.");
      return;
    }

    const response = await axios.get(API_URL, {
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    
    const data = response.data;
    // Django 모델의 Decimal 필드를 적절히 처리
    userFields.value = {
      id: data.id,
      username: data.username,
      email: data.email,
      name: data.name,
      age: data.age,
      money: data.money ? parseFloat(data.money) : null,
      salary: data.salary ? parseFloat(data.salary) : null,
      desire_amount_deposit: data.desire_amount_deposit ? parseFloat(data.desire_amount_deposit) : null,
      deposit_period: data.deposit_period,
      desire_amount_saving: data.desire_amount_saving ? parseFloat(data.desire_amount_saving) : null,
      saving_period: data.saving_period,
    };
  } catch (error) {
    console.error("사용자 정보 가져오기 실패:", error.response?.data || error);
    userFields.value = null;
  }
};

onMounted(() => {
  fetchUserFields();
});
</script>

<template>
  <div class="profile-container">
    <!-- 프로필 헤더 -->
    <div class="profile-header" v-if="userFields">
      <div class="profile-image">
        <!-- <img src="@/assets/profile-placeholder.png" alt="프로필 이미지" /> -->
      </div>
      <h1 class="profile-title">{{ userFields.name || userFields.username }}님의 프로필</h1>
    </div>

    <!-- 사용자 정보 -->
    <div v-if="userFields" class="info-sections">
      <!-- 기본 정보 -->
      <section class="info-section">
        <h2>기본 정보</h2>
        <div class="info-content">
          <div class="info-item">
            <span class="label">아이디</span>
            <span class="value">{{ userFields.username }}</span>
          </div>
          <div class="info-item">
            <span class="label">이메일</span>
            <span class="value">{{ userFields.email }}</span>
          </div>
          <div class="info-item">
            <span class="label">닉네임</span>
            <span class="value">{{ userFields.name || '미입력' }}</span>
          </div>
          <div class="info-item">
            <span class="label">나이</span>
            <span class="value">{{ userFields.age ? `${userFields.age}세` : '미입력' }}</span>
          </div>
        </div>
      </section>

      <!-- 자산 정보 -->
      <section class="info-section">
        <h2>자산 정보</h2>
        <div class="info-content">
          <div class="info-item">
            <span class="label">현재 자산</span>
            <span class="value">{{ formatCurrency(userFields.money) }}</span>
          </div>
          <div class="info-item">
            <span class="label">연봉</span>
            <span class="value">{{ formatCurrency(userFields.salary) }}</span>
          </div>
        </div>
      </section>

      <!-- 금융 상품 희망 정보 -->
      <section class="info-section">
        <h2>예금 희망 정보</h2>
        <div class="info-content">
          <div class="info-item">
            <span class="label">희망 금액</span>
            <span class="value">{{ formatCurrency(userFields.desire_amount_deposit) }}</span>
          </div>
          <div class="info-item">
            <span class="label">희망 기간</span>
            <span class="value">{{ formatPeriod(userFields.deposit_period) }}</span>
          </div>
        </div>
      </section>

      <section class="info-section">
        <h2>적금 희망 정보</h2>
        <div class="info-content">
          <div class="info-item">
            <span class="label">월 희망 금액</span>
            <span class="value">{{ formatCurrency(userFields.desire_amount_saving) }}</span>
          </div>
          <div class="info-item">
            <span class="label">희망 기간</span>
            <span class="value">{{ formatPeriod(userFields.saving_period) }}</span>
          </div>
        </div>
      </section>
    </div>

    <!-- 로딩 상태 -->
    <div v-else class="loading">
      사용자 정보를 불러오는 중입니다...
    </div>
  </div>
</template>

<style scoped>
.profile-container {
  max-width: 800px;
  /* margin: 0 auto; */
  padding: 20px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.profile-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  background-color: #f5f5f5;
}

.profile-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.info-sections {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.info-section h2 {
  font-size: 18px;
  color: #333;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.info-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.label {
  font-size: 14px;
  color: #666;
}

.value {
  font-size: 16px;
  color: #333;
  font-weight: 500;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

@media (max-width: 600px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
  }

  .info-content {
    grid-template-columns: 1fr;
  }
}
</style>