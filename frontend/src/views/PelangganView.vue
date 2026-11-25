<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import api from "@/api/axios";
import {
  Users,
  Plus,
  Edit3,
  Trash2,
  Check,
  AlertCircle,
  Phone,
  MapPin,
} from "@lucide/vue";

import PageHeader from "@/components/PageHeader.vue";
import SearchInput from "@/components/SearchInput.vue";
import DataTable from "@/components/DataTable.vue";
import StatusBadge from "@/components/StatusBadge.vue";
import BaseModal from "@/components/BaseModal.vue";
import BaseButton from "@/components/BaseButton.vue";

interface PelangganItem {
  id: number;
  kode_pelanggan: string;
  nama_pelanggan: string;
  tipe: string;
  telepon: string;
  alamat: string;
}

const columns = [
  { key: "kode", label: "Kode Pelanggan" },
  { key: "nama", label: "Nama Pelanggan" },
  { key: "tipe", label: "Kategori / Tipe" },
  { key: "telepon", label: "Kontak" },
  { key: "alamat", label: "Alamat / Lokasi" },
  { key: "aksi", label: "Aksi", align: "right" as const },
];

const tipeOptions = ["Umum", "BPJS"];

const listPelanggan = ref<PelangganItem[]>([]);
const loading = ref(true);
const searchQuery = ref("");
const filterTipe = ref("Semua");

// State Modal Tambah & Edit
const showModal = ref(false);
const isEditMode = ref(false);
const editingId = ref<number | null>(null);
const saving = ref(false);
const errorMsg = ref("");

const form = ref({
  kode_pelanggan: "",
  nama_pelanggan: "",
  tipe: "Poli / Internal",
  telepon: "",
  alamat: "",
});

const fetchPelanggan = async () => {
  loading.value = true;
  try {
    const res = await api.get("/pelanggan");
    listPelanggan.value = res.data;
  } catch (err) {
    console.error("Gagal memuat data pelanggan:", err);
  } finally {
    loading.value = false;
  }
};

const filteredPelanggan = computed(() => {
  const q = searchQuery.value.toLowerCase();
  return listPelanggan.value.filter((item) => {
    const cocokCari =
      item.nama_pelanggan.toLowerCase().includes(q) ||
      item.kode_pelanggan.toLowerCase().includes(q) ||
      (item.telepon && item.telepon.toLowerCase().includes(q)) ||
      (item.alamat && item.alamat.toLowerCase().includes(q));
    const cocokTipe =
      filterTipe.value === "Semua" || item.tipe === filterTipe.value;
    return cocokCari && cocokTipe;
  });
});

const generateNextKode = () => {
  const nextNum = listPelanggan.value.length + 1;
  return `PLG-${String(nextNum).padStart(3, "0")}`;
};

const openCreateModal = () => {
  isEditMode.value = false;
  editingId.value = null;
  errorMsg.value = "";
  form.value = {
    kode_pelanggan: generateNextKode(),
    nama_pelanggan: "",
    tipe: "Poli / Internal",
    telepon: "",
    alamat: "",
  };
  showModal.value = true;
};

const openEditModal = (item: PelangganItem) => {
  isEditMode.value = true;
  editingId.value = item.id;
  errorMsg.value = "";
  form.value = {
    kode_pelanggan: item.kode_pelanggan,
    nama_pelanggan: item.nama_pelanggan,
    tipe: item.tipe || "Poli / Internal",
    telepon: item.telepon || "",
    alamat: item.alamat || "",
  };
  showModal.value = true;
};

const handleSubmit = async () => {
  saving.value = true;
  errorMsg.value = "";
  try {
    if (isEditMode.value && editingId.value !== null) {
      const res = await api.put(`/pelanggan/${editingId.value}`, form.value);
      const index = listPelanggan.value.findIndex(
        (p) => p.id === editingId.value,
      );
      if (index !== -1) listPelanggan.value[index] = res.data;
    } else {
      const res = await api.post("/pelanggan", form.value);
      listPelanggan.value.push(res.data);
    }
    showModal.value = false;
  } catch (err: any) {
    errorMsg.value =
      err.response?.data?.detail || "Gagal menyimpan data pelanggan";
  } finally {
    saving.value = false;
  }
};

const handleDelete = async (item: PelangganItem) => {
  if (
    !confirm(
      `Hapus data pelanggan "${item.nama_pelanggan}" (${item.kode_pelanggan})?`,
    )
  )
    return;
  try {
    await api.delete(`/pelanggan/${item.id}`);
    listPelanggan.value = listPelanggan.value.filter((p) => p.id !== item.id);
  } catch (err: any) {
    alert(err.response?.data?.detail || "Gagal menghapus data pelanggan");
  }
};

const getTipeVariant = (tipe: string) => {
  if (tipe === "Umum") return "info" as const;
  if (tipe === "BPJS") return "success" as const;
  return "neutral" as const;
};

onMounted(fetchPelanggan);
</script>

