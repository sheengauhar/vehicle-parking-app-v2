<script setup>
import { ref } from "vue"
import { useAuthStore } from "@/stores/authStore"

const props = defineProps(["spot"])
const authStore = useAuthStore()

const showModal = ref(false)
const userInfo = ref(null)
const loading = ref(false)
const error = ref(null)

// Fetch user info for this spot
async function viewUserDetails() {
  if (props.spot.status !== "occupied") return

  try {
    loading.value = true
    error.value = null

    const res = await fetch(`http://127.0.0.1:5000/api/spot/${props.spot.id}/user_info`, {
      method: "GET",
      headers: {
        "Authentication-Token": authStore.getAuthToken()
      },
      credentials: "include"
    })

    const data = await res.json()
    if (!res.ok) throw new Error(data.message)

    userInfo.value = data
    showModal.value = true
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

function closeModal() {
  showModal.value = false
}
</script>

<template>
  <!-- Spot Box -->
  <div
    class="spot"
    :class="spot.status === 'occupied' ? 'occupied' : 'available'"
    @click="viewUserDetails"
  >
    {{ spot.spot_number }}
  </div>

  <!-- User Info Modal -->
  <div v-if="showModal" class="modal-overlay">
    <div class="modal-card">
      <h2 class="modal-title">Reservation Details — Spot {{ props.spot.spot_number }}</h2>

      <p v-if="loading">Loading...</p>
      <p v-if="error" class="error">{{ error }}</p>

      <div v-if="userInfo" class="modal-details">
        <p><strong>Name:</strong> {{ userInfo.user.full_name }}</p>
        <p><strong>Email:</strong> {{ userInfo.user.email }}</p>
        <p><strong>Phone:</strong> {{ userInfo.user.phone_number }}</p>
        <p><strong>Vehicle:</strong> {{ userInfo.reservation.vehicle_number }}</p>
        <p><strong>Parking Time:</strong> {{ new Date(userInfo.reservation.parking_timestamp).toLocaleString() }}</p>
      </div>

      <div class="modal-actions">
        <button class="close-btn" @click="closeModal">Close</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.spot {
  width: 30px;
  height: 30px;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  border-radius: 4px;
  color: white;
  font-weight: bold;
  font-size: 14px;
  cursor: pointer;
}

.available {
  background: linear-gradient(135deg, #00c9a7, #92fe9d);
  color: black;
}

.occupied {
  background: linear-gradient(135deg, #ff416c, #ff4b2b);
  color: white;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.55);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-card {
  background: white;
  padding: 30px 40px;
  border-radius: 12px;
  width: 480px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.25);
  animation: fadeIn 0.25s ease-out;
}

.modal-title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
  color: #3b0a57;
  font-weight: 600;
}

.modal-details p {
  font-size: 16px;
  margin: 10px 0;
}

.modal-actions {
  margin-top: 25px;
  display: flex;
  justify-content: center;
}

.close-btn {
  background: #ff4757;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.2s;
}
.close-btn:hover {
  background: #e84118;
}

.error {
  color: red;
  text-align: center;
  margin-top: 10px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>




