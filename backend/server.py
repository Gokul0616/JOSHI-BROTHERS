from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
from datetime import datetime, timedelta
import jwt
import bcrypt
from pymongo import MongoClient
from bson import ObjectId
import uuid
from contextlib import asynccontextmanager

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URL)
db = client.joshi_brothers_db

# Collections
users_collection = db.users
products_collection = db.products
orders_collection = db.orders
categories_collection = db.categories
brands_collection = db.brands
cart_collection = db.cart

# JWT Secret
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-here')

# Models
class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    phone: Optional[str] = None
    address: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class AdminLogin(BaseModel):
    email: str
    password: str

class Product(BaseModel):
    id: str
    name: str
    description: str
    price: float
    category: str
    brand: str
    image_url: str
    stock: int
    unit: str

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    brand: str
    image_url: str
    stock: int
    unit: str

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    image_url: Optional[str] = None
    stock: Optional[int] = None
    unit: Optional[str] = None

class CategoryCreate(BaseModel):
    name: str
    description: str
    icon: str

class BrandCreate(BaseModel):
    name: str
    logo: str

class OrderStatusUpdate(BaseModel):
    status: str
    
class CartItem(BaseModel):
    product_id: str
    quantity: int

class Order(BaseModel):
    id: str
    user_id: str
    items: List[Dict]
    total_amount: float
    status: str
    delivery_address: str
    order_date: datetime
    delivery_date: Optional[datetime] = None

# Security
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database with sample data
    await init_database()
    yield

