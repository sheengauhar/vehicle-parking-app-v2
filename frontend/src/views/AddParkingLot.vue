<script setup>
import { ref } from 'vue'
import { useParkingLotStore } from '@/stores/parkingLotStore'
import { useRouter } from 'vue-router'

const lotStore = useParkingLotStore()
const router = useRouter()

const prime_location = ref('')
const address = ref('')
const pincode = ref('')
const max_spots = ref('')
const price = ref('')

const success = ref('')
const error = ref('')

const submit = async () => {
  error.value = ''
  success.value = ''

  try {
    await lotStore.createLot({
      prime_location: prime_location.value,
      address: address.value,
      pincode: pincode.value,
      max_spots: max_spots.value,
      price: price.value
    })

    success.value = "Parking Lot created successfully!"

    setTimeout(() => router.push('/admin/dashboard'), 800)

  } catch (err) {
    error.value = err.message
  }
}
</script>

<template>
  <div class="add-lot-wrapper">
    <h1>Add Parking Lot</h1>

    <div class="form-box">
      <input v-model="prime_location" placeholder="Prime Location" />
      <input v-model="address" placeholder="Address" />
      <input v-model="pincode" type="number" placeholder="Pincode" />
      <input v-model="max_spots" type="number" placeholder="Max Spots" />
      <input v-model="price" type="number" placeholder="Price" />

      <button class="btn-save" @click="submit">Create Lot</button>
      <button class="btn-cancel" @click="router.push('/admin/dashboard')">Cancel</button>

      <p v-if="success" class="success">{{ success }}</p>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<style>
.add-lot-wrapper {
  max-width: 500px;
  margin: 50px auto;
  padding: 25px 60px;
  border-radius: 16px;
  border: 1px solid rgba(231, 9, 9, 0.464);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.216);
  text-align: center;
}

.add-lot-wrapper h1 {
  font-size: 28px;
  font-weight: 700;
  color: #4b0082;
  margin-bottom: 20px;
}

.form-box input {
  width: 90%;
  margin: 10px 0;
  padding: 12px 14px;
  border-radius: 8px;

  background: #f7f7fb;
  border: 1px solid #d5d5e0;
  font-size: 15px;
  transition: all 0.3s ease;
}

.form-box input:focus {
  border-color: #7b2cbf;
  box-shadow: 0 0 8px rgba(123, 44, 191, 0.4);
  outline: none;
}

.btn-save {
  width: 100%;
  padding: 12px;
  margin-top: 15px;
  background: linear-gradient(135deg, #6a1b9a, #8e24aa);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s ease;
}

.btn-save:hover {
  background: linear-gradient(135deg, #5e1486, #7b1fa2);
  transform: translateY(-2px);
}

.btn-cancel {
  width: 100%;
  padding: 12px;
  margin-top: 10px;
  background: #c62828;
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s ease;
}

.btn-cancel:hover {
  background: #b71c1c;
  transform: translateY(-2px);
}

.success,
.error {
  margin-top: 15px;
  padding: 10px 12px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 14px;
}

.success {
  background: rgba(46, 204, 113, 0.15);
  color: #2ecc71;
  border: 1px solid #2ecc71;
}

.error {
  background: rgba(231, 76, 60, 0.15);
  color: #e74c3c;
  border: 1px solid #e74c3c;
}

</style>
