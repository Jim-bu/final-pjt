<template>
  <div class="exchange-view">
    <h1>환율 정보</h1>

    <!-- 기준 통화 -->
    <p><strong>기준 통화:</strong> 대한민국 원 (KRW)</p>

    <!-- 미국 달러와 일본 엔화 시각화 -->
    <div id="chart" class="exchange-chart"></div>

    <!-- 사용자 입력: 기준 통화 선택 -->
    <div class="controls">
      <label for="base-currency">비교할 통화 선택:</label>
      <select v-model="selectedBaseCurrency">
        <option v-for="currency in availableCurrencies" :key="currency" :value="currency">
          {{ currency }}
        </option>
      </select>
    </div>

    <!-- 기준 통화에 따른 환율 비교 -->
    <div v-if="selectedBaseCurrency" class="conversion-table">
      <h2>{{ selectedBaseCurrency }} 환율 비교</h2>
      <table>
        <thead>
          <tr>
            <th>통화 단위</th>
            <th>통화명</th>
            <th>비율 (KRW 기준)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rate in conversionRates" :key="rate.cur_unit">
            <td>{{ rate.cur_unit }}</td>
            <td>{{ rate.cur_nm }}</td>
            <td>{{ rate.rate }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 전체 환율 데이터 테이블 -->
    <div class="all-rates">
      <h2>전체 환율 정보</h2>
      <table>
        <thead>
          <tr>
            <th>통화 단위</th>
            <th>통화명</th>
            <th>매매기준율</th>
            <th>장부가격</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="exchange in exchanges" :key="exchange.cur_unit">
            <td>{{ exchange.cur_unit }}</td>
            <td>{{ exchange.cur_nm }}</td>
            <td>{{ exchange.deal_bas_r }}</td>
            <td>{{ exchange.bkpr }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { fetchExchangeData, getExchangeData } from "@/stores/exchange";
import * as echarts from "echarts";

// 상태 변수
const exchanges = ref([]);
const loading = ref(false);
const selectedBaseCurrency = ref("USD"); // 초기 비교 통화: USD (사용자 선택)

// 전체 통화 단위 목록
const availableCurrencies = computed(() =>
  exchanges.value.map((item) => item.cur_unit)
);

// 기준 통화: 대한민국 원 (KRW)
const krwRate = computed(() => {
  const krw = exchanges.value.find((item) => item.cur_unit === "KRW");
  return krw ? parseFloat(krw.deal_bas_r) : 1;
});

// 미국 달러와 일본 엔화 데이터
const usdJpyData = computed(() => {
  const usd = exchanges.value.find((item) => item.cur_unit === "USD");
  const jpy = exchanges.value.find((item) => item.cur_unit === "JPY");

  return [
    { name: "미국 달러 (USD)", rate: usd ? parseFloat(usd.deal_bas_r) : 0 },
    { name: "일본 엔화 (JPY)", rate: jpy ? parseFloat(jpy.deal_bas_r) : 0 },
  ];
});

// 기준 통화에 따른 환율 계산
const conversionRates = computed(() => {
  const baseCurrency = exchanges.value.find(
    (item) => item.cur_unit === selectedBaseCurrency.value
  );

  if (!baseCurrency || !baseCurrency.deal_bas_r) return [];

  const baseRate = parseFloat(baseCurrency.deal_bas_r);
  return exchanges.value
    .filter((item) => item.cur_unit !== selectedBaseCurrency.value)
    .map((item) => ({
      cur_unit: item.cur_unit,
      cur_nm: item.cur_nm,
      rate: (parseFloat(item.deal_bas_r) / baseRate).toFixed(4), // 기준 통화 대비 비율
    }));
});

// 데이터 로드
const loadExchangeData = async () => {
  try {
    loading.value = true;
    const data = await getExchangeData();
    exchanges.value = data;
    renderChart(); // 데이터 로드 후 차트 렌더링
  } catch (error) {
    console.error("환율 데이터를 가져오는 중 오류 발생:", error);
  } finally {
    loading.value = false;
  }
};

// ECharts 차트 렌더링
const renderChart = () => {
  const chart = echarts.init(document.getElementById("chart"));
  const data = usdJpyData.value;

  const options = {
    title: {
      text: "KRW 기준 주요 통화 환율",
      left: "center",
    },
    tooltip: {
      trigger: "item",
    },
    xAxis: {
      type: "category",
      data: data.map((item) => item.name),
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        data: data.map((item) => item.rate),
        type: "bar",
        label: {
          show: true,
          position: "top",
        },
      },
    ],
  };

  chart.setOption(options);
};

// Vue 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  loadExchangeData();
});
</script>

<style scoped>
.exchange-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: "Arial", sans-serif;
}

.controls {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.controls select {
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.conversion-table,
.all-rates {
  margin-top: 30px;
}

.exchange-chart {
  width: 100%;
  height: 400px;
  margin: 20px 0;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

th {
  background-color: #f4f4f4;
  font-weight: bold;
}

label {
  font-size: 16px;
  font-weight: bold;
}

h2 {
  margin-top: 20px;
  font-size: 18px;
}
</style>
