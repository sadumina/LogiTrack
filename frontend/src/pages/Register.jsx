import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";

function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fuelCardNo, setFuelCardNo] = useState("");
  const [role, setRole] = useState("employee"); // default
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await API.post("/users/register", {
        name,
        email,
        password,
        fuel_card_no: fuelCardNo,
        role,
      });
      alert("✅ Registered successfully. Please login.");
      navigate("/");
    } catch (error) {
      console.error(error.response?.data || error.message);
      alert(error.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white shadow-md rounded-lg p-8 w-96">
        <h2 className="text-2xl font-bold text-center mb-6">Register</h2>
        <form onSubmit={handleRegister} className="space-y-4">
          <input
            type="text"
            placeholder="Full Name"
            className="border border-gray-300 rounded px-3 py-2 w-full"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <input
            type="email"
            placeholder="Email"
            className="border border-gray-300 rounded px-3 py-2 w-full"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            className="border border-gray-300 rounded px-3 py-2 w-full"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Fuel Card Number"
            className="border border-gray-300 rounded px-3 py-2 w-full"
            value={fuelCardNo}
            onChange={(e) => setFuelCardNo(e.target.value)}
            required
          />
          <select
            className="border border-gray-300 rounded px-3 py-2 w-full"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            <option value="employee">Employee</option>
            <option value="admin">Admin (Finance)</option>
          </select>
          <button
            type="submit"
            className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700"
          >
            Register
          </button>
        </form>
        <p className="text-sm mt-4 text-center">
          Already have an account?{" "}
          <span
            className="text-green-600 cursor-pointer"
            onClick={() => navigate("/")}
          >
            Login
          </span>
        </p>
      </div>
    </div>
  );
}

export default Register;
