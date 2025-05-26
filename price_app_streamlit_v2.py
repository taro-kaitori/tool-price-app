
import streamlit as st
import pandas as pd

def login():
    st.sidebar.title("🔐 ログイン")
    username = st.sidebar.text_input("ユーザー名")
    password = st.sidebar.text_input("パスワード", type="password")
    if st.sidebar.button("ログイン"):
        if username == "admin" and password == "okoku1038":
            st.session_state["logged_in"] = True
        else:
            st.error("ユーザー名またはパスワードが間違っています")
    return st.session_state.get("logged_in", False)

if not login():
    st.stop()



import streamlit as st
import pandas as pd

def login():
        if username == "admin" and password == "okoku1038":
        else:
            st.error("ユーザー名またはパスワードが間違っています")

if not login():



import streamlit as st
import pandas as pd

def login():
        if username == "admin" and password == "okoku1038":
        else:
            st.error("ユーザー名またはパスワードが間違っています")

    login()



import streamlit as st
import pandas as pd

def login():
        if username == "admin" and password == "okoku1038":
        else:
            st.error("ユーザー名またはパスワードが間違っています")

    login()



import streamlit as st
import pandas as pd

def login():

        if username == "admin" and password == "okoku1038":
        else:
            st.error("ユーザー名またはパスワードが間違っています")

    login()

# --- メイン画面 ---
st.title("🔧 工具価格査定フォーム")