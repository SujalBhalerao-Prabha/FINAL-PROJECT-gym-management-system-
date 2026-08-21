import React, { useEffect, useState } from 'react'
import {
  getMemberships, addMembership, updateMembership, deleteMembership
} from '../api.js'
import { getMembers } from '../api.js'
import { getPlans } from '../api.js'

const emptyForm = { member_id: '', plan_id: '', start_date: '', end_date: '', status: 'Active' }

function Memberships() {
  const [memberships, setMemberships] = useState([])
  const [members, setMembers] = useState([])
  const [plans, setPlans] = useState([])
  const [form, setForm] = useState(emptyForm)
  const [editingId, setEditingId] = useState(null)
  const [errorMsg, setErrorMsg] = useState('')

  const loadAll = async () => {
    const [membershipData, memberData, planData] = await Promise.all([
      getMemberships(),
      getMembers(),
      getPlans()
    ])
    setMemberships(membershipData)
    setMembers(memberData)
    setPlans(planData)
  }

  useEffect(() => {
    loadAll()
  }, [])

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setErrorMsg('')

    const result = editingId
      ? await updateMembership(editingId, {
          start_date: form.start_date,
          end_date: form.end_date,
          status: form.status
        })
      : await addMembership({
          member_id: Number(form.member_id),
          plan_id: Number(form.plan_id),
          start_date: form.start_date,
          end_date: form.end_date
        })

    if (!result.success) {
      setErrorMsg(result.message || 'Something went wrong, please try again')
      return
    }

    setForm(emptyForm)
    setEditingId(null)
    loadAll()
  }

  const handleEdit = (membership) => {
    setForm({
      member_id: membership.member_id,
      plan_id: membership.plan_id,
      start_date: membership.start_date,
      end_date: membership.end_date,
      status: membership.status
    })
    setEditingId(membership.id)
  }

  const handleDelete = async (id) => {
    const result = await deleteMembership(id)
    if (!result.success) {
      setErrorMsg(result.message || 'Something went wrong, please try again')
      return
    }
    loadAll()
  }

  const handleCancel = () => {
    setForm(emptyForm)
    setEditingId(null)
    setErrorMsg('')
  }

  return (
    <div className="section">
      <h2>Memberships</h2>
      <p className="section-sub">Link members to plans and track active memberships.</p>

      <form className="form" onSubmit={handleSubmit}>
        {errorMsg && <p className="form-error">{errorMsg}</p>}

        <select name="member_id" value={form.member_id} onChange={handleChange} required disabled={!!editingId}>
          <option value="">Select Member</option>
          {members.map((m) => (
            <option key={m.id} value={m.id}>{m.name}</option>
          ))}
        </select>

        <select name="plan_id" value={form.plan_id} onChange={handleChange} required disabled={!!editingId}>
          <option value="">Select Plan</option>
          {plans.map((p) => (
            <option key={p.id} value={p.id}>{p.plan_name}</option>
          ))}
        </select>

        <input name="start_date" type="date" value={form.start_date} onChange={handleChange} required />
        <input name="end_date" type="date" value={form.end_date} onChange={handleChange} required />

        {editingId && (
          <select name="status" value={form.status} onChange={handleChange}>
            <option value="Active">Active</option>
            <option value="Expired">Expired</option>
          </select>
        )}

        <button type="submit">{editingId ? 'Update Membership' : 'Add Membership'}</button>
        {editingId && <button type="button" onClick={handleCancel}>Cancel</button>}
      </form>

      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Member</th>
            <th>Plan</th>
            <th>Start</th>
            <th>End</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {memberships.map((m) => (
            <tr key={m.id}>
              <td>{m.id}</td>
              <td>{m.member_name}</td>
              <td>{m.plan_name}</td>
              <td>{m.start_date}</td>
              <td>{m.end_date}</td>
              <td>{m.status}</td>
              <td>
                <button onClick={() => handleEdit(m)}>Edit</button>
                <button onClick={() => handleDelete(m.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Memberships
