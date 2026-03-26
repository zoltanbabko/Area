import api from "./api";

export const AreaService = {
  getAll: async () => {
    return (await api.get("/areas/")).data;
  },

  getOne: async (id) => {
    return (await api.get(`/areas/${id}`)).data;
  },

  create: async (data) => {
    return await api.post("/areas/", data);
  },

  update: async (id, data) => {
    return await api.patch(`/areas/${id}`, data);
  },

  delete: async (id) => {
    return await api.delete(`/areas/${id}`);
  },

  getServices: async () => {
    return (await api.get("/services")).data;
  }
};