import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useProductStore = defineStore('product', () => {
  const API_URL = 'http://127.0.0.1:8000'; // Django API URL

  const deposits = ref([]); // 예금 목록 저장
  const savings = ref([]); // 적금 목록 저장
  const selectedProduct = ref(null); // 선택된 상품 저장

  // 예금 데이터 저장 요청
  const saveDeposits = function () {
    const token = localStorage.getItem('token');
    axios({
      method: 'get',
      url: `${API_URL}/bankings/deposit-fetch-data/`,
      // headers: {
      //   Authorization: `Token ${token}`,
      // },
    })
      .then(() => {
        console.log('예금 데이터가 서버에 저장되었습니다.');
      })
      .catch((err) => {
        console.error('예금 데이터 저장 실패:', err.response?.data || err.message);
      });
  };

  // 적금 데이터 저장 요청
  const saveSavings = function () {
    const token = localStorage.getItem('token');
    axios({
      method: 'get',
      url: `${API_URL}/bankings/saving-fetch-data/`,
      // headers: {
      //   Authorization: `Token ${token}`,
      // },
    })
      .then(() => {
        console.log('적금 데이터가 서버에 저장되었습니다.');
      })
      .catch((err) => {
        console.error('적금 데이터 저장 실패:', err.response?.data || err.message);
      });
  };

  // 예금 데이터 가져오기
  const fetchDeposits = async function () {
    const token = localStorage.getItem('token');
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/bankings/deposit-get-products/`,
        // headers: {
        //   Authorization: `Token ${token}`,
        // },
      });
      deposits.value = response.data;
    } catch (err) {
      console.error('예금 데이터 가져오기 실패:', err.response?.data || err.message);
      deposits.value = []; // 오류 발생 시 초기화
    }
  };

  // 적금 데이터 가져오기
  const fetchSavings = async function () {
    const token = localStorage.getItem('token');
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/bankings/saving-get-products/`,
        // headers: {
        //   Authorization: `Token ${token}`,
        // },
      });
      savings.value = response.data;
    } catch (err) {
      console.error('적금 데이터 가져오기 실패:', err.response?.data || err.message);
      savings.value = []; // 오류 발생 시 초기화
    }
  };

  // 특정 상품 조회
  const fetchProductById = async function (id, type) {
    const token = localStorage.getItem('token');
    if (!id || !type) {
      console.error('유효하지 않은 상품 ID 또는 타입:', { id, type });
      selectedProduct.value = null;
      return;
    }

    const endpoint =
      type === 'deposit'
        ? `${API_URL}/bankings/deposit-get-products/${id}/`
        : `${API_URL}/bankings/saving-get-products/${id}/`;

    try {
      const response = await axios({
        method: 'get',
        url: endpoint,
        // headers: {
        //   Authorization: `Token ${token}`,
        // },
      });
      selectedProduct.value = response.data;
    } catch (err) {
      console.error(`상품 ID ${id} 가져오기 실패:`, err.response?.data || err.message);
      selectedProduct.value = null;
    }
  };

  return {
    deposits,
    savings,
    selectedProduct,
    saveDeposits,
    saveSavings,
    fetchDeposits,
    fetchSavings,
    fetchProductById,
  };
});
