import React from 'react';
import { Link } from 'react-router-dom';

interface Brand {
  id: string;
  name: string;
  logo: string;
}

interface BrandCardProps {
  brand: Brand;
}

const BrandCard: React.FC<BrandCardProps> = ({ brand }) => {
  return (
    <Link to={`/products?brand=${encodeURIComponent(brand.name)}`}>
      <div className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-all duration-300 text-center brand-hover">
        <img
          src={brand.logo}
          alt={brand.name}
          className="w-20 h-20 mx-auto mb-4 object-contain"
        />
        <h3 className="text-lg font-semibold text-gray-800">{brand.name}</h3>
      </div>
    </Link>
  );
};

export default BrandCard;