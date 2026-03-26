import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../services/api";
import toast from "react-hot-toast";

export default function Register() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const register = async () => {
        if (!username || !password) {
            toast.error("Please fill in all fields");
            return;
        }
        try {
            await api.post("/auth/register", { 
                username: username, 
                password: password 
            });
            toast.success("Account created! Please login.");
            navigate("/login");
        } catch (err) {
            console.error(err);
            toast.error(err.response?.data?.detail || "Registration failed.");
        }
    };

    return (
        <div className="container-center">
            <div className="auth-card">
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px', marginBottom: '2rem' }}>
                    <div className="logo-icon"></div>
                    <span className="logo-text" style={{ fontSize: '1.5rem' }}>AREA</span>
                </div>

                <h2 style={{textAlign: 'center', marginBottom: '0.5rem', color: '#4f46e5'}}>Create Account</h2>
                <p style={{textAlign: 'center', color: '#6b7280', marginBottom: '2rem'}}>Join the AREA platform</p>

                <label>Username</label>
                <input type="username" onChange={(e) => setUsername(e.target.value)} />
                
                <label>Password</label>
                <input type="password" onChange={(e) => setPassword(e.target.value)} />
                
                <button className="btn btn-primary btn-block" onClick={register}>Sign Up</button>

                <div style={{ margin: '1.5rem 0', borderTop: '1px solid #e5e7eb' }}></div>
                
                <p style={{textAlign: 'center', fontSize: '0.9rem'}}>
                    Already have an account? <Link to="/login" style={{color: '#4f46e5', fontWeight: '600'}}>Login</Link>
                </p>
            </div>
        </div>
    );
}