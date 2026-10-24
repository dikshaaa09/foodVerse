import streamlit as st
import json
from modules.ai_engine import FoodVerseAIEngine

def build_recipe_prompt(pantry_items: list, dietary_pref: str, max_time: str, skill_level: str) -> str:
    return f"""
You are a Michelin-caliber chef and functional nutrition consultant.
Create an inventive, healthy, restaurant-quality recipe utilizing the following pantry inventory:
Available Pantry Ingredients: {', '.join(pantry_items)}
Dietary Preference / Constraint: {dietary_pref}
Target Time Limit: {max_time}
Skill Level: {skill_level}

Return a STRICT JSON object with these exact keys:
{{
  "recipe_title": "Creative and appetizing dish name",
  "difficulty": "Beginner / Intermediate / Advanced",
  "prep_time_minutes": 10,
  "cook_time_minutes": 20,
  "total_time_minutes": 30,
  "servings": 2,
  "calories_per_serving": 420,
  "macros_per_serving": {{
    "protein_g": 34.0,
    "carbs_g": 26.0,
    "fats_g": 18.0,
    "fiber_g": 6.0
  }},
  "ingredients_required": [
    "Item name with specific measured quantities"
  ],
  "cooking_steps": [
    {{"step": 1, "action": "Clear concise culinary instruction"}}
  ],
  "chef_pro_tip": "Insider chef technique to maximize flavor depth",
  "smart_substitutions": [
    {{"original": "Original ingredient", "substitute": "Alternative healthy swap"}}
  ],
  "zero_waste_hack": "Practical tip to use stems, rinds, or leftover stock"
}}
Return ONLY valid JSON.
"""

