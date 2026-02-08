<script>
  import { onMount } from 'svelte'

  import AuthPage from './components/AuthPage.svelte'
  import ModulePage from './components/ModulePage.svelte'
  import NavTabs from './components/NavTabs.svelte'
  import { currentPath, routes } from './router'

  let activePath = '/auth'
  const routeByPath = Object.fromEntries(routes.map((route) => [route.path, route]))

  let token = ''
  let auth = { username: '', password: '' }
  let authError = ''
  let pageError = ''

  const modules = {
    inventory: { endpoint: '/api/items', title: '库存管理', form: { sku: '', name: '', quantity: 0, min_stock: 0, location: '' } },
    warehouse: { endpoint: '/api/warehouses', title: '仓库管理', form: { code: '', name: '', location: '' } },
    staff: { endpoint: '/api/warehouse-staff', title: '库员管理', form: { name: '', phone: '', warehouse_id: '' } },
    supplier: { endpoint: '/api/suppliers', title: '供应商管理', form: { name: '', contact: '', phone: '' } },
    customer: { endpoint: '/api/customers', title: '客户管理', form: { name: '', contact: '', phone: '' } },
    inbound: { endpoint: '/api/inbound-orders', title: '入库管理', form: { item_id: '', supplier_id: '', quantity: 0, note: '' } },
    outbound: { endpoint: '/api/outbound-orders', title: '出库管理', form: { item_id: '', customer_id: '', quantity: 0, note: '' } },
    alerts: { endpoint: '/api/alerts', title: '库存预警', form: {} },
    bill: { endpoint: '/api/bills', title: '账单管理', form: { bill_no: '', bill_type: 'receivable', amount: 0 } },
    employee: { endpoint: '/api/employees', title: '员工管理', form: { name: '', email: '', position: '' } },
    role: { endpoint: '/api/roles', title: '角色管理', form: { code: '', name: '', permission_ids: '' } },
    permission: { endpoint: '/api/permissions', title: '权限管理', form: { code: '', name: '' } }
  }

  const lists = Object.fromEntries(Object.keys(modules).map((key) => [key, []]))

  const toNumberFields = ['quantity', 'min_stock', 'item_id', 'supplier_id', 'customer_id', 'warehouse_id', 'amount']

  $: activeKey = routeByPath[activePath]?.key || 'auth'

  currentPath.subscribe((path) => {
    activePath = path
    const route = routeByPath[path]
    if (route && route.key !== 'auth') {
      fetchModule(route.key)
    }
  })

  async function doAuth(path) {
    authError = ''
    const res = await fetch(`/api/auth/${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(auth)
    })
    const body = await res.json()
    if (!res.ok) {
      authError = body.error || `${path} failed`
      return
    }
    if (body.token) token = body.token
  }

  async function fetchModule(key) {
    pageError = ''
    try {
      const res = await fetch(modules[key].endpoint)
      if (!res.ok) throw new Error(`加载 ${modules[key].title} 失败`)
      lists[key] = await res.json()
    } catch (error) {
      pageError = error.message
    }
  }

  async function createModule(key) {
    pageError = ''
    const payload = { ...modules[key].form }

    if (key === 'role' && payload.permission_ids) {
      payload.permission_ids = String(payload.permission_ids)
        .split(',')
        .map((item) => Number(item.trim()))
        .filter((id) => Number.isInteger(id) && id > 0)
    }

    toNumberFields.forEach((field) => {
      if (payload[field] !== undefined && payload[field] !== '') {
        payload[field] = Number(payload[field])
      }
    })

    try {
      const res = await fetch(modules[key].endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      const body = await res.json().catch(() => ({}))
      if (!res.ok) throw new Error(body.error || '创建失败')
      await fetchModule(key)
    } catch (error) {
      pageError = error.message
    }
  }

  async function generateAlerts() {
    await fetch('/api/alerts/generate', { method: 'POST' })
    await fetchModule('alerts')
  }

  async function generateBill() {
    await fetch('/api/bills/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ source: 'outbound', reference_id: 1, amount: 99.9 })
    })
    await fetchModule('bill')
  }

  function pageActions(key) {
    if (key === 'alerts') return [{ label: '生成库存预警', handler: generateAlerts }]
    if (key === 'bill') return [{ label: '自动生成账单', handler: generateBill }]
    return []
  }

  onMount(() => {
    routes.filter((route) => route.key !== 'auth').forEach((route) => fetchModule(route.key))
  })
</script>

<main>
  <h1>仓储管理系统（Flask + Svelte + PostgreSQL）</h1>

  <NavTabs {routes} {activePath} navigate={currentPath.navigate} />

  {#if activeKey === 'auth'}
    <AuthPage auth={auth} token={token} authError={authError} onRegister={() => doAuth('register')} onLogin={() => doAuth('login')} />
  {:else}
    <ModulePage
      title={modules[activeKey].title}
      fields={Object.keys(modules[activeKey].form)}
      form={modules[activeKey].form}
      records={lists[activeKey]}
      error={pageError}
      onCreate={() => createModule(activeKey)}
      actions={pageActions(activeKey)}
    />
  {/if}
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: system-ui, sans-serif;
    background: #f3f4f6;
  }

  :global(main) {
    max-width: 1200px;
    margin: 1.5rem auto;
    padding: 0 1rem;
  }

  :global(.card) {
    background: #fff;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }

  :global(.tabs) {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  :global(button) {
    border: 0;
    border-radius: 8px;
    padding: 0.45rem 0.7rem;
    background: #2563eb;
    color: #fff;
    cursor: pointer;
  }

  :global(button.active) {
    background: #1d4ed8;
  }

  :global(input) {
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 0.45rem 0.65rem;
  }

  :global(.row),
  :global(.grid) {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  :global(.grid) {
    margin-bottom: 0.75rem;
  }

  :global(.error) {
    color: #dc2626;
    font-weight: 600;
  }

  :global(.ok) {
    color: #047857;
    font-weight: 600;
  }

  :global(pre) {
    background: #111827;
    color: #f9fafb;
    border-radius: 8px;
    padding: 0.8rem;
    overflow: auto;
    font-size: 0.8rem;
  }
</style>
