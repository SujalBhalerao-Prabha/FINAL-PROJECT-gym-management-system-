const BASE_URL = "http://127.0.0.1:5000"

// Generic helper so we don't repeat fetch boilerplate in every component
async function request(url, method = "GET", body = null) {
  const options = {
    method,
    headers: { "Content-Type": "application/json" }
  }

  if (body) {
    options.body = JSON.stringify(body)
  }

  const response = await fetch(BASE_URL + url, options)
  return response.json()
}

// ---- Members ----
export const getMembers = () => request("/members")
export const getMember = (id) => request(`/members/${id}`)
export const addMember = (data) => request("/members", "POST", data)
export const updateMember = (id, data) => request(`/members/${id}`, "PUT", data)
export const deleteMember = (id) => request(`/members/${id}`, "DELETE")

// ---- Plans ----
export const getPlans = () => request("/plans")
export const addPlan = (data) => request("/plans", "POST", data)
export const updatePlan = (id, data) => request(`/plans/${id}`, "PUT", data)
export const deletePlan = (id) => request(`/plans/${id}`, "DELETE")

// ---- Memberships ----
export const getMemberships = () => request("/memberships")
export const addMembership = (data) => request("/memberships", "POST", data)
export const updateMembership = (id, data) => request(`/memberships/${id}`, "PUT", data)
export const deleteMembership = (id) => request(`/memberships/${id}`, "DELETE")

// ---- Equipment ----
export const getEquipmentList = () => request("/equipment")
export const addEquipment = (data) => request("/equipment", "POST", data)
export const updateEquipment = (id, data) => request(`/equipment/${id}`, "PUT", data)
export const deleteEquipment = (id) => request(`/equipment/${id}`, "DELETE")

// ---- Supplements ----
export const getSupplementList = () => request("/supplements")
export const addSupplement = (data) => request("/supplements", "POST", data)
export const updateSupplement = (id, data) => request(`/supplements/${id}`, "PUT", data)
export const deleteSupplement = (id) => request(`/supplements/${id}`, "DELETE")
