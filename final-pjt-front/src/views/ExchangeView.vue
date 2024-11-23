<template>
  <div class="exchange-view">
    <h1>환율 정보</h1>

    <!-- 기준 통화 -->
    <!-- <p><strong>기준 통화:</strong> 대한민국 1000원 (KRW) 대비 환율</p> -->
     <br>

    <!-- 전체 통화 환율 시각화 -->
    <div id="chart" class="exchange-chart"></div>

    <!-- 환율 계산기 -->
    <div class="calculator-section">
      <h2>환율 계산기</h2>
      <div class="calculator">
        <div class="input-group">
          <input 
            v-model.number="calculatorAmount" 
            type="number" 
            min="0"
            placeholder="변환 금액 입력"
          >
          <select v-model="fromCurrency">
            <option v-for="currency in availableCurrencies" 
                    :key="currency" 
                    :value="currency">
              {{ getCurrencyName(currency) }}
            </option>
          </select>
        </div>

        <button @click="swapCurrencies" class="swap-button">⇄</button>

        <div class="input-group">
          <input 
            v-model="calculatedAmount" 
            type="number" 
            readonly 
            :placeholder="calculationResult || '변환된 금액'"
          >
          <select v-model="toCurrency">
            <option v-for="currency in availableCurrencies" 
                    :key="currency" 
                    :value="currency">
              {{ getCurrencyName(currency) }}
            </option>
          </select>
        </div>

        <button 
          @click="calculateAmount" 
          :disabled="!isValidCalculation"
          class="calculate-button"
        >
          계산하기
        </button>
      </div>
    </div>
    <br>

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
import { fetchExchangeData, getExchangeData, calculateExchange } from "@/stores/exchange";
import * as echarts from "echarts";

// 상태 변수
const exchanges = ref([]);
const loading = ref(false);
const selectedBaseCurrency = ref("USD");
const calculatorAmount = ref(null);
const fromCurrency = ref('USD');
const toCurrency = ref('KRW');
const calculatedAmount = ref(null);
const calculationResult = ref('');

// 전체 통화 단위 목록
const availableCurrencies = computed(() =>
  exchanges.value.map((item) => item.cur_unit)
);

// 기준 통화: 대한민국 원 (KRW)
const krwRate = computed(() => {
  const krw = exchanges.value.find((item) => item.cur_unit === "KRW");
  return krw ? parseFloat(krw.deal_bas_r) : 1;
});

// 전체 통화 환율 데이터 (1000원 기준, 정규화 적용)
const allCurrencyData = computed(() => {
  if (!exchanges.value.length) return [];
  
  // KRW를 제외한 모든 통화의 환율 데이터 추출
  const currencyData = exchanges.value
    .filter(item => item.cur_unit !== 'KRW')
    .map(item => {
      let rate;
      if (item.cur_unit === 'JPY(100)') {
        // 엔화의 경우 100엔 단위로 제공되므로 조정
        rate = (1000 / parseFloat(item.deal_bas_r.replace(',', ''))) * 100;
      } else {
        rate = 1000 / parseFloat(item.deal_bas_r.replace(',', ''));
      }
      return {
        name: `${item.cur_unit} (${item.cur_nm})`,
        rate: rate,
        original: parseFloat(item.deal_bas_r.replace(',', ''))
      };
    });

  // 정규화를 위한 최대/최소값 계산
  const maxRate = Math.max(...currencyData.map(item => item.rate));
  const minRate = Math.min(...currencyData.map(item => item.rate));

  // 정규화 적용 (0~100 범위로 스케일링)
  return currencyData.map(item => ({
    ...item,
    normalizedRate: (((item.rate - minRate) / (maxRate - minRate)) * 100).toFixed(2)
  }));
});

// 기준 통화에 따른 환율 계산
const conversionRates = computed(() => {
  const baseCurrency = exchanges.value.find(
    (item) => item.cur_unit === selectedBaseCurrency.value
  );

  if (!baseCurrency || !baseCurrency.deal_bas_r) return [];

  const baseRate = parseFloat(baseCurrency.deal_bas_r.replace(',', ''));
  return exchanges.value
    .filter((item) => item.cur_unit !== selectedBaseCurrency.value)
    .map((item) => ({
      cur_unit: item.cur_unit,
      cur_nm: item.cur_nm,
      rate: (parseFloat(item.deal_bas_r.replace(',', '')) / baseRate).toFixed(4),
    }));
});

