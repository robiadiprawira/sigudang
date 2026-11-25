<script setup lang="ts">
import type { Component } from "vue";

defineProps<{
  title: string;
  subtitle?: string;
  icon?: Component;
}>();
</script>

<template>
  <div class="bg-white rounded-2xl border border-slate-200/80 p-6">
    <div
      class="flex flex-col md:flex-row md:items-center justify-between gap-4"
    >
      <div class="flex items-center gap-3">
        <div
          v-if="icon"
          class="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0"
        >
          <component :is="icon" class="w-5 h-5" />
        </div>
        <div>
          <h2 class="text-lg font-bold text-slate-900">{{ title }}</h2>
          <p v-if="subtitle" class="text-xs text-slate-500 mt-0.5">
            {{ subtitle }}
          </p>
        </div>
      </div>

      <div
        v-if="$slots.actions"
        class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3"
      >
        <slot name="actions" />
      </div>
    </div>
  </div>
</template>
