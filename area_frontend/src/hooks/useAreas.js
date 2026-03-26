import { useState, useEffect } from "react";
import { AreaService } from "../services/area.service";
import toast from "react-hot-toast";

export const useAreas = () => {
  const [areas, setAreas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAreas = async () => {
    try {
      setLoading(true);
      const data = await AreaService.getAll();
      setAreas(data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  const toggleArea = async (id, currentStatus) => {
    try {
      setAreas(areas.map(a => a.id === id ? { ...a, is_active: !currentStatus } : a));
      
      await AreaService.update(id, { is_active: !currentStatus });
    } catch (err) {
      console.error("Failed to update area", err);
      fetchAreas();
    }
  };

  const deleteArea = async (id) => {
    if (!window.confirm("Delete this AREA?")) return;
    try {
      await AreaService.delete(id);
      setAreas(areas.filter((a) => a.id !== id));
      toast.success("Area deleted");
    } catch (err) {
      console.error("Failed to delete", err);
      toast.error("Failed to delete area");
    }
  };

  useEffect(() => {
    fetchAreas();
  }, []);

  return { areas, loading, error, toggleArea, deleteArea, refresh: fetchAreas };
};