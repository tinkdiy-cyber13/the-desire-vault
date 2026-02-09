import streamlit as st
import time
import random
import json
import os

# Configurare Pagina
st.set_page_config(page_title="The Desire Vault v1.8", page_icon="✨", layout="centered")

DB_FILE = "baza_dorinte.json"

# --- FUNCTII BAZA DE DATE ---
def incarca_tot():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                date = json.load(f)
                # Conversie format vechi daca e cazul
                if "total_multumiri" not in date:
                    date = {"total_multumiri": date.get("total_multumiri", 0), "vizite": 0}
                return date
        except:
            return {"total_multumiri": 0, "vizite": 0}
    return {"total_multumiri": 0, "vizite": 0}

def salveaza_tot(date_complete):
    with open(DB_FILE, "w") as f:
        json.dump(date_complete, f)

# --- INITIALIZARE SI CONTORIZARE ---
date_sistem = incarca_tot()

if 'numarat_v' not in st.session_state:
    date_sistem["vizite"] = date_sistem.get("vizite", 0) + 1
    salveaza_tot(date_sistem)
    st.session_state['numarat_v'] = True

if 'vault_id' not in st.session_state:
    st.session_state.vault_id = random.randint(1000, 9999)

# --- TITLU SI AFISARE "OO" (Design Admin) ---
st.title("✨ The Desire Vault")

st.markdown(
    f"""
    <div style='text-align: right; margin-top: -55px;'>
        <span style='color: #22d3ee; font-size: 16px; font-weight: bold; border: 2px solid #22d3ee; padding: 4px 12px; border-radius: 15px; background-color: rgba(34, 211, 238, 0.1);'>
            OO: {date_sistem.get('vizite', 0)}
        </span>
    </div>
    """, 
    unsafe_allow_html=True
)

st.write("---")
st.markdown("> *\"Become naive enough to believe it will happen!\"*")

# --- 1. SPATIUL DE MANIFESTARE ---
st.subheader("🗝️ Seal your desire")

dorinta = st.text_area(
    "Your Sacred Space:", 
    placeholder="Start writing your new reality here...", 
    key=f"area_{st.session_state.vault_id}",
    height=150
)

st.markdown("<p style='text-align: center; color: #888; font-size: 0.8em; font-style: italic;'>🔒 Privacy Protocol: Your desires are never stored. They are processed in real-time and sent directly to the Universe.</p>", unsafe_allow_html=True)

if st.button("🚀 Seal in the Vault"):
    if dorinta.strip():
        progres = st.progress(0)
        status_text = st.empty()
        
        for i, litera in enumerate(dorinta[:50]):
            procent = int((i + 1) / min(len(dorinta), 50) * 100)
            status_text.markdown(f"**Vibrating:** `{litera}`")
            progres.progress(procent)
            time.sleep(0.04)
            
        st.balloons()
        st.success("✨ It is done. Your desire has been released!")
        
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

# --- 3. CONTORUL DE INIMIOARE (MULTUMIRI) ---
st.markdown(
    f"""
    <div style='position: fixed; top: 70px; right: 10px; background-color: rgba(255, 75, 75, 0.1); 
    padding: 10px; border-radius: 20px; border: 2px solid #ff4b4b; text-align: center; z-index: 999;'>
        <span style='color: #ff4b4b; font-size: 18px; font-weight: bold;'>❤️ {date_sistem.get('total_multumiri', 0)}</span>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- 4. SURPRISE (MENTOR) ---
st.divider()
if st.button("🎁 MENTOR"):
    st.info(random.choice(["Work on yourself!", "Profits over wages.", "Believe!"]))



