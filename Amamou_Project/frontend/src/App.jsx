import { useState } from 'react'
import Header from './Header.jsx'
import Sidebar from './Sidebar.jsx'
import Home from './Home.jsx'
import Upload from './Upload.jsx'
import Prediction from './Prediction.jsx'
import Statistics from './Statistics.jsx'  // <-- import Statistics
import Footer from './Footer.jsx'
import { Routes, Route } from 'react-router-dom'
import './App.css'

function App() {
  const [openSidebarToggle, setOpenSidebarToggle] = useState(false)
  const [darkMode, setDarkMode] = useState(false)

  const OpenSidebar = () => {
    setOpenSidebarToggle(!openSidebarToggle)
  }

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
    document.body.classList.toggle('dark')
  }

  return (
    <div className="grid-container">
      <Header OpenSidebar={OpenSidebar} toggleDarkMode={toggleDarkMode} darkMode={darkMode} />
      <Sidebar openSidebarToggle={openSidebarToggle} OpenSidebar={OpenSidebar} />
      <div className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/prediction" element={<Prediction />} />
          <Route path="/statistics" element={<Statistics />} /> {/* <-- add this */}
        </Routes>
        <Footer />
      </div>
    </div>
  )
}

export default App
