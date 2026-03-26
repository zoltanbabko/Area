export const isAuthenticated = () => {
    return Boolean(localStorage.getItem("token"));
};



export const logout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
};