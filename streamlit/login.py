import streamlit as st
from streamlit_google_auth import Authenticate


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()



col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.subheader("welcome to potluck :)")
    if 'connected' not in st.session_state:
        authenticator = Authenticate(
            secret_credentials_path = '/home/tiny_ling/projects/potluckai/google_credentials.json',
            cookie_name='potluck-client',
            cookie_key='this_is_secret',
            redirect_uri = 'http://localhost:8501',
        )
        st.session_state["authenticator"] = authenticator

    # Catch the login event
    st.session_state["authenticator"].check_authentification()

    # Create the login button
    st.session_state["authenticator"].login()
with col3:
    st.write(' ')


if st.session_state['connected']:
    st.image(st.session_state['user_info'].get('picture'))
    st.write('Hello, '+ st.session_state['user_info'].get('name'))
    st.write('Your email is '+ st.session_state['user_info'].get('email'))
    st.session_state.logged_in = True
    st.rerun()
    if st.button('Log out'):
        st.session_state["authenticator"].logout()

