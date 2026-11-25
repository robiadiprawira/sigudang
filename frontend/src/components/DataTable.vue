<script setup lang="ts">
defineProps<{
  columns: {
    key: string;
    label: string;
    align?: "left" | "right" | "center";
  }[];
  loading?: boolean;
  isEmpty?: boolean;
  emptyText?: string;
}>();
</script>

<template>
  <div class="bg-white rounded-2xl border border-slate-200/80 overflow-hidden">
    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr
            class="border-b border-slate-200/80 bg-slate-50/70 text-[11px] font-semibold uppercase tracking-wider text-slate-500"
          >
            <th
              v-for="col in columns"
              :key="col.key"
              class="py-3.5 px-6"
              :class="{
                'text-right': col.align === 'right',
                'text-center': col.align === 'center',
              }"
            >
              {{ col.label }}
            </th>
          </tr>
        </thead>

        <tbody class="divide-y divide-slate-100 text-sm">
          <tr v-if="loading">
            <td
              :colspan="columns.length"
              class="py-10 text-center text-slate-400"
            >
              Memuat data...
            </td>
          </tr>

          <tr v-else-if="isEmpty">
            <td
              :colspan="columns.length"
              class="py-10 text-center text-slate-400"
            >
              {{ emptyText || "Data tidak ditemukan." }}
            </td>
          </tr>

          <slot v-else />
        </tbody>
      </table>
    </div>
  </div>
</template>
