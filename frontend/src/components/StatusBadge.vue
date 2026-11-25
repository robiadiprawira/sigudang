<script setup lang="ts">
withDefaults(
  defineProps<{
    variant?: "success" | "warning" | "danger" | "info" | "neutral";
    label: string;
  }>(),
  {
    variant: "neutral",
  },
);

const variantClasses = {
  success: "bg-emerald-50 text-emerald-700 border-emerald-200",
  warning: "bg-amber-50 text-amber-700 border-amber-200",
  danger: "bg-red-50 text-red-600 border-red-200",
  info: "bg-blue-50 text-blue-600 border-blue-200",
  neutral: "bg-slate-100 text-slate-600 border-slate-200",
};
</script>

<template>
  <span
    class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium border"
    :class="variantClasses[variant]"
  >
    {{ label }}
  </span>
</template>
