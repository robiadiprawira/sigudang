<script setup lang="ts">
import { ref, onMounted } from "vue";
import api from "@/api/axios";
import { Tags, Plus, Trash2, Layers, AlertCircle } from "@lucide/vue";

import PageHeader from "@/components/PageHeader.vue";
import BaseButton from "@/components/BaseButton.vue";

interface KategoriItem {
  id: number;
  nama_kategori: string;
}

interface SatuanItem {
  id: number;
  nama_satuan: string;
}

const listKategori = ref<KategoriItem[]>([]);
const listSatuan = ref<SatuanItem[]>([]);

const inputKategori = ref("");
const inputSatuan = ref("");

const loadingKategori = ref(false);
const loadingSatuan = ref(false);

const errorKategori = ref("");
const errorSatuan = ref("");

const fetchData = async () => {
  try {
    const [resKat, resSat] = await Promise.all([
      api.get("/kategori"),
      api.get("/satuan"),
    ]);
    listKategori.value = resKat.data;
    listSatuan.value = resSat.data;
  } catch (err) {
    console.error("Gagal memuat data kategori & satuan:", err);
  }
};

const tambahKategori = async () => {
  if (!inputKategori.value.trim()) return;
  loadingKategori.value = true;
  errorKategori.value = "";
  try {
    const res = await api.post("/kategori", {
      nama_kategori: inputKategori.value,
    });
    listKategori.value.push(res.data);
    inputKategori.value = "";
  } catch (err: any) {
    errorKategori.value =
      err.response?.data?.detail || "Gagal menambah kategori";
  } finally {
    loadingKategori.value = false;
  }
};

const hapusKategori = async (item: KategoriItem) => {
  if (!confirm(`Hapus kategori "${item.nama_kategori}"?`)) return;
  try {
    await api.delete(`/kategori/${item.id}`);
    listKategori.value = listKategori.value.filter((k) => k.id !== item.id);
  } catch (err) {
    alert("Gagal menghapus kategori");
  }
};

const tambahSatuan = async () => {
  if (!inputSatuan.value.trim()) return;
  loadingSatuan.value = true;
  errorSatuan.value = "";
  try {
    const res = await api.post("/satuan", { nama_satuan: inputSatuan.value });
    listSatuan.value.push(res.data);
    inputSatuan.value = "";
  } catch (err: any) {
    errorSatuan.value = err.response?.data?.detail || "Gagal menambah satuan";
  } finally {
    loadingSatuan.value = false;
  }
};

const hapusSatuan = async (item: SatuanItem) => {
  if (!confirm(`Hapus satuan "${item.nama_satuan}"?`)) return;
  try {
    await api.delete(`/satuan/${item.id}`);
    listSatuan.value = listSatuan.value.filter((s) => s.id !== item.id);
  } catch (err) {
    alert("Gagal menghapus satuan");
  }
};

onMounted(fetchData);
</script>

