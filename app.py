import streamlit as st
import pandas as pd
import json
import random
from datetime import date

st.set_page_config(page_title="Me & Myself", layout="centered", initial_sidebar_state="expanded")

# ==================== DESIGN ====================
st.markdown("""
<style>
    .main {background-color: #0a0a0a; color: #ffffff;}
    h1 {color: #ff4b4b; font-size: 2.3em;}
    .stButton>button {background-color: #ff4b4b; color: white; border-radius: 12px; height: 52px; font-weight: bold;}
    .quote {background: linear-gradient(90deg, #1e1e1e, #2a2a2a); padding: 22px; border-radius: 16px; border-left: 6px solid #ff4b4b;}
    .metric {background-color: #1e1e1e; padding: 16px; border-radius: 12px; text-align: center;}
</style>
""", unsafe_allow_html=True)

st.title("💪 Me & Myself")
st.caption("Dein persönlicher Klimmzüge & Spagat Coach")

# ==================== DATEIEN LADEN ====================
def load_json(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

quotes = load_json("quotes.json").get("quotes", [])
training_plan = load_json("training_plan.json")
nutrition_plan = load_json("nutrition_plan.json")

# Täglicher Spruch
today = date.today()
random.seed(today.toordinal())
daily_quote = random.choice(quotes) if quotes else {}

st.markdown(f"""
<div class="quote">
    "{daily_quote.get('text', 'Bleib dran!')}"<br>
    <strong>— {daily_quote.get('author', 'Me & Myself')}</strong>
</div>
""", unsafe_allow_html=True)

# ==================== USER DATA ====================
if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "pullups": [],
        "front_split": [],
        "side_split": [],
        "streak": 0,
        "last_training": None
    }

uploaded = st.file_uploader("📤 Backup laden", type="json", label_visibility="collapsed")
if uploaded:
    st.session_state.user_data = json.load(uploaded)
    st.success("✅ Backup geladen!")

# ===================== SIDEBAR ====================
with st.sidebar:
    st.header("📊 Dein Status")
    st.metric("Aktueller Streak", f"{st.session_state.user_data['streak']} Tage 🔥")
    st.metric("Trainings-Tage", len({x["Datum"] for x in st.session_state.user_data["pullups"]}))
    
    st.divider()
    if st.button("💾 Backup herunterladen"):
        backup = json.dumps(st.session_state.user_data, indent=2, ensure_ascii=False)
        st.download_button("JSON speichern", backup, f"me_myself_backup_{today}.json", "application/json")

# ===================== TABS =====================
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🏋️ Training", "🥗 Ernährung", "📈 Fortschritt"])

with tab1:
    st.subheader(f"Guten Tag! Heute ist {today.strftime('%A, %d. %B')}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        best_pull = max([x.get("Wiederholungen",0) for x in st.session_state.user_data["pullups"]] or [0])
        st.metric("Beste Klimmzüge", f"{best_pull} WH")
    with col2:
        best_front = min([x.get("cm", 999) for x in st.session_state.user_data["front_split"]] or [999])
        st.metric("Bester Front Spagat", f"{best_front} cm")
    with col3:
        st.metric("Streak", f"{st.session_state.user_data['streak']} Tage")

with tab2:
    subtab1, subtab2 = st.tabs(["💪 Kraft", "🧘 Dehnung"])
    with subtab1:
        st.subheader("Krafttraining")
        for ex in training_plan.get("phasen", [{}])[0].get("kraft", []):
            st.checkbox(ex)
        reps = st.number_input("Saubere Klimmzüge heute", 0, 30, 0)
        if st.button("✅ Kraft-Einheit abschließen", type="primary"):
            st.session_state.user_data["pullups"].append({"Datum": str(today), "Wiederholungen": reps})
            st.success("Super gemacht! 🔥")
            st.session_state.user_data["streak"] += 1

    with subtab2:
        st.subheader("Dehnung")
        for ex in training_plan.get("phasen", [{}])[0].get("dehnung", []):
            st.checkbox(ex)
        front = st.number_input("Front Spagat (cm)", 0.0, 50.0, 20.0, 0.5)
        if st.button("✅ Dehn-Einheit abschließen", type="primary"):
            st.session_state.user_data["front_split"].append({"Datum": str(today), "cm": front})
            st.success("Sehr gut!")

with tab3:
    st.subheader("🥗 Ernährung heute")
    for name, desc in nutrition_plan.get("tagesstruktur", {}).items():
        st.checkbox(f"{name} – {desc}")
    if st.button("✅ Ernährungstag speichern"):
        st.success("Eingetragen!")

with tab4:
    st.subheader("Dein Fortschritt")
    if st.session_state.user_data["pullups"]:
        df = pd.DataFrame(st.session_state.user_data["pullups"])
        st.line_chart(df.set_index("Datum")["Wiederholungen"])

st.divider()
st.caption("Me & Myself Coach • Alles bleibt auf deinem Gerät")
