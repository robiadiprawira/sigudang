<script setup lang="ts">
import { useRoute } from "vue-router";
import { Wrench } from "@lucide/vue";

const route = useRoute();
</script>

<template>
  <div class="bg-white rounded-2xl border border-slate-200/80 p-12 text-center">
    <div
      class="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center mx-auto mb-4"
    >
      <Wrench class="w-6 h-6" />
    </div>
    <h2 class="text-lg font-bold text-slate-800">
      {{ route.meta.title || "Halaman Dalam Pengembangan" }}
    </h2>
    <p class="text-sm text-slate-500 mt-1">
      Fitur ini akan segera dibangun pada tahap berikutnya.
    </p>
  </div>
</template>
