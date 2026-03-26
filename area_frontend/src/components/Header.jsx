import React from 'react';
import { logout } from '../services/auth';

export default function Header() {
  return (
    <header className="top-header">
      <button onClick={logout} className="btn">
        Logout
      </button>
    </header>
  );
}