import React, { useState } from 'react';
import axios from 'axios';

const LogForm = () => {
  const [log, setLog] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    const res = await axios.post('http://localhost:8000/predict/log', { log });
    setResult(res.data);
  };

  return (
    <div>
      <h2>Log Classification</h2>
      <input value={log} onChange={(e) => setLog(e.target.value)} placeholder="Enter log..." />
      <button onClick={handleSubmit}>Classify</button>
      {result && <p><strong>Prediction:</strong> {result.prediction}</p>}
    </div>
  );
};

export default LogForm;
