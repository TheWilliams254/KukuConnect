import React from 'react';
import "./Products.css";
const dummyProducts = [
  { id: 1, name: 'Day-old Chicks', price: 'KES 100', description: 'Healthy and vaccinated.' },
  { id: 2, name: 'Broiler Chicken', price: 'KES 450', description: 'Ready for meat production.' },
  { id: 3, name: 'Chicken Feed (50kg)', price: 'KES 3,200', description: 'Premium quality feed.' },
];

const Products = () => {
  return (
    <div className="products-page">
      <h2>Our Products</h2>
      <div className="products-list">
        {dummyProducts.map(product => (
          <div className="product-card" key={product.id}>
            <h3>{product.name}</h3>
            <p>{product.description}</p>
            <strong>{product.price}</strong>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Products;
