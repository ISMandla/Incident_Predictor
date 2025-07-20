// src/components/Dashboard.js

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-black text-white p-6 font-sans">
      <div className="max-w-md mx-auto space-y-6">
        <h1 className="text-3xl font-bold leading-tight">
          Incident<br />Prediction<br />Dashboard
        </h1>

        {/* System Metric Anomaly Detection */}
        <div className="bg-gray-900 p-4 rounded-xl space-y-3">
          <h2 className="text-lg font-semibold">System Metric<br />Anomaly<br />Detection</h2>
          <div className="flex space-x-2">
            <input
              type="number"
              placeholder="CPU"
              className="w-1/2 p-2 rounded bg-gray-800 text-white"
            />
            <input
              type="number"
              placeholder="MEM"
              className="w-1/2 p-2 rounded bg-gray-800 text-white"
            />
            <button className="bg-gray-700 px-4 rounded hover:bg-gray-600">
              Predict
            </button>
          </div>
          <div className="text-sm">Prediction: <span className="font-medium">Normal</span></div>
        </div>

        {/* Log Classification */}
        <div className="bg-gray-900 p-4 rounded-xl space-y-3">
          <h2 className="text-lg font-semibold">Log Classification</h2>
          <div className="flex space-x-2">
            <input
              type="text"
              placeholder="word"
              className="w-full p-2 rounded bg-gray-800 text-white"
            />
            <button className="bg-gray-700 px-4 rounded hover:bg-gray-600">
              Classify
            </button>
          </div>
          <div className="text-sm">Prediction: <span className="font-medium">error</span></div>
        </div>
      </div>
    </div>
  );
}
