import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 120000,
  expect: {
    timeout: 15000,
  },
  workers: 1,
  use: {
    baseURL: 'http://frontend:3000',
  },
  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
  ],
})
