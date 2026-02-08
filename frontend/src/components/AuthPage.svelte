<script>
  export let auth = { username: '', password: '' }
  export let token = ''
  export let authError = ''
  export let onRegister = () => {}
  export let onLogin = () => {}
</script>

<section class="rounded-2xl bg-white p-6 shadow-sm">
  <div class="mb-4 flex items-center justify-between">
    <div>
      <h2 class="text-lg font-semibold text-slate-800">登录与注册</h2>
      <p class="text-sm text-slate-500">输入账号密码完成登录或创建新账号。</p>
    </div>
  </div>

  <div class="grid gap-3 md:grid-cols-2">
    <label class="flex flex-col gap-2 text-sm text-slate-600">
      用户名
      <input
        class="rounded-lg border border-slate-200 px-3 py-2 text-slate-800 focus:border-blue-500 focus:outline-none"
        placeholder="请输入用户名"
        bind:value={auth.username}
      />
    </label>
    <label class="flex flex-col gap-2 text-sm text-slate-600">
      密码
      <input
        class="rounded-lg border border-slate-200 px-3 py-2 text-slate-800 focus:border-blue-500 focus:outline-none"
        placeholder="请输入密码"
        type="password"
        bind:value={auth.password}
      />
    </label>
  </div>

  <div class="mt-4 flex flex-wrap gap-3">
    <button class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white" on:click={onRegister}>
      注册
    </button>
    <button class="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white" on:click={onLogin}>
      登录
    </button>
  </div>

  {#if token}
    <p class="mt-4 rounded-lg bg-emerald-50 px-3 py-2 text-sm text-emerald-700">
      已登录，Token: {token}
    </p>
  {/if}
  {#if authError}
    <p class="mt-4 rounded-lg bg-rose-50 px-3 py-2 text-sm text-rose-700">
      {authError}
    </p>
  {/if}
</section>
