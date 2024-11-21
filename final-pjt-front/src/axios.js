// src/axios.js
import axios from 'axios';

// 기본 URL을 .env 파일에서 가져옴
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'; // 기본값 설정

const instance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터
instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token'); // 토큰 가져오기
    if (token) {
      config.headers.Authorization = `Token ${token}`;
      console.log(token)
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 응답 인터셉터
instance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.error('인증 실패. 다시 로그인하세요.');
      // 토큰 만료 시 추가 동작 필요 시 여기에 작성
    }
    return Promise.reject(error);
  }
);

export default instance;
