import React from 'react';
import { Link } from 'react-router-dom';

interface Category {
  id: string;
  name: string;
  description: string;
  icon: string;
}

interface CategoryCardProps {
  category: Category;
}

const CategoryCard: React.FC<CategoryCardProps> = ({ category }) => {
  return (
    <Link to={`/products?category=${encodeURIComponent(category.name)}`}>
      <div className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-all duration-300 text-center category-card">
        <div className="text-4xl mb-4">{category.icon}</div>
        <h3 className="text-lg font-semibold text-gray-800 mb-2">{category.name}</h3>
        <p className="text-gray-600 text-sm">{category.description}</p>
      </div>
    </Link>
  );
};

export default CategoryCard;