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

<main class="mx-auto flex min-h-screen max-w-6xl flex-col gap-6 px-6 py-8">
  <header class="rounded-2xl bg-gradient-to-r from-blue-600 to-indigo-500 p-6 text-white shadow-lg">
    <p class="text-sm text-blue-100">Warehouse System</p>
    <h1 class="mt-2 text-2xl font-semibold">仓储管理系统（Flask + Svelte + PostgreSQL）</h1>
    <p class="mt-1 text-sm text-blue-100">全流程业务协同面板</p>
  </header>

  <NavTabs {routes} {activePath} navigate={currentPath.navigate} />

  {#if activeKey === 'auth'}
    <AuthPage
      auth={auth}
      token={token}
      authError={authError}
      onRegister={() => doAuth('register')}
      onLogin={() => doAuth('login')}
    />
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
