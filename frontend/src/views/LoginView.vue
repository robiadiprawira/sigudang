<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { Pill, Lock, User, AlertCircle } from "@lucide/vue";

const router = useRouter();
const authStore = useAuthStore();

const username = ref("");
const password = ref("");
const errorMsg = ref("");
const loading = ref(false);

const handleLogin = async () => {
  errorMsg.value = "";
  loading.value = true;
  try {
    await authStore.login(username.value, password.value);
    router.push("/");
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || "Gagal terhubung ke server";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen bg-[#F8FAFC] flex items-center justify-center p-4">
    <div
      class="w-full max-w-md bg-white rounded-2xl border border-slate-200/80 shadow-sm p-8"
    >
      <!-- Brand Header -->
      <div class="flex items-center gap-3 mb-8">
        <div
          class="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white shadow-sm"
        >
          <Pill class="w-5 h-5" />
        </div>
        <div>
          <h1 class="text-lg font-bold text-slate-900 leading-tight">
            PharmaStock
          </h1>
          <p class="text-xs text-slate-500">Sistem Manajemen Gudang Obat</p>
        </div>
      </div>

      <h2 class="text-xl font-semibold text-slate-800 mb-1">
        Selamat Datang Kembali
      </h2>
      <p class="text-sm text-slate-500 mb-6">
        Masuk menggunakan akun petugas gudang Anda.
      </p>

      <!-- Alert Error -->
      <div
        v-if="errorMsg"
        class="mb-5 p-3.5 rounded-xl bg-red-50 border border-red-200 flex items-center gap-2.5 text-sm text-red-600"
      >
        <AlertCircle class="w-4 h-4 shrink-0" />
        <span>{{ errorMsg }}</span>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-xs font-medium text-slate-700 mb-1.5"
            >Username</label
          >
          <div class="relative">
            <User
              class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2"
            />
            <input
              v-model="username"
              type="text"
              required
              placeholder="Masukkan username"
              class="w-full pl-10 pr-4 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:bg-white focus:border-blue-600 transition"
            />
          </div>
        </div>

        <div>
          <label class="block text-xs font-medium text-slate-700 mb-1.5"
            >Password</label
          >
          <div class="relative">
            <Lock
              class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2"
            />
            <input
              v-model="password"
              type="password"
              required
              placeholder="••••••••"
              class="w-full pl-10 pr-4 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:bg-white focus:border-blue-600 transition"
            />
          </div>
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white text-sm font-medium rounded-xl transition shadow-sm cursor-pointer mt-2"
        >
          {{ loading ? "Memverifikasi..." : "Masuk ke Dashboard" }}
        </button>
      </form>

      <div class="mt-6 pt-5 border-t border-slate-100 text-center">
        <p class="text-xs text-slate-400">
          Default Akun: <span class="font-medium text-slate-600">admin</span> /
          <span class="font-medium text-slate-600">admin123</span>
        </p>
      </div>
    </div>
  </div>
</template>
