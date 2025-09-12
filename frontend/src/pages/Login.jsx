// Login.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';
import API_BASE from '../api';

const Login = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ username: '', password: '' });

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        username: formData.username,
        password: formData.password,
      }),
    });

    const data = await res.json();

    if (res.ok) {
      // Store token + role
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("role", data.role);

      // Redirect user based on role
      navigate(data.role === "admin" ? "/admin" : "/dashboard");
    } else {
      alert(data.detail || "Login failed");
    }
  } catch (err) {
    console.error("Login error:", err);
  }
};
  return (
    <div className="auth-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit">Login</button>
      </form>
      <p
        className="toggle-link"
        onClick={() => navigate('/register')}
        style={{ cursor: 'pointer', color: 'blue' }}
      >
        Don't have an account? Register
      </p>
    </div>
  );
};

export default Login;
