<script>
  import { onMount } from 'svelte'

  let token = ''
  let auth = { username: '', password: '' }
  let authError = ''
  const tabs = [
    { key: 'inventory', label: '库存管理' },
    { key: 'warehouse', label: '仓库管理' },
    { key: 'staff', label: '库员管理' },
    { key: 'supplier', label: '供应商管理' },
    { key: 'customer', label: '客户管理' },
    { key: 'inbound', label: '入库管理' },
    { key: 'outbound', label: '出库管理' },
    { key: 'alerts', label: '库存预警' },
    { key: 'bill', label: '账单管理' },
    { key: 'employee', label: '员工管理' },
    { key: 'role', label: '角色管理' },
    { key: 'permission', label: '权限管理' }
  ]
  let activeTab = 'inventory'

  const state = {
    inventory: { list: [], endpoint: '/api/items', form: { sku: '', name: '', quantity: 0, min_stock: 0, location: '' } },
    warehouse: { list: [], endpoint: '/api/warehouses', form: { code: '', name: '', location: '' } },
    staff: { list: [], endpoint: '/api/warehouse-staff', form: { name: '', phone: '', warehouse_id: '' } },
    supplier: { list: [], endpoint: '/api/suppliers', form: { name: '', contact: '', phone: '' } },
    customer: { list: [], endpoint: '/api/customers', form: { name: '', contact: '', phone: '' } },
    inbound: { list: [], endpoint: '/api/inbound-orders', form: { item_id: '', supplier_id: '', quantity: 0, note: '' } },
    outbound: { list: [], endpoint: '/api/outbound-orders', form: { item_id: '', customer_id: '', quantity: 0, note: '' } },
    alerts: { list: [], endpoint: '/api/alerts', form: {} },
    bill: { list: [], endpoint: '/api/bills', form: { bill_no: '', bill_type: 'receivable', amount: 0 } },
    employee: { list: [], endpoint: '/api/employees', form: { name: '', email: '', position: '' } },
    role: { list: [], endpoint: '/api/roles', form: { code: '', name: '', permission_ids: [] } },
    permission: { list: [], endpoint: '/api/permissions', form: { code: '', name: '' } }
  }

  let error = ''

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
    error = ''
    try {
      const module = state[key]
      const res = await fetch(module.endpoint)
      if (!res.ok) throw new Error(`加载 ${key} 失败`)
      module.list = await res.json()
    } catch (e) {
      error = e.message
    }
  }

  async function createModule(key) {
    error = ''
    const module = state[key]
    try {
      const payload = { ...module.form }
      ;['quantity', 'min_stock', 'item_id', 'supplier_id', 'customer_id', 'warehouse_id', 'amount'].forEach((field) => {
        if (payload[field] !== undefined && payload[field] !== '') payload[field] = Number(payload[field])
      })
      const res = await fetch(module.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      const body = await res.json().catch(() => ({}))
      if (!res.ok) throw new Error(body.error || '创建失败')
      await fetchModule(key)
    } catch (e) {
      error = e.message
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

  onMount(() => {
    tabs.forEach((tab) => fetchModule(tab.key))
  })
</script>

<main>
  <h1>仓储管理系统（Flask + Svelte + PostgreSQL）</h1>
  <section class="card">
    <h2>登录与注册</h2>
    <div class="row">
      <input placeholder="用户名" bind:value={auth.username} />
      <input placeholder="密码" type="password" bind:value={auth.password} />
      <button on:click={() => doAuth('register')}>注册</button>
      <button on:click={() => doAuth('login')}>登录</button>
    </div>
    {#if token}<p class="ok">已登录，Token: {token}</p>{/if}
    {#if authError}<p class="error">{authError}</p>{/if}
  </section>

  <div class="tabs">
    {#each tabs as tab}
      <button class:active={activeTab === tab.key} on:click={() => (activeTab = tab.key)}>{tab.label}</button>
    {/each}
  </div>

  {#if error}<p class="error">{error}</p>{/if}

  {#each tabs as tab}
    {#if activeTab === tab.key}
      <section class="card">
        <h2>{tab.label}</h2>
        {#if tab.key === 'alerts'}
          <button on:click={generateAlerts}>生成库存预警</button>
        {/if}
        {#if tab.key === 'bill'}
          <button on:click={generateBill}>自动生成账单</button>
        {/if}
        {#if Object.keys(state[tab.key].form).length > 0}
          <div class="grid">
            {#each Object.entries(state[tab.key].form) as [field, value]}
              <input placeholder={field} bind:value={state[tab.key].form[field]} />
            {/each}
            <button on:click={() => createModule(tab.key)}>新增</button>
          </div>
        {/if}
        <pre>{JSON.stringify(state[tab.key].list, null, 2)}</pre>
      </section>
    {/if}
  {/each}
</main>

<style>
  :global(body) { margin: 0; font-family: system-ui, sans-serif; background: #f3f4f6; }
  main { max-width: 1200px; margin: 1.5rem auto; padding: 0 1rem; }
  .card { background: #fff; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 4px 12px rgba(0,0,0,.08); }
  .tabs { display: flex; flex-wrap: wrap; gap: .5rem; margin-bottom: 1rem; }
  button { border: 0; border-radius: 8px; padding: .45rem .7rem; background: #2563eb; color: #fff; cursor: pointer; }
  button.active { background: #1d4ed8; }
  input { border: 1px solid #d1d5db; border-radius: 8px; padding: .45rem .65rem; }
  .row, .grid { display: flex; flex-wrap: wrap; gap: .5rem; }
  .error { color: #dc2626; font-weight: 600; }
  .ok { color: #047857; font-weight: 600; }
  pre { background: #111827; color: #f9fafb; border-radius: 8px; padding: .8rem; overflow: auto; font-size: .8rem; }
</style>
