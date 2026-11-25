<script setup lang="ts">
import { X } from "@lucide/vue";

defineProps<{
  show: boolean;
  title: string;
  subtitle?: string;
}>();

const emit = defineEmits<{
  (e: "close"): void;
}>();
</script>

<template>
  <div
    v-if="show"
    class="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center p-4"
    @click.self="emit('close')"
  >
    <div
      class="bg-white rounded-2xl border border-slate-200 shadow-lg w-full max-w-md p-6"
    >
      <!-- Header Modal -->
      <div
        class="flex items-center justify-between pb-4 border-b border-slate-100"
      >
        <div>
          <h3 class="text-base font-bold text-slate-900">{{ title }}</h3>
          <p v-if="subtitle" class="text-xs text-slate-500 mt-0.5">
            {{ subtitle }}
          </p>
        </div>
        <button
          type="button"
          @click="emit('close')"
          class="w-8 h-8 rounded-lg text-slate-400 hover:bg-slate-100 flex items-center justify-center cursor-pointer transition"
        >
          <X class="w-4 h-4" />
        </button>
      </div>

      <!-- Konten Form -->
      <div class="mt-5">
        <slot />
      </div>

      <!-- Area Tombol Bawah (Opsional) -->
      <div
        v-if="$slots.footer"
        class="flex items-center justify-end gap-2 pt-4 mt-5 border-t border-slate-100"
      >
        <slot name="footer" />
      </div>
    </div>
  </div>
</template>
