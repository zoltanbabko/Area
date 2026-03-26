import { useEffect, useState } from "react";
import api from "../services/api";
import toast from "react-hot-toast";

const getUserId = () => {
    const token = localStorage.getItem("token");
    if (!token) return null;
    try {
        return JSON.parse(atob(token.split('.')[1])).user_id; 
    } catch {
        return null;
    }
};

export default function Services() {
    const [services, setServices] = useState({});
    const [loading, setLoading] = useState(true);
    const userId = getUserId();

    const fetchServices = async () => {
        try {
            const res = await api.get("/services");
            setServices(res.data);
            setLoading(false);
        } catch (err) { 
            console.error(err); 
            toast.error("Failed to load services");
        }
    };

    useEffect(() => { fetchServices(); }, []);

    const connectService = (serviceName, authProvider) => {
        if (!authProvider) { 
            toast("No authentication required for this service.", { icon: 'ℹ️' });
            return; 
        }
        window.location.href = `${import.meta.env.VITE_API_URL}/auth/${authProvider}/login?user_id=${userId}`;
    };

    if (loading) return <div className="container-center">Loading services...</div>;

    return (
        <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
            <div className="page-header">
                <div>
                    <h1 className="page-title">Services Dashboard</h1>
                    <p className="page-subtitle">Manage your connected accounts</p>
                </div>
            </div>

            <div className="grid-container">
                {Object.entries(services).map(([name, data]) => (
                    <div key={name} className="service-card">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                            <h3 style={{ textTransform: 'capitalize', margin: 0, fontSize: '1.3rem', fontWeight: '600' }}>
                                {name.replace('_', ' ')}
                            </h3>
                            <span className={`status-badge ${data.connected ? 'connected' : 'disconnected'}`}>
                                {data.connected ? 'Connected' : 'Not Connected'}
                            </span>
                        </div>

                        <div style={{ marginBottom: '1.5rem', flex: 1 }}>
                            <p style={{ fontSize: '0.9rem', color: '#4b5563', lineHeight: '1.5' }}>
                                <strong>{data.actions.length}</strong> Actions<br/>
                                <strong>{data.reactions.length}</strong> Reactions
                            </p>
                        </div>

                        {!data.connected && data.auth_provider && (
                            <button className="btn btn-primary btn-block" onClick={() => connectService(name, data.auth_provider)}>
                                Connect
                            </button>
                        )}
                        
                        {data.connected && (
                            <button className="btn btn-secondary btn-block" disabled style={{ opacity: 0.7, color: '#166534', borderColor: '#dcfce7', background: '#f0fdf4' }}>
                                ✓ Linked
                            </button>
                        )}
                        
                        {!data.auth_provider && !data.connected && (
                            <button className="btn btn-secondary btn-block" disabled style={{ opacity: 0.5 }}>
                                No Auth Required
                            </button>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}