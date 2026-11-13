<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

defineProps({
  user: Object
})

/* ---------- Recording state ---------- */
const isRecording = ref(false)
const isStarting = ref(false)
const micError = ref('')
const elapsed = ref(0) // seconds since record was pressed

const timeLabel = computed(() => {
  const s = elapsed.value
  const h = String(Math.floor(s / 3600)).padStart(2, '0')
  const m = String(Math.floor((s % 3600) / 60)).padStart(2, '0')
  const sec = String(s % 60).padStart(2, '0')
  return `${h}:${m}:${sec}`
})

/* ---------- Microphone analysis (visual only, nothing is saved or sent) ---------- */
let stream = null
let audioCtx = null
let source = null
let analyser = null
let timeData = null
let freqData = null
let timerId = 0
let startedAt = 0

const level = ref(0) // 0..1  loudness / syllable energy (smoothed)
const pitch = ref(0) // 0..1  low voice -> high voice (smoothed)
const rec = ref(0)   // 0..1  eased "recording mode" blend

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
  source.connect(analyser) // not connected to speakers, so no echo
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
  if (!analyser) {
    level.value *= 0.9 // fade out smoothly after stopping
    return
  }

  // loudness (RMS) -> level. Rises fast on a syllable, falls slowly.
  analyser.getByteTimeDomainData(timeData)
  let sum = 0
  for (let i = 0; i < timeData.length; i++) {
    const x = (timeData[i] - 128) / 128
    sum += x * x
  }
  const rms = Math.sqrt(sum / timeData.length)
  const target = Math.min(1, Math.max(0, (rms - 0.015) * 6)) // small noise gate
  level.value += (target - level.value) * (target > level.value ? 0.45 : 0.1)

  // pitch-ish: spectral centroid (where the energy sits) in the voice range
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

  if (isRecording.value) {
    isRecording.value = false
    clearInterval(timerId)
    stopMic()
    elapsed.value = 0
    return
  }

  isStarting.value = true
  try {
    await startMic()
    isRecording.value = true
    startedAt = Date.now()
    elapsed.value = 0
    timerId = setInterval(() => {
      elapsed.value = Math.floor((Date.now() - startedAt) / 1000)
    }, 250)
  } catch (err) {
    stopMic()
    micError.value =
      err && err.name === 'NotAllowedError'
        ? 'Microphone access was blocked. Allow it in your browser settings.'
        : 'Could not start the microphone on this device.'
  } finally {
    isStarting.value = false
  }
}

/* ---------- Morphing wave strands ---------- */
const STRANDS = 14
const CORE = 9 // the original strands; the rest fade in while recording
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

  const p = i * (0.22 + r0 * 0.2)                         // strands fan apart into a ribbon
  const gain = 1 + lv * 1.4                                // voice makes the waves taller
  const base = 52 + r0 * 14 + lv * 8                       // ring grows big + pulses with voice
  const fan = (i - (STRANDS - 1) / 2) * 0.7 * r0 * (1 + lv) // ribbon thickness

  let d = ''
  for (let n = 0; n <= POINTS; n++) {
    const a = (n / POINTS) * Math.PI * 2
    const r =
      base +
      fan +
      gain *
        (7 * ((1 - pt) * Math.sin(4 * a + t + p) + pt * Math.sin(6 * a - t * 1.2 + p)) + // pitch blends 4 -> 6 lobes
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
  rec.value += ((isRecording.value ? 1 : 0) - rec.value) * 0.05

  // calm drift at idle, speeds up with recording and with your voice
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
  <div class="flex-1 flex flex-col justify-between items-center max-w-md mx-auto w-full py-6 px-4">

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

      <!-- Ambient Glow Backdrop (grows and brightens with your voice) -->
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

        <!-- soft glow layer -->
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

        <!-- crisp thin strands -->
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
          <span class="w-2 h-2 rounded-full bg-neonLime animate-pulse"></span>
          Capturing audio
        </p>
        <p class="mt-1 font-mono tabular-nums text-sm sm:text-base text-neonLime tracking-widest">
          {{ timeLabel }}
        </p>
      </div>

    </div>

    <!-- 3. BOTTOM: RECORD ACTION PILL BUTTON -->
    <div class="relative z-10 w-full pb-4">
      <p v-if="micError" class="text-xs text-red-400 text-center pb-3">{{ micError }}</p>

      <button
        @click="toggleRecording"
        :disabled="isStarting"
        :class="[
          'w-full flex items-center justify-between p-2.5 rounded-full border shadow-2xl transition-all duration-300 group disabled:opacity-60',
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