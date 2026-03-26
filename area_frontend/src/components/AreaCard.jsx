import React from "react";
import { useNavigate } from "react-router-dom";

export default function AreaCard({ area, onToggle, onDelete }) {
    const navigate = useNavigate();

    const formatName = (str) => {
        if (!str) return "Unknown";
        const actionPart = str.split('.')[1] || str;
        return actionPart.split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    };

    const formatService = (str) => {
        if (!str) return "";
        return str.split('.')[0].charAt(0).toUpperCase() + str.split('.')[0].slice(1);
    };

    return (
    <div className="card" style={{ padding: '1.5rem', opacity: area.is_active ? 1 : 0.75 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <div style={{ width: 40, height: 40, background: '#eef2ff', borderRadius: 8, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#4f46e5', fontWeight: 'bold' }}>
            {area.action.split('.')[0][0].toUpperCase()}
          </div>
          <div>
            <h3 style={{ margin: 0, fontSize: '1.1rem' }}>{area.name || "Untitled"}</h3>
            <span style={{ fontSize: '0.8rem', color: area.is_active ? '#10b981' : '#6b7280', fontWeight: '600' }}>
              {area.is_active ? '● Active' : '○ Paused'}
            </span>
          </div>
        </div>
      </div>

      <div style={{ background: '#f9fafb', padding: '1rem', borderRadius: '8px', fontSize: '0.9rem', marginBottom: '1.5rem', border: '1px solid #f3f4f6' }}>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            <span style={{ fontWeight: 'bold', color: '#4f46e5', minWidth: '40px' }}>IF</span>
            <span style={{ background: '#e0e7ff', padding: '2px 8px', borderRadius: '4px', fontSize: '0.85rem', color: '#3730a3' }}>
                {formatService(area.action)}
            </span>
            <span>{formatName(area.action)}</span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontWeight: 'bold', color: '#10b981', minWidth: '40px' }}>THEN</span>
            <span style={{ background: '#dcfce7', padding: '2px 8px', borderRadius: '4px', fontSize: '0.85rem', color: '#166534' }}>
                {formatService(area.reaction)}
            </span>
            <span>{formatName(area.reaction)}</span>
        </div>

      </div>

      <div style={{ display: 'flex', gap: '8px', marginTop: 'auto' }}>
        <button 
          className="btn btn-secondary btn-sm" 
          style={{ flex: 1 }}
          onClick={() => onToggle(area.id, area.is_active)}
        >
          {area.is_active ? 'Pause' : 'Resume'}
        </button>
        
        <button 
          className="btn btn-secondary btn-sm"
          onClick={() => navigate(`/areas/${area.id}/edit`)}
        >
          Edit
        </button>

        <button 
          className="btn btn-danger btn-sm"
          onClick={() => onDelete(area.id)}
        >
          Delete
        </button>
      </div>
    </div>
  );
}