// 계산기 유효성 검사
const isValidCalculation = computed(() => {
  return calculatorAmount.value > 0 && 
         fromCurrency.value && 
         toCurrency.value && 
         fromCurrency.value !== toCurrency.value;
});

// 데이터 로드
const loadExchangeData = async () => {
  try {
    loading.value = true;
    const data = await getExchangeData();
    exchanges.value = data;
    renderChart();
  } catch (error) {
    console.error("환율 데이터를 가져오는 중 오류 발생:", error);
  } finally {
    loading.value = false;
  }
};

// ECharts 차트 렌더링
const renderChart = () => {
  const chart = echarts.init(document.getElementById("chart"));
  const data = allCurrencyData.value;

  const options = {
    title: {
      text: "1,000원 기준 각국 통화 환율",
      left: "center",
    },
    tooltip: {
      trigger: "item",
      formatter: function (params) {
        return `
          ${params.name}<br/>
          1,000원 = ${params.data.rate.toFixed(2)}<br/>
          (1 ${params.name.split(" ")[0]} = ${params.data.original}원)
        `;
      },
    },
    grid: {
      top: "20%", // 상단 여백
      bottom: "20%", // 하단 여백 제거
      left: "12%", // 왼쪽 여백
      right: "7%", // 오른쪽 여백
      containLabel: false, // 레이블 공간 제거
    },
    xAxis: {
      type: "category",
      data: data.map((item) => item.name.split(' ')[0]), // 약어만 출력
      axisLabel: {
        interval: 0,
        rotate: 45,
        fontSize: 10,
      },
      show: true, // X축 숨기기
    },
    yAxis: {
      type: "log", // 로그 스케일 적용
      logBase: 10, // 로그 베이스를 10으로 설정
      name: "LOG SCALE",
      axisLabel: {
        formatter: (value) => `${value.toFixed(2)}`, // 값을 보기 쉽게 표시
      },
    },
    series: [
      {
        data: data.map((item) => ({
          value: item.rate,
          rate: item.rate,
          original: item.original,
        })),
        type: "bar", // 막대 그래프로 시각화
        barWidth: "60%",
        itemStyle: {
          color: "#85725d", // 막대 색상
        },
        label: {
          show: false,
          position: "top",
          formatter: (params) => params.data.rate.toFixed(2),
          fontSize: 10,
        },
      },
    ],
  };

  chart.setOption(options);

  window.addEventListener("resize", () => {
    chart.resize();
  });
};

// 통화명 조회 함수
const getCurrencyName = (currencyUnit) => {
  const currency = exchanges.value.find(c => c.cur_unit === currencyUnit);
  return currency ? `${currencyUnit} (${currency.cur_nm})` : currencyUnit;
};

// 환율 계산 함수
const calculateAmount = async () => {
  if (!isValidCalculation.value) return;
  
  try {
    const result = await calculateExchange(
      calculatorAmount.value,
      fromCurrency.value,
      toCurrency.value
    );
    calculatedAmount.value = result.converted_amount;
    calculationResult.value = `${result.converted_amount} ${toCurrency.value}`;
  } catch (error) {
    console.error('환율 계산 실패:', error);
    calculationResult.value = '계산 실패';
  }
};

// 통화 스왑 함수
const swapCurrencies = () => {
  [fromCurrency.value, toCurrency.value] = 
    [toCurrency.value, fromCurrency.value];
  if (calculatorAmount.value) {
    calculateAmount();
  }
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

.calculator-section {
  margin-top: 1rem; /* 공간 줄이기 */
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.calculator {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.input-group {
  display: flex;
  gap: 0.5rem;
}

.input-group input {
  width: 150px;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.input-group select {
  min-width: 120px;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
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
  margin: 0; /* 기존 여백 제거 */
  padding: 0; /* 기존 패딩 제거 */
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

.swap-button {
  padding: 0.5rem 1rem;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.calculate-button {
  padding: 0.5rem 1rem;
  background-color: #85725d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.calculate-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>