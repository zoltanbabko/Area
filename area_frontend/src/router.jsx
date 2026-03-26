import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { isAuthenticated } from "./services/auth";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Areas from "./pages/Areas";
import EditArea from "./pages/EditArea";
import CreateArea from "./pages/CreateArea";
import Services from "./pages/Services";
import Layout from "./components/Layout";

const PrivateRoute = ({ children }) => {
    return isAuthenticated() ? children : <Navigate to="/login" />;
};

const PublicRoute = ({ children }) =>
    isAuthenticated() ? <Navigate to="/dashboard" /> : children;

export default function Router() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
                <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />

                <Route element={<PrivateRoute><Layout /></PrivateRoute>}>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/areas" element={<Areas />} />
                    <Route path="/areas/create" element={<CreateArea />} />
                    <Route path="/areas/:id/edit" element={<EditArea />} />
                    <Route path="/services" element={<Services />} />
                    <Route path="*" element={<Navigate to="/dashboard" />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}