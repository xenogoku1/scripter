<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from '@/composables/useTheme'
// Note: We don't strictly need the supabase client here anymore unless you use it elsewhere, 
// but you can leave or remove the import as you prefer.
import Navbar from '@/components/Navbar.vue'
import TranscribeWorkspace from '@/components/TranscribeWorkspace.vue'
import StudioWorkspace from '@/components/StudioWorkspace.vue'
import SettingsWorkspace from '@/components/SettingsWorkspace.vue'

const { currentTheme } = useTheme()
const activeTab = ref('transcribe')

// Dynamic user state initialized with a clean fallback
const user = ref({ name: 'User' })

const router = useRouter()

onMounted(() => {
  // 1. Handle Supabase OAuth tokens from the URL hash if present (for Google login)
  const hash = window.location.hash
  if (hash && hash.includes('access_token')) {
    const params = new URLSearchParams(hash.replace('#', '?'))
    const accessToken = params.get('access_token')
    
    if (accessToken) {
      localStorage.setItem('access_token', accessToken)
      localStorage.setItem('scripter_username', 'User') // Fallback for OAuth
      // Clean up the URL hash so it looks clean
      window.history.replaceState({}, document.title, window.location.pathname)
    }
  }

  // 2. Load the saved username from localStorage (saved during custom backend login)
  const savedName = localStorage.getItem('scripter_username')
  if (savedName) {
    user.value = { name: savedName }
  }
})
</script>

<template>
  <div class="relative min-h-screen flex flex-col justify-between overflow-hidden px-4 py-6 md:px-8">
    
    <!-- Floating Navbar Component -->
    <Navbar v-model:activeTab="activeTab" />

    <!-- Dynamic Workspace Views -->
    <TranscribeWorkspace v-if="activeTab === 'transcribe'" :user="user" />
    <StudioWorkspace v-else-if="activeTab === 'recorder'" :user="user" />
    <SettingsWorkspace v-else-if="activeTab === 'settings'" :user="user" />

    <!-- Workspace Footer -->
    <footer class="w-full max-w-4xl mx-auto text-center py-2 text-[11px] text-lightBlue/30">
      Scripter Workspace • Theme: <span class="text-neonLime capitalize">{{ currentTheme }}</span>
    </footer>

  </div>
</template>