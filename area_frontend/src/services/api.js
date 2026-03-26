import axios from "axios";

const hostname = window.location.hostname;

const API_URL = `http://${hostname}:8080`;

const api = axios.create({ baseURL: API_URL });

api.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});

export default api;