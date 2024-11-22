<template>
  <div class="exchange-container">
    <h1>환율 정보</h1>

    <!-- 환율 차트 -->
    <div class="exchange-chart">
      <canvas id="exchangeChart"></canvas>
    </div>

    <!-- 환율 데이터 테이블 -->
    <table class="exchange-table">
      <thead>
        <tr>
          <th>통화</th>
          <th>매매기준율</th>
          <th>변동률</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="rate in exchangeRates" :key="rate.currency">
          <td>{{ rate.currency }}</td>
          <td>{{ rate.rate }}</td>
          <td :class="{ up: rate.change > 0, down: rate.change < 0 }">
            {{ rate.change > 0 ? "▲" : "▼" }} {{ rate.change }}%
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Chart } from 'chart.js';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/'; // API URL
const token = localStorage.getItem('token'); // 토큰 가져오기
const exchangeRates = ref([]); // 환율 데이터 저장

const fetchExchangeRates = function () {
  axios({
    method: 'get',
    url: `${API_URL}/exchange-rates/`,
    headers: {
      Authorization: `Token ${token}`,
    },
  })
    .then((res) => {
      exchangeRates.value = res.data;
      drawChart(res.data); // 차트 그리기
    })
    .catch((err) => {
      console.error('환율 데이터 가져오기 실패:', err.response?.data || err.message);
    });
};

const drawChart = (data) => {
  const ctx = document.getElementById('exchangeChart').getContext('2d');
  const currencies = data.map((rate) => rate.currency);
  const rates = data.map((rate) => rate.rate);

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: currencies,
      datasets: [
        {
          label: '환율',
          data: rates,
          borderColor: '#3366cc',
          borderWidth: 2,
          fill: false,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
};

onMounted(() => {
  fetchExchangeRates();
});
</script>

<style scoped>
.exchange-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.exchange-chart {
  margin-bottom: 20px;
}

.exchange-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.exchange-table th,
.exchange-table td {
  padding: 10px;
  border: 1px solid #ddd;
}

.exchange-table th {
  background-color: #f4f4f4;
}

.exchange-table .up {
  color: green;
}

.exchange-table .down {
  color: red;
}
</style>
