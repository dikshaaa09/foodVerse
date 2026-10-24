import streamlit as st
import json
from modules.ai_engine import FoodVerseAIEngine

def calculate_bmr_tdee(gender: str, weight_kg: float, height_cm: float, age: int, activity_level: str, goal: str):
    """
    Computes Basal Metabolic Rate using Mifflin-St Jeor equation
    and Total Daily Energy Expenditure (TDEE).
    """
    if gender.lower() == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        
    activity_multipliers = {
        "Sedentary (Desk Job, little exercise)": 1.2,
        "Lightly Active (1-3 days/week exercise)": 1.375,
        "Moderately Active (3-5 days/week moderate exercise)": 1.55,
        "Very Active (6-7 days/week hard exercise)": 1.725,
        "Extra Active (Physical job + daily training)": 1.9
    }
    
    mult = activity_multipliers.get(activity_level, 1.375)
    tdee = bmr * mult
    
    goal_deltas = {
        "Fat Loss (-500 kcal deficit)": -500,
        "Aggressive Cut (-750 kcal deficit)": -750,
        "Lean Muscle Gain (+300 kcal surplus)": +300,
        "Weight Maintenance (0 kcal)": 0
    }
    
    target_cal = round(tdee + goal_deltas.get(goal, 0))
    # Safety floor
    if target_cal < 1200:
        target_cal = 1200
        
    # Macro distribution (High protein / balanced sports nutrition)
    # Protein: 2.0g per kg of bodyweight
    protein_g = round(weight_kg * 2.0)
    protein_cal = protein_g * 4
    
    # Fats: 25% of target calories
    fat_cal = target_cal * 0.25
    fats_g = round(fat_cal / 9)
    
    # Carbs: remainder
    carb_cal = target_cal - (protein_cal + fat_cal)
    carbs_g = max(round(carb_cal / 4), 50)
    
    return {
        "bmr": round(bmr),
        "tdee": round(tdee),
        "target_calories": target_cal,
        "protein_g": protein_g,
        "carbs_g": carbs_g,
        "fats_g": fats_g
    }

def build_planner_prompt(metrics: dict, dietary: str, goal: str) -> str:
    return f"""
You are a licensed sports nutritionist and dietetic planner.
Generate a structured 7-day meal plan and consolidated grocery checklist conforming strictly to these parameters:
Target Daily Calories: {metrics['target_calories']} kcal
Target Macros: Protein {metrics['protein_g']}g, Carbs {metrics['carbs_g']}g, Fats {metrics['fats_g']}g
Dietary Constraint: {dietary}
Primary Goal: {goal}

Return a STRICT JSON object with these exact keys:
{{
  "user_summary": {{
    "bmr_kcal": {metrics['bmr']},
    "tdee_kcal": {metrics['tdee']},
    "target_calories": {metrics['target_calories']},
    "macro_split_target": {{"protein_g": {metrics['protein_g']}, "carbs_g": {metrics['carbs_g']}, "fats_g": {metrics['fats_g']}}}
  }},
  "plan_days": [
    {{
      "day": "Monday",
      "meals": [
        {{"type": "Breakfast", "name": "Detailed healthy meal name", "kcal": 400, "protein_g": 30, "carbs_g": 40, "fats_g": 12}},
        {{"type": "Lunch", "name": "Detailed healthy meal name", "kcal": 550, "protein_g": 45, "carbs_g": 50, "fats_g": 18}},
        {{"type": "Snack", "name": "Detailed healthy snack name", "kcal": 200, "protein_g": 15, "carbs_g": 20, "fats_g": 6}},
        {{"type": "Dinner", "name": "Detailed healthy dinner name", "kcal": 550, "protein_g": 45, "carbs_g": 45, "fats_g": 18}}
      ]
    }}
  ],
  "grocery_list": {{
    "Fresh Produce": ["Item 1 with quantity", "Item 2"],
    "Lean Proteins": ["Item 1 with quantity", "Item 2"],
    "Complex Carbohydrates & Grains": ["Item 1", "Item 2"],
    "Dairy & Plant Alternatives": ["Item 1", "Item 2"],
    "Pantry, Oils & Seasonings": ["Item 1", "Item 2"]
  }}
}}
Generate all 7 days (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday).
Return ONLY valid JSON.
"""

