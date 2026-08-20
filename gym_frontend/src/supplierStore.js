// The backend's Equipment/Supplement tables don't have a "supplier" column,
// and per the brief we're not allowed to add or change anything in the
// backend. So the supplier field the shop forms collect is kept here, in
// the browser's localStorage, keyed by product type + id, and merged into
// whatever the API returns. Without this, supplier would be typed into the
// form but forgotten the moment the list reloads.
const KEY = 'p45_suppliers'

function readAll() {
  try {
    return JSON.parse(localStorage.getItem(KEY)) || {}
  } catch {
    return {}
  }
}

function writeAll(data) {
  localStorage.setItem(KEY, JSON.stringify(data))
}

export function getSupplier(type, id) {
  return readAll()[`${type}-${id}`] || ''
}

export function setSupplier(type, id, supplier) {
  const all = readAll()
  all[`${type}-${id}`] = supplier
  writeAll(all)
}

export function removeSupplier(type, id) {
  const all = readAll()
  delete all[`${type}-${id}`]
  writeAll(all)
}
