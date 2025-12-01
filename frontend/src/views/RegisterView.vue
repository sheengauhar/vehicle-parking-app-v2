<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useMessageStore } from '@/stores/counter';

const router = useRouter();
const message_store = useMessageStore();
const full_name = ref('');
const email = ref('');
const phone_number = ref('');
const password = ref('');
const confirm_password = ref('');
const checkEmailMessage = ref('');
const emailAvailable = ref(null);
const passwordMessage = ref('');

let emailTimeout = null;

function IfEmailExits() {
  clearTimeout(emailTimeout)

  if (!email.value) {
    checkEmailMessage.value = ''
    emailAvailable.value = null
    return
  }

  emailTimeout = setTimeout(()=>{
    fetch("http://127.0.0.1:5000/api/check-email", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email: email.value })
  })
    .then(res => res.json())
    .then(data => {
      emailAvailable.value = data.available
      checkEmailMessage.value = data.available
        ? "email address is available."
        : "email address already taken.";
    });
  },400)
}

function validatePassword() {
  if (password.value.length < 8) {
    passwordMessage.value = "Password must be atleast 8 characters long.";
    return false;
  }
  passwordMessage.value = "";
  return true;
}

async function register() {
    if (
        full_name.value === '' ||
        email.value === '' ||
        phone_number.value === '' ||
        password.value === '' ||
        confirm_password.value === ''
    ) {
        alert('Please fill all the details.');
        return;
    }

    if (emailAvailable.value === false) {
        alert("Email Already Registered.");
        return;
    }

    if (!validatePassword()) {
        alert("Please enter a valid password.");
        return;
    }

    if (password.value !== confirm_password.value) {
        alert("Passwords do not match!");
        return;
    }

    if (phone_number.value.length !== 10) {
    alert("Phone number must be 10 digits.")
    return
    }

  const user = {
    full_name: full_name.value,
    email: email.value,
    phone_number: phone_number.value,
    password: password.value,
    confirm_password: confirm_password.value
  };

  const response = await fetch("http://127.0.0.1:5000/api/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(user)
  });

  const data = await response.json()

  if (!response.ok) {
    message_store.showMessage(data.message || "Registration failed", "error")
    return 
  } 
  message_store.updateErrorMessages(data.message)
  router.push("/login")
}


onMounted(() => {
  document.body.classList.add("login-bg")
})
onUnmounted(() => {
  document.body.classList.remove("login-bg")
})
</script>

<template>
  <div class="register-wrapper">
    <div class="container">
      <h2>Create a New Account</h2>

      <form @submit.prevent="register">
        <label>Full Name</label>
        <input type="text" v-model="full_name">

        <label>Email</label>
        <input type="email" v-model="email" @input="IfEmailExits" />
        <p class="info-msg aqua" v-if="checkEmailMessage">{{ checkEmailMessage }}</p>

        <label>Phone Number</label>
        <input type="tel" v-model="phone_number">

        <label>Password</label>
        <input type="password" v-model="password" @input="validatePassword" />
        <p class="info-msg red" v-if="passwordMessage">{{ passwordMessage }}</p>

        <label>Confirm Password</label>
        <input type="password" v-model="confirm_password">

        <button type="submit">Register</button>
      </form>

      <router-link to="/login" class="login-link">
        Already have an account? Login here
      </router-link>
    </div>
  </div>
</template>

<style scoped>

.register-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 80px;
}

.container {
  max-width: 500px;
  width: 100%;
  padding: 30px;
  background-color: #1c1c1c;
  border-radius: 16px;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.15);
  color: #f2f2f2;
}

.container h2 {
  text-align: center;
  margin-bottom: 25px;
  color: #00eaff;
}

label {
  font-weight: 600;
  display: block;
  margin-bottom: 6px;
}

input[type="text"],
input[type="email"],
input[type="tel"],
input[type="password"] {
  width: 90%;
  padding: 10px;
  background-color: #2c2c2c;
  border: 2px solid #502c7d;
  border-radius: 10px;
  color: #fff;
  margin-bottom: 15px;
  transition: 0.3s;
}

input:focus {
  outline: none;
  border-color: #00eaff;
}

button[type="submit"] {
  width: 100%;
  padding: 12px;
  background-image: linear-gradient(to right, #00eaff, #7b2ff7);
  border: none;
  color: white;
  font-weight: bold;
  border-radius: 10px;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.3s;
}

button[type="submit"]:hover {
  filter: brightness(1.1);
}

.login-link {
  display: block;
  text-align: center;
  margin-top: 20px;
  color: #a784ec;
  text-decoration: none;
}

.login-link:hover {
  text-decoration: underline;
  color: #a784ec;
}

.info-msg {
  margin-top: -10px;
  margin-bottom: 10px;
  font-size: 14px;
  font-weight: 500;
}
.aqua { color: aqua; }
.red { color: red; }
</style>

