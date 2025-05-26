
import streamlit as st
import pandas as pd

# --- ログイン認証 ---
def login():
    st.sidebar.title("🔐 ログイン")
    username = st.sidebar.text_input("ユーザー名")
    password = st.sidebar.text_input("パスワード", type="password")

    if st.sidebar.button("ログイン"):
        if username == "admin" and password == "okoku1038":
            st.session_state["logged_in"] = True
        else:
            st.error("ユーザー名またはパスワードが間違っています")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login()
    st.stop()

# --- メイン画面 ---
st.title("🔧 工具価格査定フォーム")
st.write("これはログイン後に表示されるダミー画面です。ここに査定機能が入ります。")
