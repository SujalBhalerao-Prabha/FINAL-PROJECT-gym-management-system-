import React, { useState } from 'react'
import Members from './components/Members.jsx'
import Plans from './components/Plans.jsx'
import Memberships from './components/Memberships.jsx'
import Equipment from './components/Equipment.jsx'
import Supplements from './components/Supplements.jsx'
import { heroImage } from './media.js'

const TABS = [
  { key: 'members', label: 'Members' },
  { key: 'plans', label: 'Plans' },
  { key: 'memberships', label: 'Memberships' },
  { key: 'equipment', label: 'Equipment Shop' },
  { key: 'supplements', label: 'Supplement Shop' }
]

function App() {
  const [activeTab, setActiveTab] = useState('members')

  return (
    <div className="app">
      <header
        className="hero"
        style={{
          backgroundImage: `linear-gradient(120deg, rgba(10, 14, 26, 0.85), rgba(10, 14, 26, 0.6)), url(${heroImage})`
        }}
      >
        <div className="hero-overlay">
          <div className="brand">
            <span className="brand-badge">P45</span>
            <div>
              <h1>P45 Fitness &amp; Nutrition</h1>
              <p>Gym &bull; Supplements &bull; Equipment</p>
            </div>
          </div>
        </div>
      </header>

      <nav className="tabs">
        {TABS.map((tab) => (
          <button
            key={tab.key}
            className={activeTab === tab.key ? 'tab active' : 'tab'}
            onClick={() => setActiveTab(tab.key)}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      <main className="content">
        {activeTab === 'members' && <Members />}
        {activeTab === 'plans' && <Plans />}
        {activeTab === 'memberships' && <Memberships />}
        {activeTab === 'equipment' && <Equipment />}
        {activeTab === 'supplements' && <Supplements />}
      </main>

      <footer className="footer">
        <p>P45 Fitness &amp; Nutrition &mdash; Gym &bull; Supplements &bull; Equipment</p>
      </footer>
    </div>
  )
}

export default App
