import { defineConfig, loadEnv } from 'vite';

// Load environment variables
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd());

  // Get the base URL and other page-specific URLs from environment variables or defaults
  const baseURL = env.VITE_BASE_URL || '/';
  const signupURL = env.VITE_SIGNUP_PAGE || '/signup.html';  // Corrected to use the correct variable
  const loginURL = env.VITE_LOGIN_PAGE || '/login.html';    // Corrected to use the correct variable

  return {
    // Set the base URL from the environment variable (for routing)
    base: baseURL,

    // Configure the build settings, including specifying entry points for different pages
    build: {
      outDir: 'dist',
      assetsDir: 'assets',
      rollupOptions: {
        input: {
          main: env.VITE_BASE_URL || '/index.html',
          signup: signupURL,
          login: loginURL,
        },
      },
    },

    // Configure development server settings
    server: {
      port: 3000,
      host: true,
      strictPort: true,
      allowedHosts: "all",
    },
  };
});
