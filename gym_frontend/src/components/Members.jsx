import React, { useEffect, useState } from 'react'
import { getMembers, addMember, updateMember, deleteMember } from '../api.js'

const emptyForm = { name: '', email: '', phone: '', age: '' }

function Members() {
  const [members, setMembers] = useState([])
  const [form, setForm] = useState(emptyForm)
  const [editingId, setEditingId] = useState(null)
  const [errorMsg, setErrorMsg] = useState('')

  const loadMembers = async () => {
    const data = await getMembers()
    setMembers(data)
  }

  useEffect(() => {
    loadMembers()
  }, [])

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setErrorMsg('')

    const payload = { ...form, age: Number(form.age) }

    const result = editingId
      ? await updateMember(editingId, payload)
      : await addMember(payload)

    if (!result.success) {
      setErrorMsg(result.message || 'Something went wrong, please try again')
      return
    }

    setForm(emptyForm)
    setEditingId(null)
    loadMembers()
  }

  const handleEdit = (member) => {
    setForm({
      name: member.name,
      email: member.email,
      phone: member.phone,
      age: member.age
    })
    setEditingId(member.id)
  }

  const handleDelete = async (id) => {
    const result = await deleteMember(id)
    if (!result.success) {
      setErrorMsg(result.message || 'Something went wrong, please try again')
      return
    }
    loadMembers()
  }

  const handleCancel = () => {
    setForm(emptyForm)
    setEditingId(null)
    setErrorMsg('')
  }

  return (
    <div className="section">
      <h2>Members</h2>
      <p className="section-sub">Add, view, edit and delete gym members.</p>

      <form className="form" onSubmit={handleSubmit}>
        {errorMsg && <p className="form-error">{errorMsg}</p>}

        <input name="name" placeholder="Name" value={form.name} onChange={handleChange} required />
        <input name="email" placeholder="Email" value={form.email} onChange={handleChange} required />
        <input name="phone" placeholder="Phone" value={form.phone} onChange={handleChange} required />
        <input name="age" type="number" placeholder="Age" value={form.age} onChange={handleChange} required />

        <button type="submit">{editingId ? 'Update Member' : 'Add Member'}</button>
        {editingId && <button type="button" onClick={handleCancel}>Cancel</button>}
      </form>

      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Age</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {members.map((member) => (
            <tr key={member.id}>
              <td>{member.id}</td>
              <td>{member.name}</td>
              <td>{member.email}</td>
              <td>{member.phone}</td>
              <td>{member.age}</td>
              <td>
                <button onClick={() => handleEdit(member)}>Edit</button>
                <button onClick={() => handleDelete(member.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Members
