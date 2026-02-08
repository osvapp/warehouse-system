import { writable } from 'svelte/store'

export const routes = [
  { path: '/auth', key: 'auth', label: '登录与注册' },
  { path: '/inventory', key: 'inventory', label: '库存管理' },
  { path: '/warehouse', key: 'warehouse', label: '仓库管理' },
  { path: '/staff', key: 'staff', label: '库员管理' },
  { path: '/supplier', key: 'supplier', label: '供应商管理' },
  { path: '/customer', key: 'customer', label: '客户管理' },
  { path: '/inbound', key: 'inbound', label: '入库管理' },
  { path: '/outbound', key: 'outbound', label: '出库管理' },
  { path: '/alerts', key: 'alerts', label: '库存预警' },
  { path: '/bill', key: 'bill', label: '账单管理' },
  { path: '/employee', key: 'employee', label: '员工管理' },
  { path: '/role', key: 'role', label: '角色管理' },
  { path: '/permission', key: 'permission', label: '权限管理' }
]

const defaultPath = '/auth'

function getPathFromHash() {
  const hash = window.location.hash || ''
  const path = hash.replace(/^#/, '')
  return routes.some((route) => route.path === path) ? path : defaultPath
}

function createRouter() {
  const store = writable(defaultPath)

  function syncFromHash() {
    store.set(getPathFromHash())
  }

  function navigate(path) {
    if (!routes.some((route) => route.path === path)) return
    if (window.location.hash !== `#${path}`) {
      window.location.hash = path
    } else {
      store.set(path)
    }
  }

  window.addEventListener('hashchange', syncFromHash)
  syncFromHash()

  return {
    subscribe: store.subscribe,
    navigate
  }
}

export const currentPath = createRouter()
