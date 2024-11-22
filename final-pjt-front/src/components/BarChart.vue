<template>
  <div class="chart-container">
    <canvas ref="barChartCanvas"></canvas>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import Chart from "chart.js/auto";

const props = defineProps({
  labels: {
    type: Array,
    required: true,
  },
  datasets: {
    type: Array,
    required: true,
  },
});

const barChartCanvas = ref(null);
let chartInstance = null;

const renderChart = () => {
  if (chartInstance) {
    chartInstance.destroy();
  }

  if (!props.labels.length || !props.datasets.length) {
    console.warn("차트 데이터가 부족합니다.");
    return;
  }

  chartInstance = new Chart(barChartCanvas.value.getContext("2d"), {
    type: "bar",
    data: {
      labels: props.labels,
      datasets: props.datasets.map((dataset, index) => ({
        label: dataset.label,
        data: dataset.data,
        backgroundColor: `rgba(${(index + 1) * 60}, 99, 132, 0.7)`,
      })),
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          position: "top",
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: (value) => `${value.toLocaleString()}원`,
          },
        },
      },
    },
  });
};

onMounted(renderChart);
watch([() => props.labels, () => props.datasets], renderChart);
</script>

<style scoped>
.chart-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f8f3eb;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