app = FastAPI(title="Hyperpure API", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Admin Panel Route
@app.get("/admin", response_class=HTMLResponse)
@app.get("/admin/", response_class=HTMLResponse)
@app.get("/admin/{path:path}", response_class=HTMLResponse)
async def admin_panel(request: Request, path: str = ""):
    try:
        with open("admin_templates/index.html", "r") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Admin Panel Loading...</h1><p>Error: {str(e)}</p>", status_code=500)

# Initialize database with sample data
async def init_database():
    # Create admin user if it doesn't exist
    admin_email = "admin@joshibrothers.com"
    if not users_collection.find_one({"email": admin_email}):
        admin_password = bcrypt.hashpw("Admin@123".encode('utf-8'), bcrypt.gensalt())
        admin_user = {
            "id": str(uuid.uuid4()),
            "name": "Admin",
            "email": admin_email,
            "password": admin_password.decode('utf-8'),
            "phone": None,
            "address": None,
            "role": "admin",
            "created_at": datetime.utcnow()
        }
        users_collection.insert_one(admin_user)
        print(f"Admin user created: {admin_email} / Admin@123")
    
    # Create sample categories
    categories = [
        {"id": str(uuid.uuid4()), "name": "Dairy", "description": "Fresh dairy products", "icon": "🧈"},
        {"id": str(uuid.uuid4()), "name": "Fruits & Vegetables", "description": "Fresh produce", "icon": "🥦"},
        {"id": str(uuid.uuid4()), "name": "Spices & Seasonings", "description": "Authentic spices", "icon": "🌶️"},
        {"id": str(uuid.uuid4()), "name": "Frozen Foods", "description": "Frozen items", "icon": "🧊"},
        {"id": str(uuid.uuid4()), "name": "Sauces & Condiments", "description": "Flavor enhancers", "icon": "🍅"},
        {"id": str(uuid.uuid4()), "name": "Bakery Products", "description": "Fresh baked goods", "icon": "🍞"},
        {"id": str(uuid.uuid4()), "name": "Oils & Vinegars", "description": "Cooking oils and vinegars", "icon": "🫒"},
        {"id": str(uuid.uuid4()), "name": "Beverages", "description": "Drinks and beverages", "icon": "🥤"},
        {"id": str(uuid.uuid4()), "name": "Pulses & Grains", "description": "Lentils, rice, and grains", "icon": "🌾"},
        {"id": str(uuid.uuid4()), "name": "Snacks & Sweets", "description": "Ready-to-eat snacks", "icon": "🍪"},
    ]
    
    for category in categories:
        if not categories_collection.find_one({"name": category["name"]}):
            categories_collection.insert_one(category)
    
    # Create sample brands
    brands = [
        {"id": str(uuid.uuid4()), "name": "Ching's Secret", "logo": "https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=100&h=100&fit=crop"},
        {"id": str(uuid.uuid4()), "name": "Everest", "logo": "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=100&h=100&fit=crop"},
        {"id": str(uuid.uuid4()), "name": "Farm King", "logo": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=100&h=100&fit=crop"},
        {"id": str(uuid.uuid4()), "name": "Funfoods", "logo": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=100&h=100&fit=crop"},
        {"id": str(uuid.uuid4()), "name": "MDH", "logo": "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=100&h=100&fit=crop"},
        {"id": str(uuid.uuid4()), "name": "Knorr", "logo": "https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=100&h=100&fit=crop"},
        {"id": str(uuid.uuid4()), "name": "Nestlé", "logo": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=100&h=100&fit=crop"},
        {"id": str(uuid.uuid4()), "name": "Amul", "logo": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=100&h=100&fit=crop"},
    ]
    
    for brand in brands:
        if not brands_collection.find_one({"name": brand["name"]}):
            brands_collection.insert_one(brand)

    # Create sample products
    sample_products = [
        {
            "id": str(uuid.uuid4()),
            "name": "Fresh Cream",
            "description": "Premium quality fresh cream for cooking and baking",
            "price": 150.0,
            "category": "Dairy",
            "brand": "Amul",
            "image_url": "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=300&h=300&fit=crop",
            "stock": 50,
            "unit": "500ml"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Organic Tomatoes",
            "description": "Fresh organic tomatoes, farm-picked",
            "price": 80.0,
            "category": "Fruits & Vegetables",
            "brand": "Farm King",
            "image_url": "https://images.unsplash.com/photo-1546470427-e15c3b6b1e2c?w=300&h=300&fit=crop",
            "stock": 100,
            "unit": "1kg"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Garam Masala",
            "description": "Authentic garam masala spice blend",
            "price": 85.0,
            "category": "Spices & Seasonings",
            "brand": "MDH",
            "image_url": "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=300&h=300&fit=crop",
            "stock": 75,
            "unit": "100g"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Tomato Sauce",
            "description": "Rich tomato sauce for cooking",
            "price": 45.0,
            "category": "Sauces & Condiments",
            "brand": "Knorr",
            "image_url": "https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=300&h=300&fit=crop",
            "stock": 60,
            "unit": "200ml"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Paneer",
            "description": "Fresh cottage cheese",
            "price": 120.0,
            "category": "Dairy",
            "brand": "Amul",
            "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=300&h=300&fit=crop",
            "stock": 40,
            "unit": "200g"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Onions",
            "description": "Fresh red onions",
            "price": 60.0,
            "category": "Fruits & Vegetables",
            "brand": "Farm King",
            "image_url": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=300&h=300&fit=crop",
            "stock": 80,
            "unit": "1kg"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Basmati Rice",
            "description": "Premium aged basmati rice",
            "price": 200.0,
            "category": "Pulses & Grains",
            "brand": "Farm King",
            "image_url": "https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?w=300&h=300&fit=crop",
            "stock": 30,
            "unit": "1kg"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Olive Oil",
            "description": "Extra virgin olive oil",
            "price": 450.0,
            "category": "Oils & Vinegars",
            "brand": "Farm King",
            "image_url": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=300&h=300&fit=crop",
            "stock": 25,
            "unit": "500ml"
        }
    ]
    
    for product in sample_products:
        if not products_collection.find_one({"name": product["name"]}):
            products_collection.insert_one(product)

# Auth endpoints
@app.post("/api/auth/register")
async def register(user: UserRegister):
    # Check if user already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    # Create user
    user_data = {
        "id": str(uuid.uuid4()),
        "name": user.name,
        "email": user.email,
        "password": hashed_password.decode('utf-8'),
        "phone": user.phone,
        "address": user.address,
        "role": "user",
        "created_at": datetime.utcnow()
    }
    
    users_collection.insert_one(user_data)
    
    # Generate token
    token = jwt.encode({
        "user_id": user_data["id"],
        "email": user.email,
        "role": "user",
        "exp": datetime.utcnow() + timedelta(days=30)
    }, JWT_SECRET, algorithm='HS256')
    
    return {"token": token, "user": {"id": user_data["id"], "name": user.name, "email": user.email}}

@app.post("/api/auth/login")
async def login(user: UserLogin):
    # Find user
    db_user = users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not bcrypt.checkpw(user.password.encode('utf-8'), db_user["password"].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate token
    token = jwt.encode({
        "user_id": db_user["id"],
        "email": user.email,
        "role": db_user.get("role", "user"),
        "exp": datetime.utcnow() + timedelta(days=30)
    }, JWT_SECRET, algorithm='HS256')
    
    return {"token": token, "user": {"id": db_user["id"], "name": db_user["name"], "email": db_user["email"]}}

# Product endpoints
@app.get("/api/products")
async def get_products(category: Optional[str] = None, brand: Optional[str] = None):
    filter_criteria = {}
    if category:
        filter_criteria["category"] = category
    if brand:
        filter_criteria["brand"] = brand
    
    products = list(products_collection.find(filter_criteria, {"_id": 0}))
    return {"products": products}

@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    product = products_collection.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/api/categories")
async def get_categories():
    categories = list(categories_collection.find({}, {"_id": 0}))
    return {"categories": categories}

@app.get("/api/brands")
async def get_brands():
    brands = list(brands_collection.find({}, {"_id": 0}))
    return {"brands": brands}

# Cart endpoints
@app.post("/api/cart/add")
async def add_to_cart(item: CartItem, user_data: dict = Depends(verify_token)):
    user_id = user_data["user_id"]
    
    # Check if product exists
    product = products_collection.find_one({"id": item.product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if item already in cart
    existing_item = cart_collection.find_one({"user_id": user_id, "product_id": item.product_id})
    
    if existing_item:
        # Update quantity
        cart_collection.update_one(
            {"user_id": user_id, "product_id": item.product_id},
            {"$set": {"quantity": existing_item["quantity"] + item.quantity}}
        )
    else:
        # Add new item
        cart_collection.insert_one({
            "user_id": user_id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "added_at": datetime.utcnow()
        })
    
    return {"message": "Item added to cart"}

@app.get("/api/cart")
async def get_cart(user_data: dict = Depends(verify_token)):
    user_id = user_data["user_id"]
    
    # Get cart items
    cart_items = list(cart_collection.find({"user_id": user_id}, {"_id": 0}))
    
    # Populate with product details
    for item in cart_items:
        product = products_collection.find_one({"id": item["product_id"]}, {"_id": 0})
        if product:
            item["product"] = product
    
    return {"cart_items": cart_items}

@app.delete("/api/cart/{product_id}")
async def remove_from_cart(product_id: str, user_data: dict = Depends(verify_token)):
    user_id = user_data["user_id"]
    
    cart_collection.delete_one({"user_id": user_id, "product_id": product_id})
    return {"message": "Item removed from cart"}

# Order endpoints
@app.post("/api/orders")
async def create_order(order_data: dict, user_data: dict = Depends(verify_token)):
    user_id = user_data["user_id"]
    
    # Get cart items
    cart_items = list(cart_collection.find({"user_id": user_id}))
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Calculate total
    total_amount = 0
    order_items = []
    
    for item in cart_items:
        product = products_collection.find_one({"id": item["product_id"]})
        if product:
            item_total = product["price"] * item["quantity"]
            total_amount += item_total
            order_items.append({
                "product_id": item["product_id"],
                "product_name": product["name"],
                "quantity": item["quantity"],
                "price": product["price"],
                "total": item_total
            })
    
    # Create order
    order = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "items": order_items,
        "total_amount": total_amount,
        "status": "pending",
        "delivery_address": order_data.get("delivery_address", ""),
        "order_date": datetime.utcnow(),
        "delivery_date": None
    }
    
    orders_collection.insert_one(order)
    
    # Clear cart
    cart_collection.delete_many({"user_id": user_id})
    
    return {"order_id": order["id"], "total_amount": total_amount}

@app.get("/api/orders")
async def get_orders(user_data: dict = Depends(verify_token)):
    user_id = user_data["user_id"]
    
    orders = list(orders_collection.find({"user_id": user_id}, {"_id": 0}))
    return {"orders": orders}

# Admin endpoints
@app.post("/api/admin/login")
async def admin_login(admin: AdminLogin):
    # Find admin user
    db_user = users_collection.find_one({"email": admin.email, "role": "admin"})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    
    # Verify password
    if not bcrypt.checkpw(admin.password.encode('utf-8'), db_user["password"].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    
    # Generate token
    token = jwt.encode({
        "user_id": db_user["id"],
        "email": admin.email,
        "role": "admin",
        "exp": datetime.utcnow() + timedelta(days=7)
    }, JWT_SECRET, algorithm='HS256')
    
    return {"token": token, "admin": {"id": db_user["id"], "name": db_user["name"], "email": db_user["email"]}}

@app.get("/api/admin/dashboard")
async def admin_dashboard(admin_data: dict = Depends(verify_admin_token)):
    # Get statistics
    total_products = products_collection.count_documents({})
    total_categories = categories_collection.count_documents({})
    total_brands = brands_collection.count_documents({})
    total_users = users_collection.count_documents({"role": {"$ne": "admin"}})
    total_orders = orders_collection.count_documents({})
    
    # Get recent orders
    recent_orders = list(orders_collection.find({}, {"_id": 0}).sort("order_date", -1).limit(5))
    
    # Get order status distribution
    order_statuses = list(orders_collection.aggregate([
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]))
    
    return {
        "statistics": {
            "total_products": total_products,
            "total_categories": total_categories,
            "total_brands": total_brands,
            "total_users": total_users,
            "total_orders": total_orders
        },
        "recent_orders": recent_orders,
        "order_statuses": order_statuses
    }

# Product Management
@app.post("/api/admin/products")
async def create_product(product: ProductCreate, admin_data: dict = Depends(verify_admin_token)):
    product_data = product.dict()
    product_data["id"] = str(uuid.uuid4())
    
    products_collection.insert_one(product_data)
    return {"message": "Product created successfully", "product_id": product_data["id"]}

@app.put("/api/admin/products/{product_id}")
async def update_product(product_id: str, product: ProductUpdate, admin_data: dict = Depends(verify_admin_token)):
    update_data = {k: v for k, v in product.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = products_collection.update_one({"id": product_id}, {"$set": update_data})
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": "Product updated successfully"}

@app.delete("/api/admin/products/{product_id}")
async def delete_product(product_id: str, admin_data: dict = Depends(verify_admin_token)):
    result = products_collection.delete_one({"id": product_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": "Product deleted successfully"}

# Category Management
@app.post("/api/admin/categories")
async def create_category(category: CategoryCreate, admin_data: dict = Depends(verify_admin_token)):
    # Check if category already exists
    if categories_collection.find_one({"name": category.name}):
        raise HTTPException(status_code=400, detail="Category already exists")
    
    category_data = category.dict()
    category_data["id"] = str(uuid.uuid4())
    
    categories_collection.insert_one(category_data)
    return {"message": "Category created successfully", "category_id": category_data["id"]}

@app.put("/api/admin/categories/{category_id}")
async def update_category(category_id: str, category: CategoryCreate, admin_data: dict = Depends(verify_admin_token)):
    result = categories_collection.update_one({"id": category_id}, {"$set": category.dict()})
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return {"message": "Category updated successfully"}

@app.delete("/api/admin/categories/{category_id}")
async def delete_category(category_id: str, admin_data: dict = Depends(verify_admin_token)):
    # Check if category is being used by any products
    category_name = categories_collection.find_one({"id": category_id})
    if category_name and products_collection.find_one({"category": category_name["name"]}):
        raise HTTPException(status_code=400, detail="Cannot delete category that is being used by products")
    
    result = categories_collection.delete_one({"id": category_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return {"message": "Category deleted successfully"}

# Brand Management
@app.post("/api/admin/brands")
async def create_brand(brand: BrandCreate, admin_data: dict = Depends(verify_admin_token)):
    # Check if brand already exists
    if brands_collection.find_one({"name": brand.name}):
        raise HTTPException(status_code=400, detail="Brand already exists")
    
    brand_data = brand.dict()
    brand_data["id"] = str(uuid.uuid4())
    
    brands_collection.insert_one(brand_data)
    return {"message": "Brand created successfully", "brand_id": brand_data["id"]}

@app.put("/api/admin/brands/{brand_id}")
async def update_brand(brand_id: str, brand: BrandCreate, admin_data: dict = Depends(verify_admin_token)):
    result = brands_collection.update_one({"id": brand_id}, {"$set": brand.dict()})
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    return {"message": "Brand updated successfully"}

@app.delete("/api/admin/brands/{brand_id}")
async def delete_brand(brand_id: str, admin_data: dict = Depends(verify_admin_token)):
    # Check if brand is being used by any products
    brand_name = brands_collection.find_one({"id": brand_id})
    if brand_name and products_collection.find_one({"brand": brand_name["name"]}):
        raise HTTPException(status_code=400, detail="Cannot delete brand that is being used by products")
    
    result = brands_collection.delete_one({"id": brand_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    return {"message": "Brand deleted successfully"}

# Order Management
@app.get("/api/admin/orders")
async def get_all_orders(admin_data: dict = Depends(verify_admin_token)):
    orders = list(orders_collection.find({}, {"_id": 0}).sort("order_date", -1))
    
    # Get user details for each order
    for order in orders:
        user = users_collection.find_one({"id": order["user_id"]}, {"_id": 0, "password": 0})
        if user:
            order["user_details"] = user
    
    return {"orders": orders}

@app.put("/api/admin/orders/{order_id}/status")
async def update_order_status(order_id: str, status_update: OrderStatusUpdate, admin_data: dict = Depends(verify_admin_token)):
    result = orders_collection.update_one(
        {"id": order_id}, 
        {"$set": {"status": status_update.status}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {"message": "Order status updated successfully"}

# User Management
@app.get("/api/admin/users")
async def get_all_users(admin_data: dict = Depends(verify_admin_token)):
    users = list(users_collection.find({"role": {"$ne": "admin"}}, {"_id": 0, "password": 0}))
    return {"users": users}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)