import React, { useEffect, useState } from 'react';
import API_BASE from '../api';

const AdminUsers = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      const token = localStorage.getItem("token");

      const res = await fetch(`${API_BASE}/auth/users`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const data = await res.json();
      if (res.ok) {
        setUsers(data);
      } else {
        alert(data.detail || "Failed to fetch users");
      }
    };

    fetchUsers();
  }, []);

  return (
    <div>
      <h3>Registered Users</h3>
      <ul>
        {users.map(user => (
          <li key={user.id}>
            {user.username} ({user.email}) - {user.role}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AdminUsers;
