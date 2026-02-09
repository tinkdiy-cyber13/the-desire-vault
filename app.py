import streamlit as st
import time
import random
import json
import os

# Configurare Pagina
st.set_page_config(page_title="The Desire Vault", page_icon="✨", layout="centered")

DB_DORINTE = "baza_dorinte.json"

def incarca_tot():
    if os.path.exists(DB_DORINTE):
        try:
            with open(DB_DORINTE, "r") as f: return json.load(f)
        except: return {"total_multumiri": 0}
    return {"total_multumiri": 0}

def salveaza_tot(date):
    with open(DB_DORINTE, "w") as f: json.dump(date, f)

date_sistem = incarca_tot()

if 'reset_input' not in st.session_state:
    st.session_state.reset_input = random.randint(1, 1000)

# --- TITLU SI FILOZOFIE ---
st.title("✨ The Desire Vault")
st.write("---")
st.markdown("> *\"Become naive enough to believe it will happen!\"*")

# --- 1. INPUT PENTRU DORINTA (BLOCARE AUTOCOMPLETE) ---
st.subheader("🗝️ Seal your desire")

# Hack de Admin: Injectăm HTML pentru a opri sugestiile browserului
st.markdown("""
    <style>
        input {
            autocomplete: off;
        }
    </style>
""", unsafe_allow_html=True)

# Folosim un label gol si widget-ul de text cu cheie dinamica
dorinta = st.text_input(
    "Write your desire here:", 
    placeholder="I am so grateful for...", 
    key=f"wish_{st.session_state.reset_input}",
    help="Browser history disabled for this vault."
)

if st.button("🚀 Send to the Vault"):
    if dorinta:
        progres = st.progress(0)
        status_text = st.empty()
        
        for i, litera in enumerate(dorinta):
            procent = int((i + 1) / len(dorinta) * 100)
            status_text.markdown(f"**Processing letter:** `{litera}`")
            progres.progress(procent)
            time.sleep(0.04)
            
        st.balloons()
        st.success("✨ Sealed!")
        
        # Reset total pentru a goli si a schimba ID-ul casutei
        st.session_state.reset_input = random.randint(1, 1000)
        st.session_state['show_thanks'] = True
        time.sleep(1.2)
        st.rerun()
    else:
        st.error("Write something first!")

# --- 2. BUTONUL DE RECUNOSTINTA ---
if st.session_state.get('show_thanks'):
    st.divider()
    if 'count_multumiri' not in st.session_state:
        st.session_state['count_multumiri'] = 0
        
    if st.session_state['count_multumiri'] < 3:
        if st.button("💖 THANK YOU!"):
            st.session_state['count_multumiri'] += 1
            date_sistem["total_multumiri"] = date_sistem.get("total_multumiri", 0) + 1
            salveaza_tot(date_sistem)
            st.snow()
            st.toast(f"Gratitude {st.session_state['count_multumiri']}/3")
    else:
        st.session_state['show_thanks'] = False
        st.session_state['count_multumiri'] = 0
        time.sleep(1)
        st.rerun()

# --- 3. CONTORUL DE INIMIOARE ---
st.markdown(
    f"""
    <div style='position: fixed; top: 70px; right: 10px; background-color: rgba(255, 75, 75, 0.1); 
    padding: 10px; border-radius: 20px; border: 2px solid #ff4b4b; text-align: center; z-index: 999;'>
        <span style='color: #ff4b4b; font-size: 18px; font-weight: bold;'>❤️ {date_sistem.get('total_multumiri', 0)}</span>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- 4. SURPRISE BUTTON ---
st.divider()
if st.button("🎁 THE MENTOR"):
    mesaje = ["Success is something you attract.", "Profits are better than wages.", "Become more!"]
    st.info(random.choice(mesaje))



