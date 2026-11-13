<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

defineProps({
  user: Object
})

/* ---------- Recording & Pause State ---------- */
const isRecording = ref(false)
const isPaused = ref(false)
const isStarting = ref(false)
const micError = ref('')
const elapsed = ref(0) // seconds recorded

// Side panel drawer state for saved transcripts
const isDrawerOpen = ref(false)

// Mock saved transcripts history (ready to connect to Supabase/Backend later)
const savedTranscripts = ref([
  { id: 1, title: 'YouTube Tech Review Draft', date: 'Today, 2:45 PM', duration: '03:42', preview: 'Welcome back to the channel, today we are looking at...' },
  { id: 2, title: 'Podcast Episode 14 - AI Trends', date: 'Yesterday', duration: '12:15', preview: 'In this episode we discuss the rapid evolution of...' },
  { id: 3, title: 'Quick Voice Memo', date: 'Nov 10', duration: '01:05', preview: 'Remember to check the deployment logs on Render...' }
])

const timeLabel = computed(() => {
  const s = elapsed.value
  const h = String(Math.floor(s / 3600)).padStart(2, '0')
  const m = String(Math.floor((s % 3600) / 60)).padStart(2, '0')
  const sec = String(s % 60).padStart(2, '0')
  return `${h}:${m}:${sec}`
})

/* ---------- Microphone analysis ---------- */
let stream = null
let audioCtx = null
let source = null
let analyser = null
let timeData = null
let freqData = null
let timerId = 0
let startedAt = 0
let totalPausedSeconds = 0
let pauseStartedAt = 0

const level = ref(0) 
const pitch = ref(0) 
const rec = ref(0)   

const startMic = async () => {
  stream = await navigator.mediaDevices.getUserMedia({
    audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true }
  })
  audioCtx = new (window.AudioContext || window.webkitAudioContext)()
  if (audioCtx.state === 'suspended') await audioCtx.resume()
  analyser = audioCtx.createAnalyser()
  analyser.fftSize = 1024
  analyser.smoothingTimeConstant = 0.5
  source = audioCtx.createMediaStreamSource(stream)
  source.connect(analyser)
  timeData = new Uint8Array(analyser.fftSize)
  freqData = new Uint8Array(analyser.frequencyBinCount)
}

const stopMic = () => {
  if (stream) stream.getTracks().forEach((tr) => tr.stop())
  if (source) source.disconnect()
  if (audioCtx && audioCtx.state !== 'closed') audioCtx.close()
  stream = audioCtx = source = analyser = timeData = freqData = null
}

const analyse = () => {
  if (!analyser || isPaused.value) {
    level.value *= 0.9 
    return
  }

  analyser.getByteTimeDomainData(timeData)
  let sum = 0
  for (let i = 0; i < timeData.length; i++) {
    const x = (timeData[i] - 128) / 128
    sum += x * x
  }
  const rms = Math.sqrt(sum / timeData.length)
  const target = Math.min(1, Math.max(0, (rms - 0.015) * 6))
  level.value += (target - level.value) * (target > level.value ? 0.45 : 0.1)

  if (target > 0.08) {
    analyser.getByteFrequencyData(freqData)
    const binHz = audioCtx.sampleRate / analyser.fftSize
    const lo = Math.floor(80 / binHz)
    const hi = Math.min(freqData.length, Math.ceil(4000 / binHz))
    let num = 0
    let den = 0
    for (let i = lo; i < hi; i++) {
      num += i * binHz * freqData[i]
      den += freqData[i]
    }
    if (den > 0) {
      const centroid = num / den
      const norm = Math.min(1, Math.max(0, Math.log2(centroid / 150) / Math.log2(2500 / 150)))
      pitch.value += (norm - pitch.value) * 0.08
    }
  }
}

