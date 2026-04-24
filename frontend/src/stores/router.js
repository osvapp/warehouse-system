import { writable } from 'svelte/store'

import { defaultRoute, routes } from '../config/routes'

function getPathFromHash() {
  const hash = window.location.hash || ''
  const path = hash.replace(/^#/, '')
  return routes.some((route) => route.path === path) ? path : defaultRoute
}

function createRouter() {
  const store = writable(defaultRoute)

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
