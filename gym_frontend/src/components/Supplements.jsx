import React, { useEffect, useMemo, useState } from 'react'
import { getSupplementList, addSupplement, updateSupplement, deleteSupplement } from '../api.js'
import { getSupplementImage, supplementImages } from '../media.js'
import { getSupplier, setSupplier, removeSupplier } from '../supplierStore.js'

const categories = ["Protein", "Vitamins", "Weight Gain", "Pre-Workout", "Other"]

const emptyForm = {
  product_name: '',
  category: categories[0],
  price: '',
  stock_quantity: '',
  supplier: '',
  expiry_date: '',
  status: 'In Stock'
}

function Supplements() {
  const [items, setItems] = useState([])
  const [form, setForm] = useState(emptyForm)
  const [editingId, setEditingId] = useState(null)
  const [search, setSearch] = useState('')

  const loadItems = async () => {
    const data = await getSupplementList()
    // supplier isn't stored by the backend, so we merge in the locally-saved value
    setItems(data.map((item) => ({ ...item, supplier: getSupplier('supplement', item.id) })))
  }

  useEffect(() => {
    loadItems()
  }, [])

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    const payload = {
      product_name: form.product_name,
      category: form.category,
      price: Number(form.price),
      stock_quantity: Number(form.stock_quantity),
      expiry_date: form.expiry_date,
      status: form.status
    }

    if (editingId) {
      await updateSupplement(editingId, payload)
      setSupplier('supplement', editingId, form.supplier)
    } else {
      await addSupplement(payload)
      // backend doesn't echo the new id back, so refresh and match on
      // name as a best-effort fallback for saving the supplier
      const refreshed = await getSupplementList()
      const match = [...refreshed].reverse().find((i) => i.product_name === form.product_name)
      if (match) setSupplier('supplement', match.id, form.supplier)
    }

    setForm(emptyForm)
    setEditingId(null)
    loadItems()
  }

  const handleEdit = (item) => {
    setForm({
      product_name: item.product_name,
      category: item.category || categories[0],
      price: item.price,
      stock_quantity: item.stock_quantity,
      supplier: item.supplier || '',
      expiry_date: item.expiry_date || '',
      status: item.status
    })
    setEditingId(item.id)
  }

  const handleDelete = async (id) => {
    await deleteSupplement(id)
    removeSupplier('supplement', id)
    loadItems()
  }

  const handleCancel = () => {
    setForm(emptyForm)
    setEditingId(null)
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
      <h2>Supplement Shop</h2>
      <p className="section-sub">Add, view, edit, delete and search supplement inventory.</p>

      <form className="form" onSubmit={handleSubmit}>
        <input name="product_name" placeholder="Product Name" value={form.product_name} onChange={handleChange} required />

        <select name="category" value={form.category} onChange={handleChange}>
          {categories.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>

        <input name="price" type="number" placeholder="Price" value={form.price} onChange={handleChange} required />
        <input name="stock_quantity" type="number" placeholder="Quantity" value={form.stock_quantity} onChange={handleChange} required />
        <input name="supplier" placeholder="Supplier" value={form.supplier} onChange={handleChange} required />
        <input name="expiry_date" type="date" value={form.expiry_date} onChange={handleChange} />

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
          placeholder="Search supplements by name, category or supplier..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="product-grid">
        {filteredItems.map((item) => (
          <div className="product-card" key={item.id}>
            <img
              src={getSupplementImage(item.category)}
              alt={item.category}
              loading="lazy"
              onError={(e) => {
                if (e.target.src !== supplementImages.default) e.target.src = supplementImages.default
              }}
            />
            <div className="product-card-body">
              <h3>{item.product_name}</h3>
              <span className="meta">{item.category}</span>
              <span className="meta">Supplier: {item.supplier || '-'}</span>
              <span className="meta">Qty: {item.stock_quantity}</span>
              <span className="meta">Expiry: {item.expiry_date || '-'}</span>
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
        {filteredItems.length === 0 && <p>No supplements found.</p>}
      </div>
    </div>
  )
}

export default Supplements
