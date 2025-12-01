<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from "@/stores/authStore";

const authStore = useAuthStore();


const success = ref('')
const route = useRoute();
const router = useRouter();
const lot = ref({});
const spot = ref({});
const vehicle_number = ref('');
const loaded = ref(false);

async function load() {
  try {
    const lot_id = route.params.lot_id;

    const res = await fetch(`http://127.0.0.1:5000/api/parking_lots/${lot_id}/next_spot`, 
    { 
      "Authentication-Token": authStore.getAuthToken()
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'No available spot');

    lot.value = data.lot;
    spot.value = data.spot;
    loaded.value = true;

  } catch (err) {
    alert(err.message);
    router.push('/book-spots');
  }
}

async function confirmBooking() {
  if (!vehicle_number.value) { 
    alert('Please Enter vehicle number'); 
    return; 
  }

  try {
    const res = await fetch('http://127.0.0.1:5000/api/reservations', {
      method: 'POST',
      credentials: 'include',
      headers: { 
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getAuthToken()
      },
      body: JSON.stringify({
        lot_id: lot.value.id,
        vehicle_number: vehicle_number.value
      })
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.message || 'Booking failed');

    success.value = `Successfully booked ${spot.value.spot_number} spot in ${lot.value.prime_location} Lot!`
    setTimeout(() => router.push('/user/dashboard'), 3000)
  } catch (err) {
    alert(err.message);
  }
}

onMounted(load);
</script>


<template>
  <div class="confirm-container" v-if="loaded">
    <p v-if="success" class="success">{{ success }}</p>
    <h2>Confirm Your Booking For {{ lot.prime_location }} Lot</h2>

    <p><strong>Spot Name:</strong> {{ spot.spot_number }}</p>
    <p><strong>Rate per Hour:</strong> ₹{{ lot.price }}</p>

    <div class="form_group">
      <label>Vehicle Number</label>
      <input v-model="vehicle_number" type="text" />
    </div>

    <button @click="confirmBooking" class="confirm_btn">Confirm Booking</button>
    <router-link to="/book-spots" class="cancel_link">Cancel</router-link>
  </div>

  <div v-else>
    <p>Loading...</p>
  </div>
</template>

<style scoped>
.confirm-container {
    max-width: 600px;
    margin: 40px auto;
    background: #f9f9fb;
    padding: 30px 40px;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #333;
}

.confirm-container h2 {
    text-align: center;
    color: #38036a;
    margin-bottom: 25px;
    font-size: 28px;
}

.confirm-container p {
    font-size: 16px;
    margin: 12px 0;
    font-weight: 500;
}

.confirm-container label {
    display: block;
    margin-top: 20px;
    font-weight: 600;
    font-size: 15px;
    color: #222;
}

.confirm-container input[type="text"] {
    width: 100%;
    padding: 10px;
    margin-top: 6px;
    border-radius: 6px;
    border: 1.5px solid #ccc;
    font-size: 15px;
    transition: border-color 0.3s ease;
}

.confirm-container input[type="text"]:focus {
    border-color: #5d28a0;
    outline: none;
}

.confirm_btn {
    margin-top: 25px;
    width: 100%;
    background-color: #38036a;
    color: white;
    padding: 12px;
    font-size: 16px;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.confirm_btn:hover {
    background-color: #5d28a0;
}

.cancel_link {
    display: block;
    margin-top: 15px;
    text-align: center;
    color: #38036a;
    font-weight: 600;
    text-decoration: none;
}

.cancel_link:hover {
    text-decoration: underline;
}

.success {
  margin-top: 18px;
  padding: 12px 15px;
  background: #e8f9f0;               
  color: #0a8a43;                   
  border-left: 4px solid #0a8a43;    
  border-radius: 6px;
  font-size: 15px;
  font-weight: 600;
  animation: fadeIn 0.3s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to   { opacity: 1; transform: translateY(0); }
}

</style>

