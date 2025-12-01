<script setup>
import ParkingSpots from './ParkingSpots.vue'
import { useParkingLotStore } from '@/stores/parkingLotStore'
import { useRouter } from 'vue-router'


const props = defineProps(['lot'])
const lotStore = useParkingLotStore()
const router = useRouter()


function handleEdit() {
    router.push(`/admin/parking_lots/${props.lot.id}/edit`)
}

async function handleDelete() {
    if (!confirm("Are you sure you want to delete this lot?")) return
    await lotStore.deleteLot(props.lot.id)
}
</script>

<template>
  <div class="lot_card">
    <h3 class="lot_name">{{ props.lot.prime_location }}</h3>
    <h2 class="lot_address">{{ props.lot.address }}</h2>

    <p class="lot_status">
      Occupied: {{ props.lot.occupied_spots }} / {{ props.lot.max_spots }}
    </p>

    <div class="spots_grid">
      <ParkingSpots
        v-for="spot in props.lot.spots"
        :key="spot.id"
        :spot="spot"
      />
    </div>

    <div class="button_row">
      <button class="action_btn edit_btn" @click="handleEdit">Edit</button>
      <button class="action_btn delete_btn" @click="handleDelete">Delete</button>
    </div>
  </div>
</template>

<style scoped>
.lot_card {
  border: 2px solid #ddd;
  border-radius: 10px;
  padding: 15px;
  background-color: #0a0a0a;
  text-align: center;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}

.lot_name {
  font-size: 20px;
  margin-bottom: 8px;
  color: #f4f2f2;
}

.lot_address {
  font-size: 18px;
  color: #dedbdb;  
  margin-top: 5px;
  margin-bottom: 10px;
  text-align: center;
}

.lot_status {
  margin-bottom: 12px;
  color: #d2d0d0;
}

.spots_grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 5px;
  margin-bottom: 10px;
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

.edit_btn {
  background: linear-gradient(to right, #6a11cb, #2575fc);
  box-shadow: 0 4px 10px rgba(106, 17, 203, 0.4);
}

.edit_btn:hover {
  background: linear-gradient(to right, #5b0eaa, #1e60cc);
  transform: scale(1.05);
}

.delete_btn {
  background-color: #d63031;
  color: white;
  box-shadow: 0 2px 6px rgba(214, 48, 49, 0.3);
}

.delete_btn:hover {
  background-color: #c0392b;
  transform: scale(1.05);
}

.button_row {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 10px;
}
</style>


