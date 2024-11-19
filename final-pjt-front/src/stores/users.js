import { ref, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStore = defineStore('users', () => {
  const API_URL = 'http://127.0.0.1:8000';
  const router = useRouter();
  const token = ref(null);
  const isLogin = computed(() => token.value !== null);
  const userInfo = ref({});
  const userContractDeposits = ref([]);
  const userContractSavings = ref([]);

  // 사용자 정보가 변경될 때 계약 정보 업데이트
  watch(userInfo, () => {
    userContractDeposits.value = userInfo.value?.contract_deposit || [];
    userContractSavings.value = userInfo.value?.contract_saving || [];
  });

  // 사용자 정보 가져오기 (비동기 함수)
  const getUserInfo = async (username) => {
    if (!token.value) {
      console.error('토큰이 없습니다. 로그인이 필요합니다.');
      return;
    }

    try {
      const response = await axios.get(`${API_URL}/users/${username}/info/`, {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      userInfo.value = response.data;
      console.log('getUserInfo: 사용자 정보:', response.data);
    } catch (error) {
      console.error('getUserInfo 오류:', error);
      userInfo.value = {}; // 사용자 정보 초기화
    }
  };

  // 회원가입 함수
  const signUp = async (payload) => {
    const { username, name, email, password1, password2 } = payload;

    try {
      await axios.post(`${API_URL}/accounts/signup/`, {
        username,
        name,
        email,
        password1,
        password2,
      });
      await logIn({ username, password: password1 });
    } catch (error) {
      console.error('회원가입 오류:', error);
    }
  };

  // 로그인 함수
  const logIn = async (payload) => {
    const { username, password } = payload;

    try {
      const response = await axios.post(`${API_URL}/accounts/login/`, {
        username,
        password,
      });
      token.value = response.data.key;
      await getUserInfo(username);
      router.push({ name: 'home' });
      return true;
    } catch (error) {
      console.clear();
      console.error('로그인 오류:', error);
      return false;
    }
  };

  // 로그아웃 함수
  const logOut = async () => {
    try {
      await axios.post(`${API_URL}/accounts/logout/`, {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      token.value = null;
      userInfo.value = {};
      router.push({ name: 'home' });
    } catch (error) {
      console.error('로그아웃 오류:', error);
    }
  };

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
}, { persist: true });
