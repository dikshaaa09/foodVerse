import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from modules.ai_engine import FoodVerseAIEngine

FRESHNESS_DIAGNOSTIC_PROMPT = """
You are an expert post-harvest food scientist and microbial decay diagnostic specialist.
Examine the perishable raw food item in the image (fruits, vegetables, meats, or dairy).
Return a STRICT JSON object with these exact keys:
{
  "item_detected": "Name of food item and scientific or commercial classification",
  "freshness_stage": "Fresh" OR "Moderately Fresh" OR "Spoiled",
  "spoilage_risk_percentage": 15,
  "visual_biomarkers": {
    "surface_texture": "Evaluation of firm cell structure, turgor, softening, or liquefaction",
    "discoloration": "Evidence of enzymatic browning, dark spots, or oxidation",
    "wrinkling_dehydration": "Epidermal shriveling, moisture loss, or skin integrity",
    "mold_fungal_growth": "Presence or absence of fungal filaments, spores, or microbial colonies"
  },
  "food_safety_verdict": "Safe to consume immediately / Consume within 24h (cook thoroughly) / Discard immediately - Biological Hazard",
  "consumption_window": "Estimated safe consumption timeframe (e.g. 7-10 Days, 24 Hours, 0 Hours)",
  "health_risks": [
    "Specific health risks or toxin alerts if consumed"
  ],
  "proper_storage_tips": [
    "Temperature & refrigeration recommendation",
    "Humidity & airflow advice",
    "Ethylene isolation or container recommendation"
  ]
}
Return ONLY valid JSON.
"""

def create_spoilage_gauge(risk_pct: int):
    """Creates a sleek Plotly gauge chart for spoilage risk."""
    color = "#10B981" if risk_pct < 35 else ("#F59E0B" if risk_pct < 70 else "#F43F5E")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_pct,
        title={'text': "Spoilage Decay Probability", 'font': {'color': "#94A3B8", 'size': 14}},
        number={'suffix': "%", 'font': {'color': color, 'size': 32, 'family': "JetBrains Mono"}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "#475569"},
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': "#1E293B",
            'borderwidth': 1,
            'bordercolor': "#334155",
            'steps': [
                {'range': [0, 35], 'color': 'rgba(16, 185, 129, 0.15)'},
                {'range': [35, 70], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [70, 100], 'color': 'rgba(244, 63, 94, 0.15)'}
            ]
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=30, b=10, l=25, r=25),
        height=200
    )
    return fig

