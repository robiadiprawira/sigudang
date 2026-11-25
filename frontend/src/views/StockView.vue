<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import api from "@/api/axios";
import { Edit3, Trash2, Package, Check, AlertCircle } from "@lucide/vue";

import PageHeader from "@/components/PageHeader.vue";
import SearchInput from "@/components/SearchInput.vue";
import DataTable from "@/components/DataTable.vue";
import StatusBadge from "@/components/StatusBadge.vue";
import BaseModal from "@/components/BaseModal.vue";
import BaseButton from "@/components/BaseButton.vue";

interface ObatStock {
  id: number;
  kode_obat: string;
  nama_obat: string;
  kategori: string;
  satuan: string;
  stok: number;
  stok_minimal: number;
}

const columns = [
  { key: "kode", label: "Kode Obat" },
  { key: "nama", label: "Nama Obat" },
  { key: "kategori", label: "Kategori" },
  { key: "stok", label: "Jumlah Stock" },
  { key: "status", label: "Status" },
  { key: "aksi", label: "Aksi", align: "right" as const },
];

const daftarObat = ref<ObatStock[]>([]);
const loading = ref(true);
const searchQuery = ref("");
const filterSatuan = ref("Semua");

const showEditModal = ref(false);
const selectedObat = ref<ObatStock | null>(null);
const inputJumlahBaru = ref<number>(0);
const saving = ref(false);
const errorMsg = ref("");

const fetchStock = async () => {
  loading.value = true;
  try {
    const res = await api.get("/stock");
    daftarObat.value = res.data;
  } catch (err) {
    console.error("Gagal mengambil data stok:", err);
  } finally {
    loading.value = false;
  }
};

const daftarSatuan = computed(() => {
  const satuanSet = new Set(daftarObat.value.map((item) => item.satuan));
  return ["Semua", ...Array.from(satuanSet)];
});

const filteredObat = computed(() => {
  return daftarObat.value.filter((item) => {
    const cocokCari =
      item.nama_obat.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.kode_obat.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.kategori.toLowerCase().includes(searchQuery.value.toLowerCase());

    const cocokSatuan =
      filterSatuan.value === "Semua" || item.satuan === filterSatuan.value;
    return cocokCari && cocokSatuan;
  });
});

const openEditModal = (obat: ObatStock) => {
  selectedObat.value = obat;
  inputJumlahBaru.value = obat.stok;
  errorMsg.value = "";
  showEditModal.value = true;
};

const handleUpdateJumlah = async () => {
  if (!selectedObat.value) return;
  if (inputJumlahBaru.value < 0) {
    errorMsg.value = "Jumlah stok tidak boleh negatif.";
    return;
  }

  saving.value = true;
  errorMsg.value = "";
  try {
    await api.patch(`/stock/${selectedObat.value.id}`, {
      stok: Number(inputJumlahBaru.value),
    });
    selectedObat.value.stok = Number(inputJumlahBaru.value);
    showEditModal.value = false;
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || "Gagal mengubah jumlah stok";
  } finally {
    saving.value = false;
  }
};

const handleDelete = async (obat: ObatStock) => {
  if (
    !confirm(
      `Yakin ingin menghapus "${obat.nama_obat}" (${obat.kode_obat}) dari daftar stok?`,
    )
  )
    return;
  try {
    await api.delete(`/stock/${obat.id}`);
    daftarObat.value = daftarObat.value.filter((item) => item.id !== obat.id);
  } catch (err: any) {
    alert(err.response?.data?.detail || "Gagal menghapus data obat");
  }
};

const getStatusBadge = (item: ObatStock) => {
  if (item.stok === 0)
    return { label: "Habis (0)", variant: "danger" as const };
  if (item.stok <= item.stok_minimal)
    return { label: "Menipis", variant: "warning" as const };
  return { label: "Tersedia", variant: "success" as const };
};

onMounted(fetchStock);
</script>

