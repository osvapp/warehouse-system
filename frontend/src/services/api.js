export async function postJson(url, payload) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })

  return parseJson(res)
}

export async function getJson(url) {
  const res = await fetch(url)
  return parseJson(res)
}

async function parseJson(res) {
  const body = await res.json().catch(() => ({}))
  if (!res.ok) {
    const message = body?.error || '请求失败'
    const error = new Error(message)
    error.status = res.status
    error.body = body
    throw error
  }
  return body
}
