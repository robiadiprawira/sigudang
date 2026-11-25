<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import api from "@/api/axios";
import { Pill, Plus, Edit3, Trash2, Check, AlertCircle } from "@lucide/vue";

import PageHeader from "@/components/PageHeader.vue";
import SearchInput from "@/components/SearchInput.vue";
import DataTable from "@/components/DataTable.vue";
import BaseModal from "@/components/BaseModal.vue";
import BaseButton from "@/components/BaseButton.vue";

interface ObatItem {
  id: number;
  kode_obat: string;
  nama_obat: string;
  kategori: string;
  satuan: string;
  stok: number;
  stok_minimal: number;
}

interface KategoriItem {
  id: number;
  nama_kategori: string;
}

interface SatuanItem {
  id: number;
  nama_satuan: string;
}

const columns = [
  { key: "kode", label: "Kode Obat" },
  { key: "nama", label: "Nama Obat" },
  { key: "kategori", label: "Kategori" },
  { key: "satuan", label: "Satuan" },
  { key: "minimal", label: "Batas Min. Stok" },
  { key: "aksi", label: "Aksi", align: "right" as const },
];

const listObat = ref<ObatItem[]>([]);
const listKategori = ref<KategoriItem[]>([]);
const listSatuan = ref<SatuanItem[]>([]);

const loading = ref(true);
const searchQuery = ref("");
const filterKategori = ref("Semua");

// State Modal Tambah & Edit
const showModal = ref(false);
const isEditMode = ref(false);
const editingId = ref<number | null>(null);
const saving = ref(false);
const errorMsg = ref("");

const form = ref({
  kode_obat: "",
  nama_obat: "",
  kategori: "",
  satuan: "",
  stok_minimal: 10,
});

const fetchAllData = async () => {
  loading.value = true;
  try {
    const [resObat, resKat, resSat] = await Promise.all([
      api.get("/stock"),
      api.get("/kategori"),
      api.get("/satuan"),
    ]);
    listObat.value = resObat.data;
    listKategori.value = resKat.data;
    listSatuan.value = resSat.data;
  } catch (err) {
    console.error("Gagal memuat master data obat:", err);
  } finally {
    loading.value = false;
  }
};

const filteredObat = computed(() => {
  return listObat.value.filter((item) => {
    const cocokCari =
      item.nama_obat.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.kode_obat.toLowerCase().includes(searchQuery.value.toLowerCase());
    const cocokKategori =
      filterKategori.value === "Semua" ||
      item.kategori === filterKategori.value;
    return cocokCari && cocokKategori;
  });
});

// Generate saran kode otomatis (contoh: OBT-006)
const generateNextKode = () => {
  const nextNum = listObat.value.length + 1;
  return `OBT-${String(nextNum).padStart(3, "0")}`;
};

const openCreateModal = () => {
  isEditMode.value = false;
  editingId.value = null;
  errorMsg.value = "";
  form.value = {
    kode_obat: generateNextKode(),
    nama_obat: "",
    kategori: listKategori.value[0]?.nama_kategori || "",
    satuan: listSatuan.value[0]?.nama_satuan || "",
    stok_minimal: 10,
  };
  showModal.value = true;
};

const openEditModal = (item: ObatItem) => {
  isEditMode.value = true;
  editingId.value = item.id;
  errorMsg.value = "";
  form.value = {
    kode_obat: item.kode_obat,
    nama_obat: item.nama_obat,
    kategori: item.kategori,
    satuan: item.satuan,
    stok_minimal: item.stok_minimal,
  };
  showModal.value = true;
};

const handleSubmit = async () => {
  if (!form.value.kategori || !form.value.satuan) {
    errorMsg.value = "Pilih kategori dan satuan terlebih dahulu.";
    return;
  }

  saving.value = true;
  errorMsg.value = "";
  try {
    if (isEditMode.value && editingId.value !== null) {
      const res = await api.put(`/obat/${editingId.value}`, form.value);
      const index = listObat.value.findIndex((o) => o.id === editingId.value);
      if (index !== -1) listObat.value[index] = res.data;
    } else {
      const res = await api.post("/obat", form.value);
      listObat.value.push(res.data);
    }
    showModal.value = false;
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || "Gagal menyimpan data obat";
  } finally {
    saving.value = false;
  }
};

const handleDelete = async (item: ObatItem) => {
  if (!confirm(`Hapus master data "${item.nama_obat}" (${item.kode_obat})?`))
    return;
  try {
    await api.delete(`/obat/${item.id}`);
    listObat.value = listObat.value.filter((o) => o.id !== item.id);
  } catch (err: any) {
    alert(err.response?.data?.detail || "Gagal menghapus data obat");
  }
};

onMounted(fetchAllData);
</script>

