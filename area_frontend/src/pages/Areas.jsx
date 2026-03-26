import React from "react";
import { Link } from "react-router-dom";
import { useAreas } from "../hooks/useAreas";
import AreaCard from "../components/AreaCard";

export default function Areas() {
  const { areas, loading, toggleArea, deleteArea } = useAreas();

  if (loading) return <div className="container-center">Loading...</div>;

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">My AREAs</h1>
          <p className="page-subtitle">Manage your active automations</p>
        </div>
        <Link to="/areas/create">
          <button className="btn btn-primary">+ New AREA</button>
        </Link>
      </div>

      <div className="area-list" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '1.5rem' }}>
        {areas.map(area => (
           <AreaCard key={area.id} area={area} onToggle={toggleArea} onDelete={deleteArea} />
        ))}
      </div>
    </div>
  );
}