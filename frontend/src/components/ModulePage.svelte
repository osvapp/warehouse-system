<script>
  export let title = ''
  export let fields = []
  export let form = {}
  export let records = []
  export let error = ''
  export let onCreate = () => {}
  export let actions = []
</script>

<section class="card">
  <h2>{title}</h2>

  {#if actions.length > 0}
    <div class="row">
      {#each actions as action}
        <button on:click={action.handler}>{action.label}</button>
      {/each}
    </div>
  {/if}

  {#if fields.length > 0}
    <div class="grid">
      {#each fields as field}
        <input
          placeholder={field}
          type="text"
          bind:value={form[field]}
        />
      {/each}
      <button on:click={onCreate}>新增</button>
    </div>
  {/if}

  {#if error}
    <p class="error">{error}</p>
  {/if}

  <pre>{JSON.stringify(records, null, 2)}</pre>
</section>
