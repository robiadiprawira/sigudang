<script setup lang="ts">
import { Search, X } from "@lucide/vue";

defineProps<{
  modelValue: string;
  placeholder?: string;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
}>();
</script>

<template>
  <div class="relative">
    <Search
      class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none"
    />
    <input
      :value="modelValue"
      @input="
        emit('update:modelValue', ($event.target as HTMLInputElement).value)
      "
      type="text"
      :placeholder="placeholder || 'Cari data...'"
      class="pl-10 pr-8 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-blue-600 focus:outline-none w-full sm:w-64 transition"
    />
    <button
      v-if="modelValue"
      type="button"
      @click="emit('update:modelValue', '')"
      class="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 cursor-pointer"
      title="Bersihkan pencarian"
    >
      <X class="w-3.5 h-3.5" />
    </button>
  </div>
</template>
