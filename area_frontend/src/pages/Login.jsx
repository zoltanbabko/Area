import api from "../services/api";
import { useEffect, useState } from "react";
import { useNavigate, useSearchParams, Link } from "react-router-dom";
import toast from "react-hot-toast";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    const token = searchParams.get("token");
    if (token) {
      localStorage.setItem("token", token);
      navigate("/dashboard");
    }
  }, [searchParams, navigate]);

  const login = async () => {
    try {
      const params = new URLSearchParams();
      params.append("username", username);
      params.append("password", password);
      const res = await api.post("/auth/login", params);
      if (res.data.access_token) {
        localStorage.setItem("token", res.data.access_token);
        toast.success("Welcome back!");
        navigate("/dashboard");
      }
    } catch (err) { 
        toast.error("Invalid credentials"); 
    }
  };

  return (
    <div className="container-center">
      <div className="auth-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px', marginBottom: '2rem' }}>
            <div className="logo-icon"></div>
            <span className="logo-text" style={{ fontSize: '1.5rem' }}>AREA</span>
        </div>
        <h2 style={{ textAlign: 'center', color: '#4f46e5', marginBottom: '0.5rem' }}>Welcome Back</h2>
        <p style={{ textAlign: 'center', color: '#6b7280', marginBottom: '2rem' }}>Sign in to your account</p>

        <label>Username</label>
        <input onChange={e => setUsername(e.target.value)} />

        <label>Password</label>
        <input type="password" onChange={e => setPassword(e.target.value)} />

        <button className="btn btn-primary btn-block" onClick={login}>Sign In</button>

        <div style={{ margin: '1.5rem 0', borderTop: '1px solid #e5e7eb' }}></div>

        <button 
          className="btn btn-secondary btn-block"
          onClick={() => window.location.href = "http://localhost:8080/auth/google/login"}
        >
          <img src="https://www.google.com/favicon.ico" alt="G" style={{width: 16, height: 16}} />
          Sign in with Google
        </button>

        <p style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.9rem' }}>
          No account? <Link to="/register" style={{ color: '#4f46e5', fontWeight: '600' }}>Sign up</Link>
        </p>
      </div>
    </div>
  );
}