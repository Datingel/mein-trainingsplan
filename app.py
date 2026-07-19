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
    .quote {background-color: #1e1e1e; padding: 20px; border-radius: 15px; border-left: 6px solid #ff4b4b; font-style: italic;}
</style>
""", unsafe_allow_html=True)

st.title("💪 Coach Max")
st.markdown("**Klimmzüge & Spagat Coach Me&Myself 2026**")

# ==================== LOAD QUOTES ====================
try:
    with open("quotes.json", "r", encoding="utf-8") as f:
        quotes_data = json.load(f)
        quotes = quotes_data["quotes"]
except:
    quotes = [{"text": "Disziplin ist die Brücke zwischen Zielen und Erfolg.", "author": "Jim Rohn"}]

# Täglicher Spruch (ändert sich jeden Tag)
today = date.today()
random.seed(today.toordinal())  # Gleicher Spruch für den ganzen Tag
daily_quote = random.choice(quotes)

st.markdown(f"""
<div class="quote">
    "{daily_quote['text']}"<br>
    <strong>— {daily_quote['author']}</strong>
</div>
""", unsafe_allow_html=True)

# ==================== DATA PERSISTENCE ====================
if "data" not in st.session_state:
    st.session_state.data = {
        "pullups": [], "front_split": [], "side_split": [],
        "completed_workouts": [], "nutrition_checks": []
    }

uploaded = st.file_uploader("Daten laden", type="json", label_visibility="collapsed")
if uploaded:
    st.session_state.data = json.load(uploaded)
    st.success("✅ Daten geladen!")

# ===================== TABS =====================
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Übersicht", "🏋️ Training", "🥗 Ernährung", "📈 Fortschritt"])

with tab1:
    st.subheader(f"Heute ist {date.today().strftime('%d. %B %Y')}")
    # ... (Rest wie in der vorherigen Version – Dashboard, Metriken, etc.)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Beste Klimmzüge", max([x.get("Wiederholungen",0) for x in st.session_state.data["pullups"]] or [0]))
    with col2:
        st.metric("Bester Front Spagat", f"{min([x.get('cm',999) for x in st.session_state.data['front_split']] or [999])} cm")

# Die anderen Tabs bleiben gleich wie in meiner letzten Version (Training mit Kraft/Dehnung, Ernährung, Fortschritt)

st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("💾 Daten herunterladen"):
        backup = json.dumps(st.session_state.data, indent=2, ensure_ascii=False)
        st.download_button("JSON herunterladen", backup, f"coach_max_{date.today()}.json", "application/json")

st.caption("Coach Max • Alle Daten bleiben auf deinem Gerät")
