import { expect, test } from '@playwright/test'

test.describe('Cotización FastExpress — E2E', () => {
  test('calcula y muestra una cotización VIP express', async ({ page }) => {
    // Valida: UI-AC-002, QUOTE-AC-001
    await page.goto('/')

    await page.locator('#weight_input').fill('5.01')
    await page.getByRole('button', { name: /VIP/ }).click()
    await page.getByRole('button', { name: /Express/ }).click()
    await page.getByRole('button', { name: /Calcular cotización/i }).click()

    await expect(page.getByText('Recibo de cotización')).toBeVisible()
    await expect(page.getByText('$26.29 USD')).toBeVisible()
    await expect(page.getByText('FastExpress API')).toBeVisible()
  })

  test('rechaza peso superior al máximo sin llamar al backend', async ({ page }) => {
    // Valida: UI-AC-003, QUOTE-AC-002
    await page.goto('/')

    await page.locator('#weight_input').fill('20.01')
    await page.getByRole('button', { name: /Calcular cotización/i }).click()

    await expect(page.getByRole('alert')).toContainText('Envío Rechazado')
    await expect(page.getByText('Tu cotización aparecerá aquí')).toBeVisible()
  })

  test('muestra error cuando el backend no está disponible', async ({ page }) => {
    // Valida: UI-AC-003, UI-REQ-006
    await page.route('http://127.0.0.1:8000/**', (route) => route.abort())
    await page.goto('/')

    await page.locator('#weight_input').fill('1.00')
    await page.getByRole('button', { name: /Calcular cotización/i }).click()

    await expect(page.getByText('Error al procesar la cotización')).toBeVisible()
    await expect(page.getByText('No fue posible comunicarse')).toBeVisible()
  })
})
