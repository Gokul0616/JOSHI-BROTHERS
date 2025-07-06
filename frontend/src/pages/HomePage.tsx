import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import ProductCard from '../components/ProductCard';
import CategoryCard from '../components/CategoryCard';
import BrandCard from '../components/BrandCard';
import { ArrowRight, CheckCircle, Truck, Users } from 'lucide-react';

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  image_url: string;
  unit: string;
  stock: number;
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

const HomePage: React.FC = () => {
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [brands, setBrands] = useState<Brand[]>([]);
  const [loading, setLoading] = useState(true);

  const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [productsRes, categoriesRes, brandsRes] = await Promise.all([
          axios.get(`${API_URL}/api/products`),
          axios.get(`${API_URL}/api/categories`),
          axios.get(`${API_URL}/api/brands`)
        ]);

        setFeaturedProducts(productsRes.data.products.slice(0, 8));
        setCategories(categoriesRes.data.categories);
        setBrands(brandsRes.data.brands.slice(0, 6));
      } catch (error) {
        console.error('Failed to fetch data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-red-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="hero-section text-white py-32">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-xl md:text-2xl font-medium mb-4">
            20+ categories • 2000+ products
          </h2>
          <h1 className="text-4xl md:text-6xl font-bold mb-8">
            All your restaurant needs delivered next day
          </h1>
          <Link
            to="/products"
            className="bg-red-600 text-white px-8 py-4 rounded-md text-lg font-semibold hover:bg-red-700 transition-colors inline-flex items-center space-x-2"
          >
            <span>Shop Now</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Why Choose Us Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">
            Why choose JOSHI BROTHERS?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Quality</h3>
              <p className="text-gray-600">Consistency</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Single Vendor</h3>
              <p className="text-gray-600">Marketplace</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Truck className="w-8 h-8 text-orange-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Next Day</h3>
              <p className="text-gray-600">Delivery</p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold text-gray-800">Featured Products</h2>
            <Link
              to="/products"
              className="text-red-600 hover:text-red-700 font-semibold flex items-center space-x-1"
            >
              <span>See All</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {featuredProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">
            Buy just about anything
          </h2>
          <p className="text-center text-gray-600 mb-12">20+ categories • 2000+ products</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {categories.map((category) => (
              <CategoryCard key={category.id} category={category} />
            ))}
          </div>
        </div>
      </section>

      {/* Brands */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">
            Choose from popular brands
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-6">
            {brands.map((brand) => (
              <BrandCard key={brand.id} brand={brand} />
            ))}
          </div>
          <div className="text-center mt-8">
            <Link
              to="/brands"
              className="text-red-600 hover:text-red-700 font-semibold flex items-center justify-center space-x-1"
            >
              <span>View All Brands</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">
            Stories from Partners
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-gray-50 p-6 rounded-lg">
              <p className="text-gray-700 mb-4">
                "Joshi Brothers is a Frozen Food Wholesaler in Junagadh. They have many products like Frozen French fries, cheese, butter, aloo tiki, frozen pizza, green peas, sweet corn, and all types of sauces, pasta, etc."
              </p>
            </div>
            <div className="bg-gray-50 p-6 rounded-lg">
              <p className="text-gray-700 mb-4">
                "They are a wholesale distributor of food products like chili sauce, tomato sauce, pizza sauce, cheese, butter, and bakery products, etc."
              </p>
            </div>
            <div className="bg-gray-50 p-6 rounded-lg">
              <p className="text-gray-700 mb-4">
                "I highly recommend Joshi Brothers for all your restaurant and FMCG Products needs in Junagadh. Wide range of goods available."
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;