def render_freshness_detector_tab(engine: FoodVerseAIEngine):
    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h2 style="font-weight: 800; color: #F8FAFC; margin-bottom: 0.3rem;">🔬 Food Freshness & Spoilage Diagnostic</h2>
            <p style="color: #94A3B8; font-size: 0.98rem;">
                Multi-spectral visual diagnostic detecting surface cellular degradation, enzymatic oxidation, dehydration wrinkling, and fungal mycelia to prevent food waste and foodborne illnesses.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_input, col_display = st.columns([1, 1], gap="large")
    chosen_image = None
    image_caption = "Perishable Food Image"
    
    with col_input:
        st.markdown("#### 1. Perishable Item Input")
        source_opt = st.radio("Choose Image Source:", ["Preset Fresh / Spoiled Samples", "Upload Perishable Photo"], horizontal=True, key="freshness_source_radio")
        
        if source_opt == "Upload Perishable Photo":
            uploaded_file = st.file_uploader("Upload raw produce, meat, or dairy (JPG, PNG, WEBP)", type=["jpg", "jpeg", "png", "webp"], key="freshness_uploader")
            if uploaded_file is not None:
                chosen_image = Image.open(uploaded_file)
                image_caption = f"Uploaded Item: {uploaded_file.name}"
        else:
            sample_choice = st.selectbox(
                "Select a Perishable Diagnostic Case:",
                ["Fresh Honeycrisp Apple (Optimal Quality)", "Spoiled Moldy Strawberries (Fungal Infestation)", "Fresh Mediterranean Bowl"],
                key="freshness_preset_select"
            )
            sample_paths = {
                "Fresh Honeycrisp Apple (Optimal Quality)": "sample_data/sample_fresh_apple.jpg",
                "Spoiled Moldy Strawberries (Fungal Infestation)": "sample_data/sample_spoiled_berries.jpg",
                "Fresh Mediterranean Bowl": "sample_data/sample_salmon_bowl.jpg"
            }
            if sample_choice in sample_paths:
                chosen_image = Image.open(sample_paths[sample_choice])
                image_caption = f"Preset Case: {sample_choice}"
        
        if chosen_image is not None:
            st.image(chosen_image, caption=image_caption, use_container_width=True)
            diagnose_btn = st.button("🧪 Run Spoilage Diagnostic", use_container_width=True)
        else:
            st.info("👆 Upload or choose a perishable food sample above to run diagnostic.")
            diagnose_btn = False

    with col_display:
        if chosen_image is not None and diagnose_btn:
            with st.spinner("🔬 Scanning epidermal integrity, spore formation & cellular turgor..."):
                result = engine.analyze_image_with_prompt(chosen_image, FRESHNESS_DIAGNOSTIC_PROMPT, task_type="freshness_detection")
                st.session_state["freshness_result"] = result
        
        if "freshness_result" in st.session_state and st.session_state["freshness_result"]:
            res = st.session_state["freshness_result"]
            
            if "_api_notice" in res:
                st.caption(f"ℹ️ {res['_api_notice']}")

            item_detected = res.get("item_detected", "Food Item")
            stage = res.get("freshness_stage", "Fresh")
            risk_pct = res.get("spoilage_risk_percentage", 10)
            verdict = res.get("food_safety_verdict", "Safe to consume")
            window = res.get("consumption_window", "3-5 Days")

            # Determine badge styling
            if stage.lower() == "fresh":
                badge_class = "badge-fresh"
                stage_icon = "🟢"
                verdict_color = "#10B981"
            elif stage.lower() in ["moderately fresh", "moderate"]:
                badge_class = "badge-moderate"
                stage_icon = "🟡"
                verdict_color = "#F59E0B"
            else:
                badge_class = "badge-spoiled"
                stage_icon = "🔴"
                verdict_color = "#F43F5E"

            st.markdown(f"""
                <div class="food-card" style="border-left: 5px solid {verdict_color};">
                    <div class="food-card-title">
                        <span>{item_detected}</span>
                        <span class="{badge_class}">
                            {stage_icon} {stage.upper()}
                        </span>
                    </div>
                    <div style="background: rgba(30, 41, 59, 0.5); padding: 12px 16px; border-radius: 10px; margin-top: 0.8rem;">
                        <div style="font-size: 0.8rem; text-transform: uppercase; color: #94A3B8; font-weight: 700;">Food Safety Direct Action:</div>
                        <div style="font-size: 1.15rem; font-weight: 700; color: {verdict_color}; margin-top: 2px;">
                            {verdict}
                        </div>
                        <div style="font-size: 0.85rem; color: #CBD5E1; margin-top: 4px;">
                            ⏱️ <strong>Usable Consumption Window:</strong> {window}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Gauge chart
            st.plotly_chart(create_spoilage_gauge(risk_pct), use_container_width=True)
            
            # Visual Biomarkers Evaluation
            st.markdown("#### 🔬 Visual Biomarker Breakdown")
            biomarkers = res.get("visual_biomarkers", {})
            b_col1, b_col2 = st.columns(2)
            with b_col1:
                st.markdown(f"""
                    <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 12px; margin-bottom: 8px;">
                        <strong style="color: #F8FAFC;">🍎 Surface Texture & Turgor</strong><br>
                        <span style="font-size: 0.85rem; color: #CBD5E1;">{biomarkers.get('surface_texture', 'Intact')}</span>
                    </div>
                    <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 12px;">
                        <strong style="color: #F8FAFC;">🍂 Oxidation & Browning</strong><br>
                        <span style="font-size: 0.85rem; color: #CBD5E1;">{biomarkers.get('discoloration', 'None')}</span>
                    </div>
                """, unsafe_allow_html=True)
            with b_col2:
                st.markdown(f"""
                    <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 12px; margin-bottom: 8px;">
                        <strong style="color: #F8FAFC;">💧 Moisture & Dehydration</strong><br>
                        <span style="font-size: 0.85rem; color: #CBD5E1;">{biomarkers.get('wrinkling_dehydration', 'Normal hydration')}</span>
                    </div>
                    <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 12px;">
                        <strong style="color: #F8FAFC;">🦠 Mold & Fungal Sporulation</strong><br>
                        <span style="font-size: 0.85rem; color: #CBD5E1;">{biomarkers.get('mold_fungal_growth', 'Negative')}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            # Health Risks if any
            risks = res.get("health_risks", [])
            if risks:
                st.markdown("#### ⚠️ Pathogen & Health Advisories")
                for r in risks:
                    st.markdown(f"""
                        <div class="hazard-alert" style="margin-bottom: 6px;">
                            <span style="color: #FCA5A5; font-size: 0.88rem;">{r}</span>
                        </div>
                    """, unsafe_allow_html=True)

            # Proper Storage & Preservation Tips
            storage_tips = res.get("proper_storage_tips", [])
            if storage_tips:
                st.markdown("#### 🧊 Scientific Preservation & Storage Protocols")
                for tip in storage_tips:
                    st.markdown(f"""
                        <div style="display: flex; gap: 8px; margin-bottom: 6px; align-items: flex-start;">
                            <span style="color: #10B981; font-weight: bold;">✔</span>
                            <span style="color: #CBD5E1; font-size: 0.9rem;">{tip}</span>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="food-card" style="text-align: center; padding: 3rem 1.5rem;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🔬</div>
                    <h3 style="color: #F8FAFC;">Awaiting Spoilage Diagnostic</h3>
                    <p style="color: #94A3B8; max-width: 400px; margin: 0 auto; font-size: 0.95rem;">
                        Inspect raw fruits, meats, or produce for active fungal colonies, structural breakdown, and safe consumption lifespan.
                    </p>
                </div>
            """, unsafe_allow_html=True)
