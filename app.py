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

# Folosim un state special pentru a goli casuta
if 'last_wish_time' not in st.session_state:
    st.session_state['last_wish_time'] = 0

# --- TITLU SI FILOZOFIE ---
st.title("✨ The Desire Vault")
st.write("---")
st.markdown("> *\"Become naive enough to believe it will happen!\"*  \n> — **J. Earl Shoaff**")

# 1. INPUT PENTRU DORINTA (Se goleste automat prin key-ul dinamic)
st.subheader("🗝️ Seal your desire")

# Trucul de Admin: schimbam cheia de input de fiecare data cand trimitem, asa se goleste singura
wish_key = f"wish_{st.session_state['last_wish_time']}"
dorinta = st.text_input("Write your desire here (be specific):", placeholder="Example: I am so grateful for...", key=wish_key)

if st.button("🚀 Send to the Vault"):
    if dorinta:
        progres = st.progress(0)
        status_text = st.empty()
        
        # Efectul vizual de procesare
        for i, litera in enumerate(dorinta):
            procent = int((i + 1) / len(dorinta) * 100)
            status_text.markdown(f"**Processing letter:** `{litera}`")
            progres.progress(procent)
            time.sleep(0.04)
            
        st.balloons()
        st.success("✨ Your desire has been sealed in the Universe's Vault!")
        
        # Incrementam starea pentru a reseta casuta la urmatorul rerun
        st.session_state['last_wish_time'] += 1
        st.session_state['show_gratitude'] = True
        time.sleep(2) # Lasam utilizatorul sa vada succesul
        st.rerun() # RESTART automat pentru casuta goala
    else:
        st.error("Please write your desire first!")

# 2. BUTONUL DE RECUNOSTINTA (Ramane activ pana la urmatoarea scriere)
if st.session_state.get('show_gratitude'):
    st.divider()
    st.subheader("🙏 Gratitude activates the Magic")
    
    if 'count_multumiri' not in st.session_state:
        st.session_state['count_multumiri'] = 0
        
    if st.session_state['count_multumiri'] < 3:
        if st.button("💖 THANK YOU!"):
            st.session_state['count_multumiri'] += 1
            date_sistem["total_multumiri"] = date_sistem.get("total_multumiri", 0) + 1
            salveaza_date(date_sistem)
            st.snow()
            st.toast(f"Gratitude confirmed! ({st.session_state['count_multumiri']}/3)")
    else:
        st.info("The 3 magic thanks are sent! ✨")
        if st.button("Reset Gratitude for new wish"):
            st.session_state['count_multumiri'] = 0
            st.session_state['show_gratitude'] = False
            st.rerun()

# 3. CONTORUL DE INIMIOARE
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
if st.button("🎁 THE MENTOR'S MESSAGE"):
    mesaje_shoaff = [
        "Don't wish it were easier, wish you were better!",
        "Profits are better than wages.",
        "Success is something you attract by the person you become.",
        "If you want to have more, you have to become more!",
        "Work harder on yourself than you do on your job."
    ]
    st.info(random.choice(mesaje_shoaff))

