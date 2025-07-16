import React, { useState } from 'react';
import './Login.css';
import API_BASE from '../api';

const Login = () => {
  const [isRegister, setIsRegister] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });

  const handleToggle = () => {
    setIsRegister(!isRegister);
    setFormData({ username: '', email: '', password: '' });
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
  e.preventDefault();

  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    const data = await res.json();

    if (res.ok) {
      localStorage.setItem("token", data.access_token);
      // Fetch user role if not returned, or store it
      navigate("/dashboard"); // or /admin
    } else {
      alert(data.detail || "Login failed");
    }
  } catch (err) {
    console.error("Login error:", err);
  }
};

  return (
    <div className="auth-container">
      <h2>{isRegister ? 'Register' : 'Login'}</h2>
      <form onSubmit={handleSubmit}>
        {isRegister && (
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        )}
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
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
        <button type="submit">{isRegister ? 'Sign Up' : 'Login'}</button>
      </form>
      <p onClick={handleToggle} className="toggle-link">
        {isRegister ? 'Already have an account? Login' : "Don't have an account? Register"}
      </p>
    </div>
  );
};

export default Login;
