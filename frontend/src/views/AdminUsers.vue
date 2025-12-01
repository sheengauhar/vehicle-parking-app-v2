<script setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/authStore";

const authStore = useAuthStore();
const users = ref([]);
const loading = ref(true);
const error = ref(null);

async function loadUsers() {
  loading.value = true;
  error.value = null;

  try {
    const res = await fetch("http://127.0.0.1:5000/api/admin/users", {
      headers: {
        "Authentication-Token": authStore.getAuthToken()
      }
    });

    if (!res.ok) {
      throw new Error("Failed to load users");
    }

    const data = await res.json();
    users.value = data.users;
  } catch (err) {
    error.value = err.message;
  }

  loading.value = false;
}

onMounted(() => {
  loadUsers();
});
</script>

<template>
  <div class="users_container">
    <h2 class="users_title">All Registered Users</h2>

    <p v-if="loading" class="info">Loading...</p>
    <p v-if="error" class="error">{{ error }}</p>

    <table v-if="!loading && !error" class="users_table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Full Name</th>
          <th>Email</th>
          <th>Phone Number</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="u in users" :key="u.id">
          <td>{{ u.id }}</td>
          <td>{{ u.full_name }}</td>
          <td>{{ u.email }}</td>
          <td>{{ u.phone_number }}</td>
        </tr>

        <tr v-if="users.length === 0">
          <td colspan="4" class="info">No users found.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.users_container {
  max-width: 900px;
  margin: 40px auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 3px 10px rgba(0,0,0,0.1);
  text-align: center;
}

.users_title {
  font-size: 32px;
  margin-bottom: 20px;
  font-weight: 600;
}

.users_table {
  width: 100%;
  border-collapse: collapse;
  font-size: 16px;
}

.users_table th {
  background: #690a9c;
  color: #fff;
  padding: 10px;
}

.users_table td {
  padding: 12px;
  border-bottom: 1px solid #ccc;
}

.info {
  margin-top: 20px;
  color: #555;
}

.error {
  margin-top: 20px;
  color: red;
}
</style>
