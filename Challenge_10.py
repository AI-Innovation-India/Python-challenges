# -------------------------------
# Event Registration System 🎉
 
# Registration form: Name, Email, Event Choice.
 
# Save all responses in st.session_state (or CSV).
 
# Show live count of total registrations.
 
# Allow CSV export for organizers.
# -------------------------------


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import re
import json
import io
from typing import Dict, List, Any, Optional

# Configure page settings
st.set_page_config(
    page_title="Event Registration Hub 🎉",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .event-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.15);
        border: 1px solid rgba(102, 126, 234, 0.1);
        margin: 1rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .event-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.25);
    }
    
    .registration-form {
        background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.2);
        border: 2px solid rgba(102, 126, 234, 0.1);
        margin: 1.5rem 0;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .event-stats-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(17, 153, 142, 0.3);
    }
    
    .popular-event-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(250, 112, 154, 0.3);
    }
    
    .success-banner {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        animation: fadeInUp 0.6s ease;
    }
    
    .admin-panel {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .metric-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .event-option {
        background: #f8f9ff;
        border: 2px solid #e0e6ff;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .event-option:hover {
        border-color: #667eea;
        background: #f0f4ff;
        transform: translateX(5px);
    }
    
    .info-tooltip {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        display: inline-block;
    }
    
    .registration-count {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin: 1rem 0;
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
        border: 1px solid #e0e6ff;
    }
    
    .stTextInput > div > div > input {
        background: #f8f9ff;
        border-radius: 10px;
        border: 1px solid #e0e6ff;
    }
    
    .stTextArea > div > div > textarea {
        background: #f8f9ff;
        border-radius: 10px;
        border: 1px solid #e0e6ff;
    }
</style>
""", unsafe_allow_html=True)

# Event Configuration
EVENTS_CONFIG = {
    "Tech Conference 2024": {
        "icon": "💻",
        "date": "2024-12-15",
        "time": "09:00 - 17:00",
        "venue": "Convention Center Hall A",
        "capacity": 500,
        "price": "Free",
        "description": "Join us for the biggest tech conference featuring AI, ML, and emerging technologies.",
        "category": "Technology",
        "color": "#667eea"
    },
    "Music Festival": {
        "icon": "🎵",
        "date": "2024-12-20",
        "time": "18:00 - 23:00",
        "venue": "City Park Amphitheater",
        "capacity": 1000,
        "price": "$25",
        "description": "An evening of live music featuring local and international artists.",
        "category": "Entertainment",
        "color": "#fa709a"
    },
    "Food & Wine Expo": {
        "icon": "🍷",
        "date": "2024-12-22",
        "time": "11:00 - 22:00",
        "venue": "Grand Exhibition Center",
        "capacity": 300,
        "price": "$15",
        "description": "Taste exquisite cuisines and fine wines from around the world.",
        "category": "Food & Beverage",
        "color": "#11998e"
    },
    "Startup Pitch Competition": {
        "icon": "🚀",
        "date": "2024-12-28",
        "time": "10:00 - 16:00",
        "venue": "Innovation Hub",
        "capacity": 200,
        "price": "Free",
        "description": "Watch innovative startups pitch their ideas to top investors.",
        "category": "Business",
        "color": "#764ba2"
    },
    "Art Exhibition": {
        "icon": "🎨",
        "date": "2024-12-30",
        "time": "10:00 - 18:00",
        "venue": "Modern Art Gallery",
        "capacity": 150,
        "price": "$10",
        "description": "Explore contemporary art from emerging and established artists.",
        "category": "Arts & Culture",
        "color": "#f093fb"
    },
    "Fitness Bootcamp": {
        "icon": "💪",
        "date": "2025-01-05",
        "time": "07:00 - 09:00",
        "venue": "Central Sports Complex",
        "capacity": 100,
        "price": "$20",
        "description": "High-intensity workout session with professional trainers.",
        "category": "Health & Fitness",
        "color": "#fee140"
    }
}

class EventValidator:
    @staticmethod
    def validate_name(name: str) -> Dict[str, Any]:
        """Validate participant name"""
        name = name.strip()
        if not name:
            return {"is_valid": False, "message": "❌ Name is required!"}
        if len(name) < 2:
            return {"is_valid": False, "message": "❌ Name must be at least 2 characters long!"}
        if len(name) > 50:
            return {"is_valid": False, "message": "❌ Name must be less than 50 characters!"}
        if not re.match(r'^[a-zA-Z\s\'-]+$', name):
            return {"is_valid": False, "message": "❌ Name can only contain letters, spaces, hyphens, and apostrophes!"}
        return {"is_valid": True, "message": "✅ Valid name!"}
    
    @staticmethod
    def validate_email(email: str) -> Dict[str, Any]:
        """Validate email address"""
        email = email.strip().lower()
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email:
            return {"is_valid": False, "message": "❌ Email is required!"}
        if not re.match(pattern, email):
            return {"is_valid": False, "message": "❌ Please enter a valid email address!"}
        if len(email) > 100:
            return {"is_valid": False, "message": "❌ Email must be less than 100 characters!"}
        return {"is_valid": True, "message": "✅ Valid email address!"}
    
    @staticmethod
    def validate_phone(phone: str) -> Dict[str, Any]:
        """Validate phone number (optional field)"""
        if not phone.strip():
            return {"is_valid": True, "message": "📱 Phone number (optional)"}
        
        # Remove all non-numeric characters for validation
        numeric_phone = re.sub(r'[^\d]', '', phone)
        if len(numeric_phone) < 10 or len(numeric_phone) > 15:
            return {"is_valid": False, "message": "❌ Phone number must be 10-15 digits!"}
        return {"is_valid": True, "message": "✅ Valid phone number!"}
    
    @staticmethod
    def validate_event_selection(event: str) -> Dict[str, Any]:
        """Validate event selection"""
        if not event or event == "Select an event":
            return {"is_valid": False, "message": "❌ Please select an event!"}
        if event not in EVENTS_CONFIG:
            return {"is_valid": False, "message": "❌ Invalid event selected!"}
        return {"is_valid": True, "message": "✅ Event selected!"}
    
    @staticmethod
    def check_duplicate_registration(email: str, event: str, registrations: List[Dict]) -> Dict[str, Any]:
        """Check for duplicate registration"""
        for reg in registrations:
            if reg['email'].lower() == email.lower() and reg['event'] == event:
                return {"is_duplicate": True, "message": "❌ You have already registered for this event!"}
        return {"is_duplicate": False, "message": "✅ New registration!"}
    
    @staticmethod
    def check_event_capacity(event: str, registrations: List[Dict]) -> Dict[str, Any]:
        """Check if event has reached capacity"""
        event_registrations = [reg for reg in registrations if reg['event'] == event]
        current_count = len(event_registrations)
        capacity = EVENTS_CONFIG[event]['capacity']
        
        if current_count >= capacity:
            return {"is_full": True, "message": f"❌ Event is full! ({current_count}/{capacity})"}
        return {"is_full": False, "message": f"✅ Available spots: {capacity - current_count}/{capacity}"}

class EventRegistrationSystem:
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize all session state variables"""
        if 'registrations' not in st.session_state:
            st.session_state.registrations = []
        if 'registration_success' not in st.session_state:
            st.session_state.registration_success = False
        if 'last_registration' not in st.session_state:
            st.session_state.last_registration = None
        if 'admin_mode' not in st.session_state:
            st.session_state.admin_mode = False
        if 'show_analytics' not in st.session_state:
            st.session_state.show_analytics = False
    
    def register_participant(self, name: str, email: str, phone: str, event: str, comments: str = "") -> Dict[str, Any]:
        """Register a new participant"""
        registration = {
            'id': len(st.session_state.registrations) + 1,
            'name': name.strip().title(),
            'email': email.strip().lower(),
            'phone': phone.strip(),
            'event': event,
            'comments': comments.strip(),
            'registration_date': datetime.now().strftime("%Y-%m-%d"),
            'registration_time': datetime.now().strftime("%H:%M:%S"),
            'timestamp': datetime.now().isoformat()
        }
        
        st.session_state.registrations.append(registration)
        st.session_state.last_registration = registration
        st.session_state.registration_success = True
        
        return {"success": True, "message": "Registration successful!", "registration": registration}
    
    def get_registration_stats(self) -> Dict[str, Any]:
        """Get comprehensive registration statistics"""
        registrations = st.session_state.registrations
        
        if not registrations:
            return {
                'total_registrations': 0,
                'events_with_registrations': 0,
                'most_popular_event': 'None',
                'registrations_by_event': {},
                'registrations_by_date': {},
                'average_per_event': 0
            }
        
        # Count registrations by event
        event_counts = {}
        for reg in registrations:
            event_counts[reg['event']] = event_counts.get(reg['event'], 0) + 1
        
        # Count registrations by date
        date_counts = {}
        for reg in registrations:
            date_counts[reg['registration_date']] = date_counts.get(reg['registration_date'], 0) + 1
        
        most_popular = max(event_counts.items(), key=lambda x: x[1]) if event_counts else ('None', 0)
        
        return {
            'total_registrations': len(registrations),
            'events_with_registrations': len(event_counts),
            'most_popular_event': most_popular[0],
            'most_popular_count': most_popular[1],
            'registrations_by_event': event_counts,
            'registrations_by_date': date_counts,
            'average_per_event': len(registrations) / len(EVENTS_CONFIG) if registrations else 0
        }
    
    def export_to_csv(self) -> io.StringIO:
        """Export registrations to CSV format"""
        if not st.session_state.registrations:
            return None
        
        df = pd.DataFrame(st.session_state.registrations)
        
        # Add event details
        event_details = []
        for _, row in df.iterrows():
            event = EVENTS_CONFIG[row['event']]
            event_details.append({
                'event_date': event['date'],
                'event_time': event['time'],
                'event_venue': event['venue'],
                'event_category': event['category'],
                'event_price': event['price']
            })
        
        event_df = pd.DataFrame(event_details)
        final_df = pd.concat([df, event_df], axis=1)
        
        # Reorder columns
        column_order = [
            'id', 'name', 'email', 'phone', 'event', 
            'event_date', 'event_time', 'event_venue', 'event_category', 'event_price',
            'comments', 'registration_date', 'registration_time'
        ]
        final_df = final_df[column_order]
        
        csv_buffer = io.StringIO()
        final_df.to_csv(csv_buffer, index=False)
        return csv_buffer
    
    def create_analytics_charts(self):
        """Create analytics visualizations"""
        stats = self.get_registration_stats()
        
        if not st.session_state.registrations:
            st.info("📊 No registrations yet. Analytics will appear after the first registration.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Registrations by Event (Pie Chart)
            event_data = stats['registrations_by_event']
            fig_pie = px.pie(
                values=list(event_data.values()),
                names=list(event_data.keys()),
                title="📊 Registrations by Event",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Registrations by Date (Bar Chart)
            date_data = stats['registrations_by_date']
            fig_bar = px.bar(
                x=list(date_data.keys()),
                y=list(date_data.values()),
                title="📅 Registrations by Date",
                labels={'x': 'Date', 'y': 'Number of Registrations'},
                color=list(date_data.values()),
                color_continuous_scale='viridis'
            )
            fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Event Capacity Utilization
        capacity_data = []
        for event, config in EVENTS_CONFIG.items():
            registered = stats['registrations_by_event'].get(event, 0)
            capacity = config['capacity']
            utilization = (registered / capacity) * 100
            capacity_data.append({
                'Event': event,
                'Registered': registered,
                'Capacity': capacity,
                'Utilization %': utilization
            })
        
        fig_capacity = px.bar(
            pd.DataFrame(capacity_data),
            x='Event',
            y=['Registered', 'Capacity'],
            title="🎯 Event Capacity Utilization",
            barmode='group',
            color_discrete_sequence=['#667eea', '#e0e6ff']
        )
        fig_capacity.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_capacity, use_container_width=True)

def main():
    # Initialize system
    registration_system = EventRegistrationSystem()
    
    # Main title
    st.markdown('<h1 class="main-title">🎉 Event Registration Hub</h1>', unsafe_allow_html=True)
    
    # Sidebar with live stats and admin controls
    with st.sidebar:
        st.markdown("### 📊 Live Statistics")
        stats = registration_system.get_registration_stats()
        
        # Live counters
        st.markdown(f"""
        <div class="stats-card">
            <div class="registration-count">{stats['total_registrations']}</div>
            <div>Total Registrations</div>
        </div>
        """, unsafe_allow_html=True)
        
        if stats['total_registrations'] > 0:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Active Events", stats['events_with_registrations'])
            with col2:
                st.metric("Avg/Event", f"{stats['average_per_event']:.1f}")
            
            if stats['most_popular_event'] != 'None':
                st.markdown(f"""
                <div class="popular-event-card">
                    <strong>🏆 Most Popular</strong><br>
                    {EVENTS_CONFIG[stats['most_popular_event']]['icon']} {stats['most_popular_event']}<br>
                    <small>{stats['most_popular_count']} registrations</small>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Admin controls
        st.markdown("### 🔧 Admin Controls")
        
        if st.button("📈 Toggle Analytics", type="secondary"):
            st.session_state.show_analytics = not st.session_state.show_analytics
        
        if st.button("👥 Toggle Admin Panel", type="secondary"):
            st.session_state.admin_mode = not st.session_state.admin_mode
        
        # CSV Export
        if st.session_state.registrations:
            csv_data = registration_system.export_to_csv()
            if csv_data:
                st.download_button(
                    label="📥 Export CSV",
                    data=csv_data.getvalue(),
                    file_name=f"event_registrations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    type="primary"
                )
        
        # Clear all data (with confirmation)
        if st.session_state.registrations:
            if st.button("🗑️ Clear All Data", type="secondary"):
                if st.session_state.get('confirm_clear', False):
                    st.session_state.registrations = []
                    st.session_state.confirm_clear = False
                    st.session_state.registration_success = False
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.warning("⚠️ Click again to confirm deletion!")

    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["🎪 Register for Events", "📊 Analytics Dashboard", "👥 Admin Panel"])
    
    with tab1:
        # Success message
        if st.session_state.registration_success and st.session_state.last_registration:
            reg = st.session_state.last_registration
            st.markdown(f"""
            <div class="success-banner">
                <h3>🎉 Registration Successful!</h3>
                <p><strong>{reg['name']}</strong>, you're registered for <strong>{EVENTS_CONFIG[reg['event']]['icon']} {reg['event']}</strong></p>
                <p>📧 Confirmation sent to: {reg['email']}</p>
                <p>🎫 Registration ID: #{reg['id']:04d}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("✨ Register for Another Event", type="secondary"):
                st.session_state.registration_success = False
                st.rerun()
        
        # Event showcase
        st.markdown("### 🌟 Upcoming Events")
        
        # Event cards grid
        cols = st.columns(2)
        for i, (event_name, event_info) in enumerate(EVENTS_CONFIG.items()):
            with cols[i % 2]:
                registered_count = len([r for r in st.session_state.registrations if r['event'] == event_name])
                capacity_status = EventValidator.check_event_capacity(event_name, st.session_state.registrations)
                
                status_color = "#e74c3c" if capacity_status['is_full'] else "#27ae60"
                status_text = "FULL" if capacity_status['is_full'] else f"{registered_count}/{event_info['capacity']}"
                
                st.markdown(f"""
                <div class="event-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h4>{event_info['icon']} {event_name}</h4>
                        <span style="background: {status_color}; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">
                            {status_text}
                        </span>
                    </div>
                    <p><strong>📅 Date:</strong> {event_info['date']}</p>
                    <p><strong>🕒 Time:</strong> {event_info['time']}</p>
                    <p><strong>📍 Venue:</strong> {event_info['venue']}</p>
                    <p><strong>💰 Price:</strong> {event_info['price']}</p>
                    <p><strong>📝 Description:</strong> {event_info['description']}</p>
                    <div class="info-tooltip">
                        🏷️ {event_info['category']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Registration form
        if not st.session_state.registration_success:
            st.markdown("### 📝 Event Registration Form")
            
            with st.container():
                st.markdown('<div class="registration-form">', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Personal Information
                    st.markdown("#### 👤 Personal Information")
                    
                    name = st.text_input(
                        "Full Name *",
                        placeholder="Enter your full name...",
                        max_chars=50,
                        key="reg_name"
                    )
                    
                    if name:
                        name_validation = EventValidator.validate_name(name)
                        if name_validation["is_valid"]:
                            st.success(name_validation["message"])
                        else:
                            st.error(name_validation["message"])
                    
                    email = st.text_input(
                        "Email Address *",
                        placeholder="your.email@example.com",
                        max_chars=100,
                        key="reg_email"
                    )
                    
                    if email:
                        email_validation = EventValidator.validate_email(email)
                        if email_validation["is_valid"]:
                            st.success(email_validation["message"])
                        else:
                            st.error(email_validation["message"])
                    
                    phone = st.text_input(
                        "Phone Number (Optional)",
                        placeholder="+1 (555) 123-4567",
                        max_chars=20,
                        key="reg_phone"
                    )
                    
                    if phone:
                        phone_validation = EventValidator.validate_phone(phone)
                        if phone_validation["is_valid"]:
                            st.success(phone_validation["message"])
                        else:
                            st.error(phone_validation["message"])
                
                with col2:
                    # Event Selection
                    st.markdown("#### 🎪 Event Selection")
                    
                    event_options = ["Select an event"] + list(EVENTS_CONFIG.keys())
                    selected_event = st.selectbox(
                        "Choose Event *",
                        options=event_options,
                        key="reg_event"
                    )
                    
                    if selected_event and selected_event != "Select an event":
                        event_validation = EventValidator.validate_event_selection(selected_event)
                        capacity_check = EventValidator.check_event_capacity(selected_event, st.session_state.registrations)
                        duplicate_check = EventValidator.check_duplicate_registration(email, selected_event, st.session_state.registrations) if email else {"is_duplicate": False, "message": ""}
                        
                        if event_validation["is_valid"]:
                            st.success(event_validation["message"])
                        
                        if capacity_check["is_full"]:
                            st.error(capacity_check["message"])
                        else:
                            st.info(capacity_check["message"])
                        
                        if duplicate_check["is_duplicate"]:
                            st.warning(duplicate_check["message"])
                        
                        # Show selected event details
                        event_info = EVENTS_CONFIG[selected_event]
                        st.markdown(f"""
                        <div class="info-tooltip">
                            {event_info['icon']} {selected_event}<br>
                            📅 {event_info['date']} at {event_info['time']}<br>
                            📍 {event_info['venue']}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Additional Comments
                    comments = st.text_area(
                        "Additional Comments (Optional)",
                        placeholder="Any special requirements or questions...",
                        max_chars=500,
                        height=100,
                        key="reg_comments"
                    )
                
                # Submit button
                st.markdown("#### 🚀 Complete Registration")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🎉 Register Now!", type="primary", use_container_width=True):
                        # Validate all fields
                        name_val = EventValidator.validate_name(name)
                        email_val = EventValidator.validate_email(email)
                        phone_val = EventValidator.validate_phone(phone)
                        event_val = EventValidator.validate_event_selection(selected_event)
                        
                        # Additional checks
                        capacity_check = EventValidator.check_event_capacity(selected_event, st.session_state.registrations) if selected_event != "Select an event" else {"is_full": True}
                        duplicate_check = EventValidator.check_duplicate_registration(email, selected_event, st.session_state.registrations) if email and selected_event != "Select an event" else {"is_duplicate": False}
                        
                        # Collect all validation results
                        validations = [name_val, email_val, phone_val, event_val]
                        all_valid = all(v["is_valid"] for v in validations)
                        
                        if all_valid and not capacity_check["is_full"] and not duplicate_check["is_duplicate"]:
                            # Register participant
                            result = registration_system.register_participant(name, email, phone, selected_event, comments)
                            if result["success"]:
                                st.rerun()
                            else:
                                st.error("❌ Registration failed. Please try again.")
                        else:
                            # Show validation errors
                            errors = []
                            for val in validations:
                                if not val["is_valid"]:
                                    errors.append(val["message"])
                            
                            if capacity_check["is_full"]:
                                errors.append(capacity_check["message"])
                            
                            if duplicate_check["is_duplicate"]:
                                errors.append(duplicate_check["message"])
                            
                            for error in errors:
                                st.error(error)
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        # Analytics Dashboard
        st.markdown("### 📊 Registration Analytics Dashboard")
        
        if st.session_state.registrations:
            # Key metrics row
            col1, col2, col3, col4 = st.columns(4)
            stats = registration_system.get_registration_stats()
            
            with col1:
                st.markdown(f"""
                <div class="metric-container">
                    <h3 style="color: #667eea; margin: 0;">📊 Total</h3>
                    <h2 style="margin: 0;">{stats['total_registrations']}</h2>
                    <p style="margin: 0; color: #666;">Registrations</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-container">
                    <h3 style="color: #11998e; margin: 0;">🎪 Active</h3>
                    <h2 style="margin: 0;">{stats['events_with_registrations']}</h2>
                    <p style="margin: 0; color: #666;">Events</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-container">
                    <h3 style="color: #fa709a; margin: 0;">📈 Average</h3>
                    <h2 style="margin: 0;">{stats['average_per_event']:.1f}</h2>
                    <p style="margin: 0; color: #666;">Per Event</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                today_registrations = len([r for r in st.session_state.registrations if r['registration_date'] == datetime.now().strftime("%Y-%m-%d")])
                st.markdown(f"""
                <div class="metric-container">
                    <h3 style="color: #764ba2; margin: 0;">📅 Today</h3>
                    <h2 style="margin: 0;">{today_registrations}</h2>
                    <p style="margin: 0; color: #666;">Registrations</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Charts
            registration_system.create_analytics_charts()
            
            # Recent registrations table
            st.markdown("### 📋 Recent Registrations")
            recent_df = pd.DataFrame(st.session_state.registrations[-10:])  # Last 10 registrations
            if not recent_df.empty:
                # Format for display
                display_df = recent_df[['name', 'email', 'event', 'registration_date', 'registration_time']].copy()
                display_df.columns = ['Name', 'Email', 'Event', 'Date', 'Time']
                st.dataframe(display_df, use_container_width=True, hide_index=True)
            else:
                st.info("No registrations to display yet.")
        
        else:
            st.markdown("""
            <div class="info-tooltip">
                📊 Analytics dashboard will be populated after the first registration.
                Register for an event to see detailed analytics and insights!
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        # Admin Panel
        st.markdown("### 👥 Event Management Admin Panel")
        
        if st.session_state.registrations:
            # Admin statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="event-stats-card">
                    <h4>💼 Total Registrations</h4>
                    <h2>{len(st.session_state.registrations)}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                unique_emails = len(set(r['email'] for r in st.session_state.registrations))
                st.markdown(f"""
                <div class="event-stats-card">
                    <h4>👤 Unique Participants</h4>
                    <h2>{unique_emails}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                total_capacity = sum(EVENTS_CONFIG[event]['capacity'] for event in EVENTS_CONFIG)
                utilization = (len(st.session_state.registrations) / total_capacity) * 100
                st.markdown(f"""
                <div class="event-stats-card">
                    <h4>📊 Overall Utilization</h4>
                    <h2>{utilization:.1f}%</h2>
                </div>
                """, unsafe_allow_html=True)
            
            # Event-wise breakdown
            st.markdown("#### 🎪 Event-wise Registration Details")
            
            for event_name, event_info in EVENTS_CONFIG.items():
                event_registrations = [r for r in st.session_state.registrations if r['event'] == event_name]
                registered_count = len(event_registrations)
                capacity = event_info['capacity']
                utilization = (registered_count / capacity) * 100
                
                with st.expander(f"{event_info['icon']} {event_name} ({registered_count}/{capacity}) - {utilization:.1f}% Full", expanded=False):
                    if event_registrations:
                        # Create a detailed dataframe for this event
                        event_df = pd.DataFrame(event_registrations)
                        display_columns = ['id', 'name', 'email', 'phone', 'registration_date', 'registration_time', 'comments']
                        
                        # Only show columns that exist
                        available_columns = [col for col in display_columns if col in event_df.columns]
                        event_display_df = event_df[available_columns].copy()
                        
                        # Rename columns for better display
                        column_renames = {
                            'id': 'ID',
                            'name': 'Name', 
                            'email': 'Email',
                            'phone': 'Phone',
                            'registration_date': 'Date',
                            'registration_time': 'Time',
                            'comments': 'Comments'
                        }
                        
                        for old_col, new_col in column_renames.items():
                            if old_col in event_display_df.columns:
                                event_display_df.rename(columns={old_col: new_col}, inplace=True)
                        
                        st.dataframe(event_display_df, use_container_width=True, hide_index=True)
                        
                        # Export individual event data
                        event_csv = io.StringIO()
                        event_df.to_csv(event_csv, index=False)
                        st.download_button(
                            f"📥 Export {event_name} Registrations",
                            data=event_csv.getvalue(),
                            file_name=f"{event_name.lower().replace(' ', '_')}_registrations_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            key=f"export_{event_name}"
                        )
                    else:
                        st.info("No registrations for this event yet.")
                    
                    # Event capacity progress bar
                    progress_percentage = utilization / 100
                    st.progress(progress_percentage)
                    st.markdown(f"**Capacity:** {registered_count} / {capacity} ({utilization:.1f}%)")
            
            # Bulk operations
            st.markdown("#### 🔧 Bulk Operations")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📧 Export All Email List", type="secondary"):
                    emails = [r['email'] for r in st.session_state.registrations]
                    email_list = '\n'.join(set(emails))  # Remove duplicates
                    
                    st.text_area(
                        "Email List (Copy & Paste)",
                        value=email_list,
                        height=200
                    )
            
            with col2:
                if st.button("📊 Generate Summary Report", type="secondary"):
                    stats = registration_system.get_registration_stats()
                    
                    report = f"""
                    📊 EVENT REGISTRATION SUMMARY REPORT
                    Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    
                    📈 OVERVIEW:
                    • Total Registrations: {stats['total_registrations']}
                    • Active Events: {stats['events_with_registrations']}/{len(EVENTS_CONFIG)}
                    • Average per Event: {stats['average_per_event']:.1f}
                    • Most Popular: {stats['most_popular_event']} ({stats.get('most_popular_count', 0)} registrations)
                    
                    🎪 EVENT BREAKDOWN:
                    """
                    
                    for event, count in stats['registrations_by_event'].items():
                        capacity = EVENTS_CONFIG[event]['capacity']
                        utilization = (count / capacity) * 100
                        report += f"• {event}: {count}/{capacity} ({utilization:.1f}%)\n"
                    
                    st.text_area("Summary Report", value=report, height=400)
            
            with col3:
                # Clear specific event registrations
                event_to_clear = st.selectbox(
                    "Clear Event Registrations",
                    options=["Select event to clear"] + list(EVENTS_CONFIG.keys())
                )
                
                if event_to_clear != "Select event to clear":
                    if st.button(f"🗑️ Clear {event_to_clear}", type="secondary"):
                        # Remove registrations for specific event
                        st.session_state.registrations = [
                            r for r in st.session_state.registrations 
                            if r['event'] != event_to_clear
                        ]
                        st.success(f"✅ Cleared all registrations for {event_to_clear}")
                        st.rerun()
        
        else:
            st.markdown("""
            <div class="admin-panel">
                <h3>👥 Admin Panel</h3>
                <p>🔒 Admin panel will be available after the first registration.</p>
                <p>📊 Here you'll be able to:</p>
                <ul>
                    <li>View detailed registration data</li>
                    <li>Export event-specific reports</li>
                    <li>Manage registrations</li>
                    <li>Generate summary reports</li>
                    <li>Bulk operations</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()