const toggleRecording = async () => {
  if (isStarting.value) return
  micError.value = ''

  if (!isRecording.value) {
    // Start Recording
    isStarting.value = true
    try {
      await startMic()
      isRecording.value = true
      isPaused.value = false
      startedAt = Date.now()
      totalPausedSeconds = 0
      elapsed.value = 0
      timerId = setInterval(() => {
        if (!isPaused.value) {
          elapsed.value = Math.floor((Date.now() - startedAt - totalPausedSeconds) / 1000)
        }
      }, 250)
    } catch (err) {
      stopMic()
      micError.value = err && err.name === 'NotAllowedError'
        ? 'Microphone access was blocked. Allow it in your browser settings.'
        : 'Could not start the microphone on this device.'
    } finally {
      isStarting.value = false
    }
  } else {
    // Stop & Complete Recording session
    isRecording.value = false
    isPaused.value = false
    clearInterval(timerId)
    stopMic()
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

/* ---------- Morphing wave strands ---------- */
const STRANDS = 14
const CORE = 9 
const POINTS = 120
const strands = ref(Array.from({ length: STRANDS }, () => ''))

let raf = 0
let last = 0
let t = 0
let speed = 0.4

const buildPath = (t, i) => {
  const r0 = rec.value
  const lv = level.value
  const pt = pitch.value

  const p = i * (0.22 + r0 * 0.2)                        
  const gain = 1 + lv * 1.4                            
  const base = 52 + r0 * 14 + lv * 8                       
  const fan = (i - (STRANDS - 1) / 2) * 0.7 * r0 * (1 + lv) 

  let d = ''
  for (let n = 0; n <= POINTS; n++) {
    const a = (n / POINTS) * Math.PI * 2
    const r =
      base +
      fan +
      gain *
        (7 * ((1 - pt) * Math.sin(4 * a + t + p) + pt * Math.sin(6 * a - t * 1.2 + p)) + 
          5 * Math.sin(3 * a - t * 1.3 + p * 1.5) +
          4 * Math.sin(2 * a + t * 0.7 - p))
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

  analyse()
  rec.value += ((isRecording.value && !isPaused.value ? 1 : 0) - rec.value) * 0.05

  const target = 0.4 + rec.value * 0.5 + level.value * 1.8
  speed += (target - speed) * 0.08
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
  stopMic()
})
</script>

<template>
  <div class="flex-1 flex flex-col justify-between items-center max-w-md mx-auto w-full py-6 px-4 relative">

    <!-- SIDE PANEL DRAWER FOR SAVED TRANSCRIPTS -->
    <div v-if="isDrawerOpen" class="fixed inset-0 z-50 flex">
      <!-- Backdrop -->
      <div @click="isDrawerOpen = false" class="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity"></div>
      
      <!-- Drawer Content -->
      <div class="relative w-80 max-w-full bg-darkBgMid border-r border-lightBlue/15 shadow-2xl p-5 flex flex-col z-10 h-full">
        <div class="flex items-center justify-between pb-4 border-b border-lightBlue/10">
          <h3 class="font-bold text-sm text-lightBlue flex items-center gap-2">
            <svg class="w-4 h-4 text-neonLime" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
            </svg>
            Saved Transcripts
          </h3>
          <button @click="isDrawerOpen = false" class="p-1 rounded-full text-lightBlue/60 hover:text-lightBlue hover:bg-white/5">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <!-- List of Transcripts -->
        <div class="flex-1 overflow-y-auto py-4 space-y-3">
          <div v-for="item in savedTranscripts" :key="item.id" class="p-3 bg-darkBgEnd/70 border border-lightBlue/10 rounded-xl hover:border-neonLime/40 transition-all cursor-pointer group">
            <div class="flex items-center justify-between mb-1">
              <h4 class="text-xs font-semibold text-lightBlue group-hover:text-neonLime transition-colors">{{ item.title }}</h4>
              <span class="text-[10px] font-mono text-neonLime">{{ item.duration }}</span>
            </div>
            <p class="text-[11px] text-lightBlue/60 line-clamp-2 mb-2">{{ item.preview }}</p>
            <span class="text-[9px] text-lightBlue/40">{{ item.date }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 1. TOP HEADER SECTION -->
    <div class="relative z-10 text-left w-full space-y-1 mt-2">
      <h1 class="text-3xl sm:text-4xl font-extrabold text-lightBlue tracking-tight">
        Hello, <span class="text-neonLime">{{ user.name }}</span>
      </h1>
      <p class="text-xs sm:text-sm text-lightBlue/70 font-light">
        What shall we record today? Save time with smart voice transcription.
      </p>
    </div>

    <!-- 2. MIDDLE: VOICE-REACTIVE GLOWING WAVE VISUALIZER -->
    <div class="relative w-full max-w-[358px] sm:max-w-[403px] aspect-square flex items-center justify-center my-auto">

      <!-- Ambient Glow Backdrop -->
      <div
        class="absolute inset-0 rounded-full filter blur-3xl bg-neonLime pointer-events-none"
        :style="{
          transform: `scale(${1 + rec * 0.25 + level * 0.35})`,
          opacity: 0.2 + rec * 0.12 + level * 0.25
        }"
      ></div>

      <!-- Multi-strand morphing ribbon ring -->
      <svg viewBox="0 0 200 200" class="absolute inset-0 w-full h-full overflow-visible pointer-events-none">
        <defs>
          <linearGradient id="ringGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" style="stop-color: var(--light-blue); transition: stop-color 0.4s ease" />
            <stop offset="50%" style="stop-color: var(--neon-lime); transition: stop-color 0.4s ease" />
            <stop offset="100%" style="stop-color: var(--app-blue); transition: stop-color 0.4s ease" />
          </linearGradient>
          <filter id="glowSoft" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="5" />
          </filter>
        </defs>

        <g filter="url(#glowSoft)" opacity="0.85">
          <path
            v-for="(d, i) in strands"
            :key="'g' + i"
            :d="d"
            fill="none"
            stroke="url(#ringGrad)"
            :stroke-width="3 + rec * 1.5"
            :opacity="i < CORE ? 1 : rec"
          />
        </g>

        <g style="mix-blend-mode: screen">
          <path
            v-for="(d, i) in strands"
            :key="'s' + i"
            :d="d"
            fill="none"
            stroke="url(#ringGrad)"
            :stroke-width="i % 3 === 0 ? 1.1 : 0.6"
            :opacity="(0.35 + (i % 4) * 0.18) * (i < CORE ? 1 : rec)"
          />
        </g>
      </svg>

      <!-- Center: capturing audio + timer -->
      <div
        :class="[
          'absolute inset-0 flex flex-col items-center justify-center pointer-events-none transition-opacity duration-500',
          isRecording ? 'opacity-100' : 'opacity-0'
        ]"
      >
        <p class="flex items-center gap-2 text-lg sm:text-xl font-semibold text-lightBlue tracking-tight">
          <span :class="['w-2 h-2 rounded-full', isPaused ? 'bg-amber-400' : 'bg-neonLime animate-pulse']"></span>
          {{ isPaused ? 'Recording paused' : 'Capturing audio' }}
        </p>
        <p class="mt-1 font-mono tabular-nums text-sm sm:text-base text-neonLime tracking-widest">
          {{ timeLabel }}
        </p>
      </div>

    </div>

    <!-- 3. BOTTOM: CONTROLS (HISTORY DRAWER BUTTON + LARGE MIC + PAUSE BUTTON) -->
    <div class="relative z-10 w-full pb-4 flex flex-col items-center">
      <p v-if="micError" class="text-xs text-red-400 text-center pb-3">{{ micError }}</p>

      <div class="flex items-center gap-4">
        <!-- Left Side: History Drawer Toggle Button -->
        <button
          @click="isDrawerOpen = true"
          class="w-14 h-14 rounded-full bg-darkBgMid/80 border border-lightBlue/15 hover:border-neonLime/50 text-lightBlue flex items-center justify-center shadow-xl transition-all hover:scale-105 group"
          title="View Saved Transcripts"
        >
          <svg class="w-5 h-5 text-lightBlue/80 group-hover:text-neonLime transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
          </svg>
        </button>

        <!-- Center: Large Prominent Circular Mic / Stop Button -->
        <button
          @click="toggleRecording"
          :disabled="isStarting"
          :class="[
            'w-20 h-20 rounded-full flex items-center justify-center shadow-2xl transition-all duration-300 group border disabled:opacity-60',
            isRecording
              ? 'bg-red-500 border-red-400 text-white shadow-red-500/40 scale-105'
              : 'bg-neonLime border-neonLime/50 text-darkBgEnd shadow-neonLime/20 hover:scale-105'
          ]"
          :title="isRecording ? 'Stop Recording' : 'Start Recording'"
        >
          <svg class="w-8 h-8 transition-transform duration-200 group-hover:scale-110" fill="currentColor" viewBox="0 0 24 24">
            <path v-if="!isRecording" d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"></path>
            <path v-if="!isRecording" d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"></path>
            <!-- Stop Square when recording active -->
            <rect v-if="isRecording" x="7" y="7" width="10" height="10" rx="2"></rect>
          </svg>
        </button>

        <!-- Right Side: Pause / Resume Button (Only visible while recording) -->
        <button
          v-if="isRecording"
          @click="togglePause"
          class="w-14 h-14 rounded-full bg-darkBgMid/80 border border-lightBlue/15 hover:border-amber-400 text-lightBlue flex items-center justify-center shadow-xl transition-all hover:scale-105 group"
          :title="isPaused ? 'Resume Recording' : 'Pause Recording'"
        >
          <!-- Play icon if paused, Pause icon if active -->
          <svg v-if="isPaused" class="w-5 h-5 text-amber-400" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z"></path>
          </svg>
          <svg v-else class="w-5 h-5 text-lightBlue/80 group-hover:text-amber-400" fill="currentColor" viewBox="0 0 24 24">
            <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"></path>
          </svg>
        </button>
      </div>

      <p class="mt-3 text-xs tracking-widest uppercase font-semibold text-lightBlue/50">
        {{ isRecording ? (isPaused ? 'Recording paused' : 'Recording active...') : 'Tap mic to start transcription' }}
      </p>
    </div>

  </div>
</template>