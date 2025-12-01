<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { useMessageStore } from './stores/counter';
import { useAuthStore } from './stores/authStore';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const message_store = useMessageStore();
const auth_store = useAuthStore();
const router = useRouter();

const ErrorMsgs = computed(() => {
  return message_store.errorMessages;
});

function logout() {
  auth_store.clearAuthToken();
  router.push('/login');
  message_store.updateErrorMessages('You have been logged out successfully.');
}
</script>

<template>
  <div>
    <div class="navbar">
      <div class="nav_left">
      <h2 class="app_title">Vehicle Parking App</h2>
    </div>

    <div class="nav_right" v-if="auth_store.isAuthenticated">
      <span class="nav_link">Welcome, {{ auth_store.getUserName() }}</span>
      
      <template v-if="auth_store.getUserRoles().includes('admin')">
        <RouterLink class="nav_link" to="/admin/dashboard">Home</RouterLink>
        <RouterLink class="nav_link" to="/admin/users">Users</RouterLink>
        <RouterLink class="nav_link" to="/admin/summary">Summary</RouterLink>
      </template>

      <RouterLink class="nav_link" to="/edit-profile">Edit Profile</RouterLink>

      <template v-if="auth_store.getUserRoles().includes('user')">
        <RouterLink class="nav_link" to="/user/dashboard">Home</RouterLink>
        <RouterLink class="nav_link" to="/user/summary/usage_per_lot">Summary</RouterLink>
      </template>
      
      <a class="nav_link" @click="logout">Logout</a>
    </div>
  </div>   

    <div v-if="ErrorMsgs" class="alert alert-success">{{ ErrorMsgs }}</div>

    <div v-if="message_store.visible" class="toast" :class="message_store.type">{{ message_store.message }}</div>

    <RouterView />
  </div>
</template>

<style scoped> 
.navbar {
  background-color: #f0f0f0;
  padding: 12px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center; /* THIS aligns children inside navbar */
  height: 50px;
  box-sizing: border-box;
}

.nav_left h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.nav_right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav_right span {
  margin-right: 10px;
  color: #444;
}

.nav_link {
  text-decoration: none;
  color: #333;
  font-weight: 500;
}

.nav_link:hover {
  text-decoration: underline;
}

.alert {
  background-color: #d4edda;
  color: #155724;
  padding: 10px;
  margin: 10px auto;
  border: 1px solid #bce8f1;
  border-radius: 4px;
  width: 90%;
  text-align: center;
}
</style>

<style>
html, body, #app {
  margin: 0 !important;
  padding: 0 !important;
}

.navbar {
  margin: 0 !important;
  padding: 35px 20px !important;
  width: 100% !important;
  box-sizing: border-box;
}

.toast {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  color: white;
  z-index: 9999;
}

.toast.success {
  background: #27ae60;
}
.toast.error {
  background: #e74c3c;
}

.login-bg {
  background-color: #0f0f11 !important;
}

.dashboard-bg {
  background-color: #ffffff !important;
}

.editlot-bg {
  background-color: #ffffff !important;
}

</style>

