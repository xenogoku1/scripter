<script setup>
import { ref } from 'vue'
import AuthInput from '../components/AuthInput.vue'

// Form state variables
const username = ref('')
const email = ref('')
const password = ref('')

const handleRegister = () => {
  console.log("Registering user:", { username: username.value, email: email.value })
}

const handleGoogleSignup = () => {
  console.log("Google Sign-up clicked")
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center p-4 sm:p-6 md:p-10 lg:p-16">
    <div class="w-full max-w-sm sm:max-w-md lg:max-w-lg bg-darkBgStart/50 backdrop-blur-2xl border border-white/10 rounded-2xl sm:rounded-3xl p-6 sm:p-8 lg:p-10 shadow-2xl relative overflow-hidden">
      
      <!-- Ambient Glow Effect -->
      <div class="absolute -top-24 -right-24 w-48 h-48 bg-[#00bbff]/10 rounded-full blur-3xl pointer-events-none"></div>

      <!-- Header Section -->
      <div class="text-center mb-8">
        <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight mb-2">Create Account </h1>
        <p class="text-xs sm:text-sm text-gray-400">Start talking out your YouTube scripts today.</p>
      </div>
      
      <!-- Form Fields -->
      <form @submit.prevent="handleRegister" class="space-y-4 sm:space-y-5">
        <AuthInput 
          label="Username" 
          type="text" 
          placeholder="e.g. AnimeCommentator" 
          v-model="username" 
        />

        <AuthInput 
          label="Email Address" 
          type="email" 
          placeholder="name@example.com" 
          v-model="email" 
        />

        <AuthInput 
          label="Password" 
          type="password" 
          placeholder="At least 6 characters" 
          v-model="password" 
        />

        <button 
          type="submit"
          class="w-full mt-2 py-3.5 px-4 bg-neonLime text-black font-bold rounded-xl text-sm sm:text-base hover:opacity-90 shadow-[0_0_20px_rgba(140,255,0,0.3)] transition-all cursor-pointer"
        >
          Sign Up
        </button>
      </form>

      <!-- Divider -->
      <div class="flex items-center my-6">
        <div class="flex-grow border-t border-white/10"></div>
        <span class="px-3 text-xs uppercase tracking-wider text-gray-500 font-medium">Or</span>
        <div class="flex-grow border-t border-white/10"></div>
      </div>

      <!-- Sign in with Google Button -->
      <button 
        @click="handleGoogleSignup"
        class="w-full py-3 px-4 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-sm sm:text-base font-semibold text-[#e0f6ff] flex items-center justify-center gap-3 transition-all cursor-pointer group"
      >
        <svg class="w-5 h-5 transition-transform group-hover:scale-110" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.17z"/>
          <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.13 0-5.78-2.11-6.73-4.96H1.18v3.15C3.15 21.32 7.23 24 12 24z"/>
          <path fill="#FBBC05" d="M5.27 14.24c-.25-.72-.38-1.49-.38-2.24s.13-1.52.38-2.24V6.61H1.18C.43 8.13 0 9.87 0 12s.43 3.87 1.18 5.39l4.09-3.15z"/>
          <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.23 0 3.15 2.68 1.18 6.61l4.09 3.15c.95-2.85 3.6-4.96 6.73-4.96z"/>
        </svg>
        Sign up with Google
      </button>

      <!-- Footer Link -->
      <p class="text-xs sm:text-sm text-center text-gray-400 mt-6">
        Already have an account? 
        <router-link to="/login" class="text-[#00bbff] hover:underline font-medium">Login</router-link>
      </p>

    </div>
  </div>
</template>