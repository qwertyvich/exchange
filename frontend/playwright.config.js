import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests', workers: 1, timeout: 30000,
  use: {browserName:process.env.PLAYWRIGHT_BROWSER || 'chromium', baseURL:process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:5173', viewport:{width:1440,height:1000}, trace:'retain-on-failure'},
});
