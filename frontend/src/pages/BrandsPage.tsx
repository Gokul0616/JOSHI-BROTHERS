import React, { useState, useEffect } from 'react';
import BrandCard from '../components/BrandCard';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

interface Brand {
  id: string;
  name: string;
  logo: string;
}

const BrandsPage: React.FC = () => {
  const [brands, setBrands] = useState<Brand[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBrands();
  }, []);

  const fetchBrands = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${BACKEND_URL}/api/brands`);
      const data = await response.json();
      setBrands(data.brands || []);
    } catch (error) {
      console.error('Error fetching brands:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Our Brands</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Discover premium quality products from trusted brands that restaurants rely on
          </p>
        </div>

        {/* Brands Grid */}
        {loading ? (
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
            {[...Array(12)].map((_, i) => (
              <div key={i} className="bg-white rounded-lg shadow-sm p-4">
                <div className="aspect-square bg-gray-200 rounded animate-pulse mb-4"></div>
                <div className="bg-gray-200 h-4 rounded animate-pulse"></div>
              </div>
            ))}
          </div>
        ) : brands.length > 0 ? (
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
            {brands.map((brand) => (
              <BrandCard key={brand.id} brand={brand} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="text-gray-500 text-lg mb-4">No brands found</div>
            <p className="text-gray-400">Brands will appear here once they are added</p>
          </div>
        )}

        {/* Brand Benefits */}
        <div className="mt-16 bg-white rounded-lg shadow-sm p-8">
          <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">
            Why Choose Our Partner Brands?
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-green-100 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                <span className="text-2xl">🏆</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Quality Assured</h3>
              <p className="text-gray-600">
                All brands are carefully selected and verified for quality standards
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-green-100 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                <span className="text-2xl">🤝</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Trusted Partners</h3>
              <p className="text-gray-600">
                Long-standing relationships with brands that understand restaurant needs
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-green-100 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                <span className="text-2xl">💰</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Best Prices</h3>
              <p className="text-gray-600">
                Competitive wholesale pricing with special restaurant discounts
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BrandsPage;