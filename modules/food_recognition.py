import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from modules.ai_engine import FoodVerseAIEngine

FOOD_RECOGNITION_PROMPT = """
You are an expert clinical dietitian and food science computer vision specialist.
Analyze the provided food/dish image and return a STRICT JSON object with these exact keys:
{
  "dish_name": "Title of the identified dish",
  "cuisine": "Cuisine classification (e.g. Mediterranean, Mexican, South Asian, Italian, etc.)",
  "confidence": 0.95,
  "portion_size": "Estimated portion in grams and description (e.g. 350g, 1 bowl)",
  "ingredients": [
    {"name": "Ingredient name", "quantity": "estimated weight/amount"}
  ],
  "nutrition": {
    "calories": 520,
    "protein_g": 38.0,
    "carbohydrates_g": 45.0,
    "fats_g": 22.0,
    "fiber_g": 7.0,
    "sugar_g": 4.0,
    "sodium_mg": 450
  },
  "micros": {
    "potassium_mg": 620,
    "calcium_mg": 140,
    "iron_mg": 3.8,
    "vitamin_c_mg": 24
  },
  "allergens": [
    {"allergen": "Gluten", "severity": "None / Low / High", "present": false},
    {"allergen": "Dairy", "severity": "None / Low / High", "present": false},
    {"allergen": "Nuts", "severity": "None / Low / High", "present": false},
    {"allergen": "Soy", "severity": "None / Low / High", "present": false},
    {"allergen": "Shellfish", "severity": "None / Low / High", "present": false}
  ],
  "health_score": 88,
  "health_badge": "Nutrient Dense / High Protein / Heart Healthy / etc.",
  "dietary_compatibility": ["High Protein", "Low GI", "Mediterranean", "Gluten-Free"],
  "dietitian_summary": "2-3 sentences explaining nutritional balance and metabolic impact."
}
Return ONLY valid JSON.
"""

def create_macro_donut_chart(nutrition: dict):
    """Generates an interactive Plotly donut chart of macronutrient distribution."""
    p = float(nutrition.get("protein_g", 0))
    c = float(nutrition.get("carbohydrates_g", 0))
    f = float(nutrition.get("fats_g", 0))
    fib = float(nutrition.get("fiber_g", 0))
    
    # Protein: 4 kcal/g, Carbs: 4 kcal/g, Fat: 9 kcal/g
    p_cal = p * 4
    c_cal = c * 4
    f_cal = f * 9
    
    labels = ["Protein", "Carbohydrates", "Healthy Fats", "Dietary Fiber"]
    values = [p, c, f, fib]
    colors = ["#10B981", "#3B82F6", "#F59E0B", "#8B5CF6"]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.62,
        marker=dict(colors=colors, line=dict(color='#0b0f19', width=3)),
        textinfo='label+percent',
        hoverinfo='label+value+percent',
        insidetextfont=dict(color='#FFFFFF', size=13),
        hovertemplate='<b>%{label}</b><br>Weight: %{value:.1f}g<br>Ratio: %{percent}<extra></extra>'
    )])
    
    total_cal = nutrition.get("calories", int(p_cal + c_cal + f_cal))
    
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color="#94A3B8", size=12)
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20, b=30, l=10, r=10),
        height=320,
        annotations=[
            dict(
                text=f"<span style='font-size:24px; font-weight:800; color:#F8FAFC;'>{total_cal}</span><br><span style='font-size:12px; color:#94A3B8;'>TOTAL KCAL</span>",
                x=0.5, y=0.5,
                font_size=16,
                showarrow=False
            )
        ]
    )
    return fig

def render_food_recognition_tab(engine: FoodVerseAIEngine):
    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h2 style="font-weight: 800; color: #F8FAFC; margin-bottom: 0.3rem;">🥗 Food Recognition & Nutrition Audit</h2>
            <p style="color: #94A3B8; font-size: 0.98rem;">
                Multimodal visual intelligence estimating dish identity, authentic ingredients, portion sizing, macronutrient/micronutrient scores, and allergen profiles.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_input, col_display = st.columns([1, 1], gap="large")
    
    chosen_image = None
    image_caption = "Selected Food Image"
    
    with col_input:
        st.markdown("#### 1. Input Food Image")
        source_opt = st.radio("Choose Input Mode:", ["Upload Photo", "Choose Preset Sample"], horizontal=True)
        
        if source_opt == "Upload Photo":
            uploaded_file = st.file_uploader("Upload meal or dish photograph (JPG, PNG, WEBP)", type=["jpg", "jpeg", "png", "webp"])
            if uploaded_file is not None:
                chosen_image = Image.open(uploaded_file)
                image_caption = f"Uploaded: {uploaded_file.name}"
        else:
            sample_choice = st.selectbox(
                "Select a Curated Sample Dish:",
                ["Mediterranean Grilled Salmon Bowl", "Fresh Honeycrisp Apple", "Spoiled Moldy Strawberries"]
            )
            sample_paths = {
                "Mediterranean Grilled Salmon Bowl": "sample_data/sample_salmon_bowl.jpg",
                "Fresh Honeycrisp Apple": "sample_data/sample_fresh_apple.jpg",
                "Spoiled Moldy Strawberries": "sample_data/sample_spoiled_berries.jpg"
            }
            if sample_choice in sample_paths:
                chosen_image = Image.open(sample_paths[sample_choice])
                image_caption = f"Preset Sample: {sample_choice}"
        
        if chosen_image is not None:
            st.image(chosen_image, caption=image_caption, use_container_width=True)
            analyze_btn = st.button("🚀 Audit Dish & Compute Nutrition", use_container_width=True)
        else:
            st.info("👆 Upload an image or select a preset sample above to begin nutritional vision analysis.")
            analyze_btn = False

    with col_display:
        if chosen_image is not None and analyze_btn:
            with st.spinner("🤖 Vision Agent examining dish composition, density & nutrient matrix..."):
                result = engine.analyze_image_with_prompt(chosen_image, FOOD_RECOGNITION_PROMPT, task_type="food_recognition")
                st.session_state["food_recognition_result"] = result
        
        if "food_recognition_result" in st.session_state and st.session_state["food_recognition_result"]:
            res = st.session_state["food_recognition_result"]
            
            if "_api_notice" in res:
                st.caption(f"ℹ️ {res['_api_notice']}")

            dish_name = res.get("dish_name", "Identified Dish")
            cuisine = res.get("cuisine", "International")
            health_score = res.get("health_score", 85)
            portion = res.get("portion_size", "1 Serving")
            
            # Health Score Header Badge
            score_color = "#10B981" if health_score >= 80 else ("#F59E0B" if health_score >= 60 else "#F43F5E")
            
            st.markdown(f"""
                <div class="food-card" style="border-top: 4px solid {score_color};">
                    <div class="food-card-title">
                        <span>{dish_name}</span>
                        <span style="font-size: 0.9rem; background: rgba(16, 185, 129, 0.15); color: #34d399; padding: 4px 12px; border-radius: 9999px;">
                            {cuisine}
                        </span>
                    </div>
                    <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 0.8rem;">
                        📏 <strong>Estimated Portion:</strong> {portion}
                    </p>
                    <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(30, 41, 59, 0.5); padding: 12px 18px; border-radius: 12px;">
                        <div>
                            <div style="font-size: 0.8rem; text-transform: uppercase; color: #94a3b8; font-weight: 700;">Composite Health Score</div>
                            <div style="font-size: 1.8rem; font-weight: 800; color: {score_color}; font-family: 'JetBrains Mono', monospace;">
                                {health_score} / 100
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <span class="stat-chip" style="border-color: {score_color};">
                                🏅 {res.get('health_badge', 'Nutrient Rich')}
                            </span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Nutrition Key Metrics Grid
            nutr = res.get("nutrition", {})
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""
                    <div class="macro-box">
                        <div class="macro-box-label">Calories</div>
                        <div class="macro-box-val" style="color: #F8FAFC;">{nutr.get('calories', 0)}</div>
                        <div style="font-size: 0.75rem; color: #94A3B8;">kcal</div>
                    </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                    <div class="macro-box">
                        <div class="macro-box-label">Protein</div>
                        <div class="macro-box-val" style="color: #10B981;">{nutr.get('protein_g', 0)}g</div>
                        <div style="font-size: 0.75rem; color: #94A3B8;">Lean Amino</div>
                    </div>
                """, unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                    <div class="macro-box">
                        <div class="macro-box-label">Carbs</div>
                        <div class="macro-box-val" style="color: #3B82F6;">{nutr.get('carbohydrates_g', 0)}g</div>
                        <div style="font-size: 0.75rem; color: #94A3B8;">Fiber {nutr.get('fiber_g', 0)}g</div>
                    </div>
                """, unsafe_allow_html=True)
            with m4:
                st.markdown(f"""
                    <div class="macro-box">
                        <div class="macro-box-label">Healthy Fats</div>
                        <div class="macro-box-val" style="color: #F59E0B;">{nutr.get('fats_g', 0)}g</div>
                        <div style="font-size: 0.75rem; color: #94A3B8;">Lipids</div>
                    </div>
                """, unsafe_allow_html=True)
                
            # Interactive Macro Donut Chart
            st.markdown("#### 📊 Macronutrient Caloric Contribution")
            chart = create_macro_donut_chart(nutr)
            st.plotly_chart(chart, use_container_width=True)
            
            # Dietitian Summary
            summary = res.get("dietitian_summary", "")
            if summary:
                st.markdown(f"""
                    <div class="safe-alert">
                        <strong>🧑‍⚕️ Clinical Dietitian Analysis:</strong><br>
                        <span style="color: #CBD5E1; font-size: 0.92rem;">{summary}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            # Dietary Compatibility Tags
            tags = res.get("dietary_compatibility", [])
            if tags:
                tag_html = " ".join([f'<span class="stat-chip">✓ {t}</span>' for t in tags])
                st.markdown(f"**Dietary Profiles:** {tag_html}", unsafe_allow_html=True)
                
            # Allergen Alerts
            st.markdown("#### ⚠️ Allergen & Sensitivity Diagnostic")
            allergens = res.get("allergens", [])
            if allergens:
                al_cols = st.columns(len(allergens))
                for idx, al in enumerate(allergens):
                    present = al.get("present", False)
                    name = al.get("allergen", "Allergen")
                    badge_style = "background: rgba(244, 63, 94, 0.2); border: 1px solid #F43F5E; color: #FCA5A5;" if present else "background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); color: #86EFAC;"
                    icon = "⚠️" if present else "✓"
                    with al_cols[idx]:
                        st.markdown(f"""
                            <div style="{badge_style} border-radius: 8px; padding: 8px; text-align: center; font-size: 0.8rem; font-weight: 600;">
                                {icon} {name}
                                <div style="font-size: 0.7rem; font-weight: 400; opacity: 0.85;">{'Present' if present else 'Free'}</div>
                            </div>
                        """, unsafe_allow_html=True)
            
            # Ingredients Breakdown Accordion
            with st.expander("🔍 Itemized Ingredients & Micronutrient Trace"):
                ingredients = res.get("ingredients", [])
                if ingredients:
                    st.write("**Identified Ingredients:**")
                    for ing in ingredients:
                        st.markdown(f"- **{ing.get('name')}**: `{ing.get('quantity')}`")
                
                micros = res.get("micros", {})
                if micros:
                    st.write("**Key Micronutrients:**")
                    for k, v in micros.items():
                        st.markdown(f"- **{k.replace('_', ' ').title()}**: `{v}`")
        else:
            st.markdown("""
                <div class="food-card" style="text-align: center; padding: 3rem 1.5rem;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🍽️</div>
                    <h3 style="color: #F8FAFC;">Awaiting Meal Image Analysis</h3>
                    <p style="color: #94A3B8; max-width: 400px; margin: 0 auto; font-size: 0.95rem;">
                        Select a meal photo or preset sample on the left, then click 'Audit Dish & Compute Nutrition' to trigger multimodal vision recognition.
                    </p>
                </div>
            """, unsafe_allow_html=True)