<template>
  <div class="space-y-6">
    <PageHeader
      title="Monitoring Stock Obat"
      subtitle="Kelola jumlah stok fisik obat sesuai satuan kemasan (Strip/Lembar, Botol, Box, Tube, dll)."
      :icon="Package"
    >
      <template #actions>
        <SearchInput
          v-model="searchQuery"
          placeholder="Cari kode atau nama obat..."
        />
        <select
          v-model="filterSatuan"
          class="px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl text-slate-700 focus:bg-white focus:border-blue-600 focus:outline-none cursor-pointer"
        >
          <option v-for="satuan in daftarSatuan" :key="satuan" :value="satuan">
            Satuan: {{ satuan }}
          </option>
        </select>
      </template>
    </PageHeader>

    <DataTable
      :columns="columns"
      :loading="loading"
      :is-empty="filteredObat.length === 0"
      empty-text="Data obat tidak ditemukan."
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
        <td class="py-4 px-6 text-slate-500">{{ item.kategori }}</td>
        <td class="py-4 px-6">
          <span class="font-bold text-slate-900 text-base">{{
            item.stok
          }}</span>
          <span
            class="ml-1.5 px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 text-xs font-medium"
          >
            {{ item.satuan }}
          </span>
        </td>
        <td class="py-4 px-6">
          <StatusBadge
            :variant="getStatusBadge(item).variant"
            :label="getStatusBadge(item).label"
          />
        </td>
        <td class="py-4 px-6 text-right">
          <div class="inline-flex items-center justify-end gap-2">
            <BaseButton
              size="sm"
              variant="secondary"
              @click="openEditModal(item)"
            >
              <Edit3 class="w-3.5 h-3.5 text-blue-600" />
              <span>Ubah Jumlah</span>
            </BaseButton>
            <BaseButton size="sm" variant="danger" @click="handleDelete(item)">
              <Trash2 class="w-3.5 h-3.5" />
              <span>Hapus</span>
            </BaseButton>
          </div>
        </td>
      </tr>
    </DataTable>

    <BaseModal
      :show="showEditModal && !!selectedObat"
      title="Ubah Jumlah Stock"
      :subtitle="
        selectedObat
          ? `${selectedObat.kode_obat} — ${selectedObat.nama_obat}`
          : ''
      "
      @close="showEditModal = false"
    >
      <form
        id="form-edit-stok"
        @submit.prevent="handleUpdateJumlah"
        class="space-y-4"
      >
        <div
          v-if="errorMsg"
          class="p-3 rounded-xl bg-red-50 border border-red-200 flex items-center gap-2 text-xs text-red-600"
        >
          <AlertCircle class="w-4 h-4 shrink-0" />
          <span>{{ errorMsg }}</span>
        </div>

        <div>
          <label class="block text-xs font-medium text-slate-700 mb-1.5">
            Jumlah Stock Baru (dalam satuan
            <span class="font-bold text-blue-600">{{
              selectedObat?.satuan
            }}</span
            >)
          </label>
          <div class="flex items-center gap-2">
            <input
              v-model.number="inputJumlahBaru"
              type="number"
              min="0"
              required
              class="w-full px-4 py-2.5 text-base font-semibold bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-blue-600 focus:outline-none"
            />
            <span
              class="px-3.5 py-2.5 bg-slate-100 border border-slate-200 rounded-xl text-xs font-semibold text-slate-600 shrink-0"
            >
              {{ selectedObat?.satuan }}
            </span>
          </div>
          <p class="text-[11px] text-slate-400 mt-1.5">
            Stok sebelumnya: {{ selectedObat?.stok }} {{ selectedObat?.satuan }}
          </p>
        </div>
      </form>

      <template #footer>
        <BaseButton size="sm" variant="ghost" @click="showEditModal = false"
          >Batal</BaseButton
        >
        <BaseButton
          size="sm"
          variant="primary"
          type="submit"
          form="form-edit-stok"
          :loading="saving"
        >
          <Check v-if="!saving" class="w-4 h-4" />
          <span>{{ saving ? "Menyimpan..." : "Simpan Perubahan" }}</span>
        </BaseButton>
      </template>
    </BaseModal>
  </div>
</template>
