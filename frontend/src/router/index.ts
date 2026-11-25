import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import LoginView from "@/views/LoginView.vue";
import DashboardLayout from "@/layouts/DashboardLayout.vue";
import DashboardView from "@/views/DashboardView.vue";
import ComingSoonView from "@/views/ComingSoonView.vue";
import NotificationView from "@/views/NotificationView.vue";
import StockView from "@/views/StockView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/",
      component: DashboardLayout,
      meta: { requiresAuth: true },
      children: [
        { path: "", name: "dashboard", component: DashboardView },
        { path: "notifikasi", name: "notifikasi", component: NotificationView },
        // Transaksi
        { path: "transaksi/stock", name: "stock-obat", component: StockView },
        {
          path: "transaksi/masuk",
          name: "barang-masuk",
          component: ComingSoonView,
          meta: { title: "Transaksi Barang Masuk" },
        },
        {
          path: "transaksi/keluar",
          name: "barang-keluar",
          component: ComingSoonView,
          meta: { title: "Transaksi Barang Keluar" },
        },
        {
          path: "transaksi/retur",
          name: "retur-barang",
          component: ComingSoonView,
          meta: { title: "Retur Barang" },
        },
        // Master Data
        {
          path: "master/obat",
          name: "master-obat",
          component: ComingSoonView,
          meta: { title: "Master Data Obat" },
        },
        {
          path: "master/kategori-satuan",
          name: "kategori-satuan",
          component: ComingSoonView,
          meta: { title: "Master Kategori & Satuan" },
        },
        {
          path: "master/supplier",
          name: "master-supplier",
          component: ComingSoonView,
          meta: { title: "Master Data Supplier" },
        },
        {
          path: "master/pelanggan",
          name: "master-pelanggan",
          component: ComingSoonView,
          meta: { title: "Master Data Pelanggan" },
        },
        // Manajemen User
        {
          path: "users",
          name: "manajemen-user",
          component: ComingSoonView,
          meta: { title: "Manajemen User" },
        },
      ],
    },
  ],
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.user) {
    next("/login");
  } else if (to.path === "/login" && authStore.user) {
    next("/");
  } else {
    next();
  }
});

export default router;
