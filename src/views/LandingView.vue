<template>
  <div class="flex flex-col items-center justify-center min-h-screen p-6 text-center">
    <h1 class="text-4xl font-extrabold text-white mb-4">Welcome to TalkScript 🚀</h1>
    <p class="text-gray-400 mb-6 max-w-md">Your voice-first YouTube script editor. Talk out your videos, clean up stumbles, and save hours of writing.</p>
    <div class="flex gap-4">
      <router-link to="/login" class="px-5 py-2.5 bg-neonLime text-black font-semibold rounded-xl hover:opacity-90">Login</router-link>
      <router-link to="/register" class="px-5 py-2.5 bg-white/10 text-white font-semibold rounded-xl hover:bg-white/20">Register</router-link>
    </div>
  </div>
  
   
</template>