def render_meal_planner_tab(engine: FoodVerseAIEngine):
    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h2 style="font-weight: 800; color: #F8FAFC; margin-bottom: 0.3rem;">📊 Personalized TDEE Meal Planner & Grocery Engine</h2>
            <p style="color: #94A3B8; font-size: 0.98rem;">
                Scientific metabolic calculations using the Mifflin-St Jeor formula paired with dynamic 7-day adaptive nutrition scheduling and automated grocery aisle consolidation.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_input, col_display = st.columns([1, 1], gap="large")
    
    with col_input:
        st.markdown("#### 1. Biometric Profile & Goals")
        
        f1, f2 = st.columns(2)
        with f1:
            age = st.number_input("Age (years):", min_value=16, max_value=90, value=28)
            gender = st.selectbox("Biological Sex:", ["Male", "Female"])
            height = st.number_input("Height (cm):", min_value=120, max_value=230, value=178)
        with f2:
            weight = st.number_input("Weight (kg):", min_value=40.0, max_value=200.0, value=75.0, step=0.5)
            goal = st.selectbox("Primary Fitness Target:", [
                "Fat Loss (-500 kcal deficit)",
                "Lean Muscle Gain (+300 kcal surplus)",
                "Weight Maintenance (0 kcal)",
                "Aggressive Cut (-750 kcal deficit)"
            ])
            activity = st.selectbox("Weekly Physical Activity:", [
                "Sedentary (Desk Job, little exercise)",
                "Lightly Active (1-3 days/week exercise)",
                "Moderately Active (3-5 days/week moderate exercise)",
                "Very Active (6-7 days/week hard exercise)",
                "Extra Active (Physical job + daily training)"
            ], index=2)
            
        st.markdown("#### 2. Dietary Framework")
        dietary = st.selectbox("Nutritional Regime:", [
            "High Protein Mediterranean",
            "Plant-Based Vegan",
            "Keto / Low-Carb High-Fat",
            "Diabetic-Friendly Low-GI",
            "Gluten-Free Clean Eating",
            "Paleo / Whole Foods"
        ])
        
        # Calculate BMR/TDEE live
        metrics = calculate_bmr_tdee(gender, weight, height, age, activity, goal)
        
        st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 14px; margin-top: 1rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                    <span style="color: #94A3B8;">Base Metabolic Rate (BMR):</span>
                    <strong style="color: #F8FAFC;">{metrics['bmr']} kcal</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                    <span style="color: #94A3B8;">Total Daily Energy Expenditure (TDEE):</span>
                    <strong style="color: #F8FAFC;">{metrics['tdee']} kcal</strong>
                </div>
                <div style="display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 8px;">
                    <span style="color: #10B981; font-weight: 700;">Target Daily Caloric Intake:</span>
                    <strong style="color: #10B981; font-size: 1.15rem; font-family: monospace;">{metrics['target_calories']} kcal/day</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        calc_btn = st.button("🚀 Generate 7-Day Meal Schedule & Grocery List", use_container_width=True)

    with col_display:
        if calc_btn:
            with st.spinner("🥗 Computing 7-day macro targets and aisle-organized grocery list..."):
                prompt = build_planner_prompt(metrics, dietary, goal)
                result = engine.generate_text_response(prompt, task_type="meal_planner")
                st.session_state["meal_planner_result"] = result
                st.session_state["meal_planner_metrics"] = metrics
                
        if "meal_planner_result" in st.session_state and st.session_state["meal_planner_result"]:
            res = st.session_state["meal_planner_result"]
            m = st.session_state.get("meal_planner_metrics", metrics)
            
            # Header summary
            st.markdown(f"""
                <div class="food-card" style="border-top: 4px solid #10B981;">
                    <div class="food-card-title">
                        <span>Personalized Daily Blueprint</span>
                        <span class="badge-fresh">{m['target_calories']} KCAL / DAY</span>
                    </div>
                    <div style="display: flex; gap: 12px; margin-top: 0.8rem;">
                        <span class="stat-chip">🍗 <strong>Protein:</strong> {m['protein_g']}g</span>
                        <span class="stat-chip">🍚 <strong>Carbs:</strong> {m['carbs_g']}g</span>
                        <span class="stat-chip">🥑 <strong>Fats:</strong> {m['fats_g']}g</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Day selector tabs
            days = res.get("plan_days", [])
            if days:
                st.markdown("#### 🗓️ 7-Day Adaptive Meal Schedule")
                day_names = [d.get("day", f"Day {i+1}") for i, d in enumerate(days)]
                selected_day_name = st.selectbox("Select Day to View:", day_names)
                
                # Find selected day object
                selected_day = next((d for d in days if d.get("day") == selected_day_name), days[0])
                meals = selected_day.get("meals", [])
                
                day_cal = sum(ml.get("kcal", 0) for ml in meals)
                day_prot = sum(ml.get("protein_g", 0) for ml in meals)
                
                st.caption(f"Daily Total: **{day_cal} kcal** | **{day_prot}g Protein**")
                
                for ml in meals:
                    ml_type = ml.get("type", "Meal")
                    ml_name = ml.get("name", "")
                    kcal = ml.get("kcal", 0)
                    p = ml.get("protein_g", 0)
                    c = ml.get("carbs_g", 0)
                    f = ml.get("fats_g", 0)
                    
                    st.markdown(f"""
                        <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 12px; margin-bottom: 8px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <strong style="color: #38BDF8; font-size: 0.85rem; text-transform: uppercase;">{ml_type}</strong>
                                <span style="font-family: monospace; font-size: 0.85rem; color: #10B981; font-weight: 700;">{kcal} kcal</span>
                            </div>
                            <div style="color: #F8FAFC; font-weight: 600; font-size: 0.95rem; margin: 4px 0;">{ml_name}</div>
                            <div style="font-size: 0.8rem; color: #94A3B8;">
                                P: <span style="color:#CBD5E1;">{p}g</span> | C: <span style="color:#CBD5E1;">{c}g</span> | F: <span style="color:#CBD5E1;">{f}g</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
            # Automated Grocery Shopping List
            st.markdown("#### 🛒 Consolidated Grocery Shopping List (By Aisle)")
            grocery = res.get("grocery_list", {})
            
            export_text_lines = [
                f"# Food Verse AI - 7-Day Meal Plan & Grocery List",
                f"Target Calories: {m['target_calories']} kcal/day",
                f"Macros: {m['protein_g']}g P | {m['carbs_g']}g C | {m['fats_g']}g F",
                "",
                "## GROCERY SHOPPING LIST"
            ]
            
            for aisle, items in grocery.items():
                with st.expander(f"📦 {aisle} ({len(items)} items)", expanded=True):
                    export_text_lines.append(f"\n### {aisle}")
                    for item in items:
                        st.markdown(f"- [ ] {item}")
                        export_text_lines.append(f"- [ ] {item}")
                        
            export_content = "\n".join(export_text_lines)
            
            st.download_button(
                label="📥 Download Plan & Grocery List (.MD)",
                data=export_content,
                file_name="foodverse_7day_meal_plan.md",
                mime="text/markdown",
                use_container_width=True
            )
        else:
            st.markdown("""
                <div class="food-card" style="text-align: center; padding: 3rem 1.5rem;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">📊</div>
                    <h3 style="color: #F8FAFC;">Awaiting Meal Plan Generation</h3>
                    <p style="color: #94A3B8; max-width: 400px; margin: 0 auto; font-size: 0.95rem;">
                        Input your biometrics, target goals, and dietary preferences on the left to compute your exact Mifflin-St Jeor TDEE and 7-day schedule.
                    </p>
                </div>
            """, unsafe_allow_html=True)
