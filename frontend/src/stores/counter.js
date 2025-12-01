import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useMessageStore = defineStore('messageStore', () => {
  const errorMessages = ref('')

  function updateErrorMessages(message) {
    errorMessages.value=message 
    setTimeout(() => {
      errorMessages.value=''
    },5000);
  }

  const message = ref('')
  const type = ref('') 
  const visible = ref(false)

  function showMessage(msg, msgType = "success") {
    message.value = msg
    type.value = msgType
    visible.value = true

    setTimeout(() => {
      visible.value = false
      message.value = ''
      type.value = ''
    }, 4000)
  }


  return { errorMessages, updateErrorMessages, message, type, visible, showMessage }
})
