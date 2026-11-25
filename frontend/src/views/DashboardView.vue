<script setup lang="ts">
import { Package, AlertTriangle, ArrowDownLeft } from "@lucide/vue";
import StatCard from "@/components/StatCard.vue";
</script>

<template>
  <div class="space-y-6">
    <!-- Top Bento Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <!-- Featured Royal Blue Card -->
      <div
        class="lg:col-span-4 bg-gradient-to-br from-blue-600 to-blue-700 rounded-2xl p-6 text-white shadow-sm flex flex-col justify-between"
      >
        <div>
          <span
            class="text-xs font-medium uppercase tracking-wider text-blue-100"
            >Status Gudang Aktif</span
          >
          <h2 class="text-2xl font-bold mt-2">Sistem FEFO Siap</h2>
          <p class="text-sm text-blue-100 mt-1">
            First Expired, First Out otomatis aktif pada setiap pengeluaran
            stok.
          </p>
        </div>
        <div
          class="mt-6 pt-4 border-t border-blue-500/50 flex items-center justify-between text-xs text-blue-100"
        >
          <span>Database: SQLite Lokal</span>
          <span
            class="px-2.5 py-1 bg-white/15 rounded-lg font-medium text-white"
            >Online</span
          >
        </div>
      </div>

      <!-- 3 Metric Cards menggunakan StatCard -->
      <div class="lg:col-span-8 grid grid-cols-1 sm:grid-cols-3 gap-6">
        <StatCard
          label="Total Item Obat"
          :value="0"
          unit="jenis"
          :icon="Package"
          color="blue"
        />
        <StatCard
          label="Mendekati Expired"
          :value="0"
          unit="batch"
          :icon="AlertTriangle"
          color="amber"
        />
        <StatCard
          label="Transaksi Hari Ini"
          :value="0"
          unit="aktivitas"
          :icon="ArrowDownLeft"
          color="emerald"
        />
      </div>
    </div>

    <!-- Quick Action Banner -->
    <div
      class="bg-white rounded-2xl border border-slate-200/80 p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
    >
      <div>
        <h3 class="text-base font-semibold text-slate-800">
          Mulai Kelola Inventaris Obat
        </h3>
        <p class="text-sm text-slate-500 mt-0.5">
          Tambahkan master data obat terlebih dahulu sebelum mencatat stok batch
          masuk.
        </p>
      </div>
      <div class="flex items-center gap-3">
        <router-link
          to="/master/obat"
          class="px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-xl transition"
        >
          + Tambah Master Obat
        </router-link>
      </div>
    </div>
  </div>
</template>
