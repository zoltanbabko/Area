import React, { useState, useEffect } from 'react';
import api from "../services/api"; 

export default function DynamicForm({ schema, values, onChange, context }) {
  
  if (!schema || Object.keys(schema).length === 0) return null;

  return (
    <div style={{ marginTop: '1rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      {Object.entries(schema).map(([key, fieldDef]) => (
        <DynamicField 
            key={key} 
            fieldKey={key} 
            fieldDef={fieldDef} 
            value={values[key]} 
            onChange={onChange} 
            context={context}
        />
      ))}
    </div>
  );
}

function DynamicField({ fieldKey, fieldDef, value, onChange, context }) {
    const [options, setOptions] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (fieldDef.type === 'select' && fieldDef.dynamic_source && context) {
            setLoading(true);
            api.get(`/services/${context.service}/${context.type}/${context.name}/options/${fieldKey}`)
               .then(res => setOptions(res.data))
               .catch(err => console.error("Failed to load options", err))
               .finally(() => setLoading(false));
        }
    }, [fieldDef.type, context?.service, context?.name]); 

    const commonStyle = {
        width: '100%', 
        padding: '0.6rem', 
        borderRadius: '6px', 
        border: '1px solid #d1d5db',
        fontFamily: 'inherit',
        background: '#fff',
        color: '#000'
    };

    return (
        <div>
            <label style={{ display: 'block', marginBottom: '0.3rem', fontSize: '0.9rem', color: '#4b5563', fontWeight: '500' }}>
                {fieldDef.label || fieldKey}
            </label>

            {fieldDef.type === 'select' ? (
                <select 
                    style={commonStyle}
                    value={value || ""}
                    onChange={(e) => onChange(fieldKey, e.target.value)}
                    disabled={loading}
                >
                    <option value="">{loading ? "Loading options..." : "Select an option..."}</option>
                    {options.map(opt => (
                        <option key={opt.value} value={opt.value}>
                            {opt.label}
                        </option>
                    ))}
                </select>

            ) : fieldDef.type === 'long_text' ? (
                <textarea
                    style={{ ...commonStyle, minHeight: '80px' }}
                    value={value || fieldDef.default || ''}
                    onChange={(e) => onChange(fieldKey, e.target.value)}
                    placeholder={`Enter ${fieldDef.label}...`}
                />

            ) : (
                <input
                    type={fieldDef.type === 'number' ? 'number' : 'text'}
                    style={commonStyle}
                    value={value || fieldDef.default || ''}
                    onChange={(e) => onChange(fieldKey, e.target.value)}
                    placeholder={`Enter ${fieldDef.label}...`}
                />
            )}

            {fieldDef.type !== 'number' && fieldDef.type !== 'select' && (
                <small style={{ color: '#9ca3af', fontSize: '0.75rem', marginTop: '4px', display: 'block' }}>
                    Tip: Use <code>{`{{ variable }}`}</code> here.
                </small>
            )}
        </div>
    );
}