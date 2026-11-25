<script setup lang="ts">
import type { Component } from "vue";

withDefaults(
  defineProps<{
    label: string;
    value: string | number;
    unit?: string;
    icon: Component;
    color?: "blue" | "amber" | "emerald" | "red";
  }>(),
  {
    color: "blue",
  },
);

const colorClasses = {
  blue: "bg-blue-50 text-blue-600",
  amber: "bg-amber-50 text-amber-600",
  emerald: "bg-emerald-50 text-emerald-600",
  red: "bg-red-50 text-red-600",
};
</script>

<template>
  <div
    class="bg-white rounded-2xl border border-slate-200/80 p-6 flex flex-col justify-between"
  >
    <div
      class="w-10 h-10 rounded-xl flex items-center justify-center mb-4"
      :class="colorClasses[color]"
    >
      <component :is="icon" class="w-5 h-5" />
    </div>
    <div>
      <p class="text-xs font-medium text-slate-400">{{ label }}</p>
      <p class="text-2xl font-bold text-slate-900 mt-1">
        {{ value }}
        <span v-if="unit" class="text-xs font-normal text-slate-400">{{
          unit
        }}</span>
      </p>
    </div>
  </div>
</template>
