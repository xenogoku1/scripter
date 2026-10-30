<script setup>
defineProps({
  modelValue: String,
  label: String,
  type: {
    type: String,
    default: 'text'
  },
  placeholder: String
})

defineEmits(['update:modelValue'])
</script>

<template>
  <div class="space-y-1.5 w-full">
    <label class="block text-xs uppercase tracking-wider text-gray-400 font-medium">{{ label }}</label>
    <input 
      :type="type"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :placeholder="placeholder"
      class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3.5 text-sm text-[#e0f6ff] placeholder-gray-500 focus:outline-none focus:border-[#00bbff] focus:ring-1 focus:ring-[#00bbff] transition-all"
    />
  </div>
</template>