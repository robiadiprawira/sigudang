<script setup lang="ts">
import { ref, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import {
  Pill,
  LayoutDashboard,
  ArrowLeftRight,
  Database,
  Users,
  LogOut,
  Search,
  Bell,
  AlertTriangle,
  ChevronDown,
} from "@lucide/vue";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

// State untuk mengontrol buka/tutup dropdown menu
const openMenus = ref<{ [key: string]: boolean }>({
  transaksi: true,
  masterData: false,
});

const toggleMenu = (key: string) => {
  openMenus.value[key] = !openMenus.value[key];
};

// Definisi Submenu
const transaksiChildren = [
  { name: "Stock", path: "/transaksi/stock" },
  { name: "Barang Masuk", path: "/transaksi/masuk" },
  { name: "Barang Keluar", path: "/transaksi/keluar" },
  { name: "Retur Barang", path: "/transaksi/retur" },
];

const masterDataChildren = [
  { name: "Data Obat", path: "/master/obat" },
  { name: "Kategori & Satuan", path: "/master/kategori-satuan" },
  { name: "Data Supplier", path: "/master/supplier" },
  { name: "Data Pelanggan", path: "/master/pelanggan" },
];

// Otomatis buka parent menu jika user mengakses URL child-nya langsung
watch(
  () => route.path,
  (newPath) => {
    if (newPath.startsWith("/transaksi")) openMenus.value.transaksi = true;
    if (newPath.startsWith("/master")) openMenus.value.masterData = true;
  },
  { immediate: true },
);

const handleLogout = () => {
  authStore.logout();
  router.push("/login");
};
</script>

<template>
  <div class="min-h-screen bg-[#F8FAFC] flex text-slate-800">
    <!-- SIDEBAR -->
    <aside
      class="w-64 bg-white border-r border-slate-200/80 flex flex-col justify-between shrink-0 overflow-y-auto"
    >
      <div>
        <!-- Logo -->
        <div
          class="h-16 px-6 flex items-center gap-3 border-b border-slate-100"
        >
          <div
            class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white"
          >
            <Pill class="w-4 h-4" />
          </div>
          <span class="font-bold text-base tracking-tight text-slate-900"
            >PharmaStock</span
          >
        </div>

        <!-- Menu Groups -->
        <div class="p-4 space-y-6">
          <!-- MAIN MENU -->
          <div>
            <p
              class="px-3 text-[11px] font-semibold tracking-wider text-slate-400 uppercase mb-2"
            >
              Main Menu
            </p>
            <nav class="space-y-1">
              <!-- Dashboard -->
              <router-link
                to="/"
                class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition"
                :class="
                  route.path === '/'
                    ? 'bg-blue-50 text-blue-600'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                "
              >
                <LayoutDashboard class="w-4 h-4" />
                <span>Dashboard</span>
              </router-link>

              <!-- Transaksi (Dropdown) -->
              <div>
                <button
                  @click="toggleMenu('transaksi')"
                  class="w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-medium transition cursor-pointer"
                  :class="
                    route.path.startsWith('/transaksi')
                      ? 'text-blue-600 bg-blue-50/50'
                      : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                  "
                >
                  <div class="flex items-center gap-3">
                    <ArrowLeftRight class="w-4 h-4" />
                    <span>Transaksi</span>
                  </div>
                  <ChevronDown
                    class="w-4 h-4 text-slate-400 transition-transform duration-200"
                    :class="{ 'rotate-180 text-blue-600': openMenus.transaksi }"
                  />
                </button>

                <!-- Child Transaksi -->
                <div
                  v-show="openMenus.transaksi"
                  class="mt-1 ml-4 pl-3 border-l border-slate-200 space-y-1"
                >
                  <router-link
                    v-for="child in transaksiChildren"
                    :key="child.path"
                    :to="child.path"
                    class="block px-3 py-2 rounded-lg text-xs font-medium transition"
                    :class="
                      route.path === child.path
                        ? 'bg-blue-50 text-blue-600 font-semibold'
                        : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'
                    "
                  >
                    {{ child.name }}
                  </router-link>
                </div>
              </div>
            </nav>
          </div>

          <!-- OTHER -->
          <div>
            <p
              class="px-3 text-[11px] font-semibold tracking-wider text-slate-400 uppercase mb-2"
            >
              Other
            </p>
            <nav class="space-y-1">
              <!-- Master Data (Dropdown) -->
              <div>
                <button
                  @click="toggleMenu('masterData')"
                  class="w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-medium transition cursor-pointer"
                  :class="
                    route.path.startsWith('/master')
                      ? 'text-blue-600 bg-blue-50/50'
                      : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                  "
                >
                  <div class="flex items-center gap-3">
                    <Database class="w-4 h-4" />
                    <span>Master Data</span>
                  </div>
                  <ChevronDown
                    class="w-4 h-4 text-slate-400 transition-transform duration-200"
                    :class="{
                      'rotate-180 text-blue-600': openMenus.masterData,
                    }"
                  />
                </button>

                <!-- Child Master Data -->
                <div
                  v-show="openMenus.masterData"
                  class="mt-1 ml-4 pl-3 border-l border-slate-200 space-y-1"
                >
                  <router-link
                    v-for="child in masterDataChildren"
                    :key="child.path"
                    :to="child.path"
                    class="block px-3 py-2 rounded-lg text-xs font-medium transition"
                    :class="
                      route.path === child.path
                        ? 'bg-blue-50 text-blue-600 font-semibold'
                        : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'
                    "
                  >
                    {{ child.name }}
                  </router-link>
                </div>
              </div>

              <!-- Manajemen User -->
              <router-link
                v-if="authStore.user?.role === 'superadmin'"
                to="/users"
                class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition"
                :class="
                  route.path === '/users'
                    ? 'bg-blue-50 text-blue-600'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                "
              >
                <Users class="w-4 h-4" />
                <span>Manajemen User</span>
              </router-link>

              <!-- Sign Out -->
              <button
                @click="handleLogout"
                class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-slate-600 hover:bg-red-50 hover:text-red-600 transition cursor-pointer"
              >
                <LogOut class="w-4 h-4" />
                <span>Sign Out</span>
              </button>
            </nav>
          </div>
        </div>
      </div>

      <!-- Bottom Card & User Profile -->
      <div class="p-4 space-y-4">
        <div class="bg-slate-50 border border-slate-200/70 rounded-2xl p-4">
          <div class="flex items-center gap-2 text-amber-600 mb-1">
            <AlertTriangle class="w-4 h-4" />
            <span class="text-xs font-semibold">Pantau Expired</span>
          </div>
          <p class="text-xs text-slate-500 leading-relaxed mb-3">
            Cek batch obat yang mendekati tanggal kedaluwarsa secara berkala.
          </p>
          <router-link
            to="/transaksi/stock"
            class="block text-center w-full py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium rounded-xl transition"
          >
            Cek Stock & Batch
          </router-link>
        </div>

        <div class="flex items-center gap-3 px-1">
          <div
            class="w-9 h-9 rounded-full bg-blue-100 text-blue-700 font-bold text-xs flex items-center justify-center uppercase"
          >
            {{ authStore.user?.nama?.slice(0, 2) || "AD" }}
          </div>
          <div class="min-w-0">
            <p class="text-sm font-semibold text-slate-800 truncate">
              {{ authStore.user?.nama }}
            </p>
            <p class="text-xs text-slate-400 capitalize">
              {{ authStore.user?.role }}
            </p>
          </div>
        </div>
      </div>
    </aside>

    <!-- MAIN CONTENT -->
    <div class="flex-1 flex flex-col min-w-0">
      <!-- Top Header -->
      <header
        class="h-16 bg-white/80 backdrop-blur-sm border-b border-slate-200/80 px-8 flex items-center justify-between sticky top-0 z-10"
      >
        <h1 class="text-lg font-semibold text-slate-800">
          Halo {{ authStore.user?.nama }}, selamat bertugas!
        </h1>

        <div class="flex items-center gap-3">
          <div class="relative hidden sm:block">
            <Search
              class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2"
            />
            <input
              type="text"
              placeholder="Cari obat atau kode batch..."
              class="pl-9 pr-4 py-1.5 text-sm bg-slate-100/80 border border-transparent rounded-xl focus:bg-white focus:border-slate-300 focus:outline-none w-64 transition"
            />
          </div>
          <button
            class="w-9 h-9 rounded-xl border border-slate-200 flex items-center justify-center text-slate-600 hover:bg-slate-50 transition"
          >
            <router-link
              to="/notifikasi"
              class="relative w-9 h-9 rounded-xl border flex items-center justify-center transition"
              :class="
                route.path === '/notifikasi'
                  ? 'bg-blue-50 border-blue-200 text-blue-600'
                  : 'border-slate-200 text-slate-600 hover:bg-slate-50'
              "
              title="Notifikasi"
            >
              <Bell class="w-4 h-4" />
              <!-- Titik indikator notifikasi belum dibaca -->
              <span
                class="absolute top-2 right-2 w-2 h-2 rounded-full bg-red-500 ring-2 ring-white"
              ></span>
            </router-link>
          </button>
        </div>
      </header>

      <!-- Page Content -->
      <main class="p-8 flex-1">
        <router-view />
      </main>
    </div>
  </div>
</template>
