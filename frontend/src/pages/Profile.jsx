import { useState, useEffect } from "react";
import API from "../services/api"; // your axios instance

function Profile() {
  const [profile, setProfile] = useState(null);
  const [form, setForm] = useState({ name: "", fuel_card_no: "" });

  // Load profile
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await API.get("/users/me");
        setProfile(res.data);
        setForm({
          name: res.data.name || "",
          fuel_card_no: res.data.fuel_card_no || "",
        });
      } catch (err) {
        console.error("Error fetching profile:", err.response?.data || err.message);
      }
    };
    fetchProfile();
  }, []);

  // Update profile
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await API.put("/users/me", form);
      alert("✅ Profile updated successfully");
    } catch (err) {
      alert(err.response?.data?.detail || "Update failed");
    }
  };

  if (!profile) return <p className="p-4">Loading profile...</p>;

  return (
    <div className="max-w-lg mx-auto p-6 bg-white rounded shadow">
      <h2 className="text-xl font-bold mb-4">My Profile</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          className="w-full border p-2 rounded"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          placeholder="Full Name"
        />
        <input
          type="email"
          className="w-full border p-2 rounded bg-gray-100"
          value={profile.email}
          disabled
        />
        <input
          type="text"
          className="w-full border p-2 rounded"
          value={form.fuel_card_no}
          onChange={(e) => setForm({ ...form, fuel_card_no: e.target.value })}
          placeholder="Fuel Card Number"
        />
        <button className="bg-green-600 text-white px-4 py-2 rounded">
          Save Changes
        </button>
      </form>
    </div>
  );
}

export default Profile;
