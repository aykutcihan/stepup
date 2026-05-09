import { test, expect } from '@playwright/test'

async function login(page: any, email: string, password: string) {
  await page.goto('/login', { waitUntil: 'domcontentloaded' })
  await expect(page.getByPlaceholder('Email')).toBeVisible()
  await page.fill('input[placeholder="Email"]', email)
  await page.fill('input[placeholder="Password"]', password)
  await page.click('button[type="submit"]')
}

test('Employee accessing HR dashboard is redirected to 403', async ({ page }) => {
  await login(page, 'employee@stepup.com', 'Employee1234!')
  await page.waitForURL('**/employee/dashboard')

  await page.goto('/hr/dashboard')
  await expect(page).toHaveURL('/403')
})

test('deactivated user sees deactivation message on login page', async ({ page }) => {
  await page.goto('/login?error=USER_DEACTIVATED')
  await expect(page.getByText('Your account has been deactivated. Please contact your HR Admin.')).toBeVisible()
})
