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

# ID dinamic pentru a forța un spațiu de scris complet nou de fiecare dată
if 'vault_id' not in st.session_state:
    st.session_state.vault_id = random.randint(1000, 9999)

# --- TITLU SI FILOZOFIE ---
st.title("✨ The Desire Vault")
st.write("---")
st.markdown("> *\"Become naive enough to believe it will happen!\"*")

# --- 1. SPATIUL DE MANIFESTARE (FĂRĂ ISTORIC) ---
st.subheader("🗝️ Seal your desire")

# Folosim TEXT_AREA în loc de TEXT_INPUT pentru a păcăli istoricul browserului
# Și îi dăm o cheie care se schimbă mereu
dorinta = st.text_area(
    "Your Sacred Space:", 
    placeholder="Start writing your new reality here...", 
    key=f"area_{st.session_state.vault_id}",
    height=150,
    help="This space is fresh. No past records allowed."
)

if st.button("🚀 Seal in the Vault"):
    if dorinta.strip():
        progres = st.progress(0)
        status_text = st.empty()
        
        # Animația de sigilare
        for i, litera in enumerate(dorinta[:50]): # Analizăm vizual primele 50 caractere
            procent = int((i + 1) / min(len(dorinta), 50) * 100)
            status_text.markdown(f"**Vibrating:** `{litera}`")
            progres.progress(procent)
            time.sleep(0.04)
            
        st.balloons()
        st.success("✨ It is done. Your desire is now part of the Universe.")
        
        # RESETARE TOTALĂ: Schimbăm ID-ul și golim ecranul
        st.session_state.vault_id = random.randint(1000, 9999)
        st.session_state['show_thanks'] = True
        time.sleep(2)
        st.rerun()
    else:
        st.error("The vault requires words to manifest.")

# --- 2. RECUNOSTINTA ---
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

# --- 4. SURPRISE ---
st.divider()
if st.button("🎁 MENTOR"):
    st.info(random.choice(["Work on yourself!", "Profits over wages.", "Believe!"]))



