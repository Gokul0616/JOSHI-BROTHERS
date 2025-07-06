#!/usr/bin/env python3
import requests
import json
import time
import os
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8001"
API_URL = f"{BASE_URL}/api"

# Test user data
TEST_USER = {
    "name": "Test User",
    "email": f"testuser_{int(time.time())}@example.com",
    "password": "Test@123",
    "phone": "9876543210",
    "address": "123 Test Street, Test City"
}

# Global variables to store test data
auth_token = None
user_id = None
product_id = None
cart_item_id = None
order_id = None
admin_token = None
created_product_id = None
created_category_id = None
created_brand_id = None

# ANSI colors for output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(message):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

def print_test(test_name):
    print(f"{Colors.OKBLUE}[TEST] {test_name}{Colors.ENDC}")

def print_success(message):
    print(f"{Colors.OKGREEN}[SUCCESS] {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.WARNING}[WARNING] {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}[ERROR] {message}{Colors.ENDC}")

def print_info(message):
    print(f"[INFO] {message}")

def test_server_health():
    print_test("Testing server health")
    try:
        response = requests.get(f"{BASE_URL}")
        if response.status_code == 404:
            # FastAPI returns 404 for root path if no root handler is defined
            print_success("Server is running")
            return True
        elif 200 <= response.status_code < 300:
            print_success("Server is running")
            return True
        else:
            print_error(f"Server returned unexpected status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error(f"Could not connect to server at {BASE_URL}")
        return False

def test_database_connection():
    print_test("Testing database connection through API endpoints")
    try:
        # We'll test database connection by checking if categories endpoint returns data
        response = requests.get(f"{API_URL}/categories")
        if response.status_code == 200:
            data = response.json()
            if "categories" in data and len(data["categories"]) > 0:
                print_success("Database connection successful - categories retrieved")
                return True
            else:
                print_warning("Database connection might be working but no categories found")
                return False
        else:
            print_error(f"Failed to retrieve categories: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error testing database connection: {str(e)}")
        return False

def test_sample_data():
    print_test("Testing sample data population")
    
    # Test categories
    response = requests.get(f"{API_URL}/categories")
    if response.status_code != 200:
        print_error(f"Failed to retrieve categories: {response.status_code}")
        return False
    
    categories = response.json().get("categories", [])
    if len(categories) < 6:
        print_error(f"Expected at least 6 categories, found {len(categories)}")
        return False
    
    category_names = [cat["name"] for cat in categories]
    expected_categories = ["Dairy", "Fruits & Vegetables", "Spices & Seasonings", 
                          "Frozen Foods", "Sauces & Condiments", "Bakery Products"]
    
    for cat in expected_categories:
        if cat not in category_names:
            print_error(f"Expected category '{cat}' not found")
            return False
    
    print_success("Categories verified successfully")
    
    # Test brands
    response = requests.get(f"{API_URL}/brands")
    if response.status_code != 200:
        print_error(f"Failed to retrieve brands: {response.status_code}")
        return False
    
    brands = response.json().get("brands", [])
    if len(brands) < 6:
        print_error(f"Expected at least 6 brands, found {len(brands)}")
        return False
    
    brand_names = [brand["name"] for brand in brands]
    expected_brands = ["Ching's Secret", "Everest", "Farm King", "Funfoods", "MDH", "Knorr"]
    
    for brand in expected_brands:
        if brand not in brand_names:
            print_error(f"Expected brand '{brand}' not found")
            return False
    
    print_success("Brands verified successfully")
    
    # Test products
    response = requests.get(f"{API_URL}/products")
    if response.status_code != 200:
        print_error(f"Failed to retrieve products: {response.status_code}")
        return False
    
    products = response.json().get("products", [])
    if len(products) < 6:
        print_error(f"Expected at least 6 products, found {len(products)}")
        return False
    
    product_names = [product["name"] for product in products]
    expected_products = ["Fresh Cream", "Milk Powder", "Cheese", "Butter", "Garam Masala", "Tomato Sauce"]
    
    for product in expected_products:
        if product not in product_names:
            print_error(f"Expected product '{product}' not found")
            return False
    
    # Store a product ID for later tests
    global product_id
    product_id = products[0]["id"]
    
    print_success("Products verified successfully")
    return True

def test_user_registration():
    print_test("Testing user registration")
    
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json=TEST_USER
        )
        
        if response.status_code == 200:
            data = response.json()
            if "token" in data and "user" in data:
                global auth_token, user_id
                auth_token = data["token"]
                user_id = data["user"]["id"]
                print_success(f"User registered successfully with ID: {user_id}")
                return True
            else:
                print_error("Registration response missing token or user data")
                return False
        else:
            print_error(f"Registration failed with status code {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error during registration: {str(e)}")
        return False