<template>
  <div class="space-y-6">
    <PageHeader
      title="Master Data Pelanggan"
      subtitle="Daftar unit tujuan, poli, atau apotek mitra yang akan muncul pada pilihan form barang keluar."
      :icon="Users"
    >
      <template #actions>
        <SearchInput
          v-model="searchQuery"
          placeholder="Cari kode atau nama pelanggan..."
        />

        <select
          v-model="filterTipe"
          class="px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl text-slate-700 focus:bg-white focus:border-blue-600 focus:outline-none cursor-pointer"
        >
          <option value="Semua">Semua Tipe</option>
          <option v-for="t in tipeOptions" :key="t" :value="t">{{ t }}</option>
        </select>

        <BaseButton @click="openCreateModal">
          <Plus class="w-4 h-4" />
          <span>Tambah Pelanggan</span>
        </BaseButton>
      </template>
    </PageHeader>

    <DataTable
      :columns="columns"
      :loading="loading"
      :is-empty="filteredPelanggan.length === 0"
      empty-text="Belum ada data pelanggan terdaftar."
    >
      <tr
        v-for="item in filteredPelanggan"
        :key="item.id"
        class="hover:bg-slate-50/70 transition"
      >
        <td class="py-4 px-6 font-mono text-xs font-semibold text-blue-600">
          {{ item.kode_pelanggan }}
        </td>
        <td class="py-4 px-6 font-medium text-slate-900">
          {{ item.nama_pelanggan }}
        </td>
        <td class="py-4 px-6">
          <StatusBadge
            :variant="getTipeVariant(item.tipe)"
            :label="item.tipe"
          />
        </td>
        <td class="py-4 px-6 text-slate-600 text-xs">
          <div v-if="item.telepon" class="inline-flex items-center gap-1.5">
            <Phone class="w-3.5 h-3.5 text-slate-400" />
            <span>{{ item.telepon }}</span>
          </div>
          <span v-else class="text-slate-400">-</span>
        </td>
        <td class="py-4 px-6 text-slate-500 text-xs max-w-xs truncate">
          <div v-if="item.alamat" class="inline-flex items-center gap-1.5">
            <MapPin class="w-3.5 h-3.5 text-slate-400 shrink-0" />
            <span class="truncate">{{ item.alamat }}</span>
          </div>
          <span v-else class="text-slate-400">-</span>
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

    <!-- MODAL TAMBAH / EDIT PELANGGAN -->
    <BaseModal
      :show="showModal"
      :title="isEditMode ? 'Edit Data Pelanggan' : 'Tambah Pelanggan Baru'"
      :subtitle="
        isEditMode
          ? 'Perbarui informasi tujuan distribusi obat.'
          : 'Pelanggan baru akan langsung tersedia pada pilihan tujuan barang keluar.'
      "
      @close="showModal = false"
    >
      <form
        id="form-master-pelanggan"
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
              >Kode Pelanggan</label
            >
            <input
              v-model="form.kode_pelanggan"
              type="text"
              required
              placeholder="PLG-004"
              class="w-full px-3.5 py-2 text-sm font-mono uppercase bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-blue-600 focus:outline-none"
            />
          </div>

          <div>
            <label class="block text-xs font-medium text-slate-700 mb-1.5"
              >Kategori / Tipe</label
            >
            <select
              v-model="form.tipe"
              class="w-full px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl text-slate-700 focus:bg-white focus:border-blue-600 focus:outline-none cursor-pointer"
            >
              <option v-for="t in tipeOptions" :key="t" :value="t">
                {{ t }}
              </option>
            </select>
          </div>
        </div>

        <div>
          <label class="block text-xs font-medium text-slate-700 mb-1.5"
            >Nama Pelanggan</label
          >
          <input
            v-model="form.nama_pelanggan"
            type="text"
            required
            placeholder="Contoh: Poli Anak / Apotek Medika"
            class="w-full px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-blue-600 focus:outline-none"
          />
        </div>

        <div>
          <label class="block text-xs font-medium text-slate-700 mb-1.5"
            >No. Telepon / Ext. Ruangan</label
          >
          <input
            v-model="form.telepon"
            type="text"
            placeholder="0812... atau Ext. 105"
            class="w-full px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-blue-600 focus:outline-none"
          />
        </div>

        <div>
          <label class="block text-xs font-medium text-slate-700 mb-1.5"
            >Alamat / Lokasi Unit</label
          >
          <textarea
            v-model="form.alamat"
            rows="2"
            placeholder="Alamat pengiriman atau lokasi ruangan (opsional)..."
            class="w-full px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-blue-600 focus:outline-none resize-none"
          ></textarea>
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
          form="form-master-pelanggan"
          :loading="saving"
        >
          <Check v-if="!saving" class="w-4 h-4" />
          <span>{{
            saving
              ? "Menyimpan..."
              : isEditMode
                ? "Simpan Perubahan"
                : "Simpan Pelanggan"
          }}</span>
        </BaseButton>
      </template>
    </BaseModal>
  </div>
</template>
