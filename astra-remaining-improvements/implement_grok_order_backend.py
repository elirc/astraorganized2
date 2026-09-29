from pathlib import Path
P=Path(__file__).resolve().parent/'stage/e502bf8af566'
def write(rel,text):
 p=P/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
write('backend/src/errors.ts',r'''
export class HttpError extends Error {
  constructor(public readonly status: number, message: string) { super(message); }
}
''')
write('backend/src/db.ts',r'''
import { PrismaClient } from '@prisma/client';
// One pool per process; tests pass their isolated client to createApp instead.
export const prisma = new PrismaClient();
''')
write('backend/src/validation.ts',r'''
import { z } from 'zod';
export const idSchema = z.string().trim().min(1).max(100);
const price = z.string().regex(/^(?:0|[1-9]\d{0,9})(?:\.\d{1,2})?$/, 'Use a positive decimal string with at most two decimal places.')
  .refine(value => Number(value) > 0, 'Price must be positive.');
export const productSchema = z.object({ name: z.string().trim().min(1).max(120), price, stock: z.number().int().min(0).max(2_000_000_000) }).strict();
export const productUpdateSchema = productSchema.extend({ version: z.number().int().positive() }).strict();
export const versionSchema = z.object({ version: z.number().int().positive() }).strict();
export const orderSchema = z.object({
  userId: z.string().trim().min(1).max(100),
  items: z.array(z.object({ productId: idSchema, quantity: z.number().int().min(1).max(10_000) }).strict()).min(1).max(50),
}).strict().superRefine((value, context) => {
  const ids = new Set<string>();
  value.items.forEach((item, index) => {
    if (ids.has(item.productId)) context.addIssue({ code: z.ZodIssueCode.custom, path: ['items', index, 'productId'], message: 'Each product must appear only once.' });
    ids.add(item.productId);
  });
});
export const statusSchema = z.object({ status: z.enum(['CANCELLED', 'FULFILLED']) }).strict();
const integerQuery = z.string().regex(/^\d+$/, 'Use a non-negative integer.').transform(Number);
export const pageSchema = z.object({ limit: integerQuery.refine(value => value >= 1 && value <= 100).default('50'), offset: integerQuery.refine(value => value <= 100_000).default('0') }).strict();
export type ProductInput = z.infer<typeof productSchema>;
export type ProductUpdate = z.infer<typeof productUpdateSchema>;
export type OrderInput = z.infer<typeof orderSchema>;
export type PageInput = z.infer<typeof pageSchema>;
''')
write('backend/src/repositories/productRepository.ts',r'''
import { Prisma, PrismaClient } from '@prisma/client';
import { HttpError } from '../errors';
import { ProductInput, ProductUpdate, PageInput } from '../validation';
export function productRepository(db: PrismaClient) {
  return {
    findAll(page: PageInput) { return db.product.findMany({ orderBy: [{ createdAt: 'asc' }, { id: 'asc' }], take: page.limit, skip: page.offset }); },
    find(id: string) { return db.product.findUnique({ where: { id } }); },
    create(input: ProductInput) { return db.product.create({ data: { ...input, price: new Prisma.Decimal(input.price) } }); },
    update(id: string, input: ProductUpdate) {
      return db.$transaction(async tx => {
        const { version, ...fields } = input;
        const result = await tx.product.updateMany({ where: { id, version }, data: { ...fields, price: new Prisma.Decimal(fields.price), version: { increment: 1 } } });
        if (!result.count) {
          if (!await tx.product.findUnique({ where: { id } })) throw new HttpError(404, 'Product not found.');
          throw new HttpError(409, 'Product changed. Refresh inventory before retrying.');
        }
        return tx.product.findUniqueOrThrow({ where: { id } });
      });
    },
    remove(id: string, version: number) {
      return db.$transaction(async tx => {
        const result = await tx.product.deleteMany({ where: { id, version } });
        if (!result.count) {
          if (!await tx.product.findUnique({ where: { id } })) throw new HttpError(404, 'Product not found.');
          throw new HttpError(409, 'Product changed. Refresh inventory before retrying.');
        }
      });
    },
  };
}
''')
write('backend/src/repositories/orderRepository.ts',r'''
import { OrderStatus, Prisma, PrismaClient } from '@prisma/client';
import { HttpError } from '../errors';
import { OrderInput, PageInput } from '../validation';
const details = { items: { orderBy: { productId: 'asc' as const } } };
export function orderRepository(db: PrismaClient) {
  return {
    findAll(page: PageInput) { return db.order.findMany({ include: details, orderBy: [{ createdAt: 'asc' }, { id: 'asc' }], take: page.limit, skip: page.offset }); },
    find(id: string) { return db.order.findUnique({ where: { id }, include: details }); },
    create(input: OrderInput) {
      return db.$transaction(async tx => {
        // A common lock order reduces deadlock risk for overlapping carts.
        const requested = [...input.items].sort((a, b) => a.productId.localeCompare(b.productId));
        const products = await tx.product.findMany({ where: { id: { in: requested.map(item => item.productId) } } });
        const byId = new Map(products.map(product => [product.id, product]));
        let total = new Prisma.Decimal(0);
        const lines: { productId: string; productName: string; quantity: number; price: Prisma.Decimal }[] = [];
        for (const item of requested) {
          const product = byId.get(item.productId);
          if (!product) throw new HttpError(404, 'A requested product was not found.');
          if (product.stock < item.quantity) throw new HttpError(409, `Insufficient stock for ${product.name}.`);
          // The condition and decrement are one database write, not a read-then-write promise.
          const reserved = await tx.product.updateMany({ where: { id: product.id, version: product.version, stock: { gte: item.quantity } }, data: { stock: { decrement: item.quantity }, version: { increment: 1 } } });
          if (!reserved.count) throw new HttpError(409, 'Inventory changed during checkout. Refresh and retry.');
          total = total.add(product.price.mul(item.quantity));
          lines.push({ productId: product.id, productName: product.name, quantity: item.quantity, price: product.price });
        }
        // Failure here rolls back every earlier reservation in the same transaction.
        return tx.order.create({ data: { userId: input.userId, total, items: { create: lines } }, include: details });
      }, { maxWait: 10_000, timeout: 15_000 });
    },
    transition(id: string, target: 'CANCELLED' | 'FULFILLED') {
      return db.$transaction(async tx => {
        const order = await tx.order.findUnique({ where: { id }, include: details });
        if (!order) throw new HttpError(404, 'Order not found.');
        if (order.status !== OrderStatus.PENDING) throw new HttpError(409, 'Only pending orders can transition.');
        const changed = await tx.order.updateMany({ where: { id, status: OrderStatus.PENDING }, data: { status: target } });
        if (!changed.count) throw new HttpError(409, 'Order status changed. Refresh and retry.');
        if (target === OrderStatus.CANCELLED) {
          for (const item of order.items) await tx.product.update({ where: { id: item.productId }, data: { stock: { increment: item.quantity }, version: { increment: 1 } } });
        }
        return tx.order.findUniqueOrThrow({ where: { id }, include: details });
      });
    },
  };
}
''')
write('backend/src/services/productService.ts',r'''
import { PrismaClient } from '@prisma/client';
import { productRepository } from '../repositories/productRepository';
import { HttpError } from '../errors';
import { idSchema, pageSchema, productSchema, productUpdateSchema, versionSchema } from '../validation';
export function productService(db: PrismaClient) {
  const repository = productRepository(db);
  return {
    getProducts(query: unknown) { return repository.findAll(pageSchema.parse(query)); },
    async getProduct(id: string) { const product = await repository.find(idSchema.parse(id)); if (!product) throw new HttpError(404, 'Product not found.'); return product; },
    createProduct(input: unknown) { return repository.create(productSchema.parse(input)); },
    updateProduct(id: string, input: unknown) { return repository.update(idSchema.parse(id), productUpdateSchema.parse(input)); },
    deleteProduct(id: string, input: unknown) { return repository.remove(idSchema.parse(id), versionSchema.parse(input).version); },
  };
}
''')
write('backend/src/services/orderService.ts',r'''
import { PrismaClient } from '@prisma/client';
import { orderRepository } from '../repositories/orderRepository';
import { HttpError } from '../errors';
import { idSchema, orderSchema, pageSchema, statusSchema } from '../validation';
export function orderService(db: PrismaClient) {
  const repository = orderRepository(db);
  return {
    getOrders(query: unknown) { return repository.findAll(pageSchema.parse(query)); },
    async getOrder(id: string) { const order = await repository.find(idSchema.parse(id)); if (!order) throw new HttpError(404, 'Order not found.'); return order; },
    createOrder(input: unknown) { return repository.create(orderSchema.parse(input)); },
    transitionOrder(id: string, input: unknown) { return repository.transition(idSchema.parse(id), statusSchema.parse(input).status); },
  };
}
''')
write('backend/src/http.ts',r'''
import { NextFunction, Request, Response } from 'express';
import { Order, OrderItem, Product } from '@prisma/client';
export const asyncRoute = (handler: (request: Request, response: Response) => Promise<unknown>) =>
  (request: Request, response: Response, next: NextFunction) => { Promise.resolve(handler(request, response)).catch(next); };
export const presentProduct = (product: Product) => ({ ...product, price: product.price.toFixed(2) });
export const presentOrder = (order: Order & { items: OrderItem[] }) => ({ ...order, total: order.total.toFixed(2), items: order.items.map(item => ({ ...item, price: item.price.toFixed(2) })) });
''')
write('backend/src/routes/productRoutes.ts',r'''
import { Router } from 'express';
import { PrismaClient } from '@prisma/client';
import { productService } from '../services/productService';
import { asyncRoute, presentProduct } from '../http';
export default function productRoutes(db: PrismaClient) {
  const router = Router(); const service = productService(db);
  router.get('/', asyncRoute(async (request, response) => response.json({ data: (await service.getProducts(request.query)).map(presentProduct) })));
  router.get('/:id', asyncRoute(async (request, response) => response.json({ data: presentProduct(await service.getProduct(request.params.id)) })));
  router.post('/', asyncRoute(async (request, response) => {
    const product = await service.createProduct(request.body);
    response.location(`/api/products/${product.id}`).status(201).json({ data: presentProduct(product) });
  }));
  router.patch('/:id', asyncRoute(async (request, response) => response.json({ data: presentProduct(await service.updateProduct(request.params.id, request.body)) })));
  router.delete('/:id', asyncRoute(async (request, response) => { await service.deleteProduct(request.params.id, request.body); response.status(204).end(); }));
  return router;
}
''')
write('backend/src/routes/orderRoutes.ts',r'''
import { Router } from 'express';
import { PrismaClient } from '@prisma/client';
import { orderService } from '../services/orderService';
import { asyncRoute, presentOrder } from '../http';
export default function orderRoutes(db: PrismaClient) {
  const router = Router(); const service = orderService(db);
  router.get('/', asyncRoute(async (request, response) => response.json({ data: (await service.getOrders(request.query)).map(presentOrder) })));
  router.get('/:id', asyncRoute(async (request, response) => response.json({ data: presentOrder(await service.getOrder(request.params.id)) })));
  router.post('/', asyncRoute(async (request, response) => {
    const order = await service.createOrder(request.body);
    response.location(`/api/orders/${order.id}`).status(201).json({ data: presentOrder(order) });
  }));
  router.patch('/:id/status', asyncRoute(async (request, response) => response.json({ data: presentOrder(await service.transitionOrder(request.params.id, request.body)) })));
  return router;
}
''')
write('backend/src/app.ts',r'''
import express, { ErrorRequestHandler } from 'express';
import cors from 'cors';
import { randomUUID } from 'node:crypto';
import { Prisma, PrismaClient } from '@prisma/client';
import { ZodError } from 'zod';
import { HttpError } from './errors';
import productRoutes from './routes/productRoutes';
import orderRoutes from './routes/orderRoutes';
export function createApp(db: PrismaClient, log: (error: unknown) => void = console.error) {
  const app = express();
  app.use((request, response, next) => { response.locals.requestId = randomUUID(); response.setHeader('X-Request-Id', response.locals.requestId); next(); });
  app.use(cors()); app.use(express.json({ limit: '32kb' }));
  app.get('/health', (_request, response) => response.json({ status: 'ok' }));
  app.use('/api/products', productRoutes(db)); app.use('/api/orders', orderRoutes(db));
  app.use((_request, _response, next) => next(new HttpError(404, 'Route not found.')));
  const errors: ErrorRequestHandler = (error, _request, response, _next) => {
    let status = 500; let message = 'The database operation could not be completed.';
    if (error instanceof HttpError) { status = error.status; message = error.message; }
    else if (error instanceof ZodError) { status = 400; message = error.issues.map(issue => `${issue.path.join('.') || 'body'}: ${issue.message}`).join('; '); }
    else if (error?.type === 'entity.parse.failed') { status = 400; message = 'Malformed JSON.'; }
    else if (error?.type === 'entity.too.large') { status = 413; message = 'Request body is too large.'; }
    else if (error instanceof Prisma.PrismaClientKnownRequestError && ['P2003', 'P2002', 'P2034'].includes(error.code)) {
      status = 409; message = error.code === 'P2003' ? 'This product is referenced by order history and cannot be deleted.' : 'A conflicting database change occurred. Refresh and retry.';
    }
    else log(error);
    response.status(status).json({ error: { message, requestId: response.locals.requestId } });
  };
  app.use(errors); return app;
}
''')
write('backend/src/index.ts',r'''
import 'dotenv/config';
import { createApp } from './app';
import { prisma } from './db';
const port = Number(process.env.PORT ?? 4000);
if (!Number.isInteger(port) || port < 0 || port > 65535) throw new Error('PORT must be an integer from 0 to 65535.');
const server = createApp(prisma).listen(port, process.env.HOST ?? '127.0.0.1', () => {
  const address = server.address();
  if (address && typeof address !== 'string') console.log(`Order API listening on http://${address.address}:${address.port}`);
});
for (const signal of ['SIGINT', 'SIGTERM']) process.once(signal, () => {
  server.close(() => { void prisma.$disconnect(); });
});
''')
