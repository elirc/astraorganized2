from pathlib import Path
s=Path('astra-remaining-improvements/stage/e502bf8af566')
def w(n,c):
 p=s/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(c.strip()+'\n',encoding='utf-8')
w('frontend/src/__tests__/ProductsPage.test.tsx',r'''
import { cleanup, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import App from '../App';
import { request } from '../api/client';
const initial = { id: 'p1', name: 'Notebook', price: '10.00', stock: 5, version: 1 };
let current = { ...initial }; let requests: { url: string; method: string; body: unknown }[];
beforeEach(() => {
  current = { ...initial }; requests = [];
  vi.stubGlobal('fetch', vi.fn(async (url: string, options?: RequestInit) => {
    const method = options?.method || 'GET'; const body = options?.body ? JSON.parse(String(options.body)) : undefined;
    requests.push({ url: String(url), method, body });
    return new Response(JSON.stringify({ data: String(url).includes('/products') ? [current] : [] }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  }));
});
afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.restoreAllMocks(); });
it('renders catalog data and the explicit demo identity boundary', async () => {
  render(<App />); expect(await screen.findByRole('heading', { name: 'Notebook' })).toBeInTheDocument();
  expect(screen.getByText(/Accounts and access control are not implemented/)).toBeInTheDocument();
  expect(screen.getByText(/5 in stock/)).toBeInTheDocument();
});
it('shows HTTP load failures instead of treating an error body as a list', async () => {
  vi.mocked(fetch).mockResolvedValue(new Response(JSON.stringify({ error: { message: 'Database unavailable' } }), { status: 503 }));
  render(<App />); expect(await screen.findByText(/Could not load products: Database unavailable/)).toBeInTheDocument();
});
it('sends an explicit product input with decimal text and integer stock', async () => {
  const user = userEvent.setup(); render(<App />); await screen.findByRole('heading', { name: 'Notebook' });
  await user.type(screen.getByLabelText('Product name'), 'Pen'); await user.type(screen.getByLabelText('Price'), '1.25');
  await user.clear(screen.getByLabelText('Stock')); await user.type(screen.getByLabelText('Stock'), '7'); await user.click(screen.getByRole('button', { name: 'Create product' }));
  await waitFor(() => expect(requests.find(r => r.method === 'POST')?.body).toEqual({ name: 'Pen', price: '1.25', stock: 7 }));
});
it('does not issue a delete when confirmation is cancelled', async () => {
  const user = userEvent.setup(); vi.spyOn(window, 'confirm').mockReturnValue(false); render(<App />);
  await user.click(await screen.findByRole('button', { name: 'Delete Notebook' })); expect(requests.filter(r => r.method === 'DELETE')).toHaveLength(0);
});
it('preserves a conflicting draft and disables its stale write until explicit reload', async () => {
  const user = userEvent.setup(); const normal = vi.mocked(fetch).getMockImplementation()!;
  vi.mocked(fetch).mockImplementation(async (url, options) => {
    if (options?.method === 'PATCH') { current = { ...initial, stock: 4, version: 2 }; return new Response(JSON.stringify({ error: { message: 'Refresh before updating.' } }), { status: 409 }); }
    return normal(url, options);
  });
  render(<App />); await user.click(await screen.findByRole('button', { name: 'Edit Notebook' }));
  await user.clear(screen.getByLabelText('Product name')); await user.type(screen.getByLabelText('Product name'), 'My draft'); await user.click(screen.getByRole('button', { name: 'Save product' }));
  await screen.findByText('Refresh before updating.'); expect(screen.getByLabelText('Product name')).toHaveValue('My draft'); expect(screen.getByRole('button', { name: 'Save product' })).toBeDisabled();
  vi.spyOn(window, 'confirm').mockReturnValue(true); await waitFor(() => expect(screen.getByRole('button', { name: 'Reload current product' })).toBeEnabled());
  await user.click(screen.getByRole('button', { name: 'Reload current product' })); expect(screen.getByLabelText('Stock')).toHaveValue(4); expect(screen.getByLabelText('Product name')).toHaveValue('Notebook');
});
it('submits cart identities and quantities without browser prices', async () => {
  const user = userEvent.setup(); render(<App />); const quantity = await screen.findByLabelText('Order quantity for Notebook');
  await user.clear(quantity); await user.type(quantity, '2'); await user.type(screen.getByLabelText('Customer reference'), 'customer-a'); await user.click(screen.getByRole('button', { name: 'Place order' }));
  await waitFor(() => expect(requests.find(r => r.method === 'POST')?.body).toEqual({ userId: 'customer-a', items: [{ productId: 'p1', quantity: 2 }] }));
});
it('accepts empty 204 delete responses without attempting JSON parsing', async () => {
  vi.mocked(fetch).mockResolvedValue(new Response(null, { status: 204 })); await expect(request('/products/p1', 'DELETE', { version: 1 })).resolves.toBeUndefined();
});
it('keeps failed order quantities for correction and retry', async () => {
  const user = userEvent.setup(); const normal = vi.mocked(fetch).getMockImplementation()!;
  vi.mocked(fetch).mockImplementation(async (url, options) => options?.method === 'POST' ? new Response(JSON.stringify({ error: { message: 'Insufficient stock' } }), { status: 409 }) : normal(url, options));
  render(<App />); const quantity = await screen.findByLabelText('Order quantity for Notebook'); await user.clear(quantity); await user.type(quantity, '2'); await user.type(screen.getByLabelText('Customer reference'), 'customer'); await user.click(screen.getByRole('button', { name: 'Place order' }));
  await screen.findByText('Insufficient stock'); expect(quantity).toHaveValue(2);
});
''')
w('playwright.config.ts',r'''
import { defineConfig } from '@playwright/test';
if (process.env.ORDER_TEST_DATABASE !== 'owned-temporary-cluster') throw new Error('Run npm run verify to create an isolated test database.');
const api = Number(process.env.ORDER_API_PORT); const web = Number(process.env.ORDER_WEB_PORT);
if (!api || !web) throw new Error('Verification ports must be allocated by the database helper.');
export default defineConfig({
  testDir: './e2e', workers: 1, retries: 0, timeout: 30000,
  use: { baseURL: `http://127.0.0.1:${web}`, browserName: 'chromium', trace: 'retain-on-failure' },
  webServer: [
    { command: 'node backend/dist/index.js', url: `http://127.0.0.1:${api}/health`, env: { PORT: String(api), HOST: '127.0.0.1' }, reuseExistingServer: false, timeout: 60000 },
    { command: `node frontend/node_modules/vite/bin/vite.js --host 127.0.0.1 --port ${web} --strictPort`, url: `http://127.0.0.1:${web}`, env: { VITE_API_URL: `http://127.0.0.1:${api}/api` }, reuseExistingServer: false, timeout: 60000 }
  ]
});
''')
w('e2e/orders.spec.ts',r'''
import { test, expect } from '@playwright/test';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';
const api = `http://127.0.0.1:${process.env.ORDER_API_PORT}/api`;
const name = (label: string) => `${label}-${Date.now()}`;
test('catalog CRUD persists across reload and cancelled deletion changes nothing', async ({ page }) => {
  const product = name('Notebook'); await page.goto('/');
  await page.getByLabel('Product name', { exact: true }).fill(product); await page.getByLabel('Price', { exact: true }).fill('12.50'); await page.getByLabel('Stock', { exact: true }).fill('5'); await page.getByRole('button', { name: 'Create product', exact: true }).click();
  const card = page.getByTestId('product-card').filter({ has: page.getByRole('heading', { name: product, exact: true }) });
  await expect(card).toContainText('$12.50'); await page.reload(); await expect(card).toContainText('5 in stock');
  await card.getByRole('button', { name: `Edit ${product}`, exact: true }).click(); await page.getByLabel('Price', { exact: true }).fill('13.25'); await page.getByRole('button', { name: 'Save product', exact: true }).click(); await expect(card).toContainText('$13.25');
  page.once('dialog', d => d.dismiss()); await card.getByRole('button', { name: `Delete ${product}`, exact: true }).click(); await expect(card).toBeVisible();
  page.once('dialog', d => d.accept()); await card.getByRole('button', { name: `Delete ${product}`, exact: true }).click(); await expect(card).toHaveCount(0);
});
test('order placement and cancellation reserve and restore real database stock', async ({ page, request }) => {
  const product = name('Reserve'); const customer = name('customer');
  expect((await request.post(`${api}/products`, { data: { name: product, price: '3.25', stock: 5 } })).status()).toBe(201);
  await page.goto('/'); const card = page.getByTestId('product-card').filter({ has: page.getByRole('heading', { name: product, exact: true }) });
  await page.getByLabel(`Order quantity for ${product}`, { exact: true }).fill('2'); await page.getByLabel('Customer reference').fill(customer); await page.getByRole('button', { name: 'Place order', exact: true }).click();
  const order = page.getByTestId('order-card').filter({ has: page.getByRole('heading', { name: customer, exact: true }) });
  await expect(order).toContainText('$6.50'); await expect(card).toContainText('3 in stock'); await page.reload(); await expect(order).toContainText('PENDING');
  page.once('dialog', d => d.accept()); await order.getByRole('button', { name: 'Cancel order', exact: true }).click(); await expect(order).toContainText('CANCELLED'); await expect(card).toContainText('5 in stock');
  page.once('dialog', d => d.accept()); await card.getByRole('button', { name: `Delete ${product}`, exact: true }).click(); await expect(page.getByRole('alert')).toContainText('history'); await expect(card).toBeVisible();
});
test('stale edit cannot overwrite inventory reserved by another client', async ({ page, request }) => {
  const product = name('Conflict'); const created = await request.post(`${api}/products`, { data: { name: product, price: '1.00', stock: 5 } }); const p = (await created.json()).data;
  await page.goto('/'); await page.getByRole('button', { name: `Edit ${product}`, exact: true }).click(); await page.getByLabel('Product name', { exact: true }).fill('Preserved proposal');
  expect((await request.post(`${api}/orders`, { data: { userId: 'outside-client', items: [{ productId: p.id, quantity: 1 }] } })).status()).toBe(201);
  await page.getByRole('button', { name: 'Save product', exact: true }).click(); await expect(page.getByRole('alert')).toBeVisible(); await expect(page.getByLabel('Product name', { exact: true })).toHaveValue('Preserved proposal'); await expect(page.getByRole('button', { name: 'Save product', exact: true })).toBeDisabled();
  page.once('dialog', d => d.accept()); await page.getByRole('button', { name: 'Reload current product', exact: true }).click(); await expect(page.getByLabel('Stock', { exact: true })).toHaveValue('4');
  await page.getByLabel('Product name', { exact: true }).fill(product + '-updated'); await page.getByRole('button', { name: 'Save product', exact: true }).click();
  await expect(page.getByRole('status')).toContainText('Product updated'); expect((await (await request.get(`${api}/products/${p.id}`)).json()).data.stock).toBe(4);
});
test('fulfillment is final and keeps reserved stock consumed', async ({ page, request }) => {
  const product = name('Fulfill'); const customer = name('ship'); const p = (await (await request.post(`${api}/products`, { data: { name: product, price: '8', stock: 2 } })).json()).data;
  await request.post(`${api}/orders`, { data: { userId: customer, items: [{ productId: p.id, quantity: 1 }] } }); await page.goto('/');
  const order = page.getByTestId('order-card').filter({ has: page.getByRole('heading', { name: customer, exact: true }) }); page.once('dialog', d => d.accept()); await order.getByRole('button', { name: 'Fulfill order', exact: true }).click(); await expect(order).toContainText('FULFILLED'); await expect(order.getByRole('button')).toHaveCount(0);
  expect((await (await request.get(`${api}/products/${p.id}`)).json()).data.stock).toBe(1);
});
test('desktop and narrow layouts stay readable without horizontal overflow', async ({ page }) => {
  const directory = process.env.ORDER_VERIFY_RESULTS_DIR; if (directory) mkdirSync(directory, { recursive: true });
  for (const [label, width] of [['desktop', 1280], ['narrow', 390]] as const) {
    await page.setViewportSize({ width, height: 900 }); await page.goto('/'); await expect(page.getByRole('heading', { name: 'Orders & inventory', exact: true })).toBeVisible(); await expect(page.getByText('Loading products…')).toHaveCount(0);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
    if (directory) await page.screenshot({ path: join(directory, `${label}.png`), fullPage: true });
  }
});
''')
print('8 frontend and 5 browser cases written')
