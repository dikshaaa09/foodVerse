import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from modules.ai_engine import FoodVerseAIEngine

KITCHEN_HYGIENE_PROMPT = """
You are a senior OSHA and FDA HACCP commercial food safety inspector.
Conduct a rigorous visual sanitary audit on the kitchen environment or food preparation station in the image.
Analyze specifically for:
1. Hairnet / chef hat restraint compliance
2. Food-grade glove usage on food handlers
3. Workstation surface sanitization and cleanliness
4. Cross-contamination hazards (e.g. raw poultry/meat touching or adjacent to ready-to-eat produce or wooden surfaces)

Return a STRICT JSON object with these exact keys:
{
  "inspection_summary": "1-2 sentence executive audit summary",
  "hygiene_compliance_score": 85,
  "letter_grade": "Grade A+ / Grade A / Grade B / Grade C / Critical Warning",
  "audited_indicators": {
    "hairnet_chef_hat_compliance": {"status": "Fully Compliant / Non-Compliant", "details": "Specific finding"},
    "glove_usage_compliance": {"status": "Fully Compliant / Non-Compliant", "details": "Specific finding"},
    "sanitization_state": {"status": "Pristine / Satisfactory / Unsatisfactory", "details": "Specific finding"},
    "cross_contamination_hazard": {"status": "Zero Hazard / Moderate Risk / Severe Hazard", "details": "Specific finding"}
  },
  "itemized_violations": [
    {
      "id": "VIO-001",
      "severity": "CRITICAL" OR "MAJOR" OR "MINOR",
      "category": "Cross-Contamination / Personal Hygiene / Sanitization",
      "description": "Specific violation narrative",
      "haccp_code": "Relevant FDA Food Code section e.g. 3-302.11",
      "corrective_action": "Immediate mandated remedial step"
    }
  ],
  "recommendation": "Overall operational directive for kitchen management"
}
Return ONLY valid JSON.
"""

