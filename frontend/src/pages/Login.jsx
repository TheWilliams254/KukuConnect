import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';
import API_BASE from '../api';

const Login = () => {
  const navigate = useNavigate();
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
    const url = isRegister ? `${API_BASE}/auth/register` : `${API_BASE}/auth/login`;

    const payload = isRegister
      ? formData
      : { username: formData.username, password: formData.password };
    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (res.ok) {
        if (!isRegister) {
          localStorage.setItem('token', data.access_token);
          navigate('/dashboard'); // or use role to redirect conditionally
        } else {
          alert('Registration successful. Please log in.');
          setIsRegister(false);
        }
      } else {
        alert(data.detail || 'Something went wrong');
      }
    } catch (err) {
      console.error('Auth error:', err);
      alert('Server error');
    }
  };

  return (
    <div className="auth-container">
      <h2>{isRegister ? 'Register' : 'Login'}</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          required
        />
        {isRegister && (
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        )}
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
        {isRegister
          ? 'Already have an account? Login'
          : "Don't have an account? Register"}
      </p>
    </div>
  );
};

export default Login;
