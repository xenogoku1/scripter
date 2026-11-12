<template>
  <div class="flex-1 flex flex-col items-center justify-center max-w-xl mx-auto w-full py-8">
    <div class="w-full bg-darkBgMid/50 border border-lightBlue/10 rounded-3xl p-6 backdrop-blur-xl text-left space-y-6">
      <h2 class="text-xl font-bold text-lightBlue border-b border-lightBlue/10 pb-4">Workspace Settings</h2>
      
      <div class="space-y-4">
        <div>
          <label class="block text-xs uppercase tracking-wider text-lightBlue/60 font-semibold mb-2">Microphone Input</label>
          <select class="w-full bg-darkBgEnd text-lightBlue border border-lightBlue/15 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-neonLime">
            <option>Default System Microphone</option>
          </select>
        </div>

        <div>
          <label class="block text-xs uppercase tracking-wider text-lightBlue/60 font-semibold mb-2">Default Audio Quality</label>
          <select class="w-full bg-darkBgEnd text-lightBlue border border-lightBlue/15 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-neonLime">
            <option>High (320 kbps MP3)</option>
            <option>Lossless (WAV)</option>
          </select>
        </div>
      </div>
    </div>
  </div>
</template>