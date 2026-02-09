import streamlit as st
import time
import random
import json
import os

# Configurare Pagina
st.set_page_config(page_title="The Desire Vault", page_icon="✨", layout="centered")

DB_DORINTE = "baza_dorinte.json"

def incarca_date():
    if os.path.exists(DB_DORINTE):
        try:
            with open(DB_DORINTE, "r") as f: return json.load(f)
        except: return {"total_multumiri": 0}
    return {"total_multumiri": 0}

def salveaza_date(date):
    with open(DB_DORINTE, "w") as f: json.dump(date, f)

date_sistem = incarca_date()

# --- LOGICA DE RESETARE ---
if 'reset_input' not in st.session_state:
    st.session_state.reset_input = random.randint(1, 1000)

# --- TITLU SI FILOZOFIE ---
st.title("✨ The Desire Vault")
st.write("---")
st.markdown("> *\"Become naive enough to believe it will happen!\"*  \n> — **J. Earl Shoaff**")

# 1. INPUT PENTRU DORINTA
st.subheader("🗝️ Seal your desire")

# Cheia dinamica forteaza casuta sa fie goala la fiecare reset
dorinta = st.text_input("Write your desire here:", placeholder="I am so grateful for...", key=f"wish_{st.session_state.reset_input}")

if st.button("🚀 Send to the Vault"):
    if dorinta:
        progres = st.progress(0)
        status_text = st.empty()
        
        # Animația literelor
        for i, litera in enumerate(dorinta):
            procent = int((i + 1) / len(dorinta) * 100)
            status_text.markdown(f"**Processing letter:** `{litera}`")
            progres.progress(procent)
            time.sleep(0.04)
            
        st.balloons()
        st.success("✨ Sealed!")
        
        # SCHIMBĂM CHEIA CA SĂ GOLIM TOT
        st.session_state.reset_input = random.randint(1, 1000)
        st.session_state['show_thanks'] = True
        time.sleep(1.5)
        st.rerun() # RESTART TOTAL
    else:
        st.error("Write something first!")

# 2. BUTONUL DE RECUNOSTINTA (Apare doar dupa trimitere)
if st.session_state.get('show_thanks'):
    st.divider()
    st.subheader("🙏 Gratitude")
    
    if 'count_multumiri' not in st.session_state:
        st.session_state['count_multumiri'] = 0
        
    if st.session_state['count_multumiri'] < 3:
        if st.button("💖 THANK YOU!"):
            st.session_state['count_multumiri'] += 1
            date_sistem["total_multumiri"] = date_sistem.get("total_multumiri", 0) + 1
            salveaza_date(date_sistem)
            st.snow()
            st.toast(f"Gratitude {st.session_state['count_multumiri']}/3")
    else:
        # Dupa 3 multumiri, curatam si sectiunea asta
        st.session_state['show_thanks'] = False
        st.session_state['count_multumiri'] = 0
        time.sleep(1)
        st.rerun()

# 3. CONTORUL DE INIMIOARE (Badge discret)
st.markdown(
    f"""
    <div style='position: fixed; top: 70px; right: 10px; background-color: rgba(255, 75, 75, 0.1); 
    padding: 10px; border-radius: 20px; border: 2px solid #ff4b4b; text-align: center; z-index: 999;'>
        <span style='color: #ff4b4b; font-size: 18px; font-weight: bold;'>❤️ {date_sistem.get('total_multumiri', 0)}</span>
    </div>
    """, 
    unsafe_allow_html=True
)

# 4. SURPRISE BUTTON
st.divider()
if st.button("🎁 THE MENTOR"):
    mesaje_shoaff = [
        "Don't wish it were easier, wish you were better!",
        "Profits are better than wages.",
        "Success is something you attract by the person you become.",
        "Work harder on yourself than you do on your job."
    ]
    st.info(random.choice(mesaje_shoaff))


