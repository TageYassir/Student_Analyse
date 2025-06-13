import React, { useRef } from 'react'

import { Link } from 'react-router-dom'  // <-- import Link
import {
  BsHouseFill,
  BsBarChartFill,
  BsUpload,
  BsGraphUp
} from 'react-icons/bs'

function Sidebar({ openSidebarToggle, OpenSidebar }) {
  const sidebarRef = useRef()

  return (
    <nav
      ref={sidebarRef}
      id="sidebar"
      className={`${openSidebarToggle ? 'sidebar_open' : ''}`}
    >
      <div className="sidebar-title">
        <span>Menu</span>
        <span
          onClick={OpenSidebar}
          className="close_icon"
          role="button"
          aria-label="Close Sidebar"
          tabIndex={0}
          onKeyDown={(e) => { if (e.key === 'Enter') OpenSidebar() }}
        >
          ×
        </span>
      </div>
      <ul className="sidebar-list">
        <li className="sidebar-list-item">
          <Link to="/">
            <BsHouseFill className="icon" />
            <span>Home</span>
          </Link>
        </li>
        <li className="sidebar-list-item">
          <Link to="/statistics">
            <BsBarChartFill className="icon" />
            <span>Statistics</span>
          </Link>
        </li>
        <li className="sidebar-list-item">
          <Link to="/upload">
            <BsUpload className="icon" />
            <span>Upload Data</span>
          </Link>
          <p>Upload new files here</p>
        </li>
        <li className="sidebar-list-item">
          <Link to="/prediction">
            <BsGraphUp className="icon" />
            <span>Prediction</span>
          </Link>
        </li>
      </ul>
    </nav>
  )
}

export default Sidebar
