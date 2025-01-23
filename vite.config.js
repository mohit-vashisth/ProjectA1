import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd());

  return {
    build: {
      rollupOptions: {
        input: {
          main: env.VITE_BASE_URL || '/index.html',
          signup: env.VITE_SIGNUP_URL || '/signup.html',
          login: env.VITE_LOGIN_URL || '/login.html',
        },
      },
    },
  };
});
