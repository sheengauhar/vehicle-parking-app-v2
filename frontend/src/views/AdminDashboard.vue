<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useParkingLotStore } from '@/stores/parkingLotStore'
import ParkingLotCard from '@/components/ParkingLotCard.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const lotStore = useParkingLotStore()

onMounted(() => {
  lotStore.fetchLots()
  document.body.classList.add("dashboard-bg")
})

onUnmounted(() => {
  document.body.classList.remove("dashboard-bg")
})
</script>

<template>
  <div class="main_container">
    <h1 class="dashboard_heading">Admin Dashboard</h1>

    <div class="lot_board">
      <h2 class="board_title">Current Parking Lots</h2>

      <div class="lot_grid">
        <ParkingLotCard
          v-for="lot in lotStore.lots"
          :key="lot.id"
          :lot="lot"
        />
      </div>

      <div class="button_row">
        <button class="action_btn" @click="router.push('/add-lot')">
          Add Parking Lot
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main_container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 10px;
}

.dashboard_heading {
  text-align: center;
  color: #191919;
  margin-bottom: 30px;
  font-size: 32px;
}

.lot_board {
  border: 2px solid #df0d0d;
  padding: 20px;
  border-radius: 12px;
  background-color: #b216c382;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.board_title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
  color: #000000;
}

.lot_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
}

.button_row {
  margin-top: 15px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.action_btn {
  background-color: #0d76a3;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.action_btn:hover {
  background-color: #0056b3;
}
</style>
