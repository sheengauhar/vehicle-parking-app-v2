<script setup>
import { ref, onMounted } from "vue";
import { Chart, registerables } from "chart.js";
import { useAuthStore } from "@/stores/authStore";
Chart.register(...registerables);

const auth = useAuthStore();
const usageChart = ref(null);

async function fetchUsage() {
  const res = await fetch("http://127.0.0.1:5000/api/user/summary/usage_per_lot", {
    headers: { "Authentication-Token": auth.getAuthToken() }
  });
  return res.json();
}

function renderUsageChart(data) {
  let lots = data.map(d => d.lot);

  let allSpots = [...new Set(
    data.flatMap(d => d.spots.map(s => s.spot))
  )];

  let datasets = allSpots.map(spot => ({
    label: spot,
    data: data.map(lot =>
      lot.spots.find(s => s.spot === spot)?.count || 0
    ),
    backgroundColor: `hsl(${Math.random()*360},70%,60%)`
  }));

  new Chart(usageChart.value, {
    type: "bar",
    data: {
      labels: lots,
      datasets
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Spot Usage per Parking Lot"
        }
      }
    }
  });
}

onMounted(async () => {
  renderUsageChart(await fetchUsage());
});
</script>

<template>
  <div class="summary-container">
    <h1>User Summary</h1>
    <canvas ref="usageChart"></canvas>
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
</style>

