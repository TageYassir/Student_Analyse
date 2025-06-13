import React, { useState, useEffect } from 'react'
import { FaSun, FaMoon, FaChartPie } from 'react-icons/fa'


function Header() {
  const [isDark, setIsDark] = useState(false)

  useEffect(() => {
    const darkMode = document.body.classList.contains('dark')
    setIsDark(darkMode)
  }, [])

  const toggleTheme = () => {
    document.body.classList.toggle('dark')
    setIsDark(!isDark)
  }

  return (
    <header className="header">
      <button className="theme-toggle-btn" onClick={toggleTheme} aria-label="Toggle theme">
        {isDark ? <FaSun size={20} /> : <FaMoon size={20} />}
      </button>
      <div className="app-icon" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <FaChartPie size={24} />
        <span style={{ fontWeight: 'bold', fontSize: '1.2rem' }}>Dashboard</span>
      </div>
    </header>
  )
}

export default Header
