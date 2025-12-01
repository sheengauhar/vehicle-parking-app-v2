<template>
  <div class="main_container">
    <h2 class="heading">Available Parking Lots & Spots</h2>

    <table class="lot_spot_table">
      <thead>
        <tr><th>Location</th><th>Address</th><th>Pincode</th><th>Total Spots</th><th>Available Spots</th><th>Price/hour</th><th>Action</th></tr>
      </thead>
      <tbody>
        <tr v-for="entry in lotData" :key="entry.id">
            <td>{{ entry.prime_location }}</td>
            <td>{{ entry.address }}</td>
            <td>{{ entry.pincode }}</td>
            <td>{{ entry.max_spots }}</td>
            <td>{{ entry.max_spots - entry.occupied_spots }}</td>
            <td>₹{{ entry.price }}</td>
            <td>
                <router-link :to="`/confirm-booking/${entry.id}`" class="btn-book">Book Now</router-link>
            </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
const lotData = ref([]);

async function loadLots() {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/parking_lots', { credentials: 'include' });
    if (!res.ok) throw new Error('Failed to load lots');
    const data = await res.json();

    lotData.value = data;
  } catch (err) {
    console.error(err);
  }
}
onMounted(loadLots);
</script>

<style scoped>
.main_container {
    max-width: 1200px;
    margin: 30px auto;
    padding: 20px;
    background: #f4f4f9;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.heading {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    text-align: center;
    color: #2c2c2c;
    margin-bottom: 30px;
    font-size: 36px;
    font-weight: bold;
}

.lot_spot_table {
    width: 100%;
    background: linear-gradient(to right, #f8f9fa, #e0e0e0);
    border-collapse: collapse;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.lot_spot_table th,
.lot_spot_table td {
    padding: 14px 9px;
    text-align: center;
    border: 1px solid #aaa;
    font-size: 16px;
}

.lot_spot_table th {
    background-color: #38036a;
    color: white;
    font-weight: bold;
    letter-spacing: 0.5px;
}

.lot_spot_table td {
    font-weight: 550;
    color: #000000;
}

.lot_spot_table tr:nth-child(even) {
    background-color: #f2f2f2;
}

.btn-book {
    background-color: #38036a;
    color: white;
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: 600;
    border: none;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    transition: 0.3s ease;
}

.btn-book:hover {
    background-color: #5d28a0;
}
</style>

