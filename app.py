import streamlit as st
import pandas as pd
import json
import random
from datetime import date

st.set_page_config(page_title="Coach Me&Myself", layout="centered")

# ==================== STYLES ====================
st.markdown("""
<style>
    .main {background-color: #0f0f0f;}
    h1, h2 {color: #ff4b4b;}
    .quote {background-color: #1e1e1e; padding: 20px; border-radius: 15px; border-left: 6px solid #ff4b4b;}
    .card {background-color: #1e1e1e; padding: 15px; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

st.title("💪 Coach Me&Myself")
st.markdown("**Klimmzüge & Spagat Coach 2026**")

# ==================== IMPORTS DER EXTERNEN DATEIEN ====================
@st.cache_data
def load_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

quotes_data = load_json("quotes.json")
training_data = load_json("training_plan.json")
nutrition_data = load_json("nutrition_plan.json")

# Täglicher Motivationsspruch
today = date.today()
random.seed(today.toordinal())
daily_quote = random.choice(quotes_data.get("quotes", [{}]))

st.markdown(f"""
<div class="quote">
    "{daily_quote.get('text', '')}"<br>
    <strong>— {daily_quote.get('author', '')}</strong>
</div>
""", unsafe_allow_html=True)

# ==================== DATA PERSISTENCE ====================
if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "pullups": [], "front_split": [], "side_split": [],
        "nutrition_checks": []
    }

uploaded = st.file_uploader("Daten laden", type="json", label_visibility="collapsed")
if uploaded:
    st.session_state.user_data = json.load(uploaded)
    st.success("✅ Fortschritt geladen!")

# ===================== TABS =====================
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Übersicht", "🏋️ Training", "🥗 Ernährung", "📈 Fortschritt"])

with tab1:
    st.subheader("Heutiger Überblick")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Beste Klimmzüge", Me&Myself([x.get("Wiederholungen",0) for x in st.session_state.user_data["pullups"]] or [0]))
    with col2:
        st.metric("Bester Spagat", f"{min([x.get('cm',999) for x in st.session_state.user_data['front_split']] or [999])} cm")

with tab2:
    sub1, sub2 = st.tabs(["💪 Kraft", "🧘 Dehnung"])
    with sub1:
        st.subheader("Kraft Training")
        for ex in training_data.get("kraft", []):
            st.checkbox(ex)
        reps = st.number_input("Saubere Klimmzüge heute", 0, 30, 0)
        if st.button("Kraft-Einheit speichern"):
            st.session_state.user_data["pullups"].append({"Datum": str(date.today()), "Wiederholungen": reps})
            st.success("Gespeichert!")
    
    with sub2:
        st.subheader("Dehnung")
        for ex in training_data.get("dehnung", []):
            st.checkbox(ex)
        front = st.number_input("Front Spagat (cm)", 0.0, 50.0, 20.0)
        if st.button("Dehn-Einheit speichern"):
            st.session_state.user_data["front_split"].append({"Datum": str(date.today()), "cm": front})
            st.success("Gespeichert!")

with tab3:
    st.subheader("Ernährung")
    for name, desc in nutrition_data.get("mahlzeiten", {}).items():
        st.checkbox(f"{name}: {desc}")
    if st.button("Ernährungstag speichern"):
        st.success("✅ Tag gespeichert!")

with tab4:
    st.subheader("Fortschritt")
    if st.session_state.user_data["pullups"]:
        df = pd.DataFrame(st.session_state.user_data["pullups"])
        st.line_chart(df.set_index("Datum")["Wiederholungen"])

# ==================== SAVE ====================
st.divider()
if st.button("💾 Daten herunterladen"):
    backup = json.dumps(st.session_state.user_data, indent=2, ensure_ascii=False)
    st.download_button("JSON herunterladen", backup, f"coach_Me&Myself_backup_{date.today()}.json", "application/json")

st.caption("Modulare Coach Me&Myself App • Daten bleiben lokal")
