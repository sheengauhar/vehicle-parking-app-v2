<script setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/authStore";

const authStore = useAuthStore();

const full_name = ref("");
const phone_number = ref("");
const email = ref("");

const loading = ref(true);
const success = ref("");
const error = ref("");

async function loadProfile() {
  loading.value = true;

  try {
    const res = await fetch("http://127.0.0.1:5000/api/profile", {
      headers: {
        "Authentication-Token": authStore.getAuthToken()
      }
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.message);

    full_name.value = data.full_name;
    phone_number.value = data.phone_number;
    email.value = data.email;
  } catch (err) {
    error.value = err.message;
  }

  loading.value = false;
}

async function saveChanges() {
  success.value = "";
  error.value = "";

  try {
    const res = await fetch("http://127.0.0.1:5000/api/profile/edit", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": authStore.getAuthToken()
      },
      body: JSON.stringify({
        full_name: full_name.value,
        phone_number: phone_number.value
      })
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.message);

    authStore.setUserName(full_name.value);

    success.value = "Profile Updated Successfully!";
  } catch (err) {
    error.value = err.message;
  }
}

onMounted(() => loadProfile());
</script>

<template>
  <div class="edit_container">
    <h2 class="title">Edit Profile</h2>

    <p v-if="loading">Loading...</p>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>

    <div v-if="!loading">
      <div class="form_group">
        <label>Name</label>
        <input type="text" v-model="full_name" />
      </div>

      <div class="form_group">
        <label>Phone Number</label>
        <input type="text" v-model="phone_number" />
      </div>

      <div class="form_group">
        <label>Email (read-only)</label>
        <input type="email" :value="email" readonly />
      </div>

      <button class="save_btn" @click="saveChanges">Save Changes</button>

      <RouterLink
        class="back_btn"
        :to="authStore.getUserRoles().includes('admin') ? '/admin/dashboard' : '/user/dashboard'"
      >
        ⬅ Back to Dashboard
      </RouterLink>

    </div>
  </div>
</template>

<style scoped>
.edit_container {
  max-width: 450px;
  margin: 40px auto;
  padding: 20px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 3px 10px rgba(0,0,0,0.1);
}

.title {
  text-align: center;
  margin-bottom: 20px;
}

.form_group {
  margin-bottom: 15px;
}

label {
  font-weight: 500;
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #aaa;
  border-radius: 5px;
}

.save_btn {
  width: 100%;
  padding: 12px;
  margin-top: 10px;
  background: #690a9c;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
}

.back_btn {
  display: block;
  text-align: center;
  margin-top: 20px;
  color: #444;
}

.error {
  color: red;
  text-align: center;
  margin-bottom: 10px;
}

.success {
  color: green;
  text-align: center;
  margin-bottom: 10px;
}
</style>
