export const modules = {
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

export const numericFields = [
  'quantity',
  'min_stock',
  'item_id',
  'supplier_id',
  'customer_id',
  'warehouse_id',
  'amount'
]