<template>
  <div class="space-y-6">
    <PageHeader
      title="Master Kategori & Satuan"
      subtitle="Atur daftar kategori obat dan satuan kemasan yang akan muncul pada pilihan form tambah obat."
      :icon="Tags"
    />

    <!-- Grid 2 Kolom Berdampingan -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
      <!-- KOLOM KIRI: KATEGORI OBAT -->
      <div
        class="bg-white rounded-2xl border border-slate-200/80 p-6 space-y-5"
      >
        <div
          class="flex items-center justify-between border-b border-slate-100 pb-4"
        >
          <div class="flex items-center gap-2.5">
            <div
              class="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center"
            >
              <Tags class="w-4 h-4" />
            </div>
            <div>
              <h3 class="text-base font-bold text-slate-900">Kategori Obat</h3>
              <p class="text-xs text-slate-400">
                Contoh: Obat Bebas, Obat Keras, Sirup
              </p>
            </div>
          </div>
          <span
            class="px-2.5 py-1 rounded-lg bg-slate-100 text-slate-600 text-xs font-semibold"
          >
            {{ listKategori.length }} item
          </span>
        </div>

        <!-- Form Free Text Kategori -->
        <form @submit.prevent="tambahKategori" class="space-y-2">
          <div class="flex items-center gap-2">
            <input
              v-model="inputKategori"
              type="text"
              placeholder="Ketik nama kategori baru..."
              required
              class="flex-1 px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-blue-600 focus:outline-none transition"
            />
            <BaseButton type="submit" size="sm" :loading="loadingKategori">
              <Plus v-if="!loadingKategori" class="w-4 h-4" />
              <span>Tambah</span>
            </BaseButton>
          </div>

          <p
            v-if="errorKategori"
            class="flex items-center gap-1.5 text-xs text-red-600 pt-1"
          >
            <AlertCircle class="w-3.5 h-3.5 shrink-0" />
            <span>{{ errorKategori }}</span>
          </p>
        </form>

        <!-- Daftar Kategori -->
        <div
          class="divide-y divide-slate-100 border border-slate-200/70 rounded-xl overflow-hidden"
        >
          <div
            v-if="listKategori.length === 0"
            class="py-8 text-center text-xs text-slate-400"
          >
            Belum ada data kategori.
          </div>

          <div
            v-for="item in listKategori"
            :key="item.id"
            class="flex items-center justify-between px-4 py-3 bg-white hover:bg-slate-50/80 transition"
          >
            <span class="text-sm font-medium text-slate-800">{{
              item.nama_kategori
            }}</span>
            <button
              type="button"
              @click="hapusKategori(item)"
              class="p-1.5 rounded-lg text-slate-400 hover:text-red-600 hover:bg-red-50 transition cursor-pointer"
              title="Hapus kategori"
            >
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <!-- KOLOM KANAN: SATUAN KEMASAN -->
      <div
        class="bg-white rounded-2xl border border-slate-200/80 p-6 space-y-5"
      >
        <div
          class="flex items-center justify-between border-b border-slate-100 pb-4"
        >
          <div class="flex items-center gap-2.5">
            <div
              class="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center"
            >
              <Layers class="w-4 h-4" />
            </div>
            <div>
              <h3 class="text-base font-bold text-slate-900">Satuan Kemasan</h3>
              <p class="text-xs text-slate-400">
                Contoh: Strip / Lembar, Botol, Box, Tube
              </p>
            </div>
          </div>
          <span
            class="px-2.5 py-1 rounded-lg bg-slate-100 text-slate-600 text-xs font-semibold"
          >
            {{ listSatuan.length }} item
          </span>
        </div>

        <!-- Form Free Text Satuan -->
        <form @submit.prevent="tambahSatuan" class="space-y-2">
          <div class="flex items-center gap-2">
            <input
              v-model="inputSatuan"
              type="text"
              placeholder="Ketik nama satuan baru..."
              required
              class="flex-1 px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-blue-600 focus:outline-none transition"
            />
            <BaseButton type="submit" size="sm" :loading="loadingSatuan">
              <Plus v-if="!loadingSatuan" class="w-4 h-4" />
              <span>Tambah</span>
            </BaseButton>
          </div>

          <p
            v-if="errorSatuan"
            class="flex items-center gap-1.5 text-xs text-red-600 pt-1"
          >
            <AlertCircle class="w-3.5 h-3.5 shrink-0" />
            <span>{{ errorSatuan }}</span>
          </p>
        </form>

        <!-- Daftar Satuan -->
        <div
          class="divide-y divide-slate-100 border border-slate-200/70 rounded-xl overflow-hidden"
        >
          <div
            v-if="listSatuan.length === 0"
            class="py-8 text-center text-xs text-slate-400"
          >
            Belum ada data satuan.
          </div>

          <div
            v-for="item in listSatuan"
            :key="item.id"
            class="flex items-center justify-between px-4 py-3 bg-white hover:bg-slate-50/80 transition"
          >
            <span class="text-sm font-medium text-slate-800">{{
              item.nama_satuan
            }}</span>
            <button
              type="button"
              @click="hapusSatuan(item)"
              class="p-1.5 rounded-lg text-slate-400 hover:text-red-600 hover:bg-red-50 transition cursor-pointer"
              title="Hapus satuan"
            >
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
