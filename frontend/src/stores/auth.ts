import { defineStore } from "pinia";
import { ref } from "vue";
import api from "@/api/axios";

export interface UserData {
  id: number;
  nama: string;
  username: string;
  role: string;
}

export const useAuthStore = defineStore("auth", () => {
  const savedUser = localStorage.getItem("gudang_user");
  const user = ref<UserData | null>(savedUser ? JSON.parse(savedUser) : null);

  async function login(username: string, password: string) {
    const res = await api.post("/login", { username, password });
    user.value = res.data.user;
    localStorage.setItem("gudang_user", JSON.stringify(res.data.user));
  }

  function logout() {
    user.value = null;
    localStorage.removeItem("gudang_user");
  }

  return { user, login, logout };
});
