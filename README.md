# 🥗 Food Verse AI – Multimodal Food Intelligence Agent
### Skill Wallet Capstone Project 3 • Platform ID: `6ac4ca021dcde6d7857c169a`
> **Category:** Generative AI | Nutrition, Freshness & Kitchen Safety  
> **Tech Stack:** Python 3.9+, Streamlit, Plotly, Google GenAI (Gemini 2.5 / 1.5), Groq, Pillow, JSON Data Contracts

---

## 🌟 Executive Overview
**Food Verse AI** is a state-of-the-art multimodal food intelligence ecosystem engineered to solve the interconnected challenges of modern dietary management, culinary waste prevention, and commercial food service sanitation. 

By unifying multimodal computer vision, clinical dietetic formulations, post-harvest decay diagnostics, and HACCP compliance standards, Food Verse AI acts as an autonomous digital food scientist, chef coach, and sanitary auditor.

---

## 🎥 Working Demo Video (1.5 Min Walkthrough)
A complete 90-second working demonstration video capturing all 5 core epics in real-time is saved directly in this repository:
- 🎬 **MP4 High-Def Video:** [`food_verse_ai_demo.mp4`](./food_verse_ai_demo.mp4) *(Duration: 90.1s | H.264)*
- 🎞️ **Animated WebP Recording:** [`food_verse_ai_demo.webp`](./food_verse_ai_demo.webp) *(High-fidelity web playback)*

---

## 🎯 Epics & Architecture

```
Food Verse AI Ecosystem
│
├── 🥗 Tab 1: Food Recognition & Nutrition Breakdown (Epic 2)
│   ├── Visual Dish & Cuisine Classification
│   ├── Authentic Ingredients & Portion Size Estimation
│   ├── Detailed Macros (Protein, Carbs, Fats, Fiber, Sugar, Sodium)
│   ├── Interactive Plotly Macronutrient Calorie Donut
│   ├── Allergen & Food Sensitivity Matrix (Gluten, Dairy, Nuts, Soy)
│   └── Composite Health Score (1-100) & Dietitian Analysis
│
├── 🔬 Tab 2: Food Freshness & Spoilage Diagnostic (Epic 3)
│   ├── Visual Decay Biomarker Analysis (Texture, Oxidation, Dehydration, Mold)
│   ├── Freshness Classification: [Fresh 🟢 | Moderately Fresh 🟡 | Spoiled 🔴]
│   ├── Spoilage Decay Probability Gauge (0 - 100%)
│   ├── Actionable Directives: (Safe | 24h Window | Discard - Biological Hazard)
│   └── Scientific Preservation Storage Protocols (Ethylene, Temp, Humidity)
│
├── 🛡️ Tab 3: Commercial Kitchen Hygiene & HACCP Compliance (Epic 4)
│   ├── Food Handler PPE Surveillance (Hairnet / Chef Hat & Nitrile Gloves)
│   ├── Workstation Sanitization State Audit
│   ├── Cross-Contamination Hazard Detection (Raw Poultry near Ready-to-Eat)
│   ├── Kitchen Hygiene Compliance Score (%) & Letter Grade
│   └── Itemized Violation Logs with FDA Food Code Citations & Remedial Steps
│
├── 🍳 Tab 4: Smart Kitchen Recipe Assistant (Epic 4)
│   ├── Dynamic Pantry Stock Inventory Selector & Custom Input
│   ├── Dietary Constraints (High Protein, Keto, Vegan, Gluten-Free, Diabetic-Friendly)
│   ├── Automated Macro & Calorie Estimation per Serving
│   ├── Clear Step-by-Step Culinary Instructions with Executive Chef Tips
│   └── Smart Ingredient Substitutions & Zero-Waste Sustainability Hacks
│
└── 📊 Tab 5: Personalized TDEE Meal Planner & Grocery Engine (Epic 5)
    ├── Biometric Profile Form (Age, Biological Sex, Height, Weight, Activity Multiplier)
    ├── Basal Metabolic Rate (Mifflin-St Jeor Equation) & TDEE Calorie Targets
    ├── 7-Day Adaptive Day-by-Day Nutrition Schedule (Breakfast, Lunch, Snack, Dinner)
    ├── Consolidated Grocery Shopping Checklist Organized by Aisles
    └── 1-Click Markdown / Text Export of Weekly Meal Plan & Shopping List
```

