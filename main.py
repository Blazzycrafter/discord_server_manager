import time
from random import randint
from tabnanny import check

import streamlit as st
import requests
from os import system, write

from streamlit import rerun, session_state
from login import getToken_QR

sidebar = st.sidebar
main = st


#inits
if 'token' not in st.session_state:
    st.session_state.token = r''






if "stage" not in st.session_state:
    st.session_state.stage = "StageLogin"

# Funktionen für die Stages

def stage_login():
    st.write("Willkommen! Wähle eine Login-Methode:")
    if st.button("Token", key="login_token"):
        st.session_state.stage = "StageLoginToken"
        st.rerun()
    if st.button("QR-Code (maybe broken)", key="login_QR"):
        st.session_state.stage = "StageLoginQR"
        st.rerun()


def stage_login_token():
    st.write("Bitte geben Sie Ihren Token ein:")
    st.session_state.token = st.text_input("Token:")
    if st.button("Bestätigen"):
        st.session_state.stage = "StageServerList"
        st.rerun()
    if st.button("Zurück"):
        st.session_state.stage = "StageLogin"
        st.rerun()


def stage_login_qr():
    st.write("Scannen Sie den QR-Code, um sich anzumelden.")
    st.session_state.token = getToken_QR(main)
    print(st.session_state.token)
    if not st.session_state.token == r"":
        st.session_state.stage = "StageServerList"
        st.rerun()
    if st.button("Zurück"):
        st.session_state.stage = "StageLogin"
        st.rerun()

def stage_server_list():
    if 'serverList' not in st.session_state:
        st.write("serverlist...")

        url = "https://discord.com/api/v10/users/@me/guilds"

        # Headers für den Request
        headers = {
            "Authorization" : st.session_state.token,
            "User-Agent": "BlazzyTools (https://example.com, 1.0)",
            "Accept-Language": "en-US",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json"
        }

        # Senden des GET-Requests
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            st.session_state.serverList = response.json()
        else:
            st.error(f"Fehler: {response.status_code} - {response.text}")
            st.stop()
    checkboxes = []
    st.write(f"server counter: {len(st.session_state.serverList)}")
    for server in st.session_state.serverList:
        if server["owner"]:
           continue
        checkboxes.append({"ServerID": server["id"], "ServerName": server["name"],
                            "checkbox": st.checkbox(key=server["id"],label=server["name"])})
    if st.button(label="Weiter"):
        st.session_state.checkboxes = checkboxes
        st.session_state.stage = "ProcessCheckboxes"
        st.rerun()

def stage_process_checkboxes():
    delete_servers = []
    for i in st.session_state.checkboxes:
        if i["checkbox"]:
            delete_servers.append(i)
    st.code(delete_servers)
    st.write("The following server gets deleted are you sure?")
    st.session_state.delete_servers = delete_servers
    for i in delete_servers:
        st.caption(i["ServerName"])
    bcm= 5
    r = randint(0,bcm-1)
    for i in range(bcm):
        if i == r:
            st.button(label="yes",key=f"ponr-{i}", on_click=TRIGGR_stage_DELETE)
        else:
            st.button(label="no",key=f"ponr-{i}", on_click=TRIGGR_stage_ABORT)



def TRIGGR_stage_ABORT():
    st.session_state.stage = "ABORT"
    st.rerun()

def TRIGGR_stage_DELETE():
    st.session_state.stage = "DELETE"

def stage_ABORT():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.write("Action arborted")
    st.write("All data deleted from memory")
    st.stop()



def stage_DELETE():
    sl = len(st.session_state.delete_servers)
    progres = st.progress(text="init", value=0)
    for n in range(sl):
        i = st.session_state.delete_servers[n]
        progres.progress(value=n/sl, text=f"deleting: {i["ServerName"]}")
        timeout= randint(0,1)+5
        time.sleep(timeout)
        server_id = i["ServerID"]







        url = f"https://discord.com/api/v9/users/@me/guilds/{server_id}"

        # Header mit Authorization
        headers = {
            "Authorization": st.session_state.token,
            "Content-Type": "application/json"
        }

        # Optionaler Body (falls erforderlich, sonst leer lassen)
        data = {"lurking" : False}

        # DELETE-Request senden
        response = requests.delete(url, headers=headers, json=data)
        print(response.status_code)
        print(response.text)

    progres.progress(value=1.0, text=f"DONE")
    st.write("all selected servers should be deleted")
    st.write("All data deleted from memory")
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.stop()





# Kontrolliere, welche Stage angezeigt wird
if st.session_state.stage == "StageLogin":
    stage_login()
elif st.session_state.stage == "StageLoginToken":
    stage_login_token()
elif st.session_state.stage == "StageLoginQR":
    stage_login_qr()
elif st.session_state.stage == "StageServerList":
    stage_server_list()
elif st.session_state.stage == "ProcessCheckboxes":
    stage_process_checkboxes()
elif st.session_state.stage == "ABORT":
    stage_ABORT()
elif st.session_state.stage == "DELETE":
    stage_DELETE()
# {'id': '898370462072053790', 'name': 'Anime-Watching', 'icon': '9c87c62d065640f2e531f2dddb3c0ada', 'banner': None, 'owner': False, 'permissions': '2251799813685247', 'features': ['COMMUNITY', 'NEWS', 'TEXT_IN_VOICE_ENABLED', 'CHANNEL_ICON_EMOJIS_GENERATED']}

