import React, { useState } from 'react';
import axios from 'axios';

const AnomalyForm = () => {
  const [input, setInput] = useState({ cpu: "", memory: "", disk: "" });
  const [result, setResult] = useState(null);

  const handleChange = e => setInput({ ...input, [e.target.name]: e.target.value });

  const handleSubmit = async () => {
    const res = await axios.post('http://localhost:8000/predict/anomaly', input);
    setResult(res.data);
  };

  return (
    <div>
      <h2>System Metric Anomaly Detection</h2>
      <input name="cpu" placeholder="CPU" onChange={handleChange} />
      <input name="memory" placeholder="Memory" onChange={handleChange} />
      <input name="disk" placeholder="Disk" onChange={handleChange} />
      <button onClick={handleSubmit}>Predict</button>
      {result && <p><strong>Prediction:</strong> {result.anomaly ? "Anomaly" : "Normal"}</p>}
    </div>
  );
};

export default AnomalyForm;
