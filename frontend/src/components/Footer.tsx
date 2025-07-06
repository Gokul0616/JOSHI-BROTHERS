import React from 'react';
import { Link } from 'react-router-dom';

const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-gray-200">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div>
            <h4 className="text-gray-800 font-semibold mb-4">Company</h4>
            <p className="text-gray-600 font-medium">JOSHI BROTHERS</p>
            <p className="text-gray-500 text-sm mt-2">
              5,Shrinathji Chembers, Danapith Junagadh, Gujarat - India
            </p>
            <p className="text-gray-600 mt-2">mananjoshi232@gmail.com</p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-gray-800 font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-gray-600 hover:text-red-600 transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/products" className="text-gray-600 hover:text-red-600 transition-colors">
                  Products
                </Link>
              </li>
              <li>
                <Link to="/brands" className="text-gray-600 hover:text-red-600 transition-colors">
                  Brands
                </Link>
              </li>
              <li>
                <Link to="/about" className="text-gray-600 hover:text-red-600 transition-colors">
                  About Us
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-gray-600 hover:text-red-600 transition-colors">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* Social Links */}
          <div>
            <h4 className="text-gray-800 font-semibold mb-4">Follow us on</h4>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-gray-600 hover:text-red-600 transition-colors">
                  LinkedIn
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-600 hover:text-red-600 transition-colors">
                  YouTube
                </a>
              </li>
            </ul>
          </div>

          {/* Logo */}
          <div className="flex justify-center md:justify-start">
            <img 
              src="/assets/logo.png" 
              alt="Joshi Brothers Logo" 
              className="w-24 h-24"
            />
          </div>
        </div>

        <div className="border-t border-gray-200 mt-8 pt-6 text-center">
          <p className="text-gray-500 text-sm">
            © copyright 2024 JOSHI BROTHERS All Rights Reserved
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;