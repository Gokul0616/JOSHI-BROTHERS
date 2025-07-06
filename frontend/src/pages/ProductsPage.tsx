import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Filter, Grid, List } from 'lucide-react';
import ProductCard from '../components/ProductCard';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  brand: string;
  image_url: string;
  stock: number;
  unit: string;
}

interface Category {
  id: string;
  name: string;
  description: string;
  icon: string;
}

interface Brand {
  id: string;
  name: string;
  logo: string;
}

const ProductsPage: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [brands, setBrands] = useState<Brand[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [selectedBrand, setSelectedBrand] = useState<string>('');
  const [searchParams, setSearchParams] = useSearchParams();

  useEffect(() => {
    fetchData();
    // Set initial filters from URL params
    const category = searchParams.get('category');
    const brand = searchParams.get('brand');
    if (category) setSelectedCategory(category);
    if (brand) setSelectedBrand(brand);
  }, [searchParams]);

  useEffect(() => {
    fetchProducts();
  }, [selectedCategory, selectedBrand]);

  const fetchData = async () => {
    try {
      const [categoriesRes, brandsRes] = await Promise.all([
        fetch(`${BACKEND_URL}/api/categories`),
        fetch(`${BACKEND_URL}/api/brands`)
      ]);

      const categoriesData = await categoriesRes.json();
      const brandsData = await brandsRes.json();

      setCategories(categoriesData.categories || []);
      setBrands(brandsData.brands || []);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const fetchProducts = async () => {
    try {
      setLoading(true);
      let url = `${BACKEND_URL}/api/products`;
      const params = new URLSearchParams();
      
      if (selectedCategory) params.append('category', selectedCategory);
      if (selectedBrand) params.append('brand', selectedBrand);
      
      if (params.toString()) {
        url += `?${params.toString()}`;
      }

      const response = await fetch(url);
      const data = await response.json();
      setProducts(data.products || []);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCategoryChange = (category: string) => {
    setSelectedCategory(category);
    updateUrlParams({ category, brand: selectedBrand });
  };

  const handleBrandChange = (brand: string) => {
    setSelectedBrand(brand);
    updateUrlParams({ category: selectedCategory, brand });
  };

  const updateUrlParams = (params: { category: string; brand: string }) => {
    const newSearchParams = new URLSearchParams();
    if (params.category) newSearchParams.set('category', params.category);
    if (params.brand) newSearchParams.set('brand', params.brand);
    setSearchParams(newSearchParams);
  };

  const clearFilters = () => {
    setSelectedCategory('');
    setSelectedBrand('');
    setSearchParams(new URLSearchParams());
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Products</h1>
            <p className="text-gray-600 mt-2">
              {products.length} product{products.length !== 1 ? 's' : ''} found
            </p>
          </div>
        </div>

        <div className="lg:grid lg:grid-cols-4 lg:gap-8">
          {/* Filters Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
                {(selectedCategory || selectedBrand) && (
                  <button
                    onClick={clearFilters}
                    className="text-sm text-green-600 hover:text-green-700"
                  >
                    Clear all
                  </button>
                )}
              </div>

              {/* Categories */}
              <div className="mb-6">
                <h4 className="text-md font-medium text-gray-700 mb-3">Categories</h4>
                <div className="space-y-2">
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="category"
                      value=""
                      checked={selectedCategory === ''}
                      onChange={(e) => handleCategoryChange(e.target.value)}
                      className="text-green-600 focus:ring-green-500"
                    />
                    <span className="ml-2 text-sm text-gray-600">All Categories</span>
                  </label>
                  {categories.map((category) => (
                    <label key={category.id} className="flex items-center">
                      <input
                        type="radio"
                        name="category"
                        value={category.name}
                        checked={selectedCategory === category.name}
                        onChange={(e) => handleCategoryChange(e.target.value)}
                        className="text-green-600 focus:ring-green-500"
                      />
                      <span className="ml-2 text-sm text-gray-600">
                        {category.icon} {category.name}
                      </span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Brands */}
              <div>
                <h4 className="text-md font-medium text-gray-700 mb-3">Brands</h4>
                <div className="space-y-2">
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="brand"
                      value=""
                      checked={selectedBrand === ''}
                      onChange={(e) => handleBrandChange(e.target.value)}
                      className="text-green-600 focus:ring-green-500"
                    />
                    <span className="ml-2 text-sm text-gray-600">All Brands</span>
                  </label>
                  {brands.map((brand) => (
                    <label key={brand.id} className="flex items-center">
                      <input
                        type="radio"
                        name="brand"
                        value={brand.name}
                        checked={selectedBrand === brand.name}
                        onChange={(e) => handleBrandChange(e.target.value)}
                        className="text-green-600 focus:ring-green-500"
                      />
                      <span className="ml-2 text-sm text-gray-600">{brand.name}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Products Grid */}
          <div className="lg:col-span-3">
            {loading ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="bg-white rounded-lg p-4 shadow-sm">
                    <div className="bg-gray-200 rounded-lg h-48 mb-4 animate-pulse"></div>
                    <div className="space-y-2">
                      <div className="bg-gray-200 h-4 rounded animate-pulse"></div>
                      <div className="bg-gray-200 h-4 rounded animate-pulse"></div>
                      <div className="bg-gray-200 h-6 rounded animate-pulse"></div>
                    </div>
                  </div>
                ))}
              </div>
            ) : products.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {products.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="text-gray-500 text-lg mb-4">No products found</div>
                <p className="text-gray-400">Try adjusting your filters or search terms</p>
                {(selectedCategory || selectedBrand) && (
                  <button
                    onClick={clearFilters}
                    className="mt-4 bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700"
                  >
                    Clear filters
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductsPage;