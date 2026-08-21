import React, { useEffect, useState } from 'react'
import { getPlans, addPlan, updatePlan, deletePlan } from '../api.js'

const emptyForm = { plan_name: '', duration_months: '', price: '', status: 'Active' }

function Plans() {
  const [plans, setPlans] = useState([])
  const [form, setForm] = useState(emptyForm)
  const [editingId, setEditingId] = useState(null)
  const [errorMsg, setErrorMsg] = useState('')

  const loadPlans = async () => {
    const data = await getPlans()
    setPlans(data)
  }

  useEffect(() => {
    loadPlans()
  }, [])

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setErrorMsg('')

    const payload = {
      ...form,
      duration_months: Number(form.duration_months),
      price: Number(form.price)
    }

    const result = editingId
      ? await updatePlan(editingId, payload)
      : await addPlan(payload)

    if (!result.success) {
      setErrorMsg(result.message || 'Something went wrong, please try again')
      return
    }

    setForm(emptyForm)
    setEditingId(null)
    loadPlans()
  }

  const handleEdit = (plan) => {
    setForm({
      plan_name: plan.plan_name,
      duration_months: plan.duration_months,
      price: plan.price,
      status: plan.status
    })
    setEditingId(plan.id)
  }

  const handleDelete = async (id) => {
    const result = await deletePlan(id)
    if (!result.success) {
      setErrorMsg(result.message || 'Something went wrong, please try again')
      return
    }
    loadPlans()
  }

  const handleCancel = () => {
    setForm(emptyForm)
    setEditingId(null)
    setErrorMsg('')
  }

  return (
    <div className="section">
      <h2>Plans</h2>
      <p className="section-sub">Manage gym membership plans.</p>

      <form className="form" onSubmit={handleSubmit}>
        {errorMsg && <p className="form-error">{errorMsg}</p>}

        <input name="plan_name" placeholder="Plan Name" value={form.plan_name} onChange={handleChange} required />
        <input name="duration_months" type="number" placeholder="Duration (months)" value={form.duration_months} onChange={handleChange} required />
        <input name="price" type="number" placeholder="Price" value={form.price} onChange={handleChange} required />
        <select name="status" value={form.status} onChange={handleChange}>
          <option value="Active">Active</option>
          <option value="Inactive">Inactive</option>
        </select>

        <button type="submit">{editingId ? 'Update Plan' : 'Add Plan'}</button>
        {editingId && <button type="button" onClick={handleCancel}>Cancel</button>}
      </form>

      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Plan Name</th>
            <th>Duration</th>
            <th>Price</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {plans.map((plan) => (
            <tr key={plan.id}>
              <td>{plan.id}</td>
              <td>{plan.plan_name}</td>
              <td>{plan.duration_months} mo</td>
              <td>₹{plan.price}</td>
              <td>{plan.status}</td>
              <td>
                <button onClick={() => handleEdit(plan)}>Edit</button>
                <button onClick={() => handleDelete(plan.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Plans
