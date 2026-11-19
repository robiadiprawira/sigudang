<script setup lang="ts">
import { ref } from "vue";
import {
  Bell,
  KeyRound,
  PackageX,
  CheckCheck,
  Clock,
  ArrowRight,
} from "@lucide/vue";

interface NotifikasiItem {
  id: number;
  tipe: "password" | "stock_habis";
  judul: string;
  deskripsi: string;
  waktu: string;
  dibaca: boolean;
  link?: string;
}

// Data contoh (dummy) khusus tampilan awal
const daftarNotifikasi = ref<NotifikasiItem[]>([
  {
    id: 1,
    tipe: "stock_habis",
    judul: "Stok Obat Habis (0)",
    deskripsi:
      "Stok Paracetamol 500mg (Kode: OBT-001) telah mencapai 0 strip. Segera lakukan pengadaan barang masuk.",
    waktu: "10 menit yang lalu",
    dibaca: false,
    link: "/transaksi/stock",
  },
  {
    id: 2,
    tipe: "password",
    judul: "Perubahan Password Pengguna",
    deskripsi:
      'Petugas gudang "Budi Santoso" (username: budi_staff) telah memperbarui kata sandi akunnya.',
    waktu: "1 jam yang lalu",
    dibaca: false,
    link: "/users",
  },
  {
    id: 3,
    tipe: "stock_habis",
    judul: "Stok Obat Habis (0)",
    deskripsi:
      "Stok Amoxicillin 500mg (Kode: OBT-014) habis setelah transaksi barang keluar terakhir.",
    waktu: "Hari ini, 09:15",
    dibaca: true,
    link: "/transaksi/stock",
  },
  {
    id: 4,
    tipe: "password",
    judul: "Perubahan Password Pengguna",
    deskripsi:
      "Admin Gudang (username: admin) berhasil mengganti password akun.",
    waktu: "Kemarin, 16:40",
    dibaca: true,
    link: "/users",
  },
]);

const filterAktif = ref<"semua" | "stock_habis" | "password">("semua");

const tandaiSemuaDibaca = () => {
  daftarNotifikasi.value.forEach((item) => {
    item.dibaca = true;
  });
};

const tandaiDibaca = (item: NotifikasiItem) => {
  item.dibaca = true;
};

const notifikasiTersaring = () => {
  if (filterAktif.value === "semua") return daftarNotifikasi.value;
  return daftarNotifikasi.value.filter(
    (item) => item.tipe === filterAktif.value,
  );
};
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <!-- Header Halaman -->
    <div
      class="flex flex-col sm:flex-row sm:items-center justify-between gap-4"
    >
      <div class="flex items-center gap-3">
        <div
          class="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center"
        >
          <Bell class="w-5 h-5" />
        </div>
        <div>
          <h2 class="text-xl font-bold text-slate-900">Pusat Notifikasi</h2>
          <p class="text-xs text-slate-500">
            Pantau peringatan stok kosong dan aktivitas keamanan akun petugas.
          </p>
        </div>
      </div>

      <button
        @click="tandaiSemuaDibaca"
        class="inline-flex items-center gap-2 px-4 py-2 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 rounded-xl text-xs font-medium transition cursor-pointer self-start sm:self-auto"
      >
        <CheckCheck class="w-4 h-4 text-blue-600" />
        <span>Tandai semua dibaca</span>
      </button>
    </div>

    <!-- Tab Filter -->
    <div class="flex items-center gap-2 border-b border-slate-200 pb-3">
      <button
        @click="filterAktif = 'semua'"
        class="px-3.5 py-1.5 rounded-xl text-xs font-medium transition cursor-pointer"
        :class="
          filterAktif === 'semua'
            ? 'bg-blue-600 text-white'
            : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200/80'
        "
      >
        Semua ({{ daftarNotifikasi.length }})
      </button>

      <button
        @click="filterAktif = 'stock_habis'"
        class="px-3.5 py-1.5 rounded-xl text-xs font-medium transition cursor-pointer"
        :class="
          filterAktif === 'stock_habis'
            ? 'bg-red-600 text-white'
            : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200/80'
        "
      >
        Stock 0 ({{
          daftarNotifikasi.filter((n) => n.tipe === "stock_habis").length
        }})
      </button>

      <button
        @click="filterAktif = 'password'"
        class="px-3.5 py-1.5 rounded-xl text-xs font-medium transition cursor-pointer"
        :class="
          filterAktif === 'password'
            ? 'bg-amber-600 text-white'
            : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200/80'
        "
      >
        Ganti Password ({{
          daftarNotifikasi.filter((n) => n.tipe === "password").length
        }})
      </button>
    </div>

    <!-- Daftar Kartu Notifikasi -->
    <div class="space-y-3">
      <div
        v-for="item in notifikasiTersaring()"
        :key="item.id"
        @click="tandaiDibaca(item)"
        class="bg-white rounded-2xl border p-5 transition flex items-start justify-between gap-4 cursor-pointer"
        :class="
          item.dibaca
            ? 'border-slate-200/70 opacity-80 hover:opacity-100'
            : 'border-blue-200 shadow-xs bg-blue-50/20'
        "
      >
        <div class="flex items-start gap-4">
          <!-- Ikon Kategori -->
          <div
            class="w-10 h-10 rounded-xl flex items-center justify-center shrink-0 mt-0.5"
            :class="
              item.tipe === 'stock_habis'
                ? 'bg-red-50 text-red-600'
                : 'bg-amber-50 text-amber-600'
            "
          >
            <PackageX v-if="item.tipe === 'stock_habis'" class="w-5 h-5" />
            <KeyRound v-else class="w-5 h-5" />
          </div>

          <!-- Konten Teks -->
          <div>
            <div class="flex items-center gap-2">
              <h3 class="text-sm font-semibold text-slate-900">
                {{ item.judul }}
              </h3>
              <span
                v-if="!item.dibaca"
                class="w-2 h-2 rounded-full bg-blue-600"
                title="Belum dibaca"
              ></span>
            </div>
            <p class="text-sm text-slate-600 mt-1 leading-relaxed">
              {{ item.deskripsi }}
            </p>
            <div class="flex items-center gap-4 mt-2.5">
              <span
                class="inline-flex items-center gap-1 text-xs text-slate-400"
              >
                <Clock class="w-3.5 h-3.5" />
                {{ item.waktu }}
              </span>

              <router-link
                v-if="item.link"
                :to="item.link"
                @click.stop
                class="inline-flex items-center gap-1 text-xs font-medium text-blue-600 hover:text-blue-700"
              >
                <span>Lihat detail</span>
                <ArrowRight class="w-3 h-3" />
              </router-link>
            </div>
          </div>
        </div>

        <!-- Badge Status -->
        <span
          class="px-2.5 py-1 rounded-lg text-[11px] font-semibold shrink-0"
          :class="
            item.tipe === 'stock_habis'
              ? 'bg-red-50 text-red-600'
              : 'bg-amber-50 text-amber-700'
          "
        >
          {{ item.tipe === "stock_habis" ? "Stock 0" : "Keamanan" }}
        </span>
      </div>
    </div>
  </div>
</template>
