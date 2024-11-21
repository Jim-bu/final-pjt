<template>
  <div>
    <canvas id="bar-chart"></canvas>
  </div>
</template>

<script setup>
import { onMounted, watch, ref } from "vue";
import Chart from "chart.js/auto";

const props = defineProps({
  chartData: {
    type: Array,
    required: true,
  },
});

const chartInstance = ref(null);

const renderChart = () => {
  const ctx = document.getElementById("bar-chart").getContext("2d");

  if (chartInstance.value) {
    chartInstance.value.destroy(); // 기존 차트 제거
  }

  const datasets = props.chartData.map((data, index) => ({
    label: data.name,
    data: data.returns,
    backgroundColor: `rgba(${(index + 1) * 50}, 100, 150, 0.7)`,
  }));

  chartInstance.value = new Chart(ctx, {
    type: "bar",
    data: {
      labels: props.chartData[0]?.labels || [],
      datasets,
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true,
        },
      },
    },
  });
};

onMounted(renderChart);
watch(() => props.chartData, renderChart);
</script>

<style scoped>
canvas {
  max-width: 100%;
  height: auto;
}
</style>
