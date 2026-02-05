# 仓库库存系统（Flask + Svelte + PostgreSQL）

一个轻量库存管理系统，支持库存项的新增、列表查看、删除，后端提供 REST API，前端使用 Svelte 单页应用。

## 技术栈

- 后端：Flask + SQLAlchemy
- 前端：Svelte + Vite
- 数据库：PostgreSQL

## 项目结构

```bash
.
├── backend
│   ├── app
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── routes.py
│   ├── tests
│   │   └── test_api.py
│   ├── requirements.txt
│   └── run.py
├── frontend
│   ├── src
│   │   ├── App.svelte
│   │   └── main.js
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
└── .env.example
```

## 快速开始

### 1) 启动 PostgreSQL

```bash
docker compose up -d
```

### 2) 启动后端

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

后端默认运行在 `http://localhost:5000`。

### 3) 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端默认运行在 `http://localhost:5173`，并通过 Vite 代理访问后端 API。

## API 简要说明

- `GET /health`：健康检查
- `GET /api/items`：查询库存
- `POST /api/items`：创建库存
- `PUT /api/items/{id}`：更新库存
- `DELETE /api/items/{id}`：删除库存

创建库存示例：

```json
{
  "sku": "SKU-001",
  "name": "Keyboard",
  "quantity": 10,
  "location": "A1"
}
```
