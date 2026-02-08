<script>
  export let auth = { username: '', password: '' }
  export let token = ''
  export let authError = ''
  export let onRegister = () => {}
  export let onLogin = () => {}
</script>

<section class="card">
  <h2>登录与注册</h2>
  <div class="row">
    <input placeholder="用户名" bind:value={auth.username} />
    <input placeholder="密码" type="password" bind:value={auth.password} />
    <button on:click={onRegister}>注册</button>
    <button on:click={onLogin}>登录</button>
  </div>
  {#if token}
    <p class="ok">已登录，Token: {token}</p>
  {/if}
  {#if authError}
    <p class="error">{authError}</p>
  {/if}
</section>
