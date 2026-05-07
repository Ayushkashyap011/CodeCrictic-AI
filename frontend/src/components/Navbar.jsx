import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar({ theme, toggleTheme }) {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <span className="logo-icon">⚙️</span>
          CodeCritic AI
        </Link>
        <ul className="navbar-menu">
          <li>
            <Link to="/problems" className="navbar-link">Problems</Link>
          </li>
          <li>
            <button className="theme-toggle" onClick={toggleTheme} title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}>
              {theme === 'dark' ? '☀️' : '🌙'}
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
