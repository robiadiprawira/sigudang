<script setup lang="ts">
import { ref, onMounted } from "vue";
import api from "./api/axios";

const statusPesan = ref("Menghubungkan ke server Python...");
const berhasil = ref(false);

onMounted(async () => {
  try {
    const res = await api.get("/ping");
    statusPesan.value = res.data.message;
    berhasil.value = true;
  } catch (err: any) {
    statusPesan.value = "Gagal terhubung ke backend: " + err.message;
  }
});
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-100 p-4">
    <div class="bg-white p-8 rounded-xl shadow-md max-w-md w-full text-center">
      <h1 class="text-xl font-bold text-slate-800 mb-2">
        Sistem Pergudangan Obat
      </h1>
      <p :class="berhasil ? 'text-emerald-600 font-medium' : 'text-red-500'">
        {{ statusPesan }}
      </p>
    </div>
  </div>
</template>
