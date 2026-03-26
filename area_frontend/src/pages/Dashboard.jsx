import React from "react";
import { Link } from "react-router-dom";

export default function Dashboard() {
  return (
    <div>
      <div className="welcome-section">
        <h2 className="welcome-title">Dashboard</h2>
        <p className="welcome-subtitle">Welcome back to your Automation Hub</p>
      </div>
      
      <div className="grid-container">
        <Link to="/areas" className="dashboard-card">
          <div className="card-icon">📂</div>
          <h3 className="card-title">My Automations</h3>
          <p className="card-desc">Manage your active triggers and reactions</p>
        </Link>

        <Link to="/areas/create" className="dashboard-card">
          <div className="card-icon">⚡</div>
          <h3 className="card-title">Create New</h3>
          <p className="card-desc">Connect services to build a new workflow</p>
        </Link>

        <Link to="/services" className="dashboard-card">
          <div className="card-icon">🔧</div>
          <h3 className="card-title">Services</h3>
          <p className="card-desc">Connect Gmail, GitHub, Discord...</p>
        </Link>
      </div>
    </div>
  );
}