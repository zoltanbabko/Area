import { useState, useEffect } from "react";
import { AreaService } from "../services/area.service";
import { useNavigate, useParams } from "react-router-dom";
import DynamicForm from "../components/DynamicForm";
import toast from "react-hot-toast";

export default function EditArea() {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [services, setServices] = useState({});
  const [loading, setLoading] = useState(true);

  const [selectedActionService, setSelectedActionService] = useState("");
  const [selectedReactionService, setSelectedReactionService] = useState("");

  const [formData, setFormData] = useState({
    name: "",
    action: "",
    reaction: "",
    action_params: {},
    reaction_params: {},
    is_active: true
  });

  useEffect(() => {
    const loadData = async () => {
      try {
        const [servicesData, areaData] = await Promise.all([
          AreaService.getServices(),
          AreaService.getOne(id)
        ]);

        setServices(servicesData);
        setFormData(areaData);

        if (areaData.action) {
          const serviceName = areaData.action.split('.')[0];
          setSelectedActionService(serviceName);
        }
        if (areaData.reaction) {
          const serviceName = areaData.reaction.split('.')[0];
          setSelectedReactionService(serviceName);
        }

        setLoading(false);
      } catch (err) {
        console.error("Error loading data", err);
        toast.error("Failed to load Automation");
        navigate("/areas");
      }
    };
    loadData();
  }, [id, navigate]);

  const getSelectedActionDef = () => {
    if (!selectedActionService || !formData.action) return null;
    const actionName = formData.action.split('.')[1];
    return services[selectedActionService]?.actions?.find(a => a.name === actionName);
  };

  const getSelectedReactionDef = () => {
    if (!selectedReactionService || !formData.reaction) return null;
    const reactionName = formData.reaction.split('.')[1];
    return services[selectedReactionService]?.reactions?.find(r => r.name === reactionName);
  };


  const handleSelectChange = (type, value) => {
    if (!value) {
        setFormData(prev => ({ ...prev, [type]: "" }));
        return;
    }

    const serviceKey = type === 'action' ? selectedActionService : selectedReactionService;
    const collection = type === 'action' ? 'actions' : 'reactions';
    
    const name = value.split('.')[1];
    const def = services[serviceKey]?.[collection]?.find(x => x.name === name);
    
    const defaults = {};
    if (def && def.args) {
        Object.entries(def.args).forEach(([k, v]) => {
            if (v.default) defaults[k] = v.default;
        });
    }

    setFormData(prev => ({
        ...prev,
        [type]: value,
        [`${type}_params`]: defaults 
    }));
  };

  const handleParamsChange = (type, key, value) => {
    setFormData(prev => ({
      ...prev,
      [`${type}_params`]: {
        ...prev[`${type}_params`],
        [key]: value
      }
    }));
  };

  const handleSubmit = async () => {
    try {
      await AreaService.update(id, formData);
      toast.success("Automation updated!");
      navigate("/areas");
    } catch (err) {
      console.error(err);
      toast.error("Update failed.");
    }
  };

  if (loading) return <div className="container-center">Loading editor...</div>;

  const handleServiceSelect = (type, serviceName) => {
    if (!serviceName) return; 

    const serviceData = services[serviceName];

    if (serviceData?.auth_provider && !serviceData?.connected) {
        toast.error(`Please connect ${serviceName} in the Services page first!`, { icon: '🔒' });
        return; 
    }

    if (type === 'action') {
        setSelectedActionService(serviceName);
        if (serviceName !== formData.action.split('.')[0]) {
            setFormData(p => ({...p, action: "", action_params: {}}));
        }
    } else {
        setSelectedReactionService(serviceName);
        if (serviceName !== formData.reaction.split('.')[0]) {
            setFormData(p => ({...p, reaction: "", reaction_params: {}}));
        }
    }
  };

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '2rem' }}>
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
            <h2 style={{ margin: 0, fontSize: '1.8rem' }}>Edit Automation</h2>
            <button 
                onClick={() => navigate('/areas')} 
                style={{ width: 'auto', background: 'white', color: '#6b7280', border: '1px solid #e5e7eb', padding: '0.5rem 1rem' }}
            >
                Cancel
            </button>
        </div>
        
        <div style={{ marginBottom: '2.5rem' }}>
          <label style={{ fontWeight: '600', display: 'block', marginBottom: '0.5rem' }}>Automation Name</label>
          <input 
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})} 
            style={{ fontSize: '1.1rem', padding: '0.8rem' }}
          />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
          
          <div style={{ background: '#f9fafb', padding: '1.5rem', borderRadius: '12px', border: '1px solid #e5e7eb' }}>
            <h3 style={{ color: '#4f46e5', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '10px', fontSize: '1.2rem' }}>
              <span style={{ background: '#eef2ff', padding: '8px', borderRadius: '8px' }}>⚡</span> 
              IF THIS
            </h3>
            
            <label style={{fontWeight: '500'}}>Service</label>
            <select 
                value={selectedActionService} 
                onChange={e => handleServiceSelect('action', e.target.value)}
            >
              {Object.keys(services)
                .filter(s => services[s].actions && services[s].actions.length > 0)
                .map(sName => (
                  <option key={sName} value={sName}>{sName.charAt(0).toUpperCase() + sName.slice(1)}</option>
              ))}
            </select>

            {selectedActionService && (
              <div style={{ marginTop: '1rem' }}>
                <label style={{fontWeight: '500'}}>Trigger</label>
                <select 
                  value={formData.action} 
                  onChange={(e) => handleSelectChange('action', e.target.value)}
                >
                  <option value="">Choose trigger...</option>
                  {services[selectedActionService]?.actions?.map(action => (
                    <option key={action.name} value={`${selectedActionService}.${action.name}`}>
                      {action.description || action.name}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {getSelectedActionDef() && getSelectedActionDef().args && Object.keys(getSelectedActionDef().args).length > 0 && (
               <div style={{ marginTop: '1.5rem', paddingTop: '1rem', borderTop: '1px dashed #cbd5e1' }}>
                <h4 style={{ fontSize: '0.85rem', textTransform: 'uppercase', color: '#64748b', letterSpacing: '0.05em', marginBottom: '0.5rem' }}>
                    Configure Trigger
                </h4>
                <DynamicForm 
                    schema={getSelectedActionDef().args}
                    values={formData.action_params}
                    onChange={(k, v) => handleParamsChange('action', k, v)}
                    context={{ 
                        service: selectedActionService, 
                        type: 'actions', 
                        name: getSelectedActionDef().name 
                    }}
                />
              </div>
            )}
          </div>

          <div style={{ background: '#f9fafb', padding: '1.5rem', borderRadius: '12px', border: '1px solid #e5e7eb' }}>
            <h3 style={{ color: '#10b981', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '10px', fontSize: '1.2rem' }}>
              <span style={{ background: '#ecfdf5', padding: '8px', borderRadius: '8px' }}>🚀</span> 
              THEN THAT
            </h3>
            
            <label style={{fontWeight: '500'}}>Service</label>
            <select 
                value={selectedReactionService} 
                onChange={e => {
                    setSelectedReactionService(e.target.value);
                    if (e.target.value !== formData.reaction.split('.')[0]) {
                        setFormData(p => ({...p, reaction: "", reaction_params: {}}));
                    }
                }}
            >
              {Object.keys(services)
                .filter(s => services[s].reactions && services[s].reactions.length > 0)
                .map(sName => (
                  <option key={sName} value={sName}>{sName.charAt(0).toUpperCase() + sName.slice(1)}</option>
              ))}
            </select>

            {selectedReactionService && (
              <div style={{ marginTop: '1rem' }}>
                <label style={{fontWeight: '500'}}>Action</label>
                <select 
                  value={formData.reaction} 
                  onChange={(e) => handleSelectChange('reaction', e.target.value)}
                >
                  <option value="">Choose action...</option>
                  {services[selectedReactionService]?.reactions?.map(reaction => (
                    <option key={reaction.name} value={`${selectedReactionService}.${reaction.name}`}>
                      {reaction.description || reaction.name}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {getSelectedReactionDef() && getSelectedReactionDef().args && Object.keys(getSelectedReactionDef().args).length > 0 && (
              <div style={{ marginTop: '1.5rem', paddingTop: '1rem', borderTop: '1px dashed #cbd5e1' }}>
                <h4 style={{ fontSize: '0.85rem', textTransform: 'uppercase', color: '#64748b', letterSpacing: '0.05em', marginBottom: '0.5rem' }}>
                    Configure Action
                </h4>
                <DynamicForm 
                    schema={getSelectedReactionDef().args}
                    values={formData.reaction_params}
                    onChange={(k, v) => handleParamsChange('reaction', k, v)}
                    context={{ 
                        service: selectedReactionService, 
                        type: 'actions', 
                        name: getSelectedReactionDef().name 
                    }}
                />
              </div>
            )}
          </div>
        </div>

        <div style={{ marginTop: '3rem', borderTop: '1px solid #e5e7eb', paddingTop: '2rem', textAlign: 'right' }}>
          <button 
            onClick={handleSubmit} 
            style={{ 
                padding: '1rem 2.5rem', 
                fontSize: '1.1rem', 
                background: '#4f46e5', 
                color: 'white', 
                fontWeight: '600',
                boxShadow: '0 4px 6px -1px rgba(79, 70, 229, 0.2)'
            }}
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  );
}