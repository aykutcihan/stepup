import { test, expect } from '@playwright/test'

test('expired invitation token shows error message', async ({ page }) => {
  await page.goto('/register?token=expired-or-invalid-token')
  await expect(page.getByText('This invitation link is invalid.')).toBeVisible()
})
