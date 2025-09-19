# -------------------------------
# Restaurant Order & Billing App 🍔
 
# Display menu items with prices.
 
# User selects items + quantity.
 
# Generate a bill summary (subtotal + tax + total).
 
# Option to download invoice as CSV/PDF.
# -------------------------------


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import io
import base64
import re
from typing import Dict, List, Any, Optional
import json

# Configure page settings
st.set_page_config(
    page_title="Delicious Bites Restaurant 🍔",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern restaurant UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    .main-title {
        font-family: 'Poppins', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 50%, #ff9ff3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .restaurant-header {
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
    }
    
    .menu-category {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 600;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .menu-item-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        border: 2px solid #e0e6ff;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
    }
    
    .menu-item-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    
    .price-tag {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1.1rem;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    .cart-summary {
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
    }
    
    .bill-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .total-amount {
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin: 1rem 0;
        color: #ff6b6b;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .order-success {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        animation: fadeInUp 0.8s ease;
        box-shadow: 0 10px 30px rgba(17, 153, 142, 0.3);
    }
    
    .quantity-controls {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .quantity-btn {
        background: #667eea;
        color: white;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        font-size: 1.2rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .quantity-btn:hover {
        background: #5a6fd8;
        transform: scale(1.1);
    }
    
    .quantity-display {
        font-size: 1.5rem;
        font-weight: 600;
        min-width: 60px;
        text-align: center;
        background: #f8f9ff;
        padding: 0.5rem;
        border-radius: 10px;
        border: 2px solid #e0e6ff;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(250, 112, 154, 0.3);
    }
    
    .customer-info-card {
        background: linear-gradient(135deg, #2196f3 0%, #21cbf3 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(33, 150, 243, 0.3);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .stSelectbox > div > div {
        background: #f8f9ff;
        border-radius: 10px;
        border: 2px solid #e0e6ff;
    }
    
    .stTextInput > div > div > input {
        background: #f8f9ff;
        border-radius: 10px;
        border: 2px solid #e0e6ff;
    }
    
    .stNumberInput > div > div > input {
        background: #f8f9ff;
        border-radius: 10px;
        border: 2px solid #e0e6ff;
    }
</style>
""", unsafe_allow_html=True)

# Restaurant Menu Configuration
MENU_DATA = {
    "🍔 Burgers & Sandwiches": {
        "Classic Cheeseburger": {"price": 12.99, "description": "Juicy beef patty with cheese, lettuce, tomato, and our special sauce", "category": "burgers", "emoji": "🍔", "popular": True},
        "BBQ Bacon Burger": {"price": 15.99, "description": "Double beef patty with BBQ sauce, crispy bacon, and onion rings", "category": "burgers", "emoji": "🥓", "popular": True},
        "Veggie Deluxe Burger": {"price": 11.99, "description": "Plant-based patty with avocado, sprouts, and herb mayo", "category": "burgers", "emoji": "🥬", "popular": False},
        "Chicken Club Sandwich": {"price": 13.99, "description": "Grilled chicken breast with bacon, lettuce, tomato, and mayo", "category": "sandwiches", "emoji": "🥪", "popular": False},
        "Fish Fillet Burger": {"price": 14.99, "description": "Crispy fish fillet with tartar sauce and fresh lettuce", "category": "burgers", "emoji": "🐟", "popular": False},
        "Pulled Pork Sandwich": {"price": 16.99, "description": "Slow-cooked pulled pork with coleslaw and BBQ sauce", "category": "sandwiches", "emoji": "🐷", "popular": True}
    },
    "🍕 Pizza & Pasta": {
        "Margherita Pizza": {"price": 18.99, "description": "Fresh mozzarella, basil, and tomato sauce on thin crust", "category": "pizza", "emoji": "🍕", "popular": True},
        "Pepperoni Supreme": {"price": 22.99, "description": "Pepperoni, mushrooms, bell peppers, and extra cheese", "category": "pizza", "emoji": "🍕", "popular": True},
        "Meat Lovers Pizza": {"price": 25.99, "description": "Pepperoni, sausage, bacon, and ham with cheese", "category": "pizza", "emoji": "🍕", "popular": False},
        "Spaghetti Carbonara": {"price": 16.99, "description": "Creamy pasta with bacon, eggs, and parmesan cheese", "category": "pasta", "emoji": "🍝", "popular": True},
        "Chicken Alfredo": {"price": 19.99, "description": "Grilled chicken breast over fettuccine with alfredo sauce", "category": "pasta", "emoji": "🍝", "popular": False},
        "Vegetarian Pasta": {"price": 15.99, "description": "Penne pasta with seasonal vegetables in marinara sauce", "category": "pasta", "emoji": "🍝", "popular": False}
    },
    "🥗 Salads & Appetizers": {
        "Caesar Salad": {"price": 9.99, "description": "Crispy romaine lettuce with caesar dressing and croutons", "category": "salads", "emoji": "🥗", "popular": True},
        "Garden Fresh Salad": {"price": 8.99, "description": "Mixed greens with cherry tomatoes, cucumbers, and balsamic", "category": "salads", "emoji": "🥗", "popular": False},
        "Buffalo Wings": {"price": 11.99, "description": "Spicy chicken wings served with ranch dip", "category": "appetizers", "emoji": "🍗", "popular": True},
        "Mozzarella Sticks": {"price": 8.99, "description": "Crispy breaded mozzarella with marinara sauce", "category": "appetizers", "emoji": "🧀", "popular": True},
        "Loaded Nachos": {"price": 12.99, "description": "Tortilla chips with cheese, jalapeños, sour cream, and guacamole", "category": "appetizers", "emoji": "🌶️", "popular": False},
        "Onion Rings": {"price": 6.99, "description": "Golden crispy onion rings with special dipping sauce", "category": "appetizers", "emoji": "🧅", "popular": False}
    },
    "🥤 Beverages & Desserts": {
        "Fresh Juice": {"price": 4.99, "description": "Choice of orange, apple, or mixed berry juice", "category": "beverages", "emoji": "🧃", "popular": False},
        "Soft Drinks": {"price": 2.99, "description": "Coca-Cola, Pepsi, Sprite, or other sodas", "category": "beverages", "emoji": "🥤", "popular": True},
        "Coffee": {"price": 3.99, "description": "Freshly brewed coffee or espresso", "category": "beverages", "emoji": "☕", "popular": True},
        "Milkshake": {"price": 6.99, "description": "Vanilla, chocolate, or strawberry milkshake", "category": "beverages", "emoji": "🥤", "popular": True},
        "Chocolate Cake": {"price": 7.99, "description": "Rich chocolate cake with chocolate ganache", "category": "desserts", "emoji": "🍰", "popular": True},
        "Ice Cream Sundae": {"price": 5.99, "description": "Vanilla ice cream with your choice of toppings", "category": "desserts", "emoji": "🍨", "popular": False},
        "Cheesecake": {"price": 8.99, "description": "New York style cheesecake with berry compote", "category": "desserts", "emoji": "🍰", "popular": False}
    }
}

class OrderValidator:
    @staticmethod
    def validate_customer_name(name: str) -> Dict[str, Any]:
        """Validate customer name"""
        name = name.strip()
        if not name:
            return {"is_valid": False, "message": "❌ Customer name is required!"}
        if len(name) < 2:
            return {"is_valid": False, "message": "❌ Name must be at least 2 characters!"}
        if len(name) > 50:
            return {"is_valid": False, "message": "❌ Name must be less than 50 characters!"}
        if not re.match(r'^[a-zA-Z\s\'-]+$', name):
            return {"is_valid": False, "message": "❌ Name can only contain letters, spaces, hyphens, and apostrophes!"}
        return {"is_valid": True, "message": "✅ Valid name!"}
    
    @staticmethod
    def validate_phone(phone: str) -> Dict[str, Any]:
        """Validate phone number"""
        if not phone.strip():
            return {"is_valid": False, "message": "❌ Phone number is required!"}
        
        numeric_phone = re.sub(r'[^\d]', '', phone)
        if len(numeric_phone) < 10 or len(numeric_phone) > 15:
            return {"is_valid": False, "message": "❌ Phone number must be 10-15 digits!"}
        return {"is_valid": True, "message": "✅ Valid phone number!"}
    
    @staticmethod
    def validate_table_number(table_num: int) -> Dict[str, Any]:
        """Validate table number"""
        if table_num <= 0 or table_num > 50:
            return {"is_valid": False, "message": "❌ Table number must be between 1 and 50!"}
        return {"is_valid": True, "message": "✅ Valid table number!"}
    
    @staticmethod
    def validate_order_items(order_items: Dict) -> Dict[str, Any]:
        """Validate order items"""
        if not order_items:
            return {"is_valid": False, "message": "❌ Please add at least one item to your order!"}
        
        total_items = sum(item_data['quantity'] for item_data in order_items.values())
        if total_items > 50:
            return {"is_valid": False, "message": "❌ Maximum 50 items per order!"}
        
        return {"is_valid": True, "message": "✅ Valid order!"}

class RestaurantBilling:
    def __init__(self):
        self.tax_rate = 0.08  # 8% tax
        self.service_charge_rate = 0.10  # 10% service charge
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        default_values = {
            'cart': {},
            'customer_info': {},
            'orders_history': [],
            'current_order_id': None,
            'order_placed': False,
            'daily_stats': {'total_orders': 0, 'total_revenue': 0.0, 'popular_items': {}}
        }
        
        for key, value in default_values.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def add_to_cart(self, item_name: str, category: str, quantity: int = 1):
        """Add item to cart"""
        if item_name not in st.session_state.cart:
            st.session_state.cart[item_name] = {
                'quantity': 0,
                'price': self.get_item_price(item_name),
                'category': category
            }
        st.session_state.cart[item_name]['quantity'] += quantity
        
        if st.session_state.cart[item_name]['quantity'] <= 0:
            del st.session_state.cart[item_name]
    
    def update_cart_quantity(self, item_name: str, quantity: int):
        """Update item quantity in cart"""
        if quantity <= 0:
            if item_name in st.session_state.cart:
                del st.session_state.cart[item_name]
        else:
            if item_name in st.session_state.cart:
                st.session_state.cart[item_name]['quantity'] = quantity
    
    def get_item_price(self, item_name: str) -> float:
        """Get price of an item"""
        for category_items in MENU_DATA.values():
            if item_name in category_items:
                return category_items[item_name]['price']
        return 0.0
    
    def calculate_bill(self) -> Dict[str, float]:
        """Calculate complete bill breakdown"""
        subtotal = sum(
            item_data['price'] * item_data['quantity'] 
            for item_data in st.session_state.cart.values()
        )
        
        tax_amount = subtotal * self.tax_rate
        service_charge = subtotal * self.service_charge_rate
        total_amount = subtotal + tax_amount + service_charge
        
        return {
            'subtotal': subtotal,
            'tax_amount': tax_amount,
            'service_charge': service_charge,
            'total_amount': total_amount,
            'tax_rate': self.tax_rate,
            'service_rate': self.service_charge_rate
        }
    
    def place_order(self, customer_info: Dict) -> str:
        """Place order and generate order ID"""
        order_id = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"
        bill_details = self.calculate_bill()
        
        order_data = {
            'order_id': order_id,
            'customer_info': customer_info,
            'items': dict(st.session_state.cart),
            'bill_details': bill_details,
            'order_time': datetime.now().isoformat(),
            'status': 'Placed'
        }
        
        st.session_state.orders_history.append(order_data)
        st.session_state.current_order_id = order_id
        
        # Update daily stats
        st.session_state.daily_stats['total_orders'] += 1
        st.session_state.daily_stats['total_revenue'] += bill_details['total_amount']
        
        for item_name, item_data in st.session_state.cart.items():
            if item_name not in st.session_state.daily_stats['popular_items']:
                st.session_state.daily_stats['popular_items'][item_name] = 0
            st.session_state.daily_stats['popular_items'][item_name] += item_data['quantity']
        
        # Clear cart after order
        st.session_state.cart = {}
        st.session_state.order_placed = True
        
        return order_id
    
    def generate_invoice_csv(self, order_id: str) -> io.StringIO:
        """Generate CSV invoice"""
        order_data = next((order for order in st.session_state.orders_history if order['order_id'] == order_id), None)
        if not order_data:
            return None
        
        # Create invoice data
        invoice_data = []
        
        # Add header information
        invoice_data.append(['DELICIOUS BITES RESTAURANT'])
        invoice_data.append(['123 Food Street, Flavor City, FC 12345'])
        invoice_data.append(['Phone: (555) 123-FOOD | Email: orders@deliciousbites.com'])
        invoice_data.append([''])
        invoice_data.append(['INVOICE'])
        invoice_data.append([f"Order ID: {order_data['order_id']}"])
        invoice_data.append([f"Date: {datetime.fromisoformat(order_data['order_time']).strftime('%Y-%m-%d %H:%M:%S')}"])
        invoice_data.append([''])
        
        # Customer information
        customer = order_data['customer_info']
        invoice_data.append(['CUSTOMER INFORMATION'])
        invoice_data.append([f"Name: {customer.get('name', 'N/A')}"])
        invoice_data.append([f"Phone: {customer.get('phone', 'N/A')}"])
        invoice_data.append([f"Table: {customer.get('table_number', 'N/A')}"])
        invoice_data.append([''])
        
        # Order items
        invoice_data.append(['ITEM', 'QUANTITY', 'UNIT PRICE', 'TOTAL'])
        invoice_data.append(['=' * 50])
        
        for item_name, item_data in order_data['items'].items():
            total_price = item_data['price'] * item_data['quantity']
            invoice_data.append([
                item_name,
                str(item_data['quantity']),
                f"${item_data['price']:.2f}",
                f"${total_price:.2f}"
            ])
        
        # Bill summary
        bill = order_data['bill_details']
        invoice_data.append([''])
        invoice_data.append(['BILL SUMMARY'])
        invoice_data.append([f"Subtotal: ${bill['subtotal']:.2f}"])
        invoice_data.append([f"Tax ({bill['tax_rate']*100:.0f}%): ${bill['tax_amount']:.2f}"])
        invoice_data.append([f"Service Charge ({bill['service_rate']*100:.0f}%): ${bill['service_charge']:.2f}"])
        invoice_data.append([f"TOTAL AMOUNT: ${bill['total_amount']:.2f}"])
        invoice_data.append([''])
        invoice_data.append(['Thank you for dining with us!'])
        invoice_data.append(['Visit us again soon!'])
        
        # Convert to CSV
        csv_buffer = io.StringIO()
        for row in invoice_data:
            csv_buffer.write(','.join(row) + '\n')
        
        return csv_buffer
    
    def get_popular_items(self, limit: int = 5) -> List[Dict]:
        """Get most popular items"""
        popular_items = st.session_state.daily_stats['popular_items']
        sorted_items = sorted(popular_items.items(), key=lambda x: x[1], reverse=True)
        
        result = []
        for item_name, quantity in sorted_items[:limit]:
            price = self.get_item_price(item_name)
            result.append({
                'name': item_name,
                'quantity_sold': quantity,
                'revenue': price * quantity
            })
        
        return result

def main():
    # Initialize billing system
    billing_system = RestaurantBilling()
    
    # Restaurant header
    st.markdown("""
    <div class="restaurant-header">
        <h1>🍽️ Delicious Bites Restaurant</h1>
        <p>Authentic flavors, Fresh ingredients, Memorable experiences</p>
        <p>📍 123 Food Street, Flavor City | 📞 (555) 123-FOOD</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with cart and stats
    with st.sidebar:
        st.markdown("### 🛒 Your Order Cart")
        
        if st.session_state.cart:
            total_items = sum(item['quantity'] for item in st.session_state.cart.values())
            total_value = sum(item['price'] * item['quantity'] for item in st.session_state.cart.values())
            
            st.markdown(f"""
            <div class="stats-card">
                <h4>📊 Cart Summary</h4>
                <p><strong>Items:</strong> {total_items}</p>
                <p><strong>Value:</strong> ${total_value:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display cart items
            for item_name, item_data in st.session_state.cart.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{item_name}**")
                    st.write(f"${item_data['price']:.2f} × {item_data['quantity']}")
                with col2:
                    if st.button("🗑️", key=f"remove_{item_name}"):
                        del st.session_state.cart[item_name]
                        st.rerun()
            
            if st.button("🗑️ Clear Cart", type="secondary"):
                st.session_state.cart = {}
                st.rerun()
        
        else:
            st.info("🛒 Your cart is empty")
        
        st.markdown("---")
        
        # Daily stats
        stats = st.session_state.daily_stats
        st.markdown("### 📊 Today's Stats")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Orders", stats['total_orders'])
        with col2:
            st.metric("Revenue", f"${stats['total_revenue']:.2f}")

    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🍽️ Menu & Order", "🧾 Checkout & Bill", "📊 Analytics", "📋 Order History"])
    
    with tab1:
        # Menu display
        st.markdown("## 🍽️ Our Delicious Menu")
        
        # Search and filter
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("🔍 Search menu items...", placeholder="Type to search...")
        with col2:
            show_popular = st.checkbox("⭐ Popular items only")
        
        # Display menu categories
        for category, items in MENU_DATA.items():
            st.markdown(f'<div class="menu-category">{category}</div>', unsafe_allow_html=True)
            
            # Filter items based on search and popular filter
            filtered_items = {}
            for item_name, item_info in items.items():
                if search_term.lower() in item_name.lower() or not search_term:
                    if not show_popular or item_info.get('popular', False):
                        filtered_items[item_name] = item_info
            
            if not filtered_items:
                st.info("No items found matching your criteria.")
                continue
            
            # Display items in grid
            cols = st.columns(2)
            for i, (item_name, item_info) in enumerate(filtered_items.items()):
                with cols[i % 2]:
                    popular_badge = "⭐ " if item_info.get('popular', False) else ""
                    
                    st.markdown(f"""
                    <div class="menu-item-card">
                        <h4>{item_info['emoji']} {popular_badge}{item_name}</h4>
                        <p>{item_info['description']}</p>
                        <div class="price-tag">${item_info['price']:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Quantity controls
                    col_minus, col_qty, col_plus = st.columns([1, 2, 1])
                    
                    current_qty = st.session_state.cart.get(item_name, {}).get('quantity', 0)
                    
                    with col_minus:
                        if st.button("➖", key=f"minus_{item_name}"):
                            if current_qty > 0:
                                billing_system.add_to_cart(item_name, category, -1)
                                st.rerun()
                    
                    with col_qty:
                        st.markdown(f'<div class="quantity-display">{current_qty}</div>', unsafe_allow_html=True)
                    
                    with col_plus:
                        if st.button("➕", key=f"plus_{item_name}"):
                            billing_system.add_to_cart(item_name, category, 1)
                            st.rerun()
                    
                    # Direct quantity input
                    new_qty = st.number_input(
                        f"Set quantity for {item_name}",
                        min_value=0,
                        max_value=20,
                        value=current_qty,
                        key=f"qty_input_{item_name}"
                    )
                    
                    if new_qty != current_qty:
                        billing_system.update_cart_quantity(item_name, new_qty)
                        st.rerun()
    
    with tab2:
        # Checkout and billing
        st.markdown("## 🧾 Checkout & Generate Bill")
        
        if not st.session_state.cart:
            st.warning("🛒 Your cart is empty. Please add items from the menu to proceed with checkout.")
            return
        
        # Customer information form
        st.markdown("### 👤 Customer Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input(
                "Customer Name *",
                placeholder="Enter customer name...",
                key="customer_name"
            )
            
            if customer_name:
                name_validation = OrderValidator.validate_customer_name(customer_name)
                if name_validation["is_valid"]:
                    st.success(name_validation["message"])
                else:
                    st.error(name_validation["message"])
            
            phone_number = st.text_input(
                "Phone Number *",
                placeholder="+1 (555) 123-4567",
                key="customer_phone"
            )
            
            if phone_number:
                phone_validation = OrderValidator.validate_phone(phone_number)
                if phone_validation["is_valid"]:
                    st.success(phone_validation["message"])
                else:
                    st.error(phone_validation["message"])
        
        with col2:
            table_number = st.number_input(
                "Table Number *",
                min_value=1,
                max_value=50,
                value=1,
                key="table_number"
            )
            
            table_validation = OrderValidator.validate_table_number(table_number)
            if table_validation["is_valid"]:
                st.success(table_validation["message"])
            else:
                st.error(table_validation["message"])
            
            order_type = st.selectbox(
                "Order Type",
                options=["Dine In", "Takeaway", "Delivery"],
                key="order_type"
            )
        
        # Order summary
        st.markdown("### 📋 Order Summary")
        
        if st.session_state.cart:
            order_df = []
            for item_name, item_data in st.session_state.cart.items():
                total_price = item_data['price'] * item_data['quantity']
                order_df.append({
                    'Item': item_name,
                    'Quantity': item_data['quantity'],
                    'Unit Price': f"${item_data['price']:.2f}",
                    'Total': f"${total_price:.2f}"
                })
            
            df = pd.DataFrame(order_df)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Bill calculation
            bill_details = billing_system.calculate_bill()
            
            st.markdown(f"""
            <div class="bill-section">
                <h3>💰 Bill Breakdown</h3>
                <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                    <span>Subtotal:</span>
                    <span>${bill_details['subtotal']:.2f}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                    <span>Tax ({bill_details['tax_rate']*100:.0f}%):</span>
                    <span>${bill_details['tax_amount']:.2f}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                    <span>Service Charge ({bill_details['service_rate']*100:.0f}%):</span>
                    <span>${bill_details['service_charge']:.2f}</span>
                </div>
                <hr style="border: 2px solid white; margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between; font-size: 1.5rem; font-weight: bold;">
                    <span>TOTAL AMOUNT:</span>
                    <span>${bill_details['total_amount']:.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Place order button
            st.markdown("### 🚀 Place Your Order")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🎉 Place Order Now!", type="primary", use_container_width=True):
                    # Validate all inputs
                    name_val = OrderValidator.validate_customer_name(customer_name)
                    phone_val = OrderValidator.validate_phone(phone_number)
                    table_val = OrderValidator.validate_table_number(table_number)
                    order_val = OrderValidator.validate_order_items(st.session_state.cart)
                    
                    all_valid = all([
                        name_val["is_valid"],
                        phone_val["is_valid"], 
                        table_val["is_valid"],
                        order_val["is_valid"]
                    ])
                    
                    if all_valid:
                        customer_info = {
                            'name': customer_name,
                            'phone': phone_number,
                            'table_number': table_number,
                            'order_type': order_type
                        }
                        
                        order_id = billing_system.place_order(customer_info)
                        st.success(f"✅ Order placed successfully! Order ID: {order_id}")
                        st.rerun()
                    else:
                        st.error("❌ Please fix the validation errors before placing the order.")
        
        # Order success message
        if st.session_state.order_placed and st.session_state.current_order_id:
            order_data = next((order for order in st.session_state.orders_history 
                             if order['order_id'] == st.session_state.current_order_id), None)
            
            if order_data:
                st.markdown(f"""
                <div class="order-success">
                    <h2>🎉 Order Placed Successfully!</h2>
                    <h3>Order ID: {order_data['order_id']}</h3>
                    <p><strong>Customer:</strong> {order_data['customer_info']['name']}</p>
                    <p><strong>Table:</strong> {order_data['customer_info']['table_number']}</p>
                    <p><strong>Total Amount:</strong> ${order_data['bill_details']['total_amount']:.2f}</p>
                    <p><strong>Order Time:</strong> {datetime.fromisoformat(order_data['order_time']).strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>Thank you for dining with us! Your order is being prepared.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Download options
                st.markdown("### 📥 Download Invoice")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    csv_data = billing_system.generate_invoice_csv(st.session_state.current_order_id)
                    if csv_data:
                        st.download_button(
                            "📄 Download CSV Invoice",
                            data=csv_data.getvalue(),
                            file_name=f"invoice_{st.session_state.current_order_id}.csv",
                            mime="text/csv",
                            type="secondary"
                        )
                
                with col2:
                    # Generate receipt text for download
                    receipt_text = f"""
DELICIOUS BITES RESTAURANT
123 Food Street, Flavor City, FC 12345
Phone: (555) 123-FOOD

RECEIPT
Order ID: {order_data['order_id']}
Date: {datetime.fromisoformat(order_data['order_time']).strftime('%Y-%m-%d %H:%M:%S')}

Customer: {order_data['customer_info']['name']}
Phone: {order_data['customer_info']['phone']}
Table: {order_data['customer_info']['table_number']}
Type: {order_data['customer_info']['order_type']}

ORDER ITEMS:
{'='*50}
"""
                    for item_name, item_data in order_data['items'].items():
                        total_price = item_data['price'] * item_data['quantity']
                        receipt_text += f"{item_name:<30} {item_data['quantity']} x ${item_data['price']:.2f} = ${total_price:.2f}\n"
                    
                    bill = order_data['bill_details']
                    receipt_text += f"""
{'='*50}
Subtotal: ${bill['subtotal']:.2f}
Tax ({bill['tax_rate']*100:.0f}%): ${bill['tax_amount']:.2f}
Service ({bill['service_rate']*100:.0f}%): ${bill['service_charge']:.2f}
TOTAL: ${bill['total_amount']:.2f}

Thank you for dining with us!
Visit again soon!
"""
                    
                    st.download_button(
                        "📄 Download TXT Receipt",
                        data=receipt_text,
                        file_name=f"receipt_{st.session_state.current_order_id}.txt",
                        mime="text/plain",
                        type="secondary"
                    )
                
                with col3:
                    if st.button("🔄 New Order", type="primary"):
                        st.session_state.order_placed = False
                        st.session_state.current_order_id = None
                        st.rerun()
    
    with tab3:
        # Analytics dashboard
        st.markdown("## 📊 Restaurant Analytics")
        
        if st.session_state.orders_history:
            # Key metrics
            total_orders = len(st.session_state.orders_history)
            total_revenue = sum(order['bill_details']['total_amount'] for order in st.session_state.orders_history)
            avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="stats-card">
                    <h4>📊 Total Orders</h4>
                    <h2>{total_orders}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stats-card">
                    <h4>💰 Total Revenue</h4>
                    <h2>${total_revenue:.2f}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="stats-card">
                    <h4>📈 Avg Order Value</h4>
                    <h2>${avg_order_value:.2f}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                popular_items = billing_system.get_popular_items(1)
                top_item = popular_items[0]['name'] if popular_items else "None"
                st.markdown(f"""
                <div class="stats-card">
                    <h4>🏆 Top Item</h4>
                    <h6>{top_item}</h6>
                </div>
                """, unsafe_allow_html=True)
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Revenue by order type
                order_types = {}
                for order in st.session_state.orders_history:
                    order_type = order['customer_info']['order_type']
                    if order_type not in order_types:
                        order_types[order_type] = 0
                    order_types[order_type] += order['bill_details']['total_amount']
                
                if order_types:
                    fig_pie = px.pie(
                        values=list(order_types.values()),
                        names=list(order_types.keys()),
                        title="💰 Revenue by Order Type"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Popular items chart
                popular_items = billing_system.get_popular_items(5)
                if popular_items:
                    item_names = [item['name'][:20] + "..." if len(item['name']) > 20 else item['name'] for item in popular_items]
                    quantities = [item['quantity_sold'] for item in popular_items]
                    
                    fig_bar = px.bar(
                        x=quantities,
                        y=item_names,
                        orientation='h',
                        title="🏆 Most Popular Items",
                        labels={'x': 'Quantity Sold', 'y': 'Items'}
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
            
            # Orders timeline
            if len(st.session_state.orders_history) > 1:
                orders_df = pd.DataFrame([
                    {
                        'Date': datetime.fromisoformat(order['order_time']).date(),
                        'Revenue': order['bill_details']['total_amount'],
                        'Order_ID': order['order_id']
                    }
                    for order in st.session_state.orders_history
                ])
                
                daily_revenue = orders_df.groupby('Date')['Revenue'].sum().reset_index()
                
                fig_timeline = px.line(
                    daily_revenue,
                    x='Date',
                    y='Revenue',
                    title="📈 Daily Revenue Trend",
                    markers=True
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
        
        else:
            st.info("📊 Analytics will be available after orders are placed.")
    
    with tab4:
        # Order history
        st.markdown("## 📋 Order History")
        
        if st.session_state.orders_history:
            # Display orders
            for i, order in enumerate(reversed(st.session_state.orders_history)):
                with st.expander(
                    f"Order #{order['order_id']} - {order['customer_info']['name']} - ${order['bill_details']['total_amount']:.2f}",
                    expanded=(i == 0)
                ):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="customer-info-card">
                            <h4>👤 Customer Details</h4>
                            <p><strong>Name:</strong> {order['customer_info']['name']}</p>
                            <p><strong>Phone:</strong> {order['customer_info']['phone']}</p>
                            <p><strong>Table:</strong> {order['customer_info']['table_number']}</p>
                            <p><strong>Type:</strong> {order['customer_info']['order_type']}</p>
                            <p><strong>Time:</strong> {datetime.fromisoformat(order['order_time']).strftime('%Y-%m-%d %H:%M:%S')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("**📦 Order Items:**")
                        for item_name, item_data in order['items'].items():
                            total_price = item_data['price'] * item_data['quantity']
                            st.write(f"• {item_name}: {item_data['quantity']} × ${item_data['price']:.2f} = ${total_price:.2f}")
                        
                        bill = order['bill_details']
                        st.markdown(f"""
                        **💰 Bill Summary:**
                        - Subtotal: ${bill['subtotal']:.2f}
                        - Tax: ${bill['tax_amount']:.2f}
                        - Service: ${bill['service_charge']:.2f}
                        - **Total: ${bill['total_amount']:.2f}**
                        """)
                    
                    # Download options for this order
                    col_csv, col_txt = st.columns(2)
                    
                    with col_csv:
                        csv_data = billing_system.generate_invoice_csv(order['order_id'])
                        if csv_data:
                            st.download_button(
                                "📄 CSV Invoice",
                                data=csv_data.getvalue(),
                                file_name=f"invoice_{order['order_id']}.csv",
                                mime="text/csv",
                                key=f"csv_{order['order_id']}"
                            )
                    
                    with col_txt:
                        receipt_text = f"Order ID: {order['order_id']}\nCustomer: {order['customer_info']['name']}\nTotal: ${order['bill_details']['total_amount']:.2f}"
                        st.download_button(
                            "📄 TXT Receipt",
                            data=receipt_text,
                            file_name=f"receipt_{order['order_id']}.txt",
                            mime="text/plain",
                            key=f"txt_{order['order_id']}"
                        )
            
            # Export all orders
            st.markdown("### 📥 Bulk Export")
            
            all_orders_data = []
            for order in st.session_state.orders_history:
                for item_name, item_data in order['items'].items():
                    all_orders_data.append({
                        'Order_ID': order['order_id'],
                        'Customer_Name': order['customer_info']['name'],
                        'Customer_Phone': order['customer_info']['phone'],
                        'Table_Number': order['customer_info']['table_number'],
                        'Order_Type': order['customer_info']['order_type'],
                        'Order_Time': order['order_time'],
                        'Item_Name': item_name,
                        'Quantity': item_data['quantity'],
                        'Unit_Price': item_data['price'],
                        'Total_Price': item_data['price'] * item_data['quantity'],
                        'Subtotal': order['bill_details']['subtotal'],
                        'Tax_Amount': order['bill_details']['tax_amount'],
                        'Service_Charge': order['bill_details']['service_charge'],
                        'Final_Total': order['bill_details']['total_amount']
                    })
            
            if all_orders_data:
                all_orders_df = pd.DataFrame(all_orders_data)
                csv_buffer = io.StringIO()
                all_orders_df.to_csv(csv_buffer, index=False)
                
                st.download_button(
                    "📊 Export All Orders (CSV)",
                    data=csv_buffer.getvalue(),
                    file_name=f"all_orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    type="primary"
                )
        
        else:
            st.info("📋 No orders placed yet. Order history will appear here after orders are placed.")

if __name__ == "__main__":
    main()