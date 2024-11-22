import { ref, computed, watch, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStore = defineStore(
  'users',
  () => {
    const API_URL = 'http://127.0.0.1:8000';
    const router = useRouter();
    const token = ref(localStorage.getItem('token') || null); // 토큰을 localStorage에서 복원
    const userInfo = ref(JSON.parse(localStorage.getItem('userInfo')) || null);
    const userContractDeposits = ref();
    const userContractSavings = ref();

    // 로그인 여부 계산
    const isLogin = computed(() => token.value !== null);

    // 계약 정보 반응형 업데이트
    watch(userInfo, () => {
      userContractDeposits.value = userInfo.value?.contract_deposit;
      userContractSavings.value = userInfo.value?.contract_saving;
    });

    // 사용자 정보 가져오기
    const getUserInfo = function () {
      if (!token.value) return; // 토큰 없으면 요청하지 않음
      axios({
        method: 'get',
        url: `${API_URL}/accounts/user_info`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((res) => {
          userInfo.value = res.data;
          localStorage.setItem('userInfo', JSON.stringify(res.data)); 
        })
        .catch((err) => {
          console.error('사용자 정보 가져오기 실패:', err);
          logOut(); 
        });
    };

    // 회원가입
    const signUp = function (payload) {
      const { username, name, email, password1, password2 } = payload;
      axios({
        method: 'post',
        url: `${API_URL}/accounts/signup/`,
        data: {
          username,
          name,
          email,
          password1,
          password2,
        },
      })
        .then(() => {
          logIn({ username, password: password1 }); // 회원가입 후 자동 로그인
        })
        .catch((err) => {
          console.error('회원가입 실패:', err);
        });
    };

    // 로그인
    const logIn = function (payload) {
      const { username, password } = payload;
      console.log('로그인 요청 데이터:', { username, password });
    
      axios({
        method: 'post',
        url: `${API_URL}/accounts/login/`,
        data: { username, password },
      })
        .then((res) => {
          console.log('로그인 응답:', res.data);
          token.value = res.data.key;
          localStorage.setItem('token', res.data.key); // 토큰 저장
          getUserInfo(); // 사용자 정보 가져오기
          router.push({ name: 'Main' });
        })
        .catch((err) => {
          console.error('로그인 요청 실패:', err.response || err);
        });
    };
    

    // 로그아웃
    const logOut = function () {
      axios({
        method: 'post',
        url: `${API_URL}/accounts/logout/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then(() => {
          token.value = null;
          userInfo.value = null;
          localStorage.removeItem('token');
          localStorage.removeItem('userInfo');
          router.push({ name: 'Main' });
        })
        .catch((err) => {
          console.error('로그아웃 실패:', err);
        });
    };

    onMounted(() => {
      if (token.value && !userInfo.value) {
        getUserInfo();
      }
    });

    return {
      API_URL,
      token,
      isLogin,
      userInfo,
      userContractDeposits,
      userContractSavings,
      getUserInfo,
      signUp,
      logIn,
      logOut,
    };
  },
  { persist: true }
);
