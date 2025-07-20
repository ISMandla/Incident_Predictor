import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Make sure this is correctly imported

function App() {
  const [cpu, setCpu] = useState('');
  const [mem, setMem] = useState('');
  const [disk, setDisk] = useState('');
  const [metricPrediction, setMetricPrediction] = useState('');
  const [log, setLog] = useState('');
  const [logPrediction, setLogPrediction] = useState('');

  const handleAnomalyPredict = async () => {
    if (!cpu || !mem || !disk) {
      alert("Please enter CPU, MEM, and DISK values.");
      return;
    }
    console.log(cpu,mem,disk);
    try {
        console.log(cpu,mem,disk);
        const response = await axios.post('http://localhost:8000/predict/anomaly', {
        cpu: parseFloat(cpu),
        memory: parseFloat(mem),
        disk: parseFloat(disk)
      });
      const label = response.data.prediction === -1 ? "Anomaly" : "Normal";
      setMetricPrediction(label);
    } catch (error) {
      setMetricPrediction('Error');
      console.error(error);
    }
  };

  const handleLogClassify = async () => {
    try {
      const response = await axios.post('http://localhost:8000/predict/log', {
        log: log
      });
      setLogPrediction(response.data.prediction);
    } catch (error) {
      setLogPrediction('Error');
      console.error(error);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <h1 className="title">Incident Prediction Dashboard</h1>

        <div className="card">
          <h2 className="subtitle">System Metric Anomaly Detection</h2>
          <div className="row">
            <input
              type="number"
              placeholder="CPU"
              value={cpu}
              onChange={(e) => setCpu(e.target.value)}
              className="input"
            />
            <input
              type="number"
              placeholder="MEM"
              value={mem}
              onChange={(e) => setMem(e.target.value)}
              className="input"
            />
            <input
              type="number"
              placeholder="DISK"
              value={disk}
              onChange={(e) => setDisk(e.target.value)}
              className="input"
            />
            <button className="button" onClick={handleAnomalyPredict}>Predict</button>
          </div>
          <div className="prediction">Prediction: <strong>{metricPrediction}</strong></div>
        </div>

        <div className="card">
          <h2 className="subtitle">Log Classification</h2>
          <div className="row">
            <input
              type="text"
              placeholder="Enter log"
              value={log}
              onChange={(e) => setLog(e.target.value)}
              className="input full"
            />
            <button className="button" onClick={handleLogClassify}>Classify</button>
          </div>
          <div className="prediction">Prediction: <strong>{logPrediction}</strong></div>
        </div>
      </div>
    </div>
  );
}

export default App;
