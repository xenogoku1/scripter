<script setup>
import { ref } from 'vue'

defineProps({
  user: Object
})

const isRecording = ref(false)
const noiseRemoval = ref(true)
const audioEnhancer = ref(true)

const toggleRecording = () => {
  isRecording.value = !isRecording.value
}
</script>

<template>
  <div class="flex-1 flex flex-col items-center justify-center text-center max-w-2xl mx-auto my-auto py-8">
    
    <!-- Audio Studio Specific Header Text -->
    <div class="space-y-2 mb-6">
      <h1 class="text-3xl sm:text-4xl md:text-5xl font-extrabold text-lightBlue tracking-tight">
        Hello, <span class="text-neonLime">{{ user.name }}</span>
      </h1>
      <p class="text-sm sm:text-base text-lightBlue/70 font-light">
        Record clean studio audio with active background noise removal.
      </p>
    </div>

    <!-- Studio Audio Enhancer Toggles -->
    <div class="flex items-center gap-4 mb-8 bg-darkBgMid/60 border border-lightBlue/10 rounded-full px-5 py-2 backdrop-blur-md">
      <label class="flex items-center space-x-2 text-xs text-lightBlue/80 cursor-pointer">
        <input type="checkbox" v-model="noiseRemoval" class="rounded accent-neonLime bg-darkBgEnd border-lightBlue/20" />
        <span>Noise Removal</span>
      </label>
      <span class="text-lightBlue/20">|</span>
      <label class="flex items-center space-x-2 text-xs text-lightBlue/80 cursor-pointer">
        <input type="checkbox" v-model="audioEnhancer" class="rounded accent-neonLime bg-darkBgEnd border-lightBlue/20" />
        <span>Audio Enhancer</span>
      </label>
    </div>

    <!-- Concentric Acoustic Frequency Rings Visualizer -->
    <div class="relative w-64 h-64 sm:w-80 sm:h-80 flex items-center justify-center my-4">
      
      <!-- Pulsing Acoustic Pulse Rings -->
      <div 
        v-for="ring in 3" 
        :key="ring"
        :class="[
          'absolute rounded-full border border-neonLime/30 transition-all duration-700',
          isRecording ? 'animate-ping opacity-30' : 'opacity-15'
        ]"
        :style="{
          width: `${ring * 30 + 50}%`,
          height: `${ring * 30 + 50}%`,
          animationDelay: `${ring * 0.4}s`
        }"
      ></div>

      <!-- Center Studio Glowing Orb -->
      <div 
        :class="[
          'w-48 h-48 sm:w-56 sm:h-56 rounded-full border-2 border-dashed border-neonLime/40 flex items-center justify-center transition-all duration-500',
          isRecording ? 'animate-[spin_10s_linear_infinite] border-neonLime scale-110 shadow-[0_0_50px_rgba(140,255,0,0.3)]' : 'animate-[spin_30s_linear_infinite]'
        ]"
      >
        <div class="w-36 h-36 sm:w-44 sm:h-44 rounded-full bg-neonLime/5 border border-appBlue/30 flex items-center justify-center"></div>
      </div>

      <!-- Studio Mic Button -->
      <button 
        @click="toggleRecording"
        :class="[
          'absolute z-20 w-20 h-20 sm:w-24 sm:h-24 rounded-full flex items-center justify-center transition-all duration-300 shadow-2xl group border',
          isRecording 
            ? 'bg-red-500 border-red-400 text-white shadow-red-500/40 animate-pulse scale-105' 
            : 'bg-neonLime border-neonLime/50 text-darkBgEnd shadow-neonLime/20 hover:scale-110'
        ]"
      >
        <svg class="w-8 h-8 sm:w-10 sm:h-10 transition-transform duration-200 group-hover:scale-110" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"></path>
          <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"></path>
        </svg>
      </button>

    </div>

    <!-- Status Text -->
    <p class="mt-4 text-xs tracking-widest uppercase font-semibold text-lightBlue/50">
      {{ isRecording ? 'Studio recording active...' : 'Tap mic to record studio audio' }}
    </p>

  </div>
</template>