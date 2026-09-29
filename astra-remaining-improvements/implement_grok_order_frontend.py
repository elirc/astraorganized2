from pathlib import Path
s=Path('astra-remaining-improvements/stage/e502bf8af566')
def w(n,c):
 p=s/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(c.strip()+'\n',encoding='utf-8')
w('frontend/src/api/client.ts',r'''
export interface Product { id: string; name: string; price: string; stock: number; version: number; }
export interface Order { id: string; userId: string; status: 'PENDING' | 'CANCELLED' | 'FULFILLED'; total: string; items: { id: string; productName: string; quantity: number; price: string }[]; }
export interface ProductInput { name: string; price: string; stock: number; }
export class ApiError extends Error { constructor(public status: number, message: string) { super(message); } }
const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:4000/api';
export async function request<T>(path: string, method = 'GET', body?: unknown, signal?: AbortSignal): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { method, signal, headers: body === undefined ? undefined : { 'Content-Type': 'application/json' }, body: body === undefined ? undefined : JSON.stringify(body) });
  if (!res.ok) {
    const payload = await res.json().catch(() => null);
    throw new ApiError(res.status, payload?.error?.message || `Request failed (${res.status}).`);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()).data as T;
}
export const fetchProducts = (offset = 0, signal?: AbortSignal) => request<Product[]>(`/products?limit=20&offset=${offset}`, 'GET', undefined, signal);
export const fetchOrders = (offset = 0, signal?: AbortSignal) => request<Order[]>(`/orders?limit=20&offset=${offset}`, 'GET', undefined, signal);
export const createProduct = (data: ProductInput) => request<Product>('/products', 'POST', data);
export const updateProduct = (id: string, data: ProductInput & { version: number }) => request<Product>(`/products/${encodeURIComponent(id)}`, 'PATCH', data);
export const deleteProduct = (id: string, version: number) => request<void>(`/products/${encodeURIComponent(id)}`, 'DELETE', { version });
export const createOrder = (data: { userId: string; items: { productId: string; quantity: number }[] }) => request<Order>('/orders', 'POST', data);
export const transitionOrder = (id: string, status: 'CANCELLED' | 'FULFILLED') => request<Order>(`/orders/${encodeURIComponent(id)}/status`, 'PATCH', { status });
''')
w('frontend/src/features/products/pages/ProductsPage.tsx',r'''
import { FormEvent, useRef, useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { ApiError, Product, createProduct, deleteProduct, fetchOrders, fetchProducts, createOrder, transitionOrder, updateProduct } from '../../../api/client';
const empty = { name: '', price: '', stock: '0' };
export function ProductsPage() {
  const client = useQueryClient();
  const [offset, setOffset] = useState(0); const [orderOffset, setOrderOffset] = useState(0);
  const products = useQuery({ queryKey: ['products', offset], queryFn: ({ signal }) => fetchProducts(offset, signal), retry: false });
  const orders = useQuery({ queryKey: ['orders', orderOffset], queryFn: ({ signal }) => fetchOrders(orderOffset, signal), retry: false });
  const [draft, setDraft] = useState(empty); const [editing, setEditing] = useState<Product | null>(null);
  const [cart, setCart] = useState<Record<string, string>>({}); const [customer, setCustomer] = useState('');
  const [busy, setBusy] = useState(false); const guard = useRef(false);
  const [message, setMessage] = useState(''); const [error, setError] = useState(''); const [conflict, setConflict] = useState(false);
  async function act(action: () => Promise<unknown>, success: string, done?: () => void) {
    if (guard.current) return; guard.current = true; setBusy(true); setError(''); setMessage('');
    try { await action(); done?.(); setMessage(success); }
    catch (cause) { setError(cause instanceof Error ? cause.message : 'Request failed.'); if (cause instanceof ApiError && cause.status === 409 && editing) setConflict(true); }
    finally { await Promise.all([client.invalidateQueries({ queryKey: ['products'] }), client.invalidateQueries({ queryKey: ['orders'] })]); guard.current = false; setBusy(false); }
  }
  function startEdit(product: Product) { setEditing(product); setDraft({ name: product.name, price: product.price, stock: String(product.stock) }); setConflict(false); setError(''); }
  function reset() { setEditing(null); setDraft(empty); setConflict(false); }
  function save(event: FormEvent) {
    event.preventDefault(); const data = { name: draft.name, price: draft.price, stock: Number(draft.stock) };
    void act(() => editing ? updateProduct(editing.id, { ...data, version: editing.version }) : createProduct(data), editing ? 'Product updated.' : 'Product created.', reset);
  }
  function place(event: FormEvent) {
    event.preventDefault(); const items = Object.entries(cart).filter(([, quantity]) => Number(quantity) > 0).map(([productId, quantity]) => ({ productId, quantity: Number(quantity) }));
    if (!items.length) { setError('Choose at least one quantity above zero.'); return; }
    void act(() => createOrder({ userId: customer, items }), 'Order placed. Inventory reserved.', () => setCart({}));
  }
  return <main>
    <header><p className="eyebrow">CRUD LEARNING LAB</p><h1>Orders & inventory</h1><p>Manage a catalog, reserve stock, and follow each order through its lifecycle.</p><p className="notice">Local demo: the customer reference is a label. Accounts and access control are not implemented.</p></header>
    {error && <p role="alert" className="error">{error}</p>}{message && <p role="status" className="success">{message}</p>}
    <div className="grid">
      <section aria-labelledby="catalog-title"><h2 id="catalog-title">Products & inventory</h2>
        <button disabled={busy} onClick={() => { void products.refetch(); void orders.refetch(); }}>Refresh data</button>
        {products.isPending && <p>Loading products…</p>}{products.isError && <p role="alert">Could not load products: {products.error.message}</p>}
        {products.data?.length === 0 && <p>No products on this page.</p>}
        <ul className="cards">{products.data?.map(product => <li key={product.id} data-testid="product-card">
          <h3>{product.name}</h3><p>${product.price} · {product.stock} in stock · version {product.version}</p>
          <div className="actions"><button disabled={busy} onClick={() => startEdit(product)}>Edit {product.name}</button><button disabled={busy} onClick={() => { if (window.confirm(`Delete ${product.name}? Referenced products cannot be deleted.`)) void act(() => deleteProduct(product.id, product.version), 'Product deleted.', () => { if (editing?.id === product.id) reset(); }); }}>Delete {product.name}</button></div>
          <label>Order quantity for {product.name}<input type="number" min="0" max="10000" step="1" value={cart[product.id] || '0'} disabled={busy} onChange={event => setCart({ ...cart, [product.id]: event.target.value })}/></label>
        </li>)}</ul>
        <nav aria-label="Product pages"><button disabled={busy || offset === 0 || products.isFetching} onClick={() => setOffset(offset - 20)}>Previous products</button><span>Page {offset / 20 + 1}</span><button disabled={busy || products.isFetching || products.data?.length !== 20} onClick={() => setOffset(offset + 20)}>Next products</button></nav>
      </section>
      <section aria-labelledby="editor-title"><h2 id="editor-title">{editing ? `Edit product: ${editing.name}` : 'New product'}</h2>
        <form onSubmit={save}><fieldset disabled={busy || conflict}><label>Product name<input required maxLength={120} value={draft.name} onChange={event => setDraft({ ...draft, name: event.target.value })}/></label><label>Price<input required inputMode="decimal" pattern="(0|[1-9][0-9]{0,9})(\.[0-9]{1,2})?" value={draft.price} onChange={event => setDraft({ ...draft, price: event.target.value })}/></label><label>Stock<input required type="number" min="0" max="2000000000" step="1" value={draft.stock} onChange={event => setDraft({ ...draft, stock: event.target.value })}/></label><button type="submit">{editing ? 'Save product' : 'Create product'}</button></fieldset></form>
        {editing && <button disabled={busy} onClick={reset}>Cancel editing</button>}
        {conflict && <div className="notice"><p>Your draft is preserved. Reload the current product before editing again; an old stock value could undo a reservation.</p><button disabled={busy} onClick={() => { const current = products.data?.find(p => p.id === editing?.id); if (current && window.confirm('Discard this draft and load the latest product?')) startEdit(current); else if (!current) setError('This product is no longer on the current page. Cancel editing and find it again.'); }}>Reload current product</button></div>}
        <h2>Place an order</h2><form onSubmit={place}><fieldset disabled={busy}><label>Customer reference<input required maxLength={100} value={customer} onChange={event => setCustomer(event.target.value)}/></label><p>{Object.values(cart).filter(q => Number(q) > 0).length} selected products across all pages. The server calculates prices and checks stock.</p><button type="submit">Place order</button><button type="button" onClick={() => setCart({})}>Clear quantities</button></fieldset></form>
      </section>
    </div>
    <section aria-labelledby="orders-title"><h2 id="orders-title">Order history</h2>{orders.isPending && <p>Loading orders…</p>}{orders.isError && <p role="alert">Could not load orders: {orders.error.message}</p>}{orders.data?.length === 0 && <p>No orders on this page.</p>}
      <ul className="cards orders">{orders.data?.map(order => <li key={order.id} data-testid="order-card"><h3>{order.userId}</h3><p className="identifier">{order.id}</p><p><strong>{order.status}</strong> · ${order.total}</p><ul>{order.items.map(item => <li key={item.id}>{item.productName} × {item.quantity} at ${item.price}</li>)}</ul>{order.status === 'PENDING' && <div className="actions"><button disabled={busy} onClick={() => { if (window.confirm('Cancel this order and restore its stock?')) void act(() => transitionOrder(order.id, 'CANCELLED'), 'Order cancelled. Stock restored.'); }}>Cancel order</button><button disabled={busy} onClick={() => { if (window.confirm('Mark this order fulfilled? This is final and does not process payment.')) void act(() => transitionOrder(order.id, 'FULFILLED'), 'Order fulfilled.'); }}>Fulfill order</button></div>}</li>)}</ul>
      <nav aria-label="Order pages"><button disabled={busy || orderOffset === 0 || orders.isFetching} onClick={() => setOrderOffset(orderOffset - 20)}>Previous orders</button><span>Page {orderOffset / 20 + 1}</span><button disabled={busy || orders.isFetching || orders.data?.length !== 20} onClick={() => setOrderOffset(orderOffset + 20)}>Next orders</button></nav>
    </section>
  </main>;
}
''')
w('frontend/src/App.tsx',r'''
import { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ProductsPage } from './features/products/pages/ProductsPage';
export default function App() {
  const [client] = useState(() => new QueryClient());
  return <QueryClientProvider client={client}><ProductsPage /></QueryClientProvider>;
}
''')
w('frontend/src/index.css',r'''
@tailwind base;
@tailwind components;
@tailwind utilities;
:root { font-family: system-ui, sans-serif; color: #192f3c; background: #f4f7f8; line-height: 1.6; }
* { box-sizing: border-box; } body { margin: 0; } main { max-width: 1180px; margin: auto; padding: 32px 24px 64px; }
h1 { font-size: clamp(2rem, 5vw, 3.1rem); line-height: 1.15; font-weight: 750; } h2 { font-size: 1.4rem; font-weight: 700; margin: 12px 0; } h3 { font-size: 1.1rem; font-weight: 700; overflow-wrap: anywhere; }
p { margin: 10px 0; } header { margin-bottom: 28px; } .eyebrow { color: #087665; font-weight: 700; letter-spacing: .12em; font-size: .8rem; }
.grid { display: grid; grid-template-columns: 1.3fr 1fr; gap: 24px; align-items: start; } section { background: white; border: 1px solid #d8e2e6; border-radius: 12px; padding: 24px; min-width: 0; margin-bottom: 24px; }
.cards { list-style: none; padding: 0; } .cards > li { padding: 16px 0; border-bottom: 1px solid #d8e2e6; } .orders { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(280px,100%), 1fr)); gap: 20px; }
label { display: flex; flex-direction: column; margin: 12px 0; font-weight: 600; } input { background: #fff; border: 1px solid #8298a3; border-radius: 6px; padding: 9px 12px; min-width: 0; width: 100%; font: inherit; }
button { border: 1px solid #147766; border-radius: 6px; color: #065d4e; background: #effaf6; padding: 8px 12px; font: inherit; cursor: pointer; margin: 4px 4px 4px 0; overflow-wrap: anywhere; } button[type=submit] { background: #087665; color: white; } button:disabled { opacity: .5; cursor: not-allowed; } :focus-visible { outline: 3px solid #e39c21; outline-offset: 2px; }
fieldset { border: 0; padding: 0; min-width: 0; } .actions, nav { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; } .notice { background: #eef5fa; padding: 12px; border-radius: 6px; } .error { background: #ffeded; color: #9b2222; padding: 12px; } .success { background: #e2f6ec; padding: 12px; } .identifier { font-family: monospace; font-size: .8rem; overflow-wrap: anywhere; }
@media (max-width: 760px) { .grid { grid-template-columns: 1fr; } main { padding: 20px 12px; } section { padding: 16px; } }
''')
w('frontend/vitest.config.ts',r'''
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
export default defineConfig({ plugins: [react()], test: { environment: 'jsdom', globals: true, setupFiles: ['./src/test/setup.ts'] } });
''')
print('Frontend CRUD implementation written')
