
import streamlit as st
import pandas as pd

def login():
    st.sidebar.title("🔐 ログイン")
    username = st.sidebar.text_input("ユーザー名")
    password = st.sidebar.text_input("パスワード", type="password")

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    login_button = st.sidebar.button("ログイン")
    if login_button:
        if username == "admin" and password == "okoku1038":
            st.session_state["logged_in"] = True
            st.success("ログイン成功！")
        else:
            st.session_state["logged_in"] = False
            st.error("ユーザー名またはパスワードが間違っています")

    return st.session_state["logged_in"]

if not login():
    st.stop()



import streamlit as st
import pandas as pd

def login():

    # 状態の初期化

        if username == "admin" and password == "okoku1038":
        else:
            st.error("ユーザー名またはパスワードが間違っています")


if not login():



import streamlit as st
import pandas as pd

def login():

    login_successful = False
        if username == "admin" and password == "okoku1038":
            login_successful = True
        else:
            st.error("ユーザー名またはパスワードが間違っています")
        login_successful = True

    return login_successful

if not login():



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