from pathlib import Path
P=Path(__file__).resolve().parent/'stage/e502bf8af566'
(P/'backend/prisma/schema.prisma').write_text('''generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

enum OrderStatus {
  PENDING
  CANCELLED
  FULFILLED
}

model Product {
  id         String      @id @default(cuid())
  name       String
  price      Decimal     @db.Decimal(12, 2)
  stock      Int         @default(0)
  version    Int         @default(1)
  createdAt  DateTime    @default(now())
  orderItems OrderItem[]
  @@index([createdAt, id])
}

model Order {
  id        String      @id @default(cuid())
  userId    String
  status    OrderStatus @default(PENDING)
  total     Decimal     @db.Decimal(18, 2)
  createdAt DateTime    @default(now())
  items     OrderItem[]
  @@index([createdAt, id])
}

model OrderItem {
  id          String  @id @default(cuid())
  orderId     String
  productId   String
  productName String
  quantity    Int
  price       Decimal @db.Decimal(12, 2)
  order       Order   @relation(fields: [orderId], references: [id], onDelete: Restrict)
  product     Product @relation(fields: [productId], references: [id], onDelete: Restrict)
  @@unique([orderId, productId])
  @@index([productId])
}

// Kept as future domain exercises; no supplier or purchase-order routes exist yet.
model Supplier {
  id             String          @id @default(cuid())
  name           String
  createdAt      DateTime        @default(now())
  purchaseOrders PurchaseOrder[]
}

model PurchaseOrder {
  id         String   @id @default(cuid())
  supplierId String
  status     String   @default("PENDING")
  createdAt  DateTime @default(now())
  supplier   Supplier @relation(fields: [supplierId], references: [id], onDelete: Restrict)
}
''',encoding='utf-8')
M=P/'backend/prisma/migrations';(M/'20260909000000_initial').mkdir(parents=True,exist_ok=True)
(M/'migration_lock.toml').write_text('provider = "postgresql"\n',encoding='utf-8')
(M/'20260909000000_initial/migration.sql').write_text('''CREATE TYPE "OrderStatus" AS ENUM ('PENDING', 'CANCELLED', 'FULFILLED');
CREATE TABLE "Product" (
  "id" TEXT PRIMARY KEY, "name" TEXT NOT NULL, "price" DECIMAL(12,2) NOT NULL,
  "stock" INTEGER NOT NULL DEFAULT 0, "version" INTEGER NOT NULL DEFAULT 1,
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "Product_price_positive" CHECK ("price" > 0),
  CONSTRAINT "Product_stock_nonnegative" CHECK ("stock" >= 0),
  CONSTRAINT "Product_version_positive" CHECK ("version" > 0)
);
CREATE TABLE "Order" (
  "id" TEXT PRIMARY KEY, "userId" TEXT NOT NULL, "status" "OrderStatus" NOT NULL DEFAULT 'PENDING',
  "total" DECIMAL(18,2) NOT NULL, "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "Order_total_nonnegative" CHECK ("total" >= 0)
);
CREATE TABLE "OrderItem" (
  "id" TEXT PRIMARY KEY, "orderId" TEXT NOT NULL, "productId" TEXT NOT NULL, "productName" TEXT NOT NULL,
  "quantity" INTEGER NOT NULL, "price" DECIMAL(12,2) NOT NULL,
  CONSTRAINT "OrderItem_quantity_positive" CHECK ("quantity" > 0),
  CONSTRAINT "OrderItem_price_positive" CHECK ("price" > 0),
  CONSTRAINT "OrderItem_orderId_fkey" FOREIGN KEY ("orderId") REFERENCES "Order"("id") ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT "OrderItem_productId_fkey" FOREIGN KEY ("productId") REFERENCES "Product"("id") ON DELETE RESTRICT ON UPDATE CASCADE
);
CREATE UNIQUE INDEX "OrderItem_orderId_productId_key" ON "OrderItem"("orderId", "productId");
CREATE INDEX "Product_createdAt_id_idx" ON "Product"("createdAt", "id");
CREATE INDEX "Order_createdAt_id_idx" ON "Order"("createdAt", "id");
CREATE INDEX "OrderItem_productId_idx" ON "OrderItem"("productId");
CREATE TABLE "Supplier" (
  "id" TEXT PRIMARY KEY, "name" TEXT NOT NULL, "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE "PurchaseOrder" (
  "id" TEXT PRIMARY KEY, "supplierId" TEXT NOT NULL, "status" TEXT NOT NULL DEFAULT 'PENDING',
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "PurchaseOrder_supplierId_fkey" FOREIGN KEY ("supplierId") REFERENCES "Supplier"("id") ON DELETE RESTRICT ON UPDATE CASCADE
);
''',encoding='utf-8')
(P/'backend/.env.example').write_text('''# Use a new local development database. The test harness creates its own cluster.
DATABASE_URL=postgresql://postgres:replace_me@127.0.0.1:5432/order_learning?schema=public
HOST=127.0.0.1
PORT=4000
''',encoding='utf-8')
(P/'frontend/.env.example').write_text('VITE_API_URL=http://127.0.0.1:4000/api\n',encoding='utf-8')
