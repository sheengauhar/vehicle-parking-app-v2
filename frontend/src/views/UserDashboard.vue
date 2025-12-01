<script setup>
import { ref, onMounted } from 'vue';
import { useMessageStore } from '@/stores/counter';
import { useAuthStore } from "@/stores/authStore";

const message_store = useMessageStore();
const authStore = useAuthStore();

const reservations = ref([]);


const showModal = ref(false);
const selectedReservation = ref(null);


function formatDate(iso) {
  if (!iso) return 'N/A';
  const d = new Date(iso);
  return d.toLocaleString();
}

async function loadReservations() {
  try {
    const res = await fetch("http://127.0.0.1:5000/api/user/reservations", {
      method: "GET",
      headers: {
        "Authentication-Token": authStore.getAuthToken()
      }
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.message);

    reservations.value = data.reservations;

  } catch (err) {
    message_store.showMessage("Failed to load reservations", "error");
    console.error(err);
  }
}

function openReleaseModal(reservation) {
  selectedReservation.value = reservation;
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
  selectedReservation.value = null;
}

async function confirmRelease() {
  try {
    const res = await fetch( `http://127.0.0.1:5000/api/reservations/${selectedReservation.value.id}/release`, {
      method: 'POST',
      headers: {
        "Authentication-Token": authStore.getAuthToken()
      }
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.message || 'Failed to release');
    message_store.updateErrorMessages(`Spot released successfully! Total Cost: ₹${data.reservation.total_cost}`);

    closeModal();
    await loadReservations();  

  } catch (err) {
    message_store.updateErrorMessages(err.message);
  }
}

async function exportCSV() {
  try {
    const res = await fetch("http://127.0.0.1:5000/api/export_csv", {
      method: "POST",
      credentials: "include",
      headers:{
        "Authentication-Token": authStore.getAuthToken()
      }
    });

    const data = await res.json();

    if (res.status === 202) {
      message_store.showMessage("CSV export started! You will receive an email shortly.", "success");
    } else {
      message_store.showMessage(data.message || "Something went wrong.", "error");
    }
  } catch (err) {
    message_store.showMessage("Failed to trigger CSV export.", "error");
  }
}

async function clearHistory() {
  if (!confirm("Are you sure you want to clear your past reservation history?")) return;

  try {
    const res = await fetch("http://127.0.0.1:5000/api/user/clear_history", {
      method: "DELETE",
      credentials: "include",
      headers: {
        "Authentication-Token": authStore.getAuthToken()
      }
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.message);

    message_store.updateErrorMessages(data.message);

    await loadReservations();

  } catch (err) {
    message_store.updateErrorMessages(err.message);
  }
}

onMounted(() => loadReservations());
</script>

<template>
  <div class="dashboard_container">
    <h1 class="user_dashboard_heading">Welcome to your Parking Dashboard</h1>

    <div class="user_lot_board">
      <template v-if="reservations.length">
        <h2 class="user_board_title">Recent Parking History</h2>
        <button class="export-btn" @click="exportCSV">
          Export CSV
        </button>

        <table class="user_hist_table">
          <thead>
            <tr>
              <th>Reservation ID</th><th>Spot Name</th><th>Location</th><th>Pincode</th>
              <th>Vehicle No</th><th>Parking Timestamp</th><th>Leaving Timestamp</th>
              <th>Price/hour (₹)</th><th>Total Cost (₹)</th><th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in reservations" :key="r.id">
              <td>{{ r.id }}</td>
              <td>{{ r.spot.spot_number }}</td>
              <td>{{ r.spot.parking_lot.prime_location }}</td>
              <td>{{ r.spot.parking_lot.pincode }}</td>
              <td>{{ r.vehicle_number || 'N/A' }}</td>
              <td>{{ formatDate(r.parking_timestamp) }}</td>
              <td>{{ r.leaving_timestamp ? formatDate(r.leaving_timestamp) : 'Not Yet Left' }}</td>
              <td>{{ r.cost_per_unit_time }}</td>
              <td>{{ r.total_cost || 'To be calculated' }}</td>
              <td>
                <button v-if="r.status === 'parked'" @click="openReleaseModal(r)" class="btn-release">Release</button>
                <button v-else disabled>Parked Out</button>
              </td>
            </tr>
          </tbody>
        </table>

        <div class="bottom-buttons">
          <router-link class="spot_btn" to="/book-spots">Book a Spot</router-link>
          <button class="spot_btn" @click="clearHistory">Clear History</button>
        </div>


      </template>

      <template v-else>
        <div class="empty_history_container">
          <p class="empty_text"> You don't have any parking history yet!</p>
          <p class="empty_subtext">Start your journey by booking your first parking spot now!</p>
          <router-link class="spot_btn" to="/book-spots">Book a Spot</router-link>
        </div>
      </template>
    </div>

    <div v-if="showModal" class="modal-overlay">
      <div class="modal-card">
        <h2 class="modal-title">Confirm Release</h2>

        <div class="modal-details">
        <p><strong>Spot:</strong> {{ selectedReservation.spot.spot_number }}</p>
        <p><strong>Vehicle Number:</strong> {{ selectedReservation.vehicle_number }}</p>
        <p><strong>Parking Time:</strong> {{ formatDate(selectedReservation.parking_timestamp) }}</p>
        <p><strong>Price Per Hour:</strong> ₹{{ selectedReservation.cost_per_unit_time }}</p>
        </div>
        <div class="modal-actions">
          <button class="btn-release-confirm" @click="confirmRelease">Release</button>
          <button class="btn-cancel" @click="closeModal">Cancel</button>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.dashboard_container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 10px;
}

.user_dashboard_heading {
  text-align: center;
  color: #1a1a1a;
  font-size: 36px;
  margin-bottom: 40px;
  font-weight: 600;
  font-family: 'Times New Roman', Times, serif;
  letter-spacing: 0.2px;
}

.user_lot_board {
  background: linear-gradient(to right, #c1bec3b6, #eceff0);
  border: 2px solid #38036a;
  padding: 24px;
  border-radius: 12px;
  max-width: 1500px;
  width: 90%;
  margin: 0 auto;
  box-shadow: 0 6px 20px rgba(0,0,0,0.15);
  overflow-x: auto;
}

.user_board_title {
  text-align: center;
  font-size: 30px;
  color: #5d1748;
  margin-bottom: 24px;
}

.user_hist_table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.user_hist_table th,
.user_hist_table td {
  border: 2px solid #020202;
  padding: 10px;
  text-align: center;
  font-size: 15px;
  background-color: #ffffff;
}

.user_hist_table th {
  background-color: #eaeaea;
  font-weight: bold;
}

.btn-release {
  background-color: #ffc2c2;
  color: black;
  border: 1px solid #a94442;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.2s ease;
}

.btn-release:hover {
  background-color: #ff9f9f;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.65);
  backdrop-filter: blur(3px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-card {
  background: white;
  padding: 40px 55px;
  border-radius: 18px;
  width: 520px;
  box-shadow: 0 12px 30px rgba(0,0,0,0.25);
  animation: scaleIn 0.25s ease-out;
  border-left: 6px solid #5d1748;
}

.modal-title {
  font-size: 28px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 30px;
  color: #5d1748;
}

.modal-details {
  background: #efeded;
  padding: 18px 25px;
  border-radius: 12px;
  margin-bottom: 25px;
  border: 1px solid #9f7f7f;
}

.modal-details p {
  margin: 10px 0;
  font-size: 17px;
  color: #1b1a1a;
}

.modal-details strong {
  color: #000;
  font-weight: 700;
}

.modal-actions {
  margin-top: 5px;
  display: flex;
  justify-content: space-between;
  padding: 0 10px;
}

.btn-release-confirm {
  background: #2ecc71;
  color: white;
  padding: 12px 32px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: 0.2s ease;
}

.btn-release-confirm:hover {
  background: #1e8a4d;
  transform: scale(1.05);
}

.btn-cancel {
  background: #e74c3c;
  color: white;
  padding: 12px 32px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: 0.2s ease;
}

.btn-cancel:hover {
  background: #c0392b;
  transform: scale(1.05);
}

@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.9); }
  to   { opacity: 1; transform: scale(1); }
}

button[disabled] {
  background-color: #bcc9bf;
  color: black;
  border: 1px solid #3c763d;
  padding: 5px 10px;
  border-radius: 5px;
}

.empty_history_container {
  text-align: center;
  padding: 40px 20px;
  margin-top: 30px;
  background: linear-gradient(to right, #ffffff, #f8f9fa);
  border: 2px dashed #bdc3c7;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

.empty_text {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.empty_subtext {
  font-size: 16px;
  color: #7f8c8d;
  margin-bottom: 20px;
}

.bottom-buttons {
  width: 100%;
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.spot_btn {
  display: inline-block;
  padding: 12px 26px;
  background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
  color: white;
  font-weight: bold;
  font-size: 15px;
  border-radius: 30px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.spot_btn:hover {
  background: linear-gradient(to right, #2c3e50, #4ca1af);
  transform: scale(1.05);
}

.export-btn {
  background-color: #6a5acd;
  padding: 10px 18px;
  border-radius: 8px;
  color: white;
  border: none;
  margin-top: 20px;
  cursor: pointer;
  transition: 0.2s ease;
}
.export-btn:hover {
  background-color: #5848c2;
}
</style>

