<script>
  import { onMount } from 'svelte'

  const apiBase = '/api/items'
  let items = []
  let error = ''
  let loading = false
  let form = { sku: '', name: '', quantity: 0, location: '' }

  async function fetchItems() {
    loading = true
    error = ''
    try {
      const res = await fetch(apiBase)
      if (!res.ok) throw new Error('Failed to load inventory')
      items = await res.json()
    } catch (e) {
      error = e.message
    } finally {
      loading = false
    }
  }

  async function addItem() {
    error = ''
    try {
      const payload = { ...form, quantity: Number(form.quantity) }
      const res = await fetch(apiBase, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })

      if (!res.ok) {
        const body = await res.json()
        throw new Error(body.error || 'Failed to create item')
      }

      form = { sku: '', name: '', quantity: 0, location: '' }
      await fetchItems()
    } catch (e) {
      error = e.message
    }
  }

  async function removeItem(id) {
    error = ''
    try {
      const res = await fetch(`${apiBase}/${id}`, { method: 'DELETE' })
      if (!res.ok) throw new Error('Failed to delete item')
      await fetchItems()
    } catch (e) {
      error = e.message
    }
  }

  onMount(fetchItems)
</script>

<main>
  <h1>库存管理系统</h1>

  <section class="card">
    <h2>新增库存</h2>
    <div class="form-grid">
      <input placeholder="SKU" bind:value={form.sku} />
      <input placeholder="名称" bind:value={form.name} />
      <input placeholder="数量" type="number" min="0" bind:value={form.quantity} />
      <input placeholder="库位" bind:value={form.location} />
      <button on:click|preventDefault={addItem}>添加</button>
    </div>
  </section>

  {#if error}
    <p class="error">{error}</p>
  {/if}

  <section class="card">
    <h2>库存列表</h2>
    {#if loading}
      <p>加载中...</p>
    {:else if items.length === 0}
      <p>暂无库存数据</p>
    {:else}
      <table>
        <thead>
          <tr>
            <th>ID</th><th>SKU</th><th>名称</th><th>数量</th><th>库位</th><th>操作</th>
          </tr>
        </thead>
        <tbody>
          {#each items as item}
            <tr>
              <td>{item.id}</td>
              <td>{item.sku}</td>
              <td>{item.name}</td>
              <td>{item.quantity}</td>
              <td>{item.location || '-'}</td>
              <td><button class="danger" on:click={() => removeItem(item.id)}>删除</button></td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  </section>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: Inter, system-ui, sans-serif;
    background: #f3f4f6;
  }
  main {
    max-width: 980px;
    margin: 2rem auto;
    padding: 0 1rem;
  }
  h1 {
    margin-bottom: 1rem;
  }
  .card {
    background: white;
    border-radius: 12px;
    padding: 1rem;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
    margin-bottom: 1rem;
  }
  .form-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(120px, 1fr));
    gap: 0.5rem;
  }
  input, button {
    padding: 0.55rem 0.7rem;
    border-radius: 8px;
    border: 1px solid #d1d5db;
  }
  button {
    background: #2563eb;
    color: white;
    border: 0;
    cursor: pointer;
  }
  .danger {
    background: #dc2626;
  }
  table {
    width: 100%;
    border-collapse: collapse;
  }
  th, td {
    padding: 0.6rem;
    border-bottom: 1px solid #e5e7eb;
    text-align: left;
  }
  .error {
    color: #dc2626;
    font-weight: 600;
  }
</style>
