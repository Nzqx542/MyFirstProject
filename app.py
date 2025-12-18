import streamlit as st
st.title("my first project")
name = st.text_input("----")
if name:
  st.write($"hello, {name}!")
