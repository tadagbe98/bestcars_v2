import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Register({ onLogin }) {
  const [formData, setFormData] = useState({
    userName: '',
    firstName: '',
    lastName: '',
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await fetch('/djangoapp/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (data.status === 'Authenticated') {
        onLogin && onLogin(data.userName, data.firstName);
        navigate('/');
      } else if (data.error === 'Already Registered') {
        setError('Username already taken. Please choose another.');
      } else {
        setError(data.message || 'Registration failed.');
      }
    } catch {
      setError('Connection error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight:'80vh', display:'flex', alignItems:'center', justifyContent:'center', background:'#f4f6f9', padding:'40px 20px' }}>
      <div style={{ background:'#fff', borderRadius:'16px', padding:'48px', width:'100%', maxWidth:'480px', boxShadow:'0 8px 32px rgba(0,0,0,0.12)' }}>
        <div style={{ textAlign:'center', marginBottom:'32px' }}>
          <div style={{ fontSize:'3rem', marginBottom:'10px' }}>🚗</div>
          <h2 style={{ color:'#1a3c6e', fontWeight:700 }}>Create Account</h2>
          <p style={{ color:'#666', margin:'8px 0 0' }}>Join the Best Cars community</p>
        </div>

        {error && (
          <div style={{ background:'#f8d7da', color:'#721c24', padding:'12px', borderRadius:'8px', marginBottom:'20px', textAlign:'center' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {/* Username */}
          <div style={{ marginBottom:'16px' }}>
            <label style={{ display:'block', fontWeight:600, marginBottom:'6px' }}>Username *</label>
            <input
              type="text" name="userName"
              style={{ width:'100%', padding:'10px 14px', border:'1.5px solid #ddd', borderRadius:'8px', fontSize:'0.95rem', boxSizing:'border-box' }}
              placeholder="Choose a username"
              value={formData.userName}
              onChange={handleChange} required
            />
          </div>

          {/* First Name */}
          <div style={{ marginBottom:'16px' }}>
            <label style={{ display:'block', fontWeight:600, marginBottom:'6px' }}>First Name *</label>
            <input
              type="text" name="firstName"
              style={{ width:'100%', padding:'10px 14px', border:'1.5px solid #ddd', borderRadius:'8px', fontSize:'0.95rem', boxSizing:'border-box' }}
              placeholder="Enter your first name"
              value={formData.firstName}
              onChange={handleChange} required
            />
          </div>

          {/* Last Name */}
          <div style={{ marginBottom:'16px' }}>
            <label style={{ display:'block', fontWeight:600, marginBottom:'6px' }}>Last Name *</label>
            <input
              type="text" name="lastName"
              style={{ width:'100%', padding:'10px 14px', border:'1.5px solid #ddd', borderRadius:'8px', fontSize:'0.95rem', boxSizing:'border-box' }}
              placeholder="Enter your last name"
              value={formData.lastName}
              onChange={handleChange} required
            />
          </div>

          {/* Email */}
          <div style={{ marginBottom:'16px' }}>
            <label style={{ display:'block', fontWeight:600, marginBottom:'6px' }}>Email Address *</label>
            <input
              type="email" name="email"
              style={{ width:'100%', padding:'10px 14px', border:'1.5px solid #ddd', borderRadius:'8px', fontSize:'0.95rem', boxSizing:'border-box' }}
              placeholder="your@email.com"
              value={formData.email}
              onChange={handleChange} required
            />
          </div>

          {/* Password */}
          <div style={{ marginBottom:'24px' }}>
            <label style={{ display:'block', fontWeight:600, marginBottom:'6px' }}>Password *</label>
            <input
              type="password" name="password"
              style={{ width:'100%', padding:'10px 14px', border:'1.5px solid #ddd', borderRadius:'8px', fontSize:'0.95rem', boxSizing:'border-box' }}
              placeholder="At least 6 characters"
              value={formData.password}
              onChange={handleChange} required minLength={6}
            />
          </div>

          {/* Register Button */}
          <button
            type="submit"
            style={{ width:'100%', padding:'13px', background:'#1a3c6e', color:'#fff', border:'none', borderRadius:'8px', fontSize:'1rem', fontWeight:600, cursor:'pointer' }}
            disabled={loading}
          >
            {loading ? 'Creating Account...' : 'Register'}
          </button>
        </form>

        <p style={{ textAlign:'center', marginTop:'24px', color:'#666' }}>
          Already have an account?{' '}
          <Link to="/login" style={{ color:'#1a3c6e', fontWeight:600 }}>Sign in</Link>
        </p>
      </div>
    </div>
  );
}

export default Register;