<template>
  <div class="space-y-6">
    <PageHeader
      title="Master Data Obat"
      subtitle="Kelola katalog identitas obat, pengelompokan kategori, dan satuan kemasan standar."
      :icon="Pill"
    >
      <template #actions>
        <SearchInput
          v-model="searchQuery"
          placeholder="Cari kode atau nama obat..."
        />

        <select
          v-model="filterKategori"
          class="px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl text-slate-700 focus:bg-white focus:border-blue-600 focus:outline-none cursor-pointer"
        >
          <option value="Semua">Semua Kategori</option>
          <option
            v-for="kat in listKategori"
            :key="kat.id"
            :value="kat.nama_kategori"
          >
            {{ kat.nama_kategori }}
          </option>
        </select>

        <BaseButton @click="openCreateModal">
          <Plus class="w-4 h-4" />
          <span>Tambah Obat</span>
        </BaseButton>
      </template>
    </PageHeader>
    <DataTable
      :columns="columns"
      :loading="loading"
      :is-empty="filteredObat.length === 0"
      empty-text="Belum ada master data obat."
    >
      <tr
        v-for="item in filteredObat"
        :key="item.id"
        class="hover:bg-slate-50/70 transition"
      >
        <td class="py-4 px-6 font-mono text-xs font-semibold text-blue-600">
          {{ item.kode_obat }}
        </td>
        <td class="py-4 px-6 font-medium text-slate-900">
          {{ item.nama_obat }}
        </td>
        <td class="py-4 px-6 text-slate-600">
          {{ item.kategori }}
        </td>
        <td class="py-4 px-6">
          <span
            class="px-2.5 py-1 rounded-md bg-slate-100 text-slate-700 text-xs font-medium"
          >
            {{ item.satuan }}
          </span>
        </td>
        <td class="py-4 px-6 text-slate-500 text-xs">
          {{ item.stok_minimal }} {{ item.satuan }}
        </td>
        <td class="py-4 px-6 text-right">
          <div class="inline-flex items-center justify-end gap-2">
            <BaseButton
              size="sm"
              variant="secondary"
              @click="openEditModal(item)"
            >
              <Edit3 class="w-3.5 h-3.5 text-blue-600" />
              <span>Edit</span>
            </BaseButton>
            <BaseButton size="sm" variant="danger" @click="handleDelete(item)">
              <Trash2 class="w-3.5 h-3.5" />
              <span>Hapus</span>
            </BaseButton>
          </div>
        </td>
      </tr>
    </DataTable>

    <!-- MODAL TAMBAH / EDIT OBAT -->
    <BaseModal
      :show="showModal"
      :title="isEditMode ? 'Edit Master Obat' : 'Tambah Obat Baru'"
      :subtitle="
        isEditMode
          ? 'Perbarui informasi identitas dan satuan obat.'
          : 'Stok awal otomatis bernilai 0 hingga ada transaksi barang masuk.'
      "
      @close="showModal = false"
    >
      <form
        id="form-master-obat"
        @submit.prevent="handleSubmit"
        class="space-y-4"
      >
        <div
          v-if="errorMsg"
          class="p-3 rounded-xl bg-red-50 border border-red-200 flex items-center gap-2 text-xs text-red-600"
        >
          <AlertCircle class="w-4 h-4 shrink-0" />
          <span>{{ errorMsg }}</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-medium text-slate-700 mb-1.5"
              >Kode Obat</label
            >
            <input
              v-model="form.kode_obat"
              type="text"
              required
              placeholder="OBT-006"
              class="w-full px-3.5 py-2 text-sm font-mono uppercase bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-blue-600 focus:outline-none"
            />
          </div>

          <div>
            <label class="block text-xs font-medium text-slate-700 mb-1.5"
              >Batas Minimal Stok</label
            >
            <input
              v-model.number="form.stok_minimal"
              type="number"
              min="0"
              required
              class="w-full px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-blue-600 focus:outline-none"
            />
          </div>
        </div>

        <div>
          <label class="block text-xs font-medium text-slate-700 mb-1.5"
            >Nama Obat</label
          >
          <input
            v-model="form.nama_obat"
            type="text"
            required
            placeholder="Contoh: Ibuprofen 400mg"
            class="w-full px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-blue-600 focus:outline-none"
          />
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-medium text-slate-700 mb-1.5"
              >Kategori</label
            >
            <select
              v-model="form.kategori"
              required
              class="w-full px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl text-slate-700 focus:bg-white focus:border-blue-600 focus:outline-none cursor-pointer"
            >
              <option value="" disabled>-- Pilih Kategori --</option>
              <option
                v-for="kat in listKategori"
                :key="kat.id"
                :value="kat.nama_kategori"
              >
                {{ kat.nama_kategori }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-medium text-slate-700 mb-1.5"
              >Satuan Kemasan</label
            >
            <select
              v-model="form.satuan"
              required
              class="w-full px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl text-slate-700 focus:bg-white focus:border-blue-600 focus:outline-none cursor-pointer"
            >
              <option value="" disabled>-- Pilih Satuan --</option>
              <option
                v-for="sat in listSatuan"
                :key="sat.id"
                :value="sat.nama_satuan"
              >
                {{ sat.nama_satuan }}
              </option>
            </select>
          </div>
        </div>
      </form>

      <template #footer>
        <BaseButton size="sm" variant="ghost" @click="showModal = false"
          >Batal</BaseButton
        >
        <BaseButton
          size="sm"
          variant="primary"
          type="submit"
          form="form-master-obat"
          :loading="saving"
        >
          <Check v-if="!saving" class="w-4 h-4" />
          <span>{{
            saving
              ? "Menyimpan..."
              : isEditMode
                ? "Simpan Perubahan"
                : "Simpan Obat"
          }}</span>
        </BaseButton>
      </template>
    </BaseModal>
  </div>
</template>
