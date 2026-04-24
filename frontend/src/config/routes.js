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

export const defaultRoute = '/auth'
