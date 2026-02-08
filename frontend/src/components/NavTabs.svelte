<script>
  export let routes = []
  export let activePath = '/auth'
  export let navigate = () => {}
</script>

<nav class="flex flex-wrap gap-2 rounded-xl bg-white p-3 shadow-sm">
  {#each routes as route}
    <button
      class={`rounded-lg px-4 py-2 text-sm font-medium transition ${
        activePath === route.path
          ? 'bg-blue-600 text-white'
          : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
      }`}
      on:click={() => navigate(route.path)}
    >
      {route.label}
    </button>
  {/each}
</nav>
