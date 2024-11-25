import { ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000"; // Django API URL

const axiosInstance = axios.create({
  baseURL: API_URL,
  // headers: {
  //   Authorization: `Token ${localStorage.getItem("token")}`,
  // },
});

export const useProductStore = defineStore("product", () => {
  const deposits = ref([]);
  const savings = ref([]);
  const selectedProduct = ref(null);
  const errorMessage = ref("");

  const handleError = (err) => {
    const message = err.response?.data || err.message || "알 수 없는 오류";
    errorMessage.value = message;
    console.error(message);
  };

  const updateState = (stateRef, data) => {
    stateRef.value = data;
  };

  const saveDeposits = async function () {
    try {
      await axiosInstance.get("/bankings/deposit-fetch-data/");
      console.log("예금 데이터가 서버에 저장되었습니다.");
    } catch (err) {
      handleError(err);
    }
  };

  const saveSavings = async function () {
    try {
      await axiosInstance.get("/bankings/saving-fetch-data/");
      console.log("적금 데이터가 서버에 저장되었습니다.");
    } catch (err) {
      handleError(err);
    }
  };

  const fetchDeposits = async function () {
    try {
      const response = await axiosInstance.get("/bankings/deposit-get-products/");
      updateState(deposits, response.data);
    } catch (err) {
      handleError(err);
      updateState(deposits, []);
    }
  };

  const fetchSavings = async function () {
    try {
      const response = await axiosInstance.get("/bankings/saving-get-products/");
      updateState(savings, response.data);
    } catch (err) {
      handleError(err);
      updateState(savings, []);
    }
  };

  const fetchProductById = async function (id, type) {
    if (!id || !type) {
      console.error("유효하지 않은 상품 ID 또는 타입:", { id, type });
      selectedProduct.value = null;
      return;
    }

    const endpoint =
      type === "deposit"
        ? `/bankings/deposit-get-products/${id}/`
        : `/bankings/saving-get-products/${id}/`;

    try {
      const response = await axiosInstance.get(endpoint);
      updateState(selectedProduct, response.data);
    } catch (err) {
      handleError(err);
      updateState(selectedProduct, null);
    }
  };

  return {
    deposits,
    savings,
    selectedProduct,
    errorMessage,
    saveDeposits,
    saveSavings,
    fetchDeposits,
    fetchSavings,
    fetchProductById,
  };
});