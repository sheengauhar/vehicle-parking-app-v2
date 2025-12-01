<script setup>
import { ref, onMounted } from 'vue';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

import { useAuthStore } from "@/stores/authStore";

const authStore = useAuthStore();

const revenueChart = ref(null);
const spotChart = ref(null);

async function fetchRevenue() {
  const res = await fetch("http://127.0.0.1:5000/api/admin/summary/revenue", {
    headers: { "Authentication-Token": authStore.getAuthToken() }
  });
  if (!res.ok) throw new Error("Failed to fetch data");
  return res.json();
}

async function fetchSpotStatus() {
  const res = await fetch("http://127.0.0.1:5000/api/admin/summary/spot_status", {
    headers: { "Authentication-Token": authStore.getAuthToken() }
  });
  return res.json();
}

function renderRevenueChart(data) {
  new Chart(revenueChart.value, {
    type: "pie",
    data: {
      labels: data.labels,
      datasets: [{
        data: data.values
      }]
    }
  });
}

function renderSpotChart(data) {
  new Chart(spotChart.value, {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [
        { label: "Occupied", data: data.occupied },
        { label: "Available", data: data.available }
      ]
    }
  });
}

onMounted(async () => {
  renderRevenueChart(await fetchRevenue());
  renderSpotChart(await fetchSpotStatus());
});
</script>

<template>
  <div class="summary-container">
    <h1>Admin Summary</h1>

    <div class="chart-block">
        <h2>Revenue per Parking Lot (In INR)</h2>
        <div class="chart-wrapper">
            <canvas ref="revenueChart"></canvas>
        </div>
        </div>

        <div class="chart-block">
        <h2>Occupied vs Available Spots</h2>
        <canvas ref="spotChart"></canvas>
        </div>
        


  </div>
</template>

<style>
.summary-container {
  max-width: 900px;
  margin: 40px auto;
  text-align: center;
}

.chart-block {
  background: #fff;
  padding: 20px;
  margin-top: 30px;
  border-radius: 14px;
}

.chart-wrapper {
  width: 350px;      
  height: 350px;     
  margin: 0 auto;
}

canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
