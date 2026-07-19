import streamlit as st
import pandas as pd
from datetime import date, datetime
import json

st.set_page_config(page_title="Coach Max - Klimmzüge & Spagat", layout="centered")

# ==================== STYLES (Modernes Fitness-Design) ====================
st.markdown("""
<style>
    .main {background-color: #0f0f0f; color: #ffffff;}
    .stButton>button {background-color: #ff4b4b; color: white; border-radius: 8px;}
    h1, h2, h3 {color: #ff4b4b;}
    .metric-card {background-color: #1e1e1e; padding: 15px; border-radius: 12px; margin: 10px 0;}
</style>
""", unsafe_allow_html=True)

st.title("💪 Coach Max")
st.markdown("**Dein persönlicher Klimmzüge & Spagat Coach**")

# ==================== DATA PERSISTENCE ====================
if "data" not in st.session_state:
    st.session_state.data = {
        "pullups": [],
        "front_split": [],
        "side_split": [],
        "start_date": str(date.today())
    }

# Load from uploaded file
uploaded = st.file_uploader("Daten laden (JSON)", type="json", label_visibility="collapsed")
if uploaded is not None:
    st.session_state.data = json.load(uploaded)
    st.success("Daten erfolgreich geladen!")

# ==================== TABS ====================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard", 
    "📝 Training Loggen", 
    "🧘 Dehnprogramm", 
    "🥗 Ernährung & Plan"
])

# ===================== DASHBOARD =====================
with tab1:
    st.subheader("Dein Fortschritt 2026")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Bester Klimmzug", 
                  f"{max([x['Wiederholungen'] for x in st.session_state.data['pullups']], default=0)} WH")
    with col2:
        st.metric("Front Spagat", 
                  f"{min([x['cm'] for x in st.session_state.data['front_split']], default=999)} cm")
    with col3:
        st.metric("Wochen Trainiert", 
                  len(set([x['Datum'] for x in st.session_state.data['pullups']])))
    
    st.divider()
    
    if st.session_state.data["pullups"]:
        dfp = pd.DataFrame(st.session_state.data["pullups"])
        st.line_chart(dfp.set_index("Datum")["Wiederholungen"])
    
    # Download Button
    if st.button("💾 Daten auf Handy speichern"):
        json_str = json.dumps(st.session_state.data, indent=2, ensure_ascii=False)
        st.download_button(
            label="JSON-Datei herunterladen",
            data=json_str,
            file_name=f"coach_max_backup_{date.today()}.json",
            mime="application/json"
        )

# ===================== TRAINING LOGGEN =====================
with tab2:
    st.subheader("Training eintragen")
    col1, col2 = st.columns(2)
    
    with col1:
        reps = st.number_input("Saubere Klimmzüge heute", 0, 30, 0)
        if st.button("Klimmzüge speichern", type="primary"):
            st.session_state.data["pullups"].append({"Datum": str(date.today()), "Wiederholungen": reps})
            st.success("Eingetragen!")
    
    with col2:
        front = st.number_input("Front Spagat (cm)", 0.0, 50.0, 25.0, 0.5)
        side = st.number_input("Seitlicher Spagat (cm)", 0.0, 50.0, 30.0, 0.5)
        if st.button("Spagat speichern", type="primary"):
            st.session_state.data["front_split"].append({"Datum": str(date.today()), "cm": front})
            st.session_state.data["side_split"].append({"Datum": str(date.today()), "cm": side})
            st.success("Eingetragen!")

# ===================== DEHNPROGRAMM =====================
with tab3:
    st.subheader("🧘 Dehnprogramm – Coach Version")
    st.write("**Dauer:** 30–40 Minuten | **Häufigkeit:** 5–6x pro Woche")
    
    for week in ["Woche 1–4 (Grundlage)", "Woche 5–8 (Intensiv)", "Woche 9–12 (Fortgeschritten)"]:
        with st.expander(week):
            st.write("**Aufwärmen:** 5 Min leichte Bewegung")
            st.write("- Hüftbeuger Lunge: 3 × 60 Sek.")
            st.write("- Hamstring Stretch: 3 × 60 Sek.")
            st.write("- Schmetterling + Vorbeuge: 3 × 60 Sek.")
            st.write("- Seitlicher Spagat: 3 × 45–90 Sek.")
            st.write("- Pigeon Pose links/rechts")
            st.write("- Frog Pose")
            st.write("**Tipp:** Tief atmen, 2–3 Sekunden pro Ausatmung tiefer gehen.")

# ===================== ERNÄHRUNG & GROSSER PLAN =====================
with tab4:
    st.subheader("🥗 Ernährungs- & Jahresplan")
    
    st.markdown("### 2026 Jahresziele")
    st.write("**Q3 2026 (bis September):** 8–10 saubere Klimmzüge + voller Front Spagat")
    st.write("**Q4 2026 (Oktober–Dezember):** 12+ Klimmzüge + perfekter Spagat beidseitig")
    
    st.divider()
    
    phase = st.selectbox("Welche Phase bist du?", 
                        ["Phase 1: Grundlage (Juli–August)", 
                         "Phase 2: Aufbau (September–Oktober)", 
                         "Phase 3: Spitzenleistung (November–Dezember)"])
    
    if phase == "Phase 1: Grundlage (Juli–August)":
        st.write("**Ziel Monat:** Erste 3–5 saubere Klimmzüge + deutliche Spagat-Verbesserung")
    elif phase == "Phase 2: Aufbau (September–Oktober)":
        st.write("**Ziel Monat:** 7–10 Klimmzüge + fast voller Spagat")
    
    st.subheader("Täglicher Ernährungsplan (Coach-Empfehlung)")
    st.write("**Protein:** 2–2,5g pro kg Körpergewicht")
    st.write("**Kalorien:** leichter Überschuss für Muskelaufbau")
    
    st.write("**Beispiel Tag:**")
    st.write("- Früh: Hafer + Whey + Beeren + Mandeln")
    st.write("- Mittag: Hähnchen/Reis/Brokkoli")
    st.write("- Snack: Quark + Honig + Nüsse")
    st.write("- Abend: Lachs/Süßkartoffel/Salat")
    st.write("- Vor dem Schlafen: Casein oder Magerquark")

# Footer
st.divider()
st.caption("Coach Max © 2026 | Daten bleiben lokal auf deinem Gerät")
