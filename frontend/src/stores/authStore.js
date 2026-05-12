import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('authStore', () => {
    const auth_token =ref(localStorage.getItem('token')|| null)
    const user = ref(JSON.parse(localStorage.getItem('user')|| null))
    const isAuthenticated = computed(()=> auth_token.value!=null)

    function setUserCred(token,userData){
        localStorage.setItem('token', token)
        localStorage.setItem('user', JSON.stringify(userData))
        auth_token.value=token
        user.value = {...userData}
    }

    function setUserName(name){
        if (user.value){
            user.value.full_name=name;
        }
    }

    function clearAuthToken(){
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        auth_token.value=null
        user.value=null
    }

    function getAuthToken(){
        return auth_token.value
    }

    function getUserEmail(){
        return user.value? user.value.email : null
    }

    function getUserPhone() {
        return user.value? user.value.phone_number : null
    }

    function getUserName() {
        return user.value? user.value.full_name : null
    }

    function getUserRoles(){
        return user.value? user.value.roles: []
    }

    return {isAuthenticated, setUserCred, setUserName, clearAuthToken ,getAuthToken, getUserEmail, getUserPhone, getUserName, getUserRoles}
})