def test_user_login():
    print_test("Testing user login")
    
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            json={
                "email": TEST_USER["email"],
                "password": TEST_USER["password"]
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if "token" in data and "user" in data:
                global auth_token
                auth_token = data["token"]
                print_success("User logged in successfully")
                return True
            else:
                print_error("Login response missing token or user data")
                return False
        else:
            print_error(f"Login failed with status code {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error during login: {str(e)}")
        return False

def test_protected_route():
    print_test("Testing protected route access")
    
    # Test without token
    try:
        response = requests.get(f"{API_URL}/cart")
        if response.status_code == 401 or response.status_code == 403:
            print_success("Protected route correctly denied access without token")
        else:
            print_error(f"Protected route should return 401/403 without token, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error testing protected route without token: {str(e)}")
        return False
    
    # Test with token
    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(f"{API_URL}/cart", headers=headers)
        if response.status_code == 200:
            print_success("Protected route correctly allowed access with token")
            return True
        else:
            print_error(f"Protected route returned {response.status_code} with valid token")
            return False
    except Exception as e:
        print_error(f"Error testing protected route with token: {str(e)}")
        return False

def test_get_all_products():
    print_test("Testing GET /api/products (all products)")
    
    try:
        response = requests.get(f"{API_URL}/products")
        if response.status_code == 200:
            data = response.json()
            if "products" in data and len(data["products"]) > 0:
                print_success(f"Successfully retrieved {len(data['products'])} products")
                return True
            else:
                print_error("No products found in response")
                return False
        else:
            print_error(f"Failed to retrieve products: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error retrieving products: {str(e)}")
        return False

def test_get_products_by_category():
    print_test("Testing GET /api/products with category filter")
    
    try:
        # First get categories
        response = requests.get(f"{API_URL}/categories")
        if response.status_code != 200:
            print_error(f"Failed to retrieve categories: {response.status_code}")
            return False
        
        categories = response.json().get("categories", [])
        if not categories:
            print_error("No categories found")
            return False
        
        # Test with first category
        category = categories[0]["name"]
        response = requests.get(f"{API_URL}/products?category={category}")
        
        if response.status_code == 200:
            data = response.json()
            if "products" in data:
                products = data["products"]
                if len(products) > 0:
                    all_match = all(p["category"] == category for p in products)
                    if all_match:
                        print_success(f"Successfully filtered products by category '{category}'")
                        return True
                    else:
                        print_error(f"Some products don't match the category filter '{category}'")
                        return False
                else:
                    print_warning(f"No products found for category '{category}'")
                    return True  # This is not necessarily an error
            else:
                print_error("No products field in response")
                return False
        else:
            print_error(f"Failed to filter products by category: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error filtering products by category: {str(e)}")
        return False

def test_get_products_by_brand():
    print_test("Testing GET /api/products with brand filter")
    
    try:
        # First get brands
        response = requests.get(f"{API_URL}/brands")
        if response.status_code != 200:
            print_error(f"Failed to retrieve brands: {response.status_code}")
            return False
        
        brands = response.json().get("brands", [])
        if not brands:
            print_error("No brands found")
            return False
        
        # Test with first brand
        brand = brands[0]["name"]
        response = requests.get(f"{API_URL}/products?brand={brand}")
        
        if response.status_code == 200:
            data = response.json()
            if "products" in data:
                products = data["products"]
                if len(products) > 0:
                    all_match = all(p["brand"] == brand for p in products)
                    if all_match:
                        print_success(f"Successfully filtered products by brand '{brand}'")
                        return True
                    else:
                        print_error(f"Some products don't match the brand filter '{brand}'")
                        return False
                else:
                    print_warning(f"No products found for brand '{brand}'")
                    return True  # This is not necessarily an error
            else:
                print_error("No products field in response")
                return False
        else:
            print_error(f"Failed to filter products by brand: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error filtering products by brand: {str(e)}")
        return False

def test_get_product_by_id():
    print_test("Testing GET /api/products/{product_id}")
    
    global product_id
    if not product_id:
        # Get a product ID if we don't have one
        try:
            response = requests.get(f"{API_URL}/products")
            if response.status_code == 200:
                products = response.json().get("products", [])
                if products:
                    product_id = products[0]["id"]
                else:
                    print_error("No products found to test individual product retrieval")
                    return False
            else:
                print_error(f"Failed to retrieve products: {response.status_code}")
                return False
        except Exception as e:
            print_error(f"Error retrieving products: {str(e)}")
            return False
    
    try:
        response = requests.get(f"{API_URL}/products/{product_id}")
        if response.status_code == 200:
            product = response.json()
            if product and product["id"] == product_id:
                print_success(f"Successfully retrieved product with ID {product_id}")
                return True
            else:
                print_error("Retrieved product doesn't match requested ID")
                return False
        else:
            print_error(f"Failed to retrieve product by ID: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error retrieving product by ID: {str(e)}")
        return False

def test_get_categories():
    print_test("Testing GET /api/categories")
    
    try:
        response = requests.get(f"{API_URL}/categories")
        if response.status_code == 200:
            data = response.json()
            if "categories" in data and len(data["categories"]) > 0:
                print_success(f"Successfully retrieved {len(data['categories'])} categories")
                return True
            else:
                print_error("No categories found in response")
                return False
        else:
            print_error(f"Failed to retrieve categories: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error retrieving categories: {str(e)}")
        return False

def test_get_brands():
    print_test("Testing GET /api/brands")
    
    try:
        response = requests.get(f"{API_URL}/brands")
        if response.status_code == 200:
            data = response.json()
            if "brands" in data and len(data["brands"]) > 0:
                print_success(f"Successfully retrieved {len(data['brands'])} brands")
                return True
            else:
                print_error("No brands found in response")
                return False
        else:
            print_error(f"Failed to retrieve brands: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error retrieving brands: {str(e)}")
        return False

def test_add_to_cart():
    print_test("Testing POST /api/cart/add")
    
    global product_id, auth_token
    if not product_id or not auth_token:
        print_error("Missing product_id or auth_token for cart test")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        cart_item = {
            "product_id": product_id,
            "quantity": 2
        }
        
        response = requests.post(
            f"{API_URL}/cart/add",
            json=cart_item,
            headers=headers
        )
        
        if response.status_code == 200:
            print_success("Successfully added item to cart")
            return True
        else:
            print_error(f"Failed to add item to cart: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error adding item to cart: {str(e)}")
        return False

def test_get_cart():
    print_test("Testing GET /api/cart")
    
    global auth_token, product_id
    if not auth_token:
        print_error("Missing auth_token for cart test")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(f"{API_URL}/cart", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if "cart_items" in data:
                cart_items = data["cart_items"]
                if len(cart_items) > 0:
                    print_success(f"Successfully retrieved {len(cart_items)} cart items")
                    # Check if our added product is in the cart
                    found = False
                    for item in cart_items:
                        if item["product_id"] == product_id:
                            found = True
                            break
                    
                    if found:
                        print_success(f"Found previously added product in cart")
                        return True
                    else:
                        print_error(f"Added product not found in cart")
                        return False
                else:
                    print_error("Cart is empty")
                    return False
            else:
                print_error("No cart_items field in response")
                return False
        else:
            print_error(f"Failed to retrieve cart: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error retrieving cart: {str(e)}")
        return False

def test_remove_from_cart():
    print_test("Testing DELETE /api/cart/{product_id}")
    
    global auth_token, product_id
    if not auth_token or not product_id:
        print_error("Missing auth_token or product_id for cart test")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.delete(f"{API_URL}/cart/{product_id}", headers=headers)
        
        if response.status_code == 200:
            print_success("Successfully removed item from cart")
            
            # Verify item was removed
            response = requests.get(f"{API_URL}/cart", headers=headers)
            if response.status_code == 200:
                data = response.json()
                cart_items = data.get("cart_items", [])
                
                for item in cart_items:
                    if item["product_id"] == product_id:
                        print_error("Item still in cart after removal")
                        return False
                
                print_success("Verified item was removed from cart")
                return True
            else:
                print_error(f"Failed to verify cart after removal: {response.status_code}")
                return False
        else:
            print_error(f"Failed to remove item from cart: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error removing item from cart: {str(e)}")
        return False

def test_create_order():
    print_test("Testing POST /api/orders")
    
    global auth_token, product_id
    if not auth_token or not product_id:
        print_error("Missing auth_token or product_id for order test")
        return False
    
    # First add an item to the cart
    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        cart_item = {
            "product_id": product_id,
            "quantity": 3
        }
        
        response = requests.post(
            f"{API_URL}/cart/add",
            json=cart_item,
            headers=headers
        )
        
        if response.status_code != 200:
            print_error(f"Failed to add item to cart for order test: {response.status_code}")
            return False
        
        # Now create the order
        order_data = {
            "delivery_address": "123 Test Street, Test City"
        }
        
        response = requests.post(
            f"{API_URL}/orders",
            json=order_data,
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if "order_id" in data and "total_amount" in data:
                global order_id
                order_id = data["order_id"]
                print_success(f"Successfully created order with ID: {order_id}")
                
                # Verify cart is empty after order creation
                response = requests.get(f"{API_URL}/cart", headers=headers)
                if response.status_code == 200:
                    cart_data = response.json()
                    if len(cart_data.get("cart_items", [])) == 0:
                        print_success("Verified cart is empty after order creation")
                        return True
                    else:
                        print_error("Cart is not empty after order creation")
                        return False
                else:
                    print_error(f"Failed to verify cart after order creation: {response.status_code}")
                    return False
            else:
                print_error("Order response missing order_id or total_amount")
                return False
        else:
            print_error(f"Failed to create order: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error creating order: {str(e)}")
        return False

def test_get_orders():
    print_test("Testing GET /api/orders")
    
    global auth_token, order_id
    if not auth_token:
        print_error("Missing auth_token for orders test")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(f"{API_URL}/orders", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if "orders" in data:
                orders = data["orders"]
                if len(orders) > 0:
                    print_success(f"Successfully retrieved {len(orders)} orders")
                    
                    # Check if our created order is in the list
                    if order_id:
                        found = False
                        for order in orders:
                            if order["id"] == order_id:
                                found = True
                                break
                        
                        if found:
                            print_success(f"Found previously created order in order history")
                            return True
                        else:
                            print_error(f"Created order not found in order history")
                            return False
                    else:
                        print_success("Orders retrieved successfully")
                        return True
                else:
                    print_error("No orders found")
                    return False
            else:
                print_error("No orders field in response")
                return False
        else:
            print_error(f"Failed to retrieve orders: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error retrieving orders: {str(e)}")
        return False

def run_tests():
    print_header("JOSHI BROTHERS HYPERPURE BACKEND API TESTS")
    print(f"Testing API at: {API_URL}")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Dictionary to track test results
    results = {}
    
    # 1. Database and Server Health
    print_header("1. Database and Server Health Tests")
    results["server_health"] = test_server_health()
    results["database_connection"] = test_database_connection()
    results["sample_data"] = test_sample_data()
    
    # 2. Authentication Endpoints
    print_header("2. Authentication Endpoints Tests")
    results["user_registration"] = test_user_registration()
    results["user_login"] = test_user_login()
    results["protected_route"] = test_protected_route()
    
    # 3. Product Management
    print_header("3. Product Management Tests")
    results["get_all_products"] = test_get_all_products()
    results["get_products_by_category"] = test_get_products_by_category()
    results["get_products_by_brand"] = test_get_products_by_brand()
    results["get_product_by_id"] = test_get_product_by_id()
    results["get_categories"] = test_get_categories()
    results["get_brands"] = test_get_brands()
    
    # 4. Shopping Cart Functionality
    print_header("4. Shopping Cart Functionality Tests")
    results["add_to_cart"] = test_add_to_cart()
    results["get_cart"] = test_get_cart()
    results["remove_from_cart"] = test_remove_from_cart()
    
    # 5. Order Management
    print_header("5. Order Management Tests")
    results["create_order"] = test_create_order()
    results["get_orders"] = test_get_orders()
    
    # Print summary
    print_header("TEST SUMMARY")
    
    all_passed = True
    for test_name, result in results.items():
        status = f"{Colors.OKGREEN}PASS{Colors.ENDC}" if result else f"{Colors.FAIL}FAIL{Colors.ENDC}"
        print(f"{test_name.ljust(30)}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}All tests passed successfully!{Colors.ENDC}")
    else:
        print(f"\n{Colors.FAIL}{Colors.BOLD}Some tests failed. Please check the logs above for details.{Colors.ENDC}")
    
    return results

if __name__ == "__main__":
    run_tests()