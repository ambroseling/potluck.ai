import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.write("Hello world!")
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page("login.py", title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

dashboard = st.Page(
    "account/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True
)

mnist = st.Page("cv/mnist.py", title="beautiful mnist", icon=":material/123:")
resnet = st.Page("cv/mnist.py", title="beautiful mnist", icon=":material/123:")
mistral = st.Page("llms/mistral.py", title="ece prof gpt", icon=":material/school:")
tweets = st.Page("rnns/tweets.py",title="tweet analyzer",icon=":material/raven:")
movie_recommender = st.Page("gnns/movie_recommender.py",title="movie_recommender",icon=":material/movie:")
if st.session_state.logged_in:
    pg = st.navigation(
        {
            "account": [logout_page,dashboard],
            "llms": [mistral],
            "rnns":[tweets],
            "gnns":[movie_recommender],
            "cv": [mnist],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()
