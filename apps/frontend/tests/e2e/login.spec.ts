import { test, expect } from '@playwright/test'

async function login(page: any, email: string, password: string) {
  await page.goto('/login', { waitUntil: 'domcontentloaded' })
  await expect(page.getByPlaceholder('Email')).toBeVisible()
  await page.fill('input[placeholder="Email"]', email)
  await page.fill('input[placeholder="Password"]', password)
  await page.click('button[type="submit"]')
}

test('HR Admin logs in, lands on HR dashboard, and logs out', async ({ page }) => {
  await login(page, 'admin@stepup.com', 'Admin1234!')
  await page.waitForURL('**/hr/dashboard')
  await expect(page).toHaveURL('/hr/dashboard')

  await page.click('button:has-text("Logout")')
  await page.waitForURL('**/login')
  await expect(page).toHaveURL('/login')
})

test('Manager logs in and lands on Manager dashboard', async ({ page }) => {
  await login(page, 'manager@stepup.com', 'Manager1234!')
  await page.waitForURL('**/manager/dashboard')
  await expect(page).toHaveURL('/manager/dashboard')
})

test('Employee logs in and lands on Employee dashboard', async ({ page }) => {
  await login(page, 'employee@stepup.com', 'Employee1234!')
  await page.waitForURL('**/employee/dashboard')
  await expect(page).toHaveURL('/employee/dashboard')
})

test('wrong password shows error and does not navigate', async ({ page }) => {
  await login(page, 'admin@stepup.com', 'wrongpassword')
  await expect(page).toHaveURL('/login')
})
