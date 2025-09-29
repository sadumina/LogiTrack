import { useEffect, useState } from "react";
import API from "../services/api";

function AdminDashboard() {
  const [users, setUsers] = useState([]);

  // Load all users
  const fetchUsers = async () => {
    try {
      const res = await API.get("/users/all");
      setUsers(res.data);
    } catch (err) {
      console.error("Error fetching users:", err.response?.data || err.message);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  // Update role
  const updateRole = async (email, role) => {
    try {
      await API.put(`/users/${email}`, { role });
      alert(`✅ Updated ${email} to ${role}`);
      fetchUsers();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to update role");
    }
  };

  // Delete user
  const deleteUser = async (email) => {
    if (!window.confirm(`Are you sure you want to delete ${email}?`)) return;
    try {
      await API.delete(`/users/${email}`);
      alert(`🗑️ Deleted ${email}`);
      fetchUsers();
    } catch (err) {
      alert(err.response?.data?.detail || "Delete failed");
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Admin Dashboard</h2>
      <table className="w-full border-collapse border">
        <thead>
          <tr className="bg-gray-200">
            <th className="border p-2">Name</th>
            <th className="border p-2">Email</th>
            <th className="border p-2">Fuel Card</th>
            <th className="border p-2">Role</th>
            <th className="border p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u, i) => (
            <tr key={i} className="border">
              <td className="p-2">{u.name}</td>
              <td className="p-2">{u.email}</td>
              <td className="p-2">{u.fuel_card_no}</td>
              <td className="p-2">{u.role}</td>
              <td className="p-2 space-x-2">
                {u.role !== "admin" && (
                  <button
                    onClick={() => updateRole(u.email, "admin")}
                    className="bg-blue-500 text-white px-2 py-1 rounded"
                  >
                    Make Admin
                  </button>
                )}
                {u.role !== "employee" && (
                  <button
                    onClick={() => updateRole(u.email, "employee")}
                    className="bg-yellow-500 text-white px-2 py-1 rounded"
                  >
                    Make Employee
                  </button>
                )}
                <button
                  onClick={() => deleteUser(u.email)}
                  className="bg-red-600 text-white px-2 py-1 rounded"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminDashboard;
