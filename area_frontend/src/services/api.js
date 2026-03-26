import axios from "axios";

const hostname = window.location.hostname;

const API_URL = process.env.VITE_API_URL || `http://${hostname}:8000/api/`;

const api = axios.create({ baseURL: API_URL });

api.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});

export default api;