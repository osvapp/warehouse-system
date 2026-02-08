<script>
  export let routes = []
  export let activePath = '/auth'
  export let navigate = () => {}
</script>

<nav class="tabs">
  {#each routes as route}
    <button class:active={activePath === route.path} on:click={() => navigate(route.path)}>
      {route.label}
    </button>
  {/each}
</nav>
