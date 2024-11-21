<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/accounts/user-fields/"; // Django API URL
const userFields = ref(null); // 사용자 정보 저장

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
        Authorization: `Token ${token}`, // 인증 토큰 설정
      },
    });
    const data = response.data;
    // 필요한 필드만 저장, 숫자 필드는 정수로 변환
    userFields.value = {
      id: data.id,
      username: data.username,
      email: data.email,
      name: data.name,
      age: data.age,
      money: data.money ? parseInt(data.money, 10) : null,
      salary: data.salary ? parseInt(data.salary, 10) : null,
      desire_amount_deposit: data.desire_amount_deposit ? parseInt(data.desire_amount_deposit, 10) : null,
      deposit_period: data.deposit_period,
      desire_amount_saving: data.desire_amount_saving ? parseInt(data.desire_amount_saving, 10) : null,
      saving_period: data.saving_period,
    };
    console.log("사용자 정보:", userFields.value); // 디버깅 로그
  } catch (error) {
    console.error("사용자 정보 가져오기 실패:", error.response?.data || error);
    userFields.value = null; // 실패 시 초기화
  }
};

onMounted(() => {
  fetchUserFields(); // 컴포넌트 마운트 시 사용자 정보 가져오기
});
</script>

<template>
  <div>
    <h1 v-if="userFields" class="page-title">{{ userFields.name }}님의 프로필 정보</h1>
    <p v-else class="loading">사용자 정보를 불러오는 중입니다...</p>

    <div v-if="userFields">
      <ul class="user-info">
        <h1>### profile picture 추가 ###</h1>
        <h1>### 숫자에 comma(,) 추가 ###</h1>

        <li><strong>유저 ID:</strong> {{ userFields.id }}</li>
        <li><strong>이메일:</strong> {{ userFields.email }}</li>
        <li><strong>나이:</strong> {{ userFields.age || "미입력" }}</li>
        <li><strong>자산:</strong> {{ userFields.money !== null ? `${userFields.money} 원` : "미입력" }}</li>
        <li><strong>연봉:</strong> {{ userFields.salary !== null ? `${userFields.salary} 원` : "미입력" }}</li>
        <li><strong>예금 희망 금액:</strong> {{ userFields.desire_amount_deposit !== null ? `${userFields.desire_amount_deposit} 원` : "미입력" }}</li>
        <li><strong>예금 희망 기간:</strong> {{ userFields.deposit_period ? `${userFields.deposit_period} 개월` : "미입력" }}</li>
        <li><strong>월 적금 희망 금액:</strong> {{ userFields.desire_amount_saving !== null ? `${userFields.desire_amount_saving} 원` : "미입력" }}</li>
        <li><strong>적금 희망 기간:</strong> {{ userFields.saving_period ? `${userFields.saving_period} 개월` : "미입력" }}</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.page-title {
  font-size: 28px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.loading {
  text-align: center;
  font-size: 18px;
  color: #666;
}

.user-info {
  margin: 0 auto;
  padding: 0;
  list-style: none;
  font-size: 18px;
  line-height: 2;
  max-width: 800px;
}

.user-info li {
  margin-bottom: 10px;
  color: #444;
}

.user-info strong {
  color: #333;
}
</style>
