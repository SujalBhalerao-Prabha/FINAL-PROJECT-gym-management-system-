import React, { useEffect, useMemo, useState } from 'react'
import { getEquipmentList, addEquipment, updateEquipment, deleteEquipment } from '../api.js'
import { getEquipmentImage, equipmentImages, equipmentVideos } from '../media.js'
import { getSupplier, setSupplier, removeSupplier } from '../supplierStore.js'

const categories = ["Gym Essentials", "Workout Accessories", "Personal Care", "Useful Extras"]

const emptyForm = {
  product_name: '',
  category: categories[0],
  price: '',
  stock_quantity: '',
  supplier: '',
  status: 'In Stock'
}

function Equipment() {
  const [items, setItems] = useState([])
  const [form, setForm] = useState(emptyForm)
  const [editingId, setEditingId] = useState(null)
  const [search, setSearch] = useState('')
  const [errorMsg, setErrorMsg] = useState('')

  const loadItems = async () => {
    const data = await getEquipmentList()
    // supplier isn't stored by the backend, so we merge in the locally-saved value
    setItems(data.map((item) => ({ ...item, supplier: getSupplier('equipment', item.id) })))
  }

  useEffect(() => {
    loadItems()
  }, [])

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setErrorMsg('')

    const payload = {
      product_name: form.product_name,
      category: form.category,
      price: Number(form.price),
      stock_quantity: Number(form.stock_quantity),
      status: form.status
    }

    let result
    if (editingId) {
      result = await updateEquipment(editingId, payload)
      if (result.success) setSupplier('equipment', editingId, form.supplier)
    } else {
      result = await addEquipment(payload)
      if (result.success) {
        const newId = result.data && result.data.id
        if (newId) {
          setSupplier('equipment', newId, form.supplier)
        } else {
          const refreshed = await getEquipmentList()
          const match = [...refreshed].reverse().find((i) => i.product_name === form.product_name)
          if (match) setSupplier('equipment', match.id, form.supplier)
        }
      }
    }

    if (!result.success) {
      setErrorMsg(result.message || 'Something went wrong, please try again')
      return
    }

    setForm(emptyForm)
    setEditingId(null)
    loadItems()
  }

  const handleEdit = (item) => {
    setForm({
      product_name: item.product_name,
      category: item.category,
      price: item.price,
      stock_quantity: item.stock_quantity,
      supplier: item.supplier || '',
      status: item.status
    })
    setEditingId(item.id)
  }

  const handleDelete = async (id) => {
    const result = await deleteEquipment(id)
    if (!result.success) {
      setErrorMsg(result.message || 'Something went wrong, please try again')
      return
    }
    removeSupplier('equipment', id)
    loadItems()
  }

  const handleCancel = () => {
    setForm(emptyForm)
    setEditingId(null)
    setErrorMsg('')
  }

  const filteredItems = useMemo(() => {
    const q = search.trim().toLowerCase()
    if (!q) return items
    return items.filter((item) =>
      [item.product_name, item.category, item.supplier]
        .filter(Boolean)
        .some((field) => field.toLowerCase().includes(q))
    )
  }, [items, search])

  return (
    <div className="section">
      <h2>Equipment Shop</h2>
      <p className="section-sub">Add, view, edit, delete and search gym equipment inventory.</p>

      <form className="form" onSubmit={handleSubmit}>
        {errorMsg && <p className="form-error">{errorMsg}</p>}

        <input name="product_name" placeholder="Product Name" value={form.product_name} onChange={handleChange} required />

        <select name="category" value={form.category} onChange={handleChange}>
          {categories.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>

        <input name="price" type="number" placeholder="Price" value={form.price} onChange={handleChange} required />
        <input name="stock_quantity" type="number" placeholder="Quantity" value={form.stock_quantity} onChange={handleChange} required />
        <input name="supplier" placeholder="Supplier" value={form.supplier} onChange={handleChange} required />

        <select name="status" value={form.status} onChange={handleChange}>
          <option value="In Stock">In Stock</option>
          <option value="Out of Stock">Out of Stock</option>
        </select>

        <button type="submit">{editingId ? 'Update Item' : 'Add Item'}</button>
        {editingId && <button type="button" onClick={handleCancel}>Cancel</button>}
      </form>

      <div className="search-bar">
        <input
          type="text"
          placeholder="Search equipment by name, category or supplier..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="product-grid">
        {filteredItems.map((item) => (
          <div className="product-card" key={item.id}>
            <img
              src={item.image_url || getEquipmentImage(item.category)}
              alt={item.product_name}
              loading="lazy"
              onError={(e) => {
                if (e.target.src !== equipmentImages.default) e.target.src = equipmentImages.default
              }}
            />
            <div className="product-card-body">
              <h3>{item.product_name}</h3>
              <span className="meta">{item.category}</span>
              <span className="meta">Supplier: {item.supplier || '-'}</span>
              <span className="meta">Qty: {item.stock_quantity}</span>
              <span className="price">₹{item.price}</span>
              <span className={item.status === 'In Stock' ? 'status-pill in-stock' : 'status-pill out-of-stock'}>
                {item.status}
              </span>
            </div>
            <div className="product-card-actions">
              <button onClick={() => handleEdit(item)}>Edit</button>
              <button onClick={() => handleDelete(item.id)}>Delete</button>
            </div>
          </div>
        ))}
        {filteredItems.length === 0 && <p>No equipment found.</p>}
      </div>

      <div className="video-section">
        <h2>Equipment Demo Videos</h2>
        <p className="section-sub">Short sample clips showing how the video player looks in the shop.</p>
        <div className="video-grid">
          {equipmentVideos.map((v) => (
            <div className="video-card" key={v.title}>
              <video src={v.src} controls preload="none" />
              <p>{v.title}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Equipment
