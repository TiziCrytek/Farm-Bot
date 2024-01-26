from time import sleep
from farm_bot import FarmBot
import streamlit as st
import json
from threading import Thread

def update():
    if st.session_state.conn:
        st.session_state.data['start_disabled'] = st.session_state.start_disabled
        st.session_state.data['stop_disabled'] = st.session_state.stop_disabled
        st.session_state.data['ip'] =   st.session_state.ip
        with open('data.json', 'w') as file:
            json.dump(st.session_state.data, file, indent=4)

def connect(addr):
    if len(addr) < 6:
        st.toast('EMPTY')
        return
        
    st.toast('CONNECT..', icon='🔰')
    st.session_state.bot = FarmBot(addr)
    if st.session_state.bot.check_connect():
        st.session_state.start_disabled = st.session_state.data['start_disabled']
        st.session_state.stop_disabled = st.session_state.data['stop_disabled']

        if st.session_state.stop_disabled:
            st.session_state.start_disabled = False

        st.toast('CONNECTING', icon='✅')
    else:
        st.toast('ERROR', icon='❌')

def start():
    try:
        st.session_state.conn = True
        Thread(target=st.session_state.bot.start).start()
        st.session_state.connect_item_disabled = True
        st.session_state.start_disabled = True
        st.session_state.stop_disabled = False
        st.toast('START', icon='✅')
    except:
        st.toast('ERROR START')

def stop():
    st.session_state.conn = True
    st.session_state.connect_item_disabled = False
    st.session_state.start_disabled = False
    st.session_state.stop_disabled = True
    st.session_state.bot.stop()
    st.session_state.bot.alive = False
    st.toast('STOP', icon='⛔')

def main():

    with open('data.json', 'r') as file:
        st.session_state.data = json.load(file)

    if 'conn' not in st.session_state:
        st.session_state.conn = False

    if 'connect_item_disabled' not in st.session_state:
        st.session_state.connect_item_disabled = False

    if 'start_disabled' not in st.session_state:
        st.session_state.start_disabled = True

    if 'stop_disabled' not in st.session_state:
        st.session_state.stop_disabled = True

    st.markdown("""
    <style>
        div.stButton {
            text-align:center;
        }
    </style>""", unsafe_allow_html=True)

    st.markdown("""
    <style>
        div.stSpinner > div {
            text-align: center;
            align-items: center;
            justify-content: center;
        }
    </style>""", unsafe_allow_html=True)

    c1 = st.container()
    col1, col2 = c1.columns(2)
    c2 = st.container()

    with c2.expander('CONNECT DEVICE'):
        ip = st.text_input('IP', key='ip', value=st.session_state.data['ip'], placeholder='IP', label_visibility='hidden', disabled=st.session_state.connect_item_disabled)
        s = st.button('CONNECT', on_click=connect, args=[ip], disabled=st.session_state.connect_item_disabled)

    col1.button('START', on_click=start, disabled=st.session_state.start_disabled)
    col2.button('STOP', on_click=stop, disabled=st.session_state.stop_disabled)

    update()

    #e451c44d0311
    # bot = FarmBot()
    # print('Start Farm')
    # try:
    #     # bot.start()
    #     bot.aim()
    # except Exception as e:
    #     print(e)

if __name__ == '__main__':
    main()