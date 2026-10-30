<script setup>
import { ref } from 'vue'

const isRecording = ref(false)
const scriptText = ref("So, today we're going to talk about Dragon Ball Super...")

const toggleRecording = () => {
  isRecording.value = !isRecording.value
}
</script>

<template>
  <main class="min-h-screen flex flex-col items-center justify-center p-6">
    <div class="w-full max-w-3xl bg-darkBgStart/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6 shadow-2xl relative overflow-hidden">
      
      <!-- Header -->
      <div class="flex justify-between items-center mb-6 border-b border-white/10 pb-4">
        <div>
          <h1 class="text-xl font-bold tracking-wide text-white">
            TalkScript <span class="text-neonLime text-xs px-2 py-0.5 bg-neonLime/10 rounded-full border border-neonLime/20">Dashboard</span>
          </h1>
          <p class="text-xs text-gray-400">Voice-first YouTube script editor</p>
        </div>
        
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full" :class="isRecording ? 'bg-red-500 animate-pulse' : 'bg-gray-500'"></span>
            <span class="text-xs text-gray-300 font-medium">{{ isRecording ? 'Recording...' : 'Idle' }}</span>
          </div>
          <router-link to="/" class="text-xs text-red-400 hover:underline">Logout</router-link>
        </div>
      </div>

      <!-- Script Editor Area -->
      <div class="mb-6">
        <label class="block text-xs uppercase tracking-wider text-gray-400 mb-2">Your Script</label>
        <textarea 
          v-model="scriptText"
          rows="8"
          class="w-full bg-black/40 border border-white/10 rounded-xl p-4 text-gray-200 focus:outline-none focus:border-neonLime/50 transition-all resize-none leading-relaxed text-sm"
          placeholder="Your speech will appear here..."
        ></textarea>
      </div>

      <!-- Controls -->
      <div class="flex items-center justify-between">
        <button 
          @click="toggleRecording"
          :class="isRecording ? 'bg-red-500/20 text-red-400 border-red-500/50 hover:bg-red-500/30' : 'bg-neonLime text-black hover:bg-neonLime/90 shadow-[0_0_20px_rgba(140,255,0,0.3)]'"
          class="px-6 py-3 rounded-xl font-semibold text-sm transition-all flex items-center gap-2 border border-transparent cursor-pointer"
        >
          {{ isRecording ? 'Stop Recording' : 'Start Recording' }}
        </button>

        <span class="text-xs text-gray-500">Router & Navigation Active</span>
      </div>

    </div>
  </main>
</template>