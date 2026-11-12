<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthInput from '@/components/AuthInput.vue'
import api from '../services/api'
import { supabase } from '../services/supabase'

const router = useRouter()

// Form state variables
const email = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
  errorMessage.value = ''
  isLoading.value = true

  try {
    const response = await api.login({
      email: email.value,
      password: password.value,
    })

    console.log("Login successful:", response.data)

    // Store the access token in localStorage (or sessionStorage)
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token)
    }

    // Redirect user to the dashboard or home view (update route as needed)
    router.push('/dashboard')
  } catch (error) {
    console.error("Login error:", error)

    // Human-friendly error parsing
    const detail = error.response?.data?.detail
    if (typeof detail === 'string') {
      errorMessage.value = detail
    } else {
      errorMessage.value = "Invalid email or password. Please try again."
    }
  } finally {
    isLoading.value = false
  }
}

const handleGoogleLogin = async () => {
  try {
    const response = await api.getGoogleAuthUrl()
    if (response.data.url) {
      // Redirect browser to Google's login page
      window.location.href = response.data.url
    }
  } catch (error) {
    console.error("Google auth error:", error)
    errorMessage.value = "Could not connect to Google sign-in. Try again."
  }
}

const handleForgotPassword = async () => {
  if (!email.value) {
    errorMessage.value = "Please enter your email address above first."
    return
  }

  try {
    isLoading.value = true
    errorMessage.value = ''

    const { error } = await supabase.auth.resetPasswordForEmail(email.value, {
      redirectTo: `${window.location.origin}/reset-password`,
    })

    if (error) throw error

    errorMessage.value = "Password reset link sent! Check your inbox."
  } catch (error) {
    errorMessage.value = error.message || "Could not send reset email. Try again."
    console.error("Forgot password error:", error)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <!-- Main wrapper: Centers content and scales padding across mobile, tablet, and TV/Large screens -->
  <div class="min-h-screen flex items-center justify-center p-4 sm:p-6 md:p-10 lg:p-16">

    <!-- Login Card -->
    <div
      class="w-full max-w-sm sm:max-w-md lg:max-w-lg bg-darkBgStart/50 backdrop-blur-2xl border border-white/10 rounded-2xl sm:rounded-3xl p-6 sm:p-8 lg:p-10 shadow-2xl relative overflow-hidden">

      <!-- Ambient Glow Effect using your electric blue accent -->
      <div class="absolute -top-24 -right-24 w-48 h-48 bg-[#00bbff]/10 rounded-full blur-3xl pointer-events-none"></div>

      <!-- Header Section -->
      <div class="text-center mb-6">
        <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight mb-2">Welcome Back</h1>
        <p class="text-xs sm:text-sm text-gray-400">Log in to access your saved YouTube scripts.</p>
      </div>

      <!-- Error Message Display-->
      <div v-if="errorMessage"
        class="mb-6 p-3 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-xs sm:text-sm text-center">
        {{ errorMessage }}
      </div>

      <!-- Form Fields -->
      <form @submit.prevent="handleLogin" class="space-y-4 sm:space-y-5">
        <AuthInput label="Email Address" type="email" placeholder="name@example.com" v-model="email" />

        <AuthInput label="Password" type="password" placeholder="Enter your password" v-model="password" />

        <!-- Login Button -->
        <button type="submit" :disabled="isLoading"
          class="w-full mt-2 py-3.5 px-4 bg-neonLime text-black font-bold rounded-xl text-sm sm:text-base hover:opacity-90 shadow-[0_0_20px_rgba(140,255,0,0.3)] transition-all cursor-pointer disabled:opacity-50">
          {{ isLoading ? 'Signing In...' : 'Sign In' }}
        </button>

        <!-- forgot password -->
        <div class="flex items-center justify-center gap-2 text-xs sm:text-sm mt-1 mb-4">
          <span class="text-gray-400">Forgot your password?</span>
          <button type="button" @click="handleForgotPassword" class="text-[#00bbff] hover:underline font-medium">
            Reset it here
          </button>
        </div>
      </form>

      <!-- Divider -->
      <div class="flex items-center my-6">
        <div class="flex-grow border-t border-white/10"></div>
        <span class="px-3 text-xs uppercase tracking-wider text-gray-500 font-medium">Or</span>
        <div class="flex-grow border-t border-white/10"></div>
      </div>

      <!-- Sign in with Google / Gmail Button -->
      <button @click="handleGoogleLogin"
        class="w-full py-3 px-4 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-sm sm:text-base font-semibold text-[#e0f6ff] flex items-center justify-center gap-3 transition-all cursor-pointer group">
        <!-- Google Icon SVG -->
        <svg class="w-5 h-5 transition-transform group-hover:scale-110" viewBox="0 0 24 24">
          <path fill="#4285F4"
            d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.17z" />
          <path fill="#34A853"
            d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.13 0-5.78-2.11-6.73-4.96H1.18v3.15C3.15 21.32 7.23 24 12 24z" />
          <path fill="#FBBC05"
            d="M5.27 14.24c-.25-.72-.38-1.49-.38-2.24s.13-1.52.38-2.24V6.61H1.18C.43 8.13 0 9.87 0 12s.43 3.87 1.18 5.39l4.09-3.15z" />
          <path fill="#EA4335"
            d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.23 0 3.15 2.68 1.18 6.61l4.09 3.15c.95-2.85 3.6-4.96 6.73-4.96z" />
        </svg>
        Sign in with Google
      </button>

      <!-- Footer Navigation Link -->
      <p class="text-xs sm:text-sm text-center text-gray-400 mt-6">
        Don't have an account?
        <router-link to="/register" class="text-[#00bbff] hover:underline font-medium">Register</router-link>
      </p>

    </div>
  </div>
</template>