def render_recipe_coach_tab(engine: FoodVerseAIEngine):
    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h2 style="font-weight: 800; color: #F8FAFC; margin-bottom: 0.3rem;">🍳 Smart Kitchen Recipe Assistant</h2>
            <p style="color: #94A3B8; font-size: 0.98rem;">
                Transform your current pantry stock into gourmet, nutrient-balanced dishes with automated culinary substitutions, macronutrient breakdowns, and zero-waste food preservation hacks.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_input, col_display = st.columns([1, 1], gap="large")
    
    with col_input:
        st.markdown("#### 1. Available Pantry Inventory")
        
        default_pantry = ["Eggs", "Baby Spinach", "Cherry Tomatoes", "Garlic", "Olive Oil", "Chicken Breast"]
        common_ingredients = [
            "Eggs", "Chicken Breast", "Salmon Fillet", "Tofu", "Canned Tuna", "Black Beans", "Chickpeas",
            "Baby Spinach", "Broccoli", "Cherry Tomatoes", "Avocado", "Mushrooms", "Bell Peppers", "Onions", "Garlic",
            "Quinoa", "Brown Rice", "Oats", "Pasta", "Sweet Potatoes",
            "Olive Oil", "Soy Sauce", "Greek Yogurt", "Feta Cheese", "Lemons", "Parmesan"
        ]
        
        selected_pantry = st.multiselect(
            "Select ingredients currently in your kitchen:",
            options=common_ingredients,
            default=default_pantry
        )
        
        custom_items = st.text_input("Add any other specific items (comma-separated):", placeholder="e.g. sourdough bread, walnuts, basil")
        
        all_pantry = list(selected_pantry)
        if custom_items:
            for item in custom_items.split(","):
                clean = item.strip()
                if clean and clean not in all_pantry:
                    all_pantry.append(clean)
                    
        st.markdown("#### 2. Cooking Parameters")
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            dietary = st.selectbox("Dietary Filter:", ["Balanced High Protein", "Keto / Low-Carb", "Plant-Based Vegan", "Gluten-Free", "Mediterranean", "Diabetic-Friendly"])
            time_limit = st.selectbox("Time Availability:", ["Quick (< 20 mins)", "Standard (30 mins)", "Gourmet (45+ mins)"])
        with p_col2:
            skill = st.selectbox("Cooking Skill Level:", ["Beginner Friendly", "Intermediate Home Cook", "Masterchef Technique"])
            servings = st.slider("Portions / Servings:", min_value=1, max_value=6, value=2)
            
        gen_btn = st.button("✨ Craft Gourmet Smart Recipe", use_container_width=True)
        
    with col_display:
        if gen_btn and all_pantry:
            with st.spinner("👨‍🍳 Master Chef assembling flavor matrices, culinary steps & macro split..."):
                prompt = build_recipe_prompt(all_pantry, dietary, time_limit, skill)
                result = engine.generate_text_response(prompt, task_type="recipe")
                st.session_state["recipe_coach_result"] = result
                
        if "recipe_coach_result" in st.session_state and st.session_state["recipe_coach_result"]:
            res = st.session_state["recipe_coach_result"]
            
            title = res.get("recipe_title", "Custom Chef Recipe")
            diff = res.get("difficulty", "Intermediate")
            prep = res.get("prep_time_minutes", 10)
            cook = res.get("cook_time_minutes", 20)
            total = res.get("total_time_minutes", prep + cook)
            cals = res.get("calories_per_serving", 400)
            macros = res.get("macros_per_serving", {})
            
            st.markdown(f"""
                <div class="food-card" style="border-top: 4px solid #10B981;">
                    <div class="food-card-title">
                        <span>{title}</span>
                        <span class="badge-fresh">⏱️ {total} MINS</span>
                    </div>
                    <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 0.4rem;">
                        <span class="stat-chip">👨‍🍳 <strong>Skill:</strong> {diff}</span>
                        <span class="stat-chip">🍽️ <strong>Servings:</strong> {res.get('servings', 2)}</span>
                        <span class="stat-chip">🔥 <strong>Calories:</strong> {cals} kcal/srv</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Nutrition pills
            mc1, mc2, mc3, mc4 = st.columns(4)
            with mc1:
                st.markdown(f"<div class='macro-box'><div class='macro-box-label'>Protein</div><div class='macro-box-val' style='color:#10B981;'>{macros.get('protein_g', 0)}g</div></div>", unsafe_allow_html=True)
            with mc2:
                st.markdown(f"<div class='macro-box'><div class='macro-box-label'>Carbs</div><div class='macro-box-val' style='color:#3B82F6;'>{macros.get('carbs_g', 0)}g</div></div>", unsafe_allow_html=True)
            with mc3:
                st.markdown(f"<div class='macro-box'><div class='macro-box-label'>Fats</div><div class='macro-box-val' style='color:#F59E0B;'>{macros.get('fats_g', 0)}g</div></div>", unsafe_allow_html=True)
            with mc4:
                st.markdown(f"<div class='macro-box'><div class='macro-box-label'>Fiber</div><div class='macro-box-val' style='color:#8B5CF6;'>{macros.get('fiber_g', 0)}g</div></div>", unsafe_allow_html=True)
                
            # Ingredients
            st.markdown("#### 🛒 Ingredients Measure")
            ings = res.get("ingredients_required", [])
            for item in ings:
                st.markdown(f"- {item}")
                
            # Cooking steps
            st.markdown("#### 🍳 Step-by-Step Cooking Instructions")
            steps = res.get("cooking_steps", [])
            for s in steps:
                step_no = s.get("step", 1)
                action = s.get("action", "")
                st.markdown(f"""
                    <div class="step-item">
                        <div class="step-number">{step_no}</div>
                        <div style="color: #F1F5F9; font-size: 0.95rem; line-height: 1.5;">{action}</div>
                    </div>
                """, unsafe_allow_html=True)
                
            # Chef pro tip
            tip = res.get("chef_pro_tip", "")
            if tip:
                st.markdown(f"""
                    <div class="safe-alert">
                        <strong>💡 Executive Chef Secret:</strong><br>
                        <span style="color: #CBD5E1; font-size: 0.92rem;">{tip}</span>
                    </div>
                """, unsafe_allow_html=True)
                
            # Substitutions & Zero Waste
            with st.expander("🔄 Smart Dietary Substitutions & Zero-Waste Hacks"):
                subs = res.get("smart_substitutions", [])
                if subs:
                    st.write("**Dietary Substitutions:**")
                    for sub in subs:
                        st.markdown(f"- Instead of **{sub.get('original')}** ➔ Swap with **{sub.get('substitute')}**")
                
                waste = res.get("zero_waste_hack", "")
                if waste:
                    st.markdown(f"**🌱 Zero-Waste Sustainability Hack:** {waste}")
        else:
            st.markdown("""
                <div class="food-card" style="text-align: center; padding: 3rem 1.5rem;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🍳</div>
                    <h3 style="color: #F8FAFC;">Awaiting Kitchen Pantry Recipe</h3>
                    <p style="color: #94A3B8; max-width: 400px; margin: 0 auto; font-size: 0.95rem;">
                        Select the ingredients you already have at home on the left, pick your dietary preference, and let AI generate a customized recipe.
                    </p>
                </div>
            """, unsafe_allow_html=True)
