import { defineConfig, loadEnv } from 'vite';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

// Convert import.meta.url to file path
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load environment variables
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, resolve(__dirname, 'frontend'));  // Fix for `undefined` error

  return {
    root: '.',
    base: env.VITE_BASE_URL || '/',
    publicDir: 'public',
    build: {
      outDir: resolve(__dirname, 'dist'), // Ensure correct output directory
      assetsDir: 'assets',
      rollupOptions: {
        input: {
          main: resolve(__dirname, 'frontend/index.html'),
          signup: resolve(__dirname, 'frontend/signup.html'),
          login: resolve(__dirname, 'frontend/login.html'),
        },
      },
    },

    server: {
      port: 3000,
      host: true,
      strictPort: true,
      allowedHosts: "all",
      open: false,
    },
  };
});
