<script>
  import { onMount } from 'svelte'

  import AuthPage from './components/AuthPage.svelte'
  import ModulePage from './components/ModulePage.svelte'
  import NavTabs from './components/NavTabs.svelte'
  import { modules, numericFields } from './config/modules'
  import { routes } from './config/routes'
  import { postJson, getJson } from './services/api'
  import { currentPath } from './stores/router'

  let activePath = '/auth'
  const routeByPath = Object.fromEntries(routes.map((route) => [route.path, route]))

  let token = ''
  let auth = { username: '', password: '' }
  let authError = ''
  let pageError = ''

  const lists = Object.fromEntries(Object.keys(modules).map((key) => [key, []]))

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
    try {
      const body = await postJson(`/api/auth/${path}`, auth)
      if (body.token) token = body.token
    } catch (error) {
      authError = error.message
    }
  }

  async function fetchModule(key) {
    pageError = ''
    try {
      lists[key] = await getJson(modules[key].endpoint)
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

    numericFields.forEach((field) => {
      if (payload[field] !== undefined && payload[field] !== '') {
        payload[field] = Number(payload[field])
      }
    })

    try {
      await postJson(modules[key].endpoint, payload)
      await fetchModule(key)
    } catch (error) {
      pageError = error.message
    }
  }

  async function generateAlerts() {
    await postJson('/api/alerts/generate', {})
    await fetchModule('alerts')
  }

  async function generateBill() {
    await postJson('/api/bills/generate', {
      source: 'outbound',
      reference_id: 1,
      amount: 99.9
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
