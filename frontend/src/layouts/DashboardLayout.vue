<script setup lang="ts">
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import {
  Pill,
  LayoutDashboard,
  Package,
  Layers,
  ArrowDownLeft,
  ArrowUpRight,
  Users,
  LogOut,
  Search,
  Bell,
  AlertTriangle,
} from "@lucide/vue";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const mainMenu = [
  { name: "Dashboard", path: "/", icon: LayoutDashboard },
  { name: "Master Obat", path: "/obat", icon: Package },
  { name: "Stok & Batch", path: "/batch", icon: Layers },
  { name: "Barang Masuk", path: "/masuk", icon: ArrowDownLeft },
  { name: "Barang Keluar", path: "/keluar", icon: ArrowUpRight },
];

const handleLogout = () => {
  authStore.logout();
  router.push("/login");
};
</script>

<template>
  <div class="min-h-screen bg-[#F8FAFC] flex text-slate-800">
    <!-- SIDEBAR -->
    <aside
      class="w-64 bg-white border-r border-slate-200/80 flex flex-col justify-between shrink-0"
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
          <div>
            <p
              class="px-3 text-[11px] font-semibold tracking-wider text-slate-400 uppercase mb-2"
            >
              Main Menu
            </p>
            <nav class="space-y-1">
              <router-link
                v-for="item in mainMenu"
                :key="item.path"
                :to="item.path"
                class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition"
                :class="
                  route.path === item.path
                    ? 'bg-blue-50 text-blue-600'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                "
              >
                <component :is="item.icon" class="w-4 h-4" />
                <span>{{ item.name }}</span>
              </router-link>
            </nav>
          </div>

          <div>
            <p
              class="px-3 text-[11px] font-semibold tracking-wider text-slate-400 uppercase mb-2"
            >
              Other
            </p>
            <nav class="space-y-1">
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
                <span>Kelola Petugas</span>
              </router-link>

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

      <!-- Bottom Card & User Profile (Sesuai Referensi) -->
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
            to="/batch"
            class="block text-center w-full py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium rounded-xl transition"
          >
            Cek Batch Obat
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
            <Bell class="w-4 h-4" />
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
