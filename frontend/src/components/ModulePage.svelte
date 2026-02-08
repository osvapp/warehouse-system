<script>
  export let title = ''
  export let fields = []
  export let form = {}
  export let records = []
  export let error = ''
  export let onCreate = () => {}
  export let actions = []
</script>

<section class="rounded-2xl bg-white p-6 shadow-sm">
  <div class="flex flex-wrap items-center justify-between gap-3">
    <div>
      <h2 class="text-lg font-semibold text-slate-800">{title}</h2>
      <p class="text-sm text-slate-500">管理{title}相关信息。</p>
    </div>
    {#if actions.length > 0}
      <div class="flex flex-wrap gap-2">
        {#each actions as action}
          <button class="rounded-lg bg-indigo-600 px-3 py-2 text-sm text-white" on:click={action.handler}>
            {action.label}
          </button>
        {/each}
      </div>
    {/if}
  </div>

  {#if fields.length > 0}
    <div class="mt-4 grid gap-3 md:grid-cols-2 lg:grid-cols-3">
      {#each fields as field}
        <label class="flex flex-col gap-2 text-sm text-slate-600">
          {field}
          <input
            class="rounded-lg border border-slate-200 px-3 py-2 text-slate-800 focus:border-blue-500 focus:outline-none"
            placeholder={`请输入${field}`}
            type="text"
            bind:value={form[field]}
          />
        </label>
      {/each}
      <div class="flex items-end">
        <button class="w-full rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white" on:click={onCreate}>
          新增
        </button>
      </div>
    </div>
  {/if}

  {#if error}
    <p class="mt-4 rounded-lg bg-rose-50 px-3 py-2 text-sm text-rose-700">
      {error}
    </p>
  {/if}

  <div class="mt-4">
    <div class="rounded-xl bg-slate-900 p-4 text-xs text-slate-100">
      <pre>{JSON.stringify(records, null, 2)}</pre>
    </div>
  </div>
</section>
