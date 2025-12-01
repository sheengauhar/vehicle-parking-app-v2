<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useParkingLotStore } from '@/stores/parkingLotStore'
import { useMessageStore } from '@/stores/counter'

const route = useRoute()
const router = useRouter()
const lotStore = useParkingLotStore()
const message_store = useMessageStore()

const lotId = route.params.id


const prime_location = ref('')
const address = ref('')
const pincode = ref('')
const max_spots = ref(null)
const price = ref(null)

const loading = ref(false)
const error = ref(null)


async function loadLot() {
  loading.value = true
  error.value = null

  try {
    await lotStore.fetchLot(lotId)     
    const l = lotStore.selectedLot 
    if (!l) {
      error.value = 'Parking lot not found'
      return
    }
    prime_location.value = l.prime_location
    address.value = l.address
    pincode.value = l.pincode
    max_spots.value = l.max_spots
    price.value = l.price
  } catch (err) {
    error.value = err.message || 'Failed to load lot'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadLot()
})

function validate() {
  if (!prime_location.value || !address.value || !pincode.value || max_spots.value == null || price.value == null) {
    error.value = 'All fields are required.'
    return false
  }
  if (String(pincode.value).length !== 6) {
    error.value = 'Pincode must be 6 digits.'
    return false
  }
  if (Number(max_spots.value) < 0) {
    error.value = 'Max spots must be non-negative.'
    return false
  }
  return true
}

async function submitForm() {
  if (!validate()) return

  loading.value = true
  error.value = null
  try {
    const payload = {
      prime_location: prime_location.value,
      address: address.value,
      pincode: pincode.value,
      max_spots: Number(max_spots.value),
      price: Number(price.value)
    }

    await lotStore.updateLot(lotId, payload)

    message_store.showMessage("Parking lot updated successfully!", "success") // FIXED
    router.push('/admin/dashboard')
  } catch (err) {

    error.value = err.message || 'Update failed'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  document.body.classList.add("editlot-bg")
}) 

onUnmounted(() => {
  document.body.classList.remove("editlot-bg")
})

</script>

<template>
  <div class="edit-wrapper">
    <div class="edit-card">
      <h2 class="edit-title">Edit Parking Lot</h2>

      <div v-if="loading" class="loading">Loading...</div>
      <div v-if="error" class="error-box">{{ error }}</div>

      <form @submit.prevent="submitForm" v-if="!loading">
        
        <label>Prime Location:</label>
        <input v-model="prime_location" type="text"/>

        <label>Address:</label>
        <input v-model="address" type="text"/>

        <label>Pincode:</label>
        <input v-model="pincode" type="text"/>

        <label>Maximum Spots:</label>
        <input v-model.number="max_spots" type="number" min="1"/>

        <label>Price per Hour (₹):</label>
        <input v-model.number="price" type="number" min="0" step="0.01"/>

        <button class="btn-update" type="submit">Update Lot</button>

        <a class="back-link" @click.prevent="router.push('/admin/dashboard')">
          ⟵ Back to Dashboard
        </a>
      </form>
    </div>
  </div>
</template>

<style scoped>
.edit-wrapper {
  display: flex;
  justify-content: center;
  padding-top: 50px;
}

.edit-card {
  width: 480px;
  background: #111;   
  padding: 45px;
  border-radius: 14px;
  border: 2px solid #333;
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}

.edit-title {
  text-align: center;
  color: #22d3ee;     
  font-size: 28px;
  margin-bottom: 25px;
}

label {
  color: #ddd;
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 4px;
  display: block;
}

input {
  width: 95%;
  padding: 10px;
  margin-bottom: 18px;
  border-radius: 8px;
  border: 1px solid #444;
  background: #1e1e1e;
  color: white;
  font-size: 15px;
}

input:focus {
  outline: none;
  border-color: #22d3ee;
  box-shadow: 0 0 8px #22d3ee;
}

.btn-update {
  width: 100%;
  padding: 12px;
  background: linear-gradient(to right, #00c6ff, #0072ff);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  font-weight: bold;
  margin-top: 10px;
}

.btn-update:hover {
  filter: brightness(1.15);
}

.back-link {
  display: block;
  text-align: center;
  margin-top: 15px;
  color: #aaa;
  font-size: 15px;
  text-decoration: none;
}

.back-link:hover {
  color: white;
  text-decoration: underline;
}
.error-box {
    background: rgba(255, 40, 40, 0.15);
    color: #ff6b6b;
    border: 1px solid #ff4d4d;
    padding: 10px 14px;
    border-radius: 6px;
    margin-bottom: 12px;
    font-weight: 600;
    text-align: center;
}
</style>
