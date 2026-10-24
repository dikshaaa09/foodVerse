import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Food Verse AI – Multimodal Food Intelligence Agent",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Import AI Engine and module views
from modules.ai_engine import FoodVerseAIEngine
from modules.food_recognition import render_food_recognition_tab
from modules.freshness_detector import render_freshness_detector_tab
from modules.kitchen_hygiene import render_kitchen_hygiene_tab
from modules.recipe_coach import render_recipe_coach_tab
from modules.meal_planner import render_meal_planner_tab

# ==============================================================================
# SIDEBAR CONFIGURATION & PERSONA
# ==============================================================================
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
            <div style="font-size: 2rem;">🥗</div>
            <div>
                <div style="font-weight: 800; font-size: 1.25rem; color: #F8FAFC; letter-spacing: -0.02em;">Food Verse AI</div>
                <div style="font-size: 0.75rem; color: #10B981; font-weight: 600;">MULTIMODAL INTELLIGENCE</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ Engine Configuration")
    
    provider = st.selectbox(
        "AI Vision Provider:",
        ["Gemini (Google GenAI)", "Groq (Llama Vision)"],
        index=0
    )
    provider_key = "gemini" if "Gemini" in provider else "groq"
    
    env_key = os.environ.get("GEMINI_API_KEY" if provider_key == "gemini" else "GROQ_API_KEY", "")
    api_key_input = st.text_input(
        f"{provider.split()[0]} API Key:",
        type="password",
        value=env_key,
        help="Optional: Enter your API key for live multimodal inferences. If left blank, standalone demonstration mode automatically activates."
    )
    
    # Standalone Demo Switch
    is_demo = st.toggle(
        "Standalone Demonstration Mode",
        value=(not bool(api_key_input)),
        help="When enabled, runs with built-in food science contracts, allowing full testing without external API quotas."
    )
    
    # Model indicator
    active_mode_str = "Demonstration Mode (Pre-Calibrated)" if is_demo or not api_key_input else f"Live {provider.split()[0]} API Active"
    status_color = "#10B981" if (api_key_input and not is_demo) else "#F59E0B"
    
    st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 10px; margin-top: 8px; margin-bottom: 1.2rem;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">Engine Status</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: {status_color}; margin-top: 2px;">
                ● {active_mode_str}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📋 Capstone Metadata")
    st.markdown("""
        <div style="font-size: 0.82rem; color: #94A3B8; line-height: 1.6;">
            • <strong>Platform ID:</strong> <code>6ac4ca021dcde6d7857c169a</code><br>
            • <strong>Project:</strong> Capstone Project 3<br>
            • <strong>Architecture:</strong> Zero external DB (1-click ready)<br>
            • <strong>Compliance:</strong> FDA HACCP & Mifflin-St Jeor
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🔄 Reset Current Session", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Instantiate AI Engine
engine = FoodVerseAIEngine(
    api_provider=provider_key,
    api_key=api_key_input,
    demo_mode=is_demo
)

# ==============================================================================
# HERO BANNER & TELEMETRY
# ==============================================================================
st.markdown("""
    <div class="foodverse-hero">
        <h1 class="hero-title">
            <span>🥗 Food Verse AI</span>
        </h1>
        <p class="hero-subtitle">
            Multimodal Food Intelligence Agent analyzing culinary images, perishable freshness, commercial kitchen sanitation compliance, and bespoke dietary metabolism.
        </p>
        <div class="stats-bar">
            <span class="stat-chip">🥑 <strong>Epic 2:</strong> Food Recognition & Macros</span>
            <span class="stat-chip">🔬 <strong>Epic 3:</strong> Spoilage & Decay Diagnostic</span>
            <span class="stat-chip">🛡️ <strong>Epic 4:</strong> HACCP Kitchen Hygiene</span>
            <span class="stat-chip">🍳 <strong>Epic 4:</strong> Smart Pantry Coach</span>
            <span class="stat-chip">📊 <strong>Epic 5:</strong> TDEE & 7-Day Meal Engine</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# INTERACTIVE NAVIGATION TABS
# ==============================================================================
tab_food, tab_fresh, tab_kitchen, tab_recipe, tab_meal = st.tabs([
    "🥗 Nutrition Audit (Epic 2)",
    "🔬 Freshness Diagnostic (Epic 3)",
    "🛡️ Kitchen Hygiene & Safety (Epic 4)",
    "🍳 Smart Recipe Coach (Epic 4)",
    "📊 Personalized Meal Planner (Epic 5)"
])

with tab_food:
    render_food_recognition_tab(engine)

with tab_fresh:
    render_freshness_detector_tab(engine)

with tab_kitchen:
    render_kitchen_hygiene_tab(engine)

with tab_recipe:
    render_recipe_coach_tab(engine)

with tab_meal:
    render_meal_planner_tab(engine)

# ==============================================================================
# APP FOOTER
# ==============================================================================
st.markdown("""
    <div style="margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid rgba(148, 163, 184, 0.1); text-align: center; color: #64748B; font-size: 0.85rem;">
        Food Verse AI • Multimodal Food Intelligence Agent • Skill Wallet Capstone Project 3 • Platform ID: <code>6ac4ca021dcde6d7857c169a</code><br>
        Engineered with Streamlit, Plotly, Google GenAI & Pillow. Clean stateless architecture for instant 1-click deployment on Streamlit Community Cloud.
    </div>
""", unsafe_allow_html=True)
