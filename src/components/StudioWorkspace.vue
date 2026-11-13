<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

defineProps({
  user: Object
})

const isRecording = ref(false)
const isPaused = ref(false)
const noiseRemoval = ref(true)
const audioEnhancer = ref(true)

// Side panel drawer state for saved raw audio clips
const isDrawerOpen = ref(false)

// Mock saved audio clips history
const savedAudioClips = ref([
  { id: 1, title: 'Studio Master - Voiceover Take 1', date: 'Today, 3:15 PM', duration: '04:20', size: '4.2 MB' },
  { id: 2, title: 'Podcast Intro Track Clean', date: 'Yesterday', duration: '01:45', size: '1.8 MB' },
  { id: 3, title: 'Commercial Raw Stem', date: 'Nov 08', duration: '02:50', size: '2.9 MB' }
])

/* ---------- Recording timer ---------- */
const elapsed = ref(0) // seconds since record was pressed
let timerId = 0
let startedAt = 0
let totalPausedSeconds = 0
let pauseStartedAt = 0

const timeLabel = computed(() => {
  const s = elapsed.value
  const h = String(Math.floor(s / 3600)).padStart(2, '0')
  const m = String(Math.floor((s % 3600) / 60)).padStart(2, '0')
  const sec = String(s % 60).padStart(2, '0')
  return `${h}:${m}:${sec}`
})

const toggleRecording = () => {
  if (!isRecording.value) {
    // Start Recording
    isRecording.value = true
    isPaused.value = false
    startedAt = Date.now()
    totalPausedSeconds = 0
    elapsed.value = 0
    clearInterval(timerId)
    timerId = setInterval(() => {
      if (!isPaused.value) {
        elapsed.value = Math.floor((Date.now() - startedAt - totalPausedSeconds) / 1000)
      }
    }, 250)
  } else {
    // Stop & Complete Session
    isRecording.value = false
    isPaused.value = false
    clearInterval(timerId)
    elapsed.value = 0
  }
}

const togglePause = () => {
  if (!isRecording.value) return
  if (isPaused.value) {
    // Resume
    totalPausedSeconds += (Date.now() - pauseStartedAt)
    isPaused.value = false
  } else {
    // Pause
    pauseStartedAt = Date.now()
    isPaused.value = true
  }
}

/* ---------- Studio visualizer: orbital ribbons + radial spectrum ---------- */
const RIBBONS = 14   // interlocking orbital strands
const POINTS = 90    // smoothness of each strand
const BARS = 72      // radial spectrum bars around the outside

const ribbons = ref(Array.from({ length: RIBBONS }, () => ''))
const bars = ref('')
const ringDeg = ref(0)

let raf = 0
let last = 0
let t = 0
let speed = 0.35 // spin/morph speed (eased)
let amp = 0.15   // spectrum intensity (eased)

const buildRibbon = (t, i) => {
  const th = (i * Math.PI) / RIBBONS + t * 0.25         
  const squash = 0.62 + 0.25 * Math.sin(t * 1.2 + i * 0.6) 
  const R = 74 + 4 * Math.sin(t * 0.9 + i)
  const c = Math.cos(th)
  const s = Math.sin(th)
  let d = ''
  for (let n = 0; n <= POINTS; n++) {
    const a = (n / POINTS) * Math.PI * 2
    const wob = 1 + 0.06 * Math.sin(3 * a + t * 1.5 + i) 
    const x = R * wob * Math.cos(a)
    const y = R * wob * squash * Math.sin(a)
    const px = 100 + x * c - y * s
    const py = 100 + x * s + y * c
    d += `${n ? 'L' : 'M'}${px.toFixed(1)},${py.toFixed(1)}`
  }
  return d + 'Z'
}

const buildBars = (t) => {
  const inner = 88
  let d = ''
  for (let k = 0; k < BARS; k++) {
    const a = (k / BARS) * Math.PI * 2
    const level =
      Math.abs(Math.sin(k * 0.35 + t * 3) * Math.sin(k * 0.11 - t * 2.1)) * 0.7 +
      Math.abs(Math.sin(k * 1.7 + t * 5)) * 0.3
    const len = 2 + level * amp * 13
    const cx = Math.cos(a)
    const sy = Math.sin(a)
    d += `M${(100 + cx * inner).toFixed(1)},${(100 + sy * inner).toFixed(1)}`
    d += `L${(100 + cx * (inner + len)).toFixed(1)},${(100 + sy * (inner + len)).toFixed(1)}`
  }
  return d
}

