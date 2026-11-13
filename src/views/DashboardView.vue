<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from '@/composables/useTheme'
import Navbar from '@/components/Navbar.vue'
import TranscribeWorkspace from '@/components/TranscribeWorkspace.vue'
import StudioWorkspace from '@/components/StudioWorkspace.vue'
import SettingsWorkspace from '@/components/SettingsWorkspace.vue'

const { currentTheme } = useTheme()
const activeTab = ref('transcribe')

// User context (Connects to Supabase Auth state later)
const user = ref({ name: 'Alex' })

const router = useRouter()

onMounted(() => {
  // Supabase stores tokens in the URL hash after OAuth redirects
  const hash = window.location.hash
  if (hash && hash.includes('access_token')) {
    const params = new URLSearchParams(hash.replace('#', '?'))
    const accessToken = params.get('access_token')
    
    if (accessToken) {
      localStorage.setItem('access_token', accessToken)
      // Clean up the URL hash so it looks clean
      window.history.replaceState({}, document.title, window.location.pathname)
    }
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