import React from 'react';
import AdminUsers from '../components/AdminUsers';
import AdminProducts from '../components/AdminProducts';

const Admin = () => {
  return (
    <div>
      <h2>Admin Dashboard</h2>
      <AdminUsers />
      <AdminProducts />
    </div>
  );
};

export default Admin;