const render = () => {
  ribbons.value = ribbons.value.map((_, i) => buildRibbon(t, i))
  bars.value = buildBars(t)
  ringDeg.value = -t * 18
}

const frame = (now) => {
  const dt = Math.min((now - last) / 1000, 0.05)
  last = now
  const targetSpeed = isRecording.value && !isPaused.value ? 1.4 : 0.35
  const targetAmp = isRecording.value && !isPaused.value ? 1 : 0.15
  speed += (targetSpeed - speed) * 0.05
  amp += (targetAmp - amp) * 0.06
  t += dt * speed
  render()
  raf = requestAnimationFrame(frame)
}

onMounted(() => {
  render()
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
  last = performance.now()
  raf = requestAnimationFrame(frame)
})

onBeforeUnmount(() => {
  cancelAnimationFrame(raf)
  clearInterval(timerId)
})
</script>

<template>
  <div class="flex-1 flex flex-col items-center justify-center text-center max-w-2xl mx-auto my-auto py-8 relative">

    <!-- SIDE PANEL DRAWER FOR SAVED AUDIO CLIPS -->
    <div v-if="isDrawerOpen" class="fixed inset-0 z-50 flex">
      <!-- Backdrop -->
      <div @click="isDrawerOpen = false" class="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity"></div>
      
      <!-- Drawer Content -->
      <div class="relative w-80 max-w-full bg-darkBgMid border-r border-lightBlue/15 shadow-2xl p-5 flex flex-col z-10 h-full text-left">
        <div class="flex items-center justify-between pb-4 border-b border-lightBlue/10">
          <h3 class="font-bold text-sm text-lightBlue flex items-center gap-2">
            <svg class="w-4 h-4 text-neonLime" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
            </svg>
            Saved Audio Recordings
          </h3>
          <button @click="isDrawerOpen = false" class="p-1 rounded-full text-lightBlue/60 hover:text-lightBlue hover:bg-white/5">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <!-- List of Audio Clips -->
        <div class="flex-1 overflow-y-auto py-4 space-y-3">
          <div v-for="clip in savedAudioClips" :key="clip.id" class="p-3 bg-darkBgEnd/70 border border-lightBlue/10 rounded-xl hover:border-neonLime/40 transition-all cursor-pointer group">
            <div class="flex items-center justify-between mb-1">
              <h4 class="text-xs font-semibold text-lightBlue group-hover:text-neonLime transition-colors">{{ clip.title }}</h4>
              <span class="text-[10px] font-mono text-neonLime">{{ clip.duration }}</span>
            </div>
            <div class="flex items-center justify-between mt-2 text-[9px] text-lightBlue/40">
              <span>{{ clip.date }}</span>
              <span>{{ clip.size }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

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
    <div class="flex items-center gap-4 mb-6 bg-darkBgMid/60 border border-lightBlue/10 rounded-full px-5 py-2 backdrop-blur-md">
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

    <!-- Recording timer -->
    <div
      :class="[
        'flex items-center gap-2 font-mono tabular-nums text-lg sm:text-xl tracking-widest transition-all duration-500 mb-2',
        isRecording ? 'text-neonLime opacity-100' : 'text-lightBlue/30 opacity-70'
      ]"
    >
      <span
        :class="[
          'w-2 h-2 rounded-full transition-colors duration-300',
          isRecording ? (isPaused ? 'bg-amber-400' : 'bg-red-500 animate-pulse') : 'bg-lightBlue/20'
        ]"
      ></span>
      {{ isPaused ? 'Paused — ' + timeLabel : timeLabel }}
    </div>

    <!-- Orbital Ribbon + Radial Spectrum Visualizer Container -->
    <div class="relative w-72 h-72 sm:w-96 sm:h-96 flex items-center justify-center my-2">

      <!-- Ambient glow -->
      <div
        :class="[
          'absolute inset-6 rounded-full filter blur-3xl bg-neonLime transition-all duration-700',
          isRecording && !isPaused ? 'opacity-35 scale-110 animate-pulse' : 'opacity-15 scale-100'
        ]"
      ></div>

      <!-- Sonar ripples while recording -->
      <div
        v-for="ring in 3"
        :key="ring"
        :class="[
          'absolute rounded-full border border-neonLime/30 transition-opacity duration-700',
          isRecording && !isPaused ? 'animate-ping opacity-30' : 'opacity-0'
        ]"
        :style="{
          width: (ring * 15 + 55) + '%',
          height: (ring * 15 + 55) + '%',
          animationDelay: (ring * 0.4) + 's'
        }"
      ></div>

      <svg viewBox="0 0 200 200" class="absolute inset-0 w-full h-full overflow-visible">
        <defs>
          <linearGradient id="studioGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" style="stop-color: var(--light-blue); transition: stop-color 0.4s ease" />
            <stop offset="50%" style="stop-color: var(--neon-lime); transition: stop-color 0.4s ease" />
            <stop offset="100%" style="stop-color: var(--app-blue); transition: stop-color 0.4s ease" />
          </linearGradient>
          <filter id="studioGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="4" />
          </filter>
        </defs>

        <g filter="url(#studioGlow)" opacity="0.8">
          <path
            v-for="(d, i) in ribbons"
            :key="'g' + i"
            :d="d"
            fill="none"
            stroke="url(#studioGrad)"
            stroke-width="2.5"
          />
        </g>

        <g style="mix-blend-mode: screen">
          <path
            v-for="(d, i) in ribbons"
            :key="'r' + i"
            :d="d"
            fill="none"
            stroke="url(#studioGrad)"
            :stroke-width="i % 2 === 0 ? 0.9 : 0.5"
            :opacity="0.45 + (i % 3) * 0.2"
          />
        </g>

        <circle
          cx="100" cy="100" r="84"
          fill="none"
          stroke="url(#studioGrad)"
          stroke-width="0.6"
          stroke-dasharray="1.5 5"
          stroke-linecap="round"
          opacity="0.7"
          :transform="'rotate(' + ringDeg + ' 100 100)'"
        />

        <path
          :d="bars"
          fill="none"
          stroke="url(#studioGrad)"
          stroke-width="1.6"
          stroke-linecap="round"
          opacity="0.95"
        />
      </svg>

      <!-- Center Studio Mic Button -->
      <button
        @click="toggleRecording"
        :class="[
          'absolute z-20 w-20 h-20 sm:w-24 sm:h-24 rounded-full flex items-center justify-center transition-all duration-300 shadow-2xl group border',
          isRecording
            ? 'bg-red-500 border-red-400 text-white shadow-red-500/40 animate-pulse scale-105'
            : 'bg-neonLime border-neonLime/50 text-darkBgEnd shadow-neonLime/20 hover:scale-110'
        ]"
        :title="isRecording ? 'Stop Recording' : 'Start Studio Recording'"
      >
        <svg class="w-8 h-8 sm:w-10 sm:h-10 transition-transform duration-200 group-hover:scale-110" fill="currentColor" viewBox="0 0 24 24">
          <path v-if="!isRecording" d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"></path>
          <path v-if="!isRecording" d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"></path>
          <rect v-if="isRecording" x="7" y="7" width="10" height="10" rx="2"></rect>
        </svg>
      </button>

    </div>

    <!-- BOTTOM CONTROLS: DRAWER TOGGLE & PAUSE BUTTON -->
    <div class="flex items-center gap-4 mt-2">
      <!-- Left Side: History Drawer Toggle Button -->
      <button
        @click="isDrawerOpen = true"
        class="w-12 h-12 rounded-full bg-darkBgMid/80 border border-lightBlue/15 hover:border-neonLime/50 text-lightBlue flex items-center justify-center shadow-xl transition-all hover:scale-105 group"
        title="View Saved Audio Recordings"
      >
        <svg class="w-5 h-5 text-lightBlue/80 group-hover:text-neonLime transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
        </svg>
      </button>

      <!-- Right Side: Pause / Resume Button (Only visible while recording) -->
      <button
        v-if="isRecording"
        @click="togglePause"
        class="w-12 h-12 rounded-full bg-darkBgMid/80 border border-lightBlue/15 hover:border-amber-400 text-lightBlue flex items-center justify-center shadow-xl transition-all hover:scale-105 group"
        :title="isPaused ? 'Resume Recording' : 'Pause Recording'"
      >
        <svg v-if="isPaused" class="w-5 h-5 text-amber-400" fill="currentColor" viewBox="0 0 24 24">
          <path d="M8 5v14l11-7z"></path>
        </svg>
        <svg v-else class="w-5 h-5 text-lightBlue/80 group-hover:text-amber-400" fill="currentColor" viewBox="0 0 24 24">
          <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"></path>
        </svg>
      </button>
    </div>

    <!-- Status Text -->
    <p class="mt-4 text-xs tracking-widest uppercase font-semibold text-lightBlue/50">
      {{ isRecording ? (isPaused ? 'Studio recording paused' : 'Studio recording active...') : 'Tap mic to record studio audio' }}
    </p>

  </div>
</template>