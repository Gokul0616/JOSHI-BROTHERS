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
    <Link 
      to={`/products?brand=${encodeURIComponent(brand.name)}`}
      className="group"
    >
      <div className="bg-white rounded-lg shadow-sm hover:shadow-md transition-all duration-200 p-4 border border-gray-100 group-hover:border-green-200">
        <div className="aspect-square flex items-center justify-center p-4">
          <img
            src={brand.logo}
            alt={brand.name}
            className="max-w-full max-h-full object-contain group-hover:scale-105 transition-transform duration-200"
          />
        </div>
        <h3 className="text-center text-sm font-semibold text-gray-900 mt-2 group-hover:text-green-600 transition-colors">
          {brand.name}
        </h3>
      </div>
    </Link>
  );
};

export default BrandCard;