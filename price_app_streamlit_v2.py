import streamlit as st
import pandas as pd

def login():
    st.sidebar.title("🔐 ログイン")
    username = st.sidebar.text_input("ユーザー名")
    password = st.sidebar.text_input("パスワード", type="password")

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.sidebar.button("ログイン"):
        if username == "admin" and password == "okoku1038":
            st.session_state["logged_in"] = True
            st.success("ログイン成功！")
        else:
            st.session_state["logged_in"] = False
            st.error("ユーザー名またはパスワードが間違っています")

    return st.session_state["logged_in"]

if not login():
    st.stop()

st.title("🔧 工具価格査定フォーム")
st.write("これは実際の査定機能が含まれる本番バージョンです（ログイン後表示）")