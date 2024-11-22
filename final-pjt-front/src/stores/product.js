import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useProductStore = defineStore('product', () => {
  const API_URL = 'http://127.0.0.1:8000'; // Django API URL
  const products = ref([]); // 상품 목록 저장

  const fetchProducts = function () {
    axios({
      method: 'get',
      url: `${API_URL}/bankings/deposit-products/`,
    })
      .then((res) => {
        products.value = res.data; // 상품 데이터 저장
      })
      .catch((err) => {
        console.error('상품 데이터 가져오기 실패:', err);
        products.value = []; // 오류 발생 시 빈 배열로 초기화
      });
  };

  return { products, fetchProducts };
});
