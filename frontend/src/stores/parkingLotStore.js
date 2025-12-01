import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useAuthStore } from './authStore'
import { useMessageStore } from './counter'


export const useParkingLotStore = defineStore('parkingLotStore', () => {
    const authStore = useAuthStore()
    const messageStore = useMessageStore()

    const lots = ref([])         
    const selectedLot = ref(null)      
    const loading = ref(false)
    const error = ref(null)

    async function fetchLots() {
        loading.value = true
        error.value = null
        try {
            const res = await fetch('http://127.0.0.1:5000/api/parking_lots',{
                headers:{
                    'Content-Type': 'application/json',
                    "Authentication-Token": authStore.getAuthToken()
                }
            })
            lots.value = await res.json()
        } catch (err) {
            error.value = "Failed to load parking lots."
        } finally {
            loading.value = false
        }
    }

    async function fetchLot(lot_id) {
        loading.value = true
        error.value = null
        try {
            const res = await fetch(`http://127.0.0.1:5000/api/parking_lots/${lot_id}`, {
                headers: {
                    'Content-Type': 'application/json',
                    "Authentication-Token": authStore.getAuthToken()
                }
            })
            selectedLot.value = await res.json()
        } catch (err) {
            error.value = "Failed to fetch parking lot."
        } finally {
            loading.value = false
        }
    }

    async function createLot(payload) {
        loading.value = true
        error.value = null
        try {
            const res = await fetch('http://127.0.0.1:5000/api/parking_lots', {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    "Authentication-Token": authStore.getAuthToken()
                },
                body: JSON.stringify(payload)
            })

            const data = await res.json()
            if (!res.ok) throw new Error(data.message)

            // refresh list after creating
            await fetchLots()
            return data

        } catch (err) {
            error.value = err?.message|| "Something went wrong"
            throw err
        } finally {
            loading.value = false
        }
    }

    async function updateLot(lot_id, payload) {
        loading.value = true
        error.value = null

        try {
            const res = await fetch(`http://127.0.0.1:5000/api/parking_lots/${lot_id}`, {
                method: "PUT",
                headers: {
                    'Content-Type': 'application/json',
                    "Authentication-Token": authStore.getAuthToken()
                },
                body: JSON.stringify(payload)
            })
            
            const data = await res.json()
            if (!res.ok) throw new Error(data.message)

            await fetchLots()
            return data

        } catch (err) {
            error.value = err?.message || "Something went wrong"
            throw err
        } finally {
            loading.value = false
        }
    }

    async function deleteLot(lot_id) {
        loading.value = true
        error.value = null
        try {
            const res = await fetch(`http://127.0.0.1:5000/api/parking_lots/${lot_id}`, {
                method: "DELETE",
                headers: {
                    'Content-Type': 'application/json',
                    "Authentication-Token": authStore.getAuthToken()
                }
            })

            const data = await res.json()
                if (!res.ok) {
                    messageStore.showMessage(data.message, "error");  // 🔥 show toast
                    return false;                                      // do NOT throw
            }

            messageStore.showMessage("Parking lot deleted successfully!", "success");

            await fetchLots()
            return data

        } catch (err) {
            messageStore.showMessage("Server error. Try again later.", "error");
            return false;
        } finally {
            loading.value = false;
        }
    }

    return {
        lots,
        selectedLot,
        loading,
        error,
        fetchLots,
        fetchLot,
        createLot,
        updateLot,
        deleteLot
    }
})
