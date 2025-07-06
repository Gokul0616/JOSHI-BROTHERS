import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';

interface CartItem {
  product_id: string;
  quantity: number;
  product: {
    id: string;
    name: string;
    price: number;
    image_url: string;
    unit: string;
  };
}

interface CartContextType {
  cartItems: CartItem[];
  addToCart: (productId: string, quantity: number) => Promise<void>;
  removeFromCart: (productId: string) => Promise<void>;
  updateQuantity: (productId: string, quantity: number) => Promise<void>;
  getTotalPrice: () => number;
  getItemCount: () => number;
  refreshCart: () => Promise<void>;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const { isAuthenticated } = useAuth();
  const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  const refreshCart = async () => {
    if (!isAuthenticated) {
      setCartItems([]);
      return;
    }

    try {
      const response = await axios.get(`${API_URL}/api/cart`);
      setCartItems(response.data.cart_items);
    } catch (error) {
      console.error('Failed to fetch cart:', error);
    }
  };

  useEffect(() => {
    refreshCart();
  }, [isAuthenticated]);

  const addToCart = async (productId: string, quantity: number) => {
    try {
      await axios.post(`${API_URL}/api/cart/add`, {
        product_id: productId,
        quantity,
      });
      await refreshCart();
    } catch (error) {
      console.error('Failed to add to cart:', error);
      throw error;
    }
  };

  const removeFromCart = async (productId: string) => {
    try {
      await axios.delete(`${API_URL}/api/cart/${productId}`);
      await refreshCart();
    } catch (error) {
      console.error('Failed to remove from cart:', error);
      throw error;
    }
  };

  const updateQuantity = async (productId: string, quantity: number) => {
    if (quantity <= 0) {
      await removeFromCart(productId);
      return;
    }

    try {
      // Remove existing item and add with new quantity
      await axios.delete(`${API_URL}/api/cart/${productId}`);
      await axios.post(`${API_URL}/api/cart/add`, {
        product_id: productId,
        quantity,
      });
      await refreshCart();
    } catch (error) {
      console.error('Failed to update quantity:', error);
      throw error;
    }
  };

  const getTotalPrice = () => {
    return cartItems.reduce((total, item) => total + (item.product.price * item.quantity), 0);
  };

  const getItemCount = () => {
    return cartItems.reduce((count, item) => count + item.quantity, 0);
  };

  return (
    <CartContext.Provider value={{
      cartItems,
      addToCart,
      removeFromCart,
      updateQuantity,
      getTotalPrice,
      getItemCount,
      refreshCart
    }}>
      {children}
    </CartContext.Provider>
  );
};