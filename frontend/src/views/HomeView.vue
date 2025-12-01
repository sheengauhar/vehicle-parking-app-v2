<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
    <div class="main_container">
        <div class="welcome_section">
        <h1 class="welcome_title">Welcome to the Vehicle Parking App</h1>
        <p class="welcome_subtext">Please choose an option to continue:</p>

        <div class="card_container">
          <RouterLink to="/login" class="auth_card login_card">
            <h3>Login</h3>
            <p>Access your dashboard</p>
          </RouterLink>

          <RouterLink to="/register" class="auth_card register_card">
            <h3>Register</h3>
            <p>Create a new account</p>
          </RouterLink>
        </div>
      </div>
    </div>
</template>

<style scoped>
.main_container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 10px;
}

.welcome_section {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #0f497c, #1c4883);
  border-radius: 16px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
  margin-top: 40px;
}

.welcome_title {
  font-size: 32px;
  color: #ffffff;
  margin-bottom: 10px;
}

.welcome_subtext {
  font-size: 18px;
  color: #aeacac;
  margin-bottom: 30px;
}

.card_container {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
}

.auth_card {
  display: block;
  width: 200px;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 12px;
  text-decoration: none;
  color: #333;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.auth_card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}

.login_card {
  border-top: 4px solid #007bff;
}
.register_card {
  border-top: 4px solid #28a745;
}

.auth_card h3 {
  margin: 0;
  font-size: 22px;
}

.auth_card p {
  font-size: 14px;
  margin-top: 8px;
  color: #555;
}
</style>