---

## 🚀 Key Technical Highlights

1. **Dual Engine Architecture (Zero Barrier to Entry)**
   - **Live Multimodal Mode:** Connects seamlessly to Gemini 2.5 / 1.5 Flash or Groq Vision models.
   - **Standalone Demonstration Mode:** Pre-calibrated food science demonstration engine enabled by default, guaranteeing 100% turnkey operation with instant 1-click test drives even without entering API keys or incurring rate limits.

2. **Zero External Database Dependencies**
   - Engineered with stateless session architecture, requiring zero SQL/NoSQL databases.
   - Perfectly architected for instant 1-click deployment on **Streamlit Community Cloud**.

3. **Curated Visual Test Gallery**
   - Includes synthesized high-resolution culinary, perishable, and kitchen inspection samples right out of the box (`sample_data/`) so evaluators can run full diagnostics immediately without needing to hunt for sample photos.

4. **Medical & Food Safety Rigor**
   - Nutrition calculations adhere to standard caloric conversion factors (4-4-9 macro rules).
   - Basal Metabolic Rate calculated via the clinical **Mifflin-St Jeor Equation**.
   - Hygiene inspection adheres to **FDA Food Code** cross-contamination and sanitation guidelines.

---

## 📂 Project Directory Structure

```
d:/project2/
├── .streamlit/
│   └── config.toml           # Theme, styling, and server configuration
├── assets/
│   └── styles.css            # Modern culinary dark mode & glassmorphism CSS
├── modules/
│   ├── __init__.py
│   ├── ai_engine.py          # Unified Multimodal AI Client (Gemini, Groq, Fallback)
│   ├── food_recognition.py   # Epic 2: Dish identification, macro breakdown & chart
│   ├── freshness_detector.py # Epic 3: Spoilage stage, biomarkers & storage tips
│   ├── kitchen_hygiene.py    # Epic 4: HACCP commercial kitchen safety surveillance
│   ├── recipe_coach.py       # Epic 4: Pantry inventory matching & chef recipes
│   └── meal_planner.py       # Epic 5: Mifflin-St Jeor TDEE & 7-day adaptive planner
├── sample_data/              # Preloaded sample test images for 1-click trials
│   ├── sample_salmon_bowl.jpg
│   ├── sample_fresh_apple.jpg
│   ├── sample_spoiled_berries.jpg
│   ├── sample_kitchen_compliant.jpg
│   └── sample_kitchen_hazard.jpg
├── scripts/
│   └── generate_samples.py   # Synthetic test asset generator script
├── app.py                    # Main Streamlit Application Entrypoint
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git exclusions
└── README.md                 # Complete project documentation
```

---

## 🛠️ Local Installation & Setup

### Prerequisites
- Python 3.9, 3.10, or 3.11
- Git

### 1. Clone & Enter Repository
```bash
git clone <your-repo-url>
cd project2
```

### 2. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 3. (Optional) Configure API Keys
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Provide your `GEMINI_API_KEY` or `GROQ_API_KEY` if you wish to run live API calls.  
*(Note: If left empty, the application will run in Standalone Demonstration Mode).*

### 4. Launch Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ 1-Click Deployment to Streamlit Community Cloud

1. Push this repository to GitHub:
   ```bash
   git add .
   git commit -m "feat: complete Food Verse AI multimodal food intelligence agent"
   git push origin main
   ```
2. Navigate to [share.streamlit.io](https://share.streamlit.io/).
3. Select your repository, branch `main`, and main file path `app.py`.
4. (Optional) Add `GEMINI_API_KEY` in the Advanced Settings / Secrets section.
5. Click **Deploy!**

---

## 📜 License & Compliance
Engineered for Skill Wallet Capstone Project 3 (Platform ID: `6ac4ca021dcde6d7857c169a`).  
HACCP audit metrics conform to FDA Food Code protocols.
