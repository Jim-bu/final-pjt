// src/axios.js
import axios from 'axios';

// 기본 URL 설정
const API_URL = 'http://127.0.0.1:8000'; // 백엔드 서버 URL

const instance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터
instance.interceptors.request.use(
  (config) => {
    // 인증 토큰이 있으면 헤더에 추가
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터
instance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // 에러 처리 로직 추가
    if (error.response?.status === 401) {
      console.error('인증 실패. 다시 로그인하세요.');
    }
    return Promise.reject(error);
  }
);

export default instance;
