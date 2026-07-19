import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Klimmzüge & Spagat", layout="centered")
st.title("💪 Klimmzüge & Spagat Tracker")

if "pullups" not in st.session_state:
    st.session_state.pullups = []
if "front_split" not in st.session_state:
    st.session_state.front_split = []
if "side_split" not in st.session_state:
    st.session_state.side_split = []

tab1, tab2, tab3 = st.tabs(["📝 Training loggen", "📈 Fortschritt", "📋 Trainingsplan"])

with tab1:
    st.subheader("Heutiges Training")
    col1, col2 = st.columns(2)
    
    with col1:
        reps = st.number_input("Saubere Klimmzüge", min_value=0, value=0, step=1)
        if st.button("✅ Klimmzüge speichern", type="primary"):
            st.session_state.pullups.append({"Datum": str(date.today()), "Wiederholungen": reps})
            st.success(f"{reps} Klimmzüge eingetragen!")
    
    with col2:
        front = st.number_input("Front Spagat (cm vom Boden)", min_value=0.0, value=25.0, step=0.5)
        side = st.number_input("Seitlicher Spagat (cm vom Boden)", min_value=0.0, value=30.0, step=0.5)
        if st.button("✅ Spagat speichern", type="primary"):
            st.session_state.front_split.append({"Datum": str(date.today()), "cm": front})
            st.session_state.side_split.append({"Datum": str(date.today()), "cm": side})
            st.success("Spagat-Fortschritt gespeichert!")

with tab2:
    st.subheader("Dein Fortschritt")
    if st.session_state.pullups:
        df_pull = pd.DataFrame(st.session_state.pullups)
        st.line_chart(df_pull.set_index("Datum")["Wiederholungen"])
        st.dataframe(df_pull, use_container_width=True)
    
    colf, cols = st.columns(2)
    with colf:
        if st.session_state.front_split:
            df_front = pd.DataFrame(st.session_state.front_split)
            st.line_chart(df_front.set_index("Datum")["cm"])
            st.write("**Front Spagat**")
    with cols:
        if st.session_state.side_split:
            df_side = pd.DataFrame(st.session_state.side_split)
            st.line_chart(df_side.set_index("Datum")["cm"])
            st.write("**Seitlicher Spagat**")

with tab3:
    st.markdown("""
    ### Empfohlener Wochenplan
    
    **Klimmzüge (3–5x pro Woche):**
    - Dead Hangs & Scapular Pulls
    - Negative Klimmzüge (langsam ablassen)
    - Band-unterstützte oder normale Klimmzüge
    - Greasing the Groove (viele kleine Sätze)
    
    **Spagat/Dehnen (4–6x pro Woche):**
    - Hüftbeuger + Hamstrings
    - Schmetterlingsdehnung
    - Seitlicher & Frontaler Spagat
    - Pigeon Pose / Lizard Pose
    """)

st.caption("Daten bleiben nur in diesem Browser-Tab gespeichert.")
