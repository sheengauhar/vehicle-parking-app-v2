<script setup>
import { ref , onMounted ,onUnmounted} from 'vue';
import { useRouter } from 'vue-router';
import { useMessageStore } from '@/stores/counter';
import { useAuthStore } from '@/stores/authStore';

const message_store = useMessageStore();
const auth_store = useAuthStore();
const router = useRouter();

const email = ref('');
const password = ref('');

async function login_func() {

    if (email.value === '' || password.value === '') {
    alert('Email and Password are required.');
    return;
  }

  const user = {
    email: email.value,
    password: password.value
  };

  const response = await fetch("http://127.0.0.1:5000/api/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(user)
  });

  const data = await response.json()

  if (!response.ok) {
    message_store.showMessage(data.message || "Login failed", "error")
    return;
  }

  message_store.updateErrorMessages(data.message);

  const userData = {
    email: data.user_details.email,
    full_name: data.user_details.full_name,
    phone_number: data.user_details.phone_number,
    roles: data.user_details.roles
  };

  auth_store.setUserCred(data.user_details.auth_token, userData);

  if (auth_store.getUserRoles().includes("admin")) {
    router.push('/admin/dashboard');
  } else {
    router.push('/user/dashboard');
  }
}

onMounted(() => {
  document.body.classList.add("login-bg")
})

onUnmounted(() => {
  document.body.classList.remove("login-bg")
})

</script>

<template>
  <div class="login-wrapper">
    <div class="login-card">
      <h2 class="login-title">Login to Your Account</h2>

      <form @submit.prevent="login_func">
        
        <div class="login-field">
          <label>Email</label>
          <input type="email" v-model="email">
        </div>

        <div class="login-field">
          <label>Password</label>
          <input type="password" v-model="password" @input="validatePassword">
        </div>

        <button type="submit" class="login-btn">Login</button>

        <a class="register-link" href="/register">
          Don't have an account? Click here to Register
        </a>
      </form>
    </div>
  </div>
</template>


<style scoped>
.login-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 60px);
  margin-top: 20px;
}

.login-card {
  background-color: #1c1c1e;
  width: 360px;
  padding: 60px; 
  border-radius: 16px;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.1);
  text-align: center;
}

.login-title {
  color: #00e0ff;
  margin-bottom: 25px;
  font-size: 24px;
  font-weight: 600;
}

.login-field {
  margin-bottom: 20px;
  text-align: left;
}

.login-field label {
  display: block;
  margin-bottom: 6px;
  color: #ccc;
  font-weight: 600;
}

.login-field input {
  width: 95%;
  padding: 10px;
  background: #2a2a2d;
  border: 2px solid transparent;
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
  outline: none;
  box-shadow: 0 0 4px #8e44ad;
}

.login-field input:focus {
  outline: none;
  border-color: #00eaff;
}

.error-text {
  margin-top: 5px;
  color: #ff6b6b;
  font-size: 13px;
}

.login-btn {
  margin-top: 10px;
  padding: 10px 20px;
  width: 100%;
  background: linear-gradient(to right, #00e0ff, #8e44ad);
  border: none;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s;
}

.login-btn:hover {
  opacity: 0.9;
}

.register-link {
  display: block;
  text-align: center;
  margin-top: 20px;
  color: #a784ec;
  text-decoration: none;
}

.register-link:hover {
  text-decoration: underline;
}
</style>