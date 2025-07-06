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
    <Link 
      to={`/products?category=${encodeURIComponent(category.name)}`}
      className="group"
    >
      <div className="bg-white rounded-lg shadow-sm hover:shadow-md transition-all duration-200 p-6 text-center border border-gray-100 group-hover:border-green-200">
        <div className="text-4xl mb-4 group-hover:scale-110 transition-transform duration-200">
          {category.icon}
        </div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-green-600 transition-colors">
          {category.name}
        </h3>
        <p className="text-gray-600 text-sm">
          {category.description}
        </p>
      </div>
    </Link>
  );
};

export default CategoryCard;