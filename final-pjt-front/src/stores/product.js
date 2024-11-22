import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useProductStore = defineStore('product', () => {
  const API_URL = 'http://127.0.0.1:8000'; // Django API URL

  const products = ref([]); // 상품 목록 저장
  const selectedProduct = ref(null); // 선택된 상품 저장

  const saveProducts = function () {
    axios({
      method: 'get',
      url: `${API_URL}/bankings/deposit-fetch-data/`, // 데이터를 백엔드에서 저장
    })
      .then(() => {
        console.log('상품 데이터가 서버에 저장되었습니다.');
      })
      .catch((err) => {
        console.error('상품 데이터 저장 실패:', err);
      });
  };


  const fetchProducts = function () {
    axios({
      method: 'get',
      url: `${API_URL}/bankings/deposit-get-products/`, // 저장된 상품 목록 가져오기
    })
      .then((res) => {
        products.value = res.data; // 상품 데이터 스토어에 저장
      })
      .catch((err) => {
        console.error('상품 데이터 가져오기 실패:', err);
        products.value = []; // 오류 발생 시 빈 배열로 초기화
      });
  };

  // 특정 상품 조회
  const fetchProductById = function (id) {
    axios({
      method: 'get',
      url: `${API_URL}/bankings/deposit-get-products/${id}/`, // 특정 상품 조회 API
    })
      .then((res) => {
        selectedProduct.value = res.data; // 선택된 상품 데이터 저장
      })
      .catch((err) => {
        console.error(`상품 ID ${id} 가져오기 실패:`, err);
        selectedProduct.value = null; // 오류 발생 시 null로 초기화
      });
  };

  // **3. 스토어에서 데이터 조회**
  const getProducts = function () {
    return products.value; // 전체 상품 반환
  };

  const getSelectedProduct = function () {
    return selectedProduct.value; // 선택된 상품 반환
  };

  return {
    products,
    selectedProduct,
    saveProducts,
    fetchProducts,
    fetchProductById,
    getProducts,
    getSelectedProduct,
  };
});
