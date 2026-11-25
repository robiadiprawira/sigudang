<script setup lang="ts">
import { Loader2 } from "@lucide/vue";

withDefaults(
  defineProps<{
    variant?: "primary" | "secondary" | "danger" | "ghost";
    size?: "sm" | "md";
    type?: "button" | "submit" | "reset";
    loading?: boolean;
    disabled?: boolean;
  }>(),
  {
    variant: "primary",
    size: "md",
    type: "button",
    loading: false,
    disabled: false,
  },
);

const variantClasses = {
  primary:
    "bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white shadow-xs",
  secondary:
    "bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 disabled:opacity-50",
  danger:
    "bg-red-50 hover:bg-red-100 text-red-600 border border-red-200/60 disabled:opacity-50",
  ghost: "text-slate-600 hover:bg-slate-100 disabled:opacity-50",
};

const sizeClasses = {
  sm: "px-3 py-1.5 text-xs rounded-xl gap-1.5",
  md: "px-4 py-2.5 text-sm rounded-xl gap-2",
};
</script>

<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    class="inline-flex items-center justify-center font-medium transition cursor-pointer disabled:cursor-not-allowed"
    :class="[variantClasses[variant], sizeClasses[size]]"
  >
    <Loader2 v-if="loading" class="w-4 h-4 animate-spin shrink-0" />
    <slot />
  </button>
</template>
