import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],

  server: {
    port: 5175,

    proxy: {
      "/django-api": {
        target: "https://curd-opration-0.onrender.com",
        changeOrigin: true,
        secure: false,

        rewrite: (path) =>
          path.replace(/^\/django-api/, ""),
      },
    },
  },
});