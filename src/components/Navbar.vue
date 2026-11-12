<script setup>
import { ref } from 'vue'
import { useTheme } from '@/composables/useTheme'

defineProps({
  activeTab: String
})

defineEmits(['update:activeTab'])

const { currentTheme, setTheme } = useTheme()
const isThemeMenuOpen = ref(false)

const themes = [
  { id: 'default', name: 'Default Tech', color: '#8CFF00' },
  { id: 'crimson', name: 'Crimson Noir', color: '#C50337' },
  { id: 'midnight', name: 'Electric Midnight', color: '#00BBFF' },
  { id: 'slate', name: 'Slate Noir', color: '#ffffff' },
  { id: 'espresso', name: 'Gilded Espresso', color: '#FFEB97' },
  { id: 'emerald', name: 'Monestra Emerald', color: '#06D6A0' }
]
</script>

<template>
  <header class="w-full max-w-xl mx-auto z-50 px-2 pt-2">
    <nav class="relative flex items-center justify-between bg-darkBgMid/80 backdrop-blur-xl border border-lightBlue/10 rounded-full px-3 py-2 shadow-2xl">
      
      <!-- Left: Logo & Branding -->
      <div class="flex items-center space-x-2 pl-1">
        <div class="w-7 h-7 rounded-full bg-neonLime/10 flex items-center justify-center border border-neonLime/30">
          <svg class="w-3.5 h-3.5 text-neonLime" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M20.24 12.24a6 6 0 0 0-8.49-8.49L3 13.5V21h7.5L20.24 12.24z"></path>
            <line x1="16" y1="8" x2="2" y2="22"></line>
          </svg>
        </div>
        <span class="font-bold text-sm tracking-wide text-lightBlue hidden sm:inline">scripter</span>
      </div>

      <!-- Center: Navigation Tabs -->
      <div class="flex items-center space-x-1 bg-darkBgEnd/60 rounded-full p-1 border border-lightBlue/5">
        <button 
          @click="$emit('update:activeTab', 'transcribe')"
          :class="[
            'flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-medium transition-all duration-200',
            activeTab === 'transcribe' ? 'bg-neonLime text-darkBgEnd shadow-md font-semibold' : 'text-lightBlue/70 hover:text-lightBlue'
          ]"
        >
          <span>Transcribe</span>
        </button>

        <button 
          @click="$emit('update:activeTab', 'recorder')"
          :class="[
            'flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-medium transition-all duration-200',
            activeTab === 'recorder' ? 'bg-neonLime text-darkBgEnd shadow-md font-semibold' : 'text-lightBlue/70 hover:text-lightBlue'
          ]"
        >
          <span>Studio</span>
        </button>

        <button 
          @click="$emit('update:activeTab', 'settings')"
          :class="[
            'flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-medium transition-all duration-200',
            activeTab === 'settings' ? 'bg-neonLime text-darkBgEnd shadow-md font-semibold' : 'text-lightBlue/70 hover:text-lightBlue'
          ]"
        >
          <span>Settings</span>
        </button>
      </div>

      <!-- Right: Theme Switcher Dropdown (Properly contained) -->
      <div class="relative">
        <button 
          @click="isThemeMenuOpen = !isThemeMenuOpen" 
          class="p-2 rounded-full bg-darkBgEnd/80 border border-lightBlue/10 hover:border-neonLime/50 transition-all text-neonLime flex items-center justify-center"
          title="Switch Mood Theme"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path>
          </svg>
        </button>

        <div 
          v-if="isThemeMenuOpen" 
          @click.outside="isThemeMenuOpen = false"
          class="absolute right-0 mt-2 w-44 bg-darkBgMid border border-lightBlue/15 rounded-2xl shadow-2xl p-2 z-[9999] space-y-1 backdrop-blur-xl"
        >
          <p class="text-[9px] uppercase font-bold tracking-wider text-lightBlue/40 px-3 py-1">Select Atmosphere</p>
          <button 
            v-for="t in themes" 
            :key="t.id"
            @click="setTheme(t.id); isThemeMenuOpen = false"
            :class="[
              'w-full flex items-center justify-between px-3 py-1.5 rounded-xl text-xs font-medium transition-all',
              currentTheme === t.id ? 'bg-neonLime/15 text-neonLime border border-neonLime/30' : 'text-lightBlue/80 hover:bg-darkBgEnd/50 hover:text-lightBlue'
            ]"
          >
            <span>{{ t.name }}</span>
            <span class="w-3 h-3 rounded-full border border-white/20" :style="{ backgroundColor: t.color }"></span>
          </button>
        </div>
      </div>

    </nav>
  </header>
</template>