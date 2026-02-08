# 仓储管理系统（Flask + Svelte + PostgreSQL）

本项目实现了完整的仓储业务基础能力：

- 仓库管理
- 库员管理
- 供应商管理
- 客户管理
- 库存管理
- 入库管理
- 出库管理
- 库存预警（含手动生成）
- 账单管理
- 账单生成
- 员工管理
- 角色管理
- 权限管理
- 登录与注册

## 前端页面与路由

前端采用 hash 路由，核心页面与路径如下：

- `#/auth`：登录与注册
- `#/inventory`：库存管理
- `#/warehouse`：仓库管理
- `#/staff`：库员管理
- `#/supplier`：供应商管理
- `#/customer`：客户管理
- `#/inbound`：入库管理
- `#/outbound`：出库管理
- `#/alerts`：库存预警
- `#/bill`：账单管理
- `#/employee`：员工管理
- `#/role`：角色管理
- `#/permission`：权限管理

组件结构：

- `frontend/src/components/NavTabs.svelte`：路由导航
- `frontend/src/components/AuthPage.svelte`：认证页面组件
- `frontend/src/components/ModulePage.svelte`：通用业务页面组件
- `frontend/src/router.js`：路由定义与导航逻辑

## 技术栈

- 后端：Flask + SQLAlchemy
- 前端：Svelte + Vite
- 数据库：PostgreSQL

## 主要 API

- 认证：`POST /api/auth/register`、`POST /api/auth/login`
- 仓库：`GET/POST /api/warehouses`
- 库员：`GET/POST /api/warehouse-staff`
- 商品库存：`GET/POST/PUT/DELETE /api/items`
- 供应商：`GET/POST /api/suppliers`
- 客户：`GET/POST /api/customers`
- 入库：`GET/POST /api/inbound-orders`
- 出库：`GET/POST /api/outbound-orders`
- 库存预警：`GET /api/alerts`、`POST /api/alerts/generate`
- 账单：`GET/POST /api/bills`、`POST /api/bills/generate`
- 员工：`GET/POST /api/employees`
- 权限：`GET/POST /api/permissions`
- 角色：`GET/POST /api/roles`、`POST /api/roles/{id}/permissions`

## 启动

### 1) PostgreSQL

```bash
docker compose up -d
```

### 2) 后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
export $(cat .env | xargs)
flask --app run.py init-db
python run.py
```

### 3) 前端

```bash
cd frontend
npm install
npm run dev
```

访问 `http://localhost:5173`。
