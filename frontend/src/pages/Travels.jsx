import { useState, useEffect } from "react";
import API from "../services/api";

function Travels() {
  const [logs, setLogs] = useState([]);
  const [meterStart, setMeterStart] = useState("");
  const [meterEnd, setMeterEnd] = useState("");
  const [officialKm, setOfficialKm] = useState("");
  const [privateKm, setPrivateKm] = useState("");
  const [remarks, setRemarks] = useState("");
  const [totalKm, setTotalKm] = useState(0);

  // Auto calculate total km when meter changes
  useEffect(() => {
    if (meterStart && meterEnd) {
      const total = parseFloat(meterEnd) - parseFloat(meterStart);
      setTotalKm(total >= 0 ? total : 0);
    } else {
      setTotalKm(0);
    }
  }, [meterStart, meterEnd]);

  // Fetch my logs
  const fetchLogs = async () => {
    try {
      const res = await API.get("/travels/me");
      setLogs(res.data);
    } catch (err) {
      console.error("Error fetching logs:", err.response?.data || err.message);
    }
  };

  // Add new log
  const addLog = async (e) => {
    e.preventDefault();
    try {
      await API.post("/travels/", {
        meter_start: parseFloat(meterStart),
        meter_end: parseFloat(meterEnd),
        official_km: parseFloat(officialKm),
        private_km: parseFloat(privateKm),
        remarks,
      });

      // Reset fields
      setMeterStart("");
      setMeterEnd("");
      setOfficialKm("");
      setPrivateKm("");
      setRemarks("");
      setTotalKm(0);

      fetchLogs();
    } catch (err) {
      console.error("Error adding log:", err.response?.data || err.message);
      alert(err.response?.data?.detail || "Failed to add travel log");
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">My Travels</h2>

      {/* Travel Form */}
      <form onSubmit={addLog} className="mb-6 grid grid-cols-2 gap-4 max-w-3xl">
        <input
          type="number"
          placeholder="Meter Start"
          value={meterStart}
          onChange={(e) => setMeterStart(e.target.value)}
          className="border p-2"
          required
        />
        <input
          type="number"
          placeholder="Meter End"
          value={meterEnd}
          onChange={(e) => setMeterEnd(e.target.value)}
          className="border p-2"
          required
        />
        <input
          type="number"
          placeholder="Official KM"
          value={officialKm}
          onChange={(e) => setOfficialKm(e.target.value)}
          className="border p-2"
          required
        />
        <input
          type="number"
          placeholder="Private KM"
          value={privateKm}
          onChange={(e) => setPrivateKm(e.target.value)}
          className="border p-2"
          required
        />
        <input
          type="text"
          placeholder="Remarks"
          value={remarks}
          onChange={(e) => setRemarks(e.target.value)}
          className="border p-2 col-span-2"
        />
        <div className="col-span-2 flex items-center justify-between">
          <span className="font-semibold">
            Total KM: <span className="text-blue-600">{totalKm}</span>
          </span>
          <button
            type="submit"
            className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700"
          >
            Add Travel
          </button>
        </div>
      </form>

      {/* Travel Logs Table */}
      <table className="border-collapse border w-full max-w-5xl">
        <thead className="bg-gray-100">
          <tr>
            <th className="border p-2">Date</th>
            <th className="border p-2">Meter Start</th>
            <th className="border p-2">Meter End</th>
            <th className="border p-2">Official KM</th>
            <th className="border p-2">Private KM</th>
            <th className="border p-2">Total KM</th>
            <th className="border p-2">Remarks</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log, idx) => (
            <tr key={idx} className="text-center">
              <td className="border p-2">{log.date}</td>
              <td className="border p-2">{log.meter_start}</td>
              <td className="border p-2">{log.meter_end}</td>
              <td className="border p-2">{log.official_km}</td>
              <td className="border p-2">{log.private_km}</td>
              <td className="border p-2">{log.total_km}</td>
              <td className="border p-2">{log.remarks}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Travels;
