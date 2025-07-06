import requests
import json

API_BASE = "http://localhost:8001/api"

# First, let's get admin token
admin_data = {
    "email": "admin@joshibrothers.com",
    "password": "Admin@123"
}

response = requests.post(f"{API_BASE}/admin/login", json=admin_data)
if response.status_code == 200:
    admin_token = response.json()["token"]
    headers = {"Authorization": f"Bearer {admin_token}"}
    print("Admin login successful!")
else:
    print("Admin login failed!")
    exit(1)

# Get current categories and brands
categories_response = requests.get(f"{API_BASE}/categories")
brands_response = requests.get(f"{API_BASE}/brands")

if categories_response.status_code == 200 and brands_response.status_code == 200:
    categories = categories_response.json()["categories"]
    brands = brands_response.json()["brands"]
    
    # Create mapping for easy access
    category_names = [cat["name"] for cat in categories]
    brand_names = [brand["name"] for brand in brands]
    
    print(f"Found {len(categories)} categories and {len(brands)} brands")
    
    # Additional sample products
    additional_products = [
        {
            "name": "Whole Wheat Bread",
            "description": "Fresh whole wheat bread loaf",
            "price": 55.0,
            "category": "Bakery Products",
            "brand": "Farm King",
            "image_url": "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=300&h=300&fit=crop",
            "stock": 45,
            "unit": "400g"
        },
        {
            "name": "Greek Yogurt",
            "description": "Creamy Greek yogurt with probiotics",
            "price": 95.0,
            "category": "Dairy",
            "brand": "Amul",
            "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=300&h=300&fit=crop",
            "stock": 65,
            "unit": "200g"
        },
        {
            "name": "Organic Spinach",
            "description": "Fresh organic spinach leaves",
            "price": 45.0,
            "category": "Fruits & Vegetables",
            "brand": "Farm King",
            "image_url": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=300&h=300&fit=crop",
            "stock": 90,
            "unit": "500g"
        },
        {
            "name": "Turmeric Powder",
            "description": "Pure turmeric powder for cooking",
            "price": 65.0,
            "category": "Spices & Seasonings",
            "brand": "Everest",
            "image_url": "https://images.unsplash.com/photo-1615485500704-8e990f9900f7?w=300&h=300&fit=crop",
            "stock": 80,
            "unit": "100g"
        },
        {
            "name": "Frozen Mixed Vegetables",
            "description": "Premium frozen mixed vegetables",
            "price": 120.0,
            "category": "Frozen Foods",
            "brand": "Farm King",
            "image_url": "https://images.unsplash.com/photo-1590779033100-9f60a05a013d?w=300&h=300&fit=crop",
            "stock": 35,
            "unit": "500g"
        },
        {
            "name": "Coconut Oil",
            "description": "Cold-pressed coconut oil",
            "price": 320.0,
            "category": "Oils & Vinegars",
            "brand": "Farm King",
            "image_url": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=300&h=300&fit=crop",
            "stock": 40,
            "unit": "500ml"
        },
        {
            "name": "Masala Chai",
            "description": "Premium masala chai blend",
            "price": 85.0,
            "category": "Beverages",
            "brand": "Everest",
            "image_url": "https://images.unsplash.com/photo-1597318045126-d7451c4c0b7f?w=300&h=300&fit=crop",
            "stock": 55,
            "unit": "200g"
        },
        {
            "name": "Almonds",
            "description": "Premium California almonds",
            "price": 680.0,
            "category": "Snacks & Sweets",
            "brand": "Farm King",
            "image_url": "https://images.unsplash.com/photo-1508061253366-f7da158b6d46?w=300&h=300&fit=crop",
            "stock": 25,
            "unit": "500g"
        },
        {
            "name": "Cheddar Cheese",
            "description": "Aged cheddar cheese slices",
            "price": 180.0,
            "category": "Dairy",
            "brand": "Amul",
            "image_url": "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=300&h=300&fit=crop",
            "stock": 30,
            "unit": "200g"
        },
        {
            "name": "Organic Carrots",
            "description": "Fresh organic carrots",
            "price": 70.0,
            "category": "Fruits & Vegetables",
            "brand": "Farm King",
            "image_url": "https://images.unsplash.com/photo-1445282768818-728615cc910a?w=300&h=300&fit=crop",
            "stock": 85,
            "unit": "1kg"
        },
        {
            "name": "Chili Powder",
            "description": "Authentic red chili powder",
            "price": 75.0,
            "category": "Spices & Seasonings",
            "brand": "MDH",
            "image_url": "https://images.unsplash.com/photo-1581484800704-06d81f2ccdc5?w=300&h=300&fit=crop",
            "stock": 70,
            "unit": "100g"
        },
        {
            "name": "Soy Sauce",
            "description": "Premium soy sauce for cooking",
            "price": 125.0,
            "category": "Sauces & Condiments",
            "brand": "Ching's Secret",
            "image_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop",
            "stock": 50,
            "unit": "200ml"
        },
        {
            "name": "Croissants",
            "description": "Butter croissants, pack of 4",
            "price": 140.0,
            "category": "Bakery Products",
            "brand": "Farm King",
            "image_url": "https://images.unsplash.com/photo-1555507036-ac018abc4084?w=300&h=300&fit=crop",
            "stock": 20,
            "unit": "4 pieces"
        },
        {
            "name": "Orange Juice",
            "description": "Fresh orange juice",
            "price": 95.0,
            "category": "Beverages",
            "brand": "Farm King",
            "image_url": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=300&h=300&fit=crop",
            "stock": 45,
            "unit": "1L"
        },
        {
            "name": "Cashews",
            "description": "Premium cashew nuts",
            "price": 750.0,
            "category": "Snacks & Sweets",
            "brand": "Farm King",
            "image_url": "https://images.unsplash.com/photo-1590944172983-25b0c7e9f4f8?w=300&h=300&fit=crop",
            "stock": 20,
            "unit": "500g"
        },
        {
            "name": "Quinoa",
            "description": "Organic quinoa seeds",
            "price": 350.0,
            "category": "Pulses & Grains",
            "brand": "Farm King",
            "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=300&h=300&fit=crop",
            "stock": 15,
            "unit": "500g"
        },
        {
            "name": "Mozzarella Cheese",
            "description": "Fresh mozzarella cheese",
            "price": 220.0,
            "category": "Dairy",
            "brand": "Amul",
            "image_url": "https://images.unsplash.com/photo-1628088062854-d1870b4553da?w=300&h=300&fit=crop",
            "stock": 25,
            "unit": "200g"
        },
        {
            "name": "Avocados",
            "description": "Ripe avocados, pack of 2",
            "price": 180.0,
            "category": "Fruits & Vegetables",
            "brand": "Farm King",
            "image_url": "https://images.unsplash.com/photo-1601039641847-7857b994d704?w=300&h=300&fit=crop",
            "stock": 40,
            "unit": "2 pieces"
        },
        {
            "name": "Pasta Sauce",
            "description": "Italian pasta sauce",
            "price": 165.0,
            "category": "Sauces & Condiments",
            "brand": "Knorr",
            "image_url": "https://images.unsplash.com/photo-1544627363-1476b5b8d346?w=300&h=300&fit=crop",
            "stock": 35,
            "unit": "350g"
        },
        {
            "name": "Dark Chocolate",
            "description": "Premium dark chocolate bar",
            "price": 145.0,
            "category": "Snacks & Sweets",
            "brand": "Nestlé",
            "image_url": "https://images.unsplash.com/photo-1511381939415-e44015466834?w=300&h=300&fit=crop",
            "stock": 60,
            "unit": "100g"
        }
    ]
    
    # Add products
    added_count = 0
    for product in additional_products:
        # Check if category and brand exist
        if product["category"] in category_names and product["brand"] in brand_names:
            response = requests.post(f"{API_BASE}/admin/products", json=product, headers=headers)
            if response.status_code == 200:
                added_count += 1
                print(f"Added: {product['name']}")
            else:
                print(f"Failed to add: {product['name']} - {response.status_code}")
        else:
            print(f"Skipped: {product['name']} - Category or Brand not found")
    
    print(f"\nSuccessfully added {added_count} products!")
    
    # Add a few more brands
    additional_brands = [
        {
            "name": "Organic Valley",
            "logo": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=100&h=100&fit=crop"
        },
        {
            "name": "Tata Salt",
            "logo": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=100&h=100&fit=crop"
        },
        {
            "name": "Kellogg's",
            "logo": "https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=100&h=100&fit=crop"
        }
    ]
    
    brand_added_count = 0
    for brand in additional_brands:
        if brand["name"] not in brand_names:
            response = requests.post(f"{API_BASE}/admin/brands", json=brand, headers=headers)
            if response.status_code == 200:
                brand_added_count += 1
                print(f"Added brand: {brand['name']}")
            else:
                print(f"Failed to add brand: {brand['name']} - {response.status_code}")
    
    print(f"\nSuccessfully added {brand_added_count} brands!")
    
else:
    print("Failed to get categories or brands")