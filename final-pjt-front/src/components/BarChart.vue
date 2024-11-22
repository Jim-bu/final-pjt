<template>
  <div>
    <div v-if="hasData" class="chart-container">
      <canvas id="bar-chart"></canvas>
    </div>
    <p v-else class="no-data-message">유효한 데이터가 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import Chart from "chart.js/auto";
import colors from "vuetify/lib/util/colors";

// Props 정의
const props = defineProps({
  labels: {
    type: Array,
    default: () => [],
  },
  intrRate: {
    type: Array,
    default: () => [],
  },
  intrRate2: {
    type: Array,
    default: () => [],
  },
});

// 차트 인스턴스 및 데이터 유효성 검사
const chartInstance = ref(null);
const hasData = computed(
  () =>
    props.labels.length > 0 &&
    (props.intrRate.some((value) => value.length > 0) || props.intrRate2.some((value) => value.length > 0))
);

// 차트 데이터 구성
const chartData = computed(() => {
  if (!hasData.value) {
    return null;
  }

  const datasets = [];
  if (props.intrRate.length) {
    datasets.push({
      label: "저축 금리",
      data: props.intrRate,
      backgroundColor: "#1089FF",
      stack: "Stack 0",
    });
  }
  if (props.intrRate2.length) {
    datasets.push({
      label: "최고 우대 금리",
      data: props.intrRate2,
      backgroundColor: colors.red.accent2,
      stack: "Stack 1",
    });
  }

  return {
    labels: props.labels,
    datasets,
  };
});

// 차트 렌더링 함수
const renderChart = () => {
  const ctx = document.getElementById("bar-chart")?.getContext("2d");
  if (!ctx || !hasData.value) {
    console.warn("유효한 데이터가 없습니다.");
    return;
  }

  if (chartInstance.value) {
    chartInstance.value.destroy(); // 기존 차트 제거
  }

  chartInstance.value = new Chart(ctx, {
    type: "bar",
    data: chartData.value,
    options: {
      plugins: {
        title: {
          display: true,
          text: "선택한 상품 비교 차트",
        },
      },
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: (value) => `${value}%`,
          },
        },
        x: {
          ticks: {
            font: {
              size: 12,
            },
          },
        },
      },
    },
  });
};

// Props 변경 감지 및 렌더링
watch([props.labels, props.intrRate, props.intrRate2], renderChart, { deep: true });

// 초기 렌더링
onMounted(() => {
  if (hasData.value) renderChart();
});
</script>

<style scoped>
.chart-container {
  max-width: 100%;
  height: 400px;
  margin: 20px auto;
  padding: 16px;
  background: #fdf6e3;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.no-data-message {
  text-align: center;
  color: #999;
  font-size: 16px;
  margin-top: 20px;
}
</style>
