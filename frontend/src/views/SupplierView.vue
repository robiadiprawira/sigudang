<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import api from "@/api/axios";
import {
  Truck,
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
import BaseModal from "@/components/BaseModal.vue";
import BaseButton from "@/components/BaseButton.vue";

interface SupplierItem {
  id: number;
  kode_supplier: string;
  nama_supplier: string;
  telepon: string;
  alamat: string;
}

const columns = [
  { key: "kode", label: "Kode Supplier" },
  { key: "nama", label: "Nama Supplier / Distributor" },
  { key: "telepon", label: "Kontak / Telepon" },
  { key: "alamat", label: "Alamat" },
  { key: "aksi", label: "Aksi", align: "right" as const },
];

const listSupplier = ref<SupplierItem[]>([]);
const loading = ref(true);
const searchQuery = ref("");

// State Modal Tambah & Edit
const showModal = ref(false);
const isEditMode = ref(false);
const editingId = ref<number | null>(null);
const saving = ref(false);
const errorMsg = ref("");

const form = ref({
  kode_supplier: "",
  nama_supplier: "",
  telepon: "",
  alamat: "",
});

const fetchSupplier = async () => {
  loading.value = true;
  try {
    const res = await api.get("/supplier");
    listSupplier.value = res.data;
  } catch (err) {
    console.error("Gagal memuat data supplier:", err);
  } finally {
    loading.value = false;
  }
};

const filteredSupplier = computed(() => {
  const q = searchQuery.value.toLowerCase();
  return listSupplier.value.filter(
    (item) =>
      item.nama_supplier.toLowerCase().includes(q) ||
      item.kode_supplier.toLowerCase().includes(q) ||
      (item.telepon && item.telepon.toLowerCase().includes(q)) ||
      (item.alamat && item.alamat.toLowerCase().includes(q)),
  );
});

const generateNextKode = () => {
  const nextNum = listSupplier.value.length + 1;
  return `SUP-${String(nextNum).padStart(3, "0")}`;
};

const openCreateModal = () => {
  isEditMode.value = false;
  editingId.value = null;
  errorMsg.value = "";
  form.value = {
    kode_supplier: generateNextKode(),
    nama_supplier: "",
    telepon: "",
    alamat: "",
  };
  showModal.value = true;
};

const openEditModal = (item: SupplierItem) => {
  isEditMode.value = true;
  editingId.value = item.id;
  errorMsg.value = "";
  form.value = {
    kode_supplier: item.kode_supplier,
    nama_supplier: item.nama_supplier,
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
      const res = await api.put(`/supplier/${editingId.value}`, form.value);
      const index = listSupplier.value.findIndex(
        (s) => s.id === editingId.value,
      );
      if (index !== -1) listSupplier.value[index] = res.data;
    } else {
      const res = await api.post("/supplier", form.value);
      listSupplier.value.push(res.data);
    }
    showModal.value = false;
  } catch (err: any) {
    errorMsg.value =
      err.response?.data?.detail || "Gagal menyimpan data supplier";
  } finally {
    saving.value = false;
  }
};

const handleDelete = async (item: SupplierItem) => {
  if (
    !confirm(
      `Hapus data supplier "${item.nama_supplier}" (${item.kode_supplier})?`,
    )
  )
    return;
  try {
    await api.delete(`/supplier/${item.id}`);
    listSupplier.value = listSupplier.value.filter((s) => s.id !== item.id);
  } catch (err: any) {
    alert(err.response?.data?.detail || "Gagal menghapus data supplier");
  }
};

onMounted(fetchSupplier);
</script>

<template>
  <div class="space-y-6">
    <PageHeader
      title="Master Data Supplier"
      subtitle="Daftar pemasok dan distributor resmi yang akan muncul pada form transaksi barang masuk."
      :icon="Truck"
    >
      <template #actions>
        <SearchInput
          v-model="searchQuery"
          placeholder="Cari kode atau nama supplier..."
        />

        <BaseButton @click="openCreateModal">
          <Plus class="w-4 h-4" />
          <span>Tambah Supplier</span>
        </BaseButton>
      </template>
    </PageHeader>

    <DataTable
      :columns="columns"
      :loading="loading"
      :is-empty="filteredSupplier.length === 0"
      empty-text="Belum ada data supplier terdaftar."
    >
      <tr
        v-for="item in filteredSupplier"
        :key="item.id"
        class="hover:bg-slate-50/70 transition"
      >
        <td class="py-4 px-6 font-mono text-xs font-semibold text-blue-600">
          {{ item.kode_supplier }}
        </td>
        <td class="py-4 px-6 font-medium text-slate-900">
          {{ item.nama_supplier }}
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

    <!-- MODAL TAMBAH / EDIT SUPPLIER -->
    <BaseModal
      :show="showModal"
      :title="isEditMode ? 'Edit Data Supplier' : 'Tambah Supplier Baru'"
      :subtitle="
        isEditMode
          ? 'Perbarui informasi pemasok obat.'
          : 'Supplier baru akan langsung tersedia pada form barang masuk.'
      "
      @close="showModal = false"
    >
      <form
        id="form-master-supplier"
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
              >Kode Supplier</label
            >
            <input
              v-model="form.kode_supplier"
              type="text"
              required
              placeholder="SUP-004"
              class="w-full px-3.5 py-2 text-sm font-mono uppercase bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-blue-600 focus:outline-none"
            />
          </div>

          <div>
            <label class="block text-xs font-medium text-slate-700 mb-1.5"
              >No. Telepon / WA</label
            >
            <input
              v-model="form.telepon"
              type="text"
              placeholder="021-xxxxxxx / 0812..."
              class="w-full px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-blue-600 focus:outline-none"
            />
          </div>
        </div>

        <div>
          <label class="block text-xs font-medium text-slate-700 mb-1.5"
            >Nama Supplier / Perusahaan</label
          >
          <input
            v-model="form.nama_supplier"
            type="text"
            required
            placeholder="Contoh: PT Bina San Prima"
            class="w-full px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-blue-600 focus:outline-none"
          />
        </div>

        <div>
          <label class="block text-xs font-medium text-slate-700 mb-1.5"
            >Alamat Lengkap</label
          >
          <textarea
            v-model="form.alamat"
            rows="2"
            placeholder="Alamat gudang atau kantor distributor (opsional)..."
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
          form="form-master-supplier"
          :loading="saving"
        >
          <Check v-if="!saving" class="w-4 h-4" />
          <span>{{
            saving
              ? "Menyimpan..."
              : isEditMode
                ? "Simpan Perubahan"
                : "Simpan Supplier"
          }}</span>
        </BaseButton>
      </template>
    </BaseModal>
  </div>
</template>