def create_compliance_gauge(score: int):
    """Visual compliance indicator gauge."""
    color = "#10B981" if score >= 85 else ("#F59E0B" if score >= 65 else "#F43F5E")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "HACCP Safety Compliance", 'font': {'color': "#94A3B8", 'size': 14}},
        number={'suffix': "%", 'font': {'color': color, 'size': 34, 'family': "JetBrains Mono"}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "#475569"},
            'bar': {'color': color, 'thickness': 0.35},
            'bgcolor': "#1E293B",
            'borderwidth': 1,
            'bordercolor': "#334155",
            'steps': [
                {'range': [0, 65], 'color': 'rgba(244, 63, 94, 0.2)'},
                {'range': [65, 85], 'color': 'rgba(245, 158, 11, 0.2)'},
                {'range': [85, 100], 'color': 'rgba(16, 185, 129, 0.2)'}
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

def render_kitchen_hygiene_tab(engine: FoodVerseAIEngine):
    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h2 style="font-weight: 800; color: #F8FAFC; margin-bottom: 0.3rem;">🛡️ Commercial Kitchen Hygiene & Safety Compliance</h2>
            <p style="color: #94A3B8; font-size: 0.98rem;">
                Autonomous computer vision surveillance auditing food handler PPE, glove & hair restraint protocols, surface sanitization, and pathogen cross-contamination vectors under FDA Food Code standards.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_input, col_display = st.columns([1, 1], gap="large")
    chosen_image = None
    image_caption = "Kitchen Station Image"
    
    with col_input:
        st.markdown("#### 1. Kitchen Station Footage / Image")
        source_opt = st.radio("Select Kitchen Media Source:", ["Preset Kitchen Audit Scenarios", "Upload Station Image / Frame"], horizontal=True, key="kitchen_source_radio")
        
        if source_opt == "Upload Station Image / Frame":
            uploaded_file = st.file_uploader("Upload commercial kitchen photo or video frame (JPG, PNG)", type=["jpg", "jpeg", "png"], key="kitchen_uploader")
            if uploaded_file is not None:
                chosen_image = Image.open(uploaded_file)
                image_caption = f"Uploaded Kitchen: {uploaded_file.name}"
        else:
            scenario_choice = st.selectbox(
                "Select a Preset Inspection Scenario:",
                [
                    "Compliant Commercial Station (Chef with PPE & Sanitizer)",
                    "Cross-Contamination Hazard (Raw Poultry near Ready-to-Eat Greens)"
                ],
                key="kitchen_preset_select"
            )
            scenario_paths = {
                "Compliant Commercial Station (Chef with PPE & Sanitizer)": "sample_data/sample_kitchen_compliant.jpg",
                "Cross-Contamination Hazard (Raw Poultry near Ready-to-Eat Greens)": "sample_data/sample_kitchen_hazard.jpg"
            }
            if scenario_choice in scenario_paths:
                chosen_image = Image.open(scenario_paths[scenario_choice])
                image_caption = f"Scenario: {scenario_choice}"
        
        if chosen_image is not None:
            st.image(chosen_image, caption=image_caption, use_container_width=True)
            audit_btn = st.button("🔍 Execute Safety Audit & HACCP Inspection", use_container_width=True)
        else:
            st.info("👆 Upload kitchen footage or choose a preloaded scenario above to conduct inspection.")
            audit_btn = False

    with col_display:
        if chosen_image is not None and audit_btn:
            with st.spinner("🕵️ Inspecting PPE restraints, sanitizer protocols, and cross-contamination hazards..."):
                result = engine.analyze_image_with_prompt(chosen_image, KITCHEN_HYGIENE_PROMPT, task_type="kitchen_hygiene")
                st.session_state["kitchen_hygiene_result"] = result
        
        if "kitchen_hygiene_result" in st.session_state and st.session_state["kitchen_hygiene_result"]:
            res = st.session_state["kitchen_hygiene_result"]
            
            if "_api_notice" in res:
                st.caption(f"ℹ️ {res['_api_notice']}")

            score = res.get("hygiene_compliance_score", 75)
            grade = res.get("letter_grade", "Grade B")
            summary = res.get("inspection_summary", "Audit completed.")
            score_color = "#10B981" if score >= 85 else ("#F59E0B" if score >= 65 else "#F43F5E")
            
            st.markdown(f"""
                <div class="food-card" style="border-top: 4px solid {score_color};">
                    <div class="food-card-title">
                        <span>HACCP Compliance Rating</span>
                        <span style="font-size: 0.9rem; background: rgba(30, 41, 59, 0.8); color: {score_color}; border: 1px solid {score_color}; padding: 4px 14px; border-radius: 9999px; font-weight: 700;">
                            {grade}
                        </span>
                    </div>
                    <p style="color: #CBD5E1; font-size: 0.92rem; margin-top: 0.4rem;">
                        {summary}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Compliance Gauge
            st.plotly_chart(create_compliance_gauge(score), use_container_width=True)
            
            # Audited Indicators Checklist
            st.markdown("#### 📋 Core Compliance Indicators")
            indicators = res.get("audited_indicators", {})
            
            ind_keys = [
                ("hairnet_chef_hat_compliance", "👨‍🍳 Hairnet / Headgear", "PPE Restraints"),
                ("glove_usage_compliance", "🧤 Single-Use Gloves", "Direct Contact Barrier"),
                ("sanitization_state", "🧼 Workstation Sanitization", "Surface Hygiene"),
                ("cross_contamination_hazard", "⚠️ Contamination Vectors", "Pathogen Isolation")
            ]
            
            c_cols = st.columns(2)
            for idx, (k, label, sub) in enumerate(ind_keys):
                item = indicators.get(k, {})
                status = item.get("status", "Unknown")
                details = item.get("details", "")
                
                is_ok = any(good in status.lower() for good in ["compliant", "pristine", "zero hazard", "satisfactory"])
                st_color = "#10B981" if is_ok else "#F43F5E"
                st_icon = "✅" if is_ok else "❌"
                
                col_target = c_cols[idx % 2]
                with col_target:
                    col_target.markdown(f"""
                        <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 10px; margin-bottom: 8px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <strong style="color: #F8FAFC; font-size: 0.9rem;">{label}</strong>
                                <span style="color: {st_color}; font-weight: 700; font-size: 0.82rem;">{st_icon} {status}</span>
                            </div>
                            <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 4px;">{details}</div>
                        </div>
                    """, unsafe_allow_html=True)
            
            # Itemized Violations Log
            violations = res.get("itemized_violations", [])
            st.markdown("#### 🚨 Itemized Violation Log & Remedial Actions")
            
            if not violations:
                st.markdown("""
                    <div class="safe-alert">
                        <strong>🎉 Zero Critical Violations Found!</strong><br>
                        <span style="font-size: 0.9rem; color: #CBD5E1;">Kitchen complies with standard operating food codes. Keep maintaining standard sanitation registers.</span>
                    </div>
                """, unsafe_allow_html=True)
            else:
                for vio in violations:
                    severity = vio.get("severity", "MAJOR")
                    s_color = "#F43F5E" if severity == "CRITICAL" else ("#F59E0B" if severity == "MAJOR" else "#3B82F6")
                    
                    st.markdown(f"""
                        <div class="hazard-alert" style="border-left-color: {s_color}; margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                                <span style="font-weight: 800; color: {s_color}; font-size: 0.85rem;">
                                    [{vio.get('id', 'VIO')}] {severity} VIOLATION - {vio.get('category')}
                                </span>
                                <span style="font-family: monospace; font-size: 0.75rem; background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px; color: #CBD5E1;">
                                    {vio.get('haccp_code', 'FDA-Code')}
                                </span>
                            </div>
                            <div style="font-size: 0.88rem; color: #F1F5F9; margin-bottom: 6px;">
                                {vio.get('description')}
                            </div>
                            <div style="font-size: 0.82rem; color: #94A3B8; background: rgba(0,0,0,0.25); padding: 6px 10px; border-radius: 6px;">
                                🛠️ <strong>Mandatory Corrective Action:</strong> {vio.get('corrective_action')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            # Executive Directive
            recom = res.get("recommendation", "")
            if recom:
                st.markdown(f"""
                    <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 8px; padding: 12px; margin-top: 1rem;">
                        <strong>📢 Inspector Directives to Kitchen Supervisor:</strong><br>
                        <span style="font-size: 0.9rem; color: #CBD5E1;">{recom}</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="food-card" style="text-align: center; padding: 3rem 1.5rem;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🛡️</div>
                    <h3 style="color: #F8FAFC;">Awaiting Kitchen Safety Inspection</h3>
                    <p style="color: #94A3B8; max-width: 400px; margin: 0 auto; font-size: 0.95rem;">
                        Audit food handler uniforms, nitrile glove compliance, sanitation registers, and cross-contamination hazards in seconds.
                    </p>
                </div>
            """, unsafe_allow_html=True)
