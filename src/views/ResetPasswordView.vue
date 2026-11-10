<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import AuthInput from '../components/AuthInput.vue'
import { supabase } from '../services/supabase'

const router = useRouter()
const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)
const ready = ref(false)
let sub
const handleResetPassword = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (password.value !== confirmPassword.value) {
    errorMessage.value = "Passwords do not match."
    return
  }

  if (password.value.length < 6) {
    errorMessage.value = "Password must be at least 6 characters long."
    return
  }

  try {
    isLoading.value = true

    // Supabase automatically grabs the token from the URL and updates the user
    const { error } = await supabase.auth.updateUser({
      password: password.value
    })

    if (error) throw error

    successMessage.value = "Password updated successfully! Redirecting to login..."
    setTimeout(() => {
      router.push('/login')
    }, 2500)
  } catch (error) {
    errorMessage.value = error.message || "Failed to update password. Link may have expired."
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  const hash = window.location.hash
  if (hash.includes('error_description=')) {
    const params = new URLSearchParams(hash.slice(1))
    errorMessage.value = params.get('error_description') || 'Link is invalid or expired.'
    return
  }

  const { data } = supabase.auth.onAuthStateChange((event) => {
    if (event === 'PASSWORD_RECOVERY') ready.value = true
  })
  sub = data.subscription
})

onUnmounted(() => sub?.unsubscribe())
</script>

<template>
  <div class="min-h-screen flex items-center justify-center p-4 sm:p-6">
    <div class="w-full max-w-md bg-darkBgStart/50 border border-white/10 rounded-2xl p-6 sm:p-8">
      <h1 class="text-2xl font-extrabold text-white text-center mb-2">Set a new password</h1>
      <p class="text-sm text-gray-400 text-center mb-6">Choose a new password for your account.</p>

      <p
        v-if="errorMessage"
        role="alert"
        class="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-sm text-center"
      >
        {{ errorMessage }}
      </p>
      <p
        v-if="successMessage"
        role="status"
        class="mb-4 p-3 bg-green-500/10 border border-green-500/30 rounded-xl text-green-400 text-sm text-center"
      >
        {{ successMessage }}
      </p>

      <form class="space-y-4" @submit.prevent="handleResetPassword">
        <AuthInput
          v-model="password"
          label="New password"
          type="password"
          placeholder="At least 6 characters"
        />
        <AuthInput
          v-model="confirmPassword"
          label="Confirm new password"
          type="password"
          placeholder="Re-enter your new password"
        />
        <button
          type="submit"
          :disabled="isLoading"
          class="w-full py-3 px-4 bg-neonLime text-black font-bold rounded-xl hover:opacity-90 disabled:opacity-50"
        >
          {{ isLoading ? 'Updating password...' : 'Update password' }}
        </button>
      </form>

      <p class="text-sm text-center text-gray-400 mt-6">
        <router-link to="/login" class="text-[#00bbff] hover:underline">Back to login</router-link>
      </p>
    </div>
  </div>
</template>