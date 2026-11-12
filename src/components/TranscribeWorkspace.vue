<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

defineProps({
  user: Object
})

const isRecording = ref(false)

const toggleRecording = () => {
  isRecording.value = !isRecording.value
}

/* ---------- Morphing wave strands ---------- */
const STRANDS = 9
const POINTS = 120
const strands = ref(Array.from({ length: STRANDS }, () => ''))

let raf = 0
let last = 0
let t = 0
let speed = 0.4

const buildPath = (t, i) => {
  const p = i * 0.22 // phase offset per strand = the crossing/ribbon effect
  let d = ''
  for (let n = 0; n <= POINTS; n++) {
    const a = (n / POINTS) * Math.PI * 2
    const r =
      52 +
      7 * Math.sin(4 * a + t + p) +
      5 * Math.sin(3 * a - t * 1.3 + p * 1.5) +
      4 * Math.sin(2 * a + t * 0.7 - p)
    d += `${n ? 'L' : 'M'}${(100 + r * Math.cos(a)).toFixed(1)},${(100 + r * Math.sin(a)).toFixed(1)}`
  }
  return d + 'Z'
}

const render = () => {
  strands.value = strands.value.map((_, i) => buildPath(t, i))
}

const frame = (now) => {
  const dt = Math.min((now - last) / 1000, 0.05)
  last = now
  // ~0.4 rad/s idle, ~1.6 rad/s recording, eased between the two
  const target = isRecording.value ? 1.6 : 0.4
  speed += (target - speed) * 0.06
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

onBeforeUnmount(() => cancelAnimationFrame(raf))
</script>

<template>
  <div class="flex-1 flex flex-col justify-between items-center max-w-md mx-auto w-full py-6 px-4">

    <!-- 1. TOP HEADER SECTION -->
    <div class="text-left w-full space-y-1 mt-2">
      <h1 class="text-3xl sm:text-4xl font-extrabold text-lightBlue tracking-tight">
        Hello, <span class="text-neonLime">{{ user.name }}</span>
      </h1>
      <p class="text-xs sm:text-sm text-lightBlue/70 font-light">
        What shall we record today? Save time with smart voice transcription.
      </p>
    </div>

    <!-- 2. MIDDLE: MORPHING GLOWING WAVE VISUALIZER (1.4x size, theme-aware) -->
    <div class="relative w-full max-w-[358px] sm:max-w-[403px] aspect-square flex items-center justify-center my-auto">

      <!-- Ambient Glow Backdrop (uses theme accent) -->
      <div
        :class="[
          'absolute inset-0 rounded-full filter blur-3xl opacity-20 transition-all duration-700 bg-neonLime',
          isRecording ? 'scale-125 opacity-40 animate-pulse' : 'scale-100'
        ]"
      ></div>

      <!-- Multi-strand morphing ribbon ring -->
      <svg viewBox="0 0 200 200" class="absolute inset-0 w-full h-full overflow-visible">
        <defs>
          <!-- Gradient reads the active theme's CSS variables -->
          <linearGradient id="ringGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" style="stop-color: var(--light-blue); transition: stop-color 0.4s ease" />
            <stop offset="50%" style="stop-color: var(--neon-lime); transition: stop-color 0.4s ease" />
            <stop offset="100%" style="stop-color: var(--app-blue); transition: stop-color 0.4s ease" />
          </linearGradient>
          <filter id="glowSoft" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="5" />
          </filter>
        </defs>

        <!-- soft glow layer -->
        <g filter="url(#glowSoft)" opacity="0.85">
          <path
            v-for="(d, i) in strands"
            :key="'g' + i"
            :d="d"
            fill="none"
            stroke="url(#ringGrad)"
            stroke-width="3"
          />
        </g>

        <!-- crisp thin strands -->
        <g style="mix-blend-mode: screen">
          <path
            v-for="(d, i) in strands"
            :key="'s' + i"
            :d="d"
            fill="none"
            stroke="url(#ringGrad)"
            :stroke-width="i % 3 === 0 ? 1.1 : 0.6"
            :opacity="0.35 + (i % 4) * 0.18"
          />
        </g>
      </svg>

    </div>

    <!-- 3. BOTTOM: RECORD ACTION PILL BUTTON -->
    <div class="w-full pb-4">
      <button
        @click="toggleRecording"
        :class="[
          'w-full flex items-center justify-between p-2.5 rounded-full border shadow-2xl transition-all duration-300 group',
          isRecording
            ? 'bg-red-500/90 border-red-400 text-white shadow-red-500/30'
            : 'bg-darkBgMid/80 border-lightBlue/15 hover:border-neonLime/50 text-lightBlue'
        ]"
      >
        <!-- Circular Mic Icon Badge -->
        <div :class="[
          'w-12 h-12 rounded-full flex items-center justify-center transition-transform duration-200 group-hover:scale-105 shadow-md',
          isRecording ? 'bg-white text-red-600' : 'bg-neonLime text-darkBgEnd'
        ]">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"></path>
            <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"></path>
          </svg>
        </div>

        <!-- Center Label Text -->
        <span class="font-semibold text-sm tracking-wide px-4">
          {{ isRecording ? 'Recording active...' : 'Start Transcription' }}
        </span>

        <!-- Right Arrow Indicator -->
        <div class="w-10 h-10 rounded-full flex items-center justify-center bg-darkBgEnd/50 border border-lightBlue/10 mr-1 text-lightBlue/70 group-hover:text-neonLime">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
          </svg>
        </div>
      </button>
    </div>

  </div>
</template>