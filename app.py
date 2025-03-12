import streamlit as st

# Read the HTML file
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Embed the HTML in Streamlit
st.components.v1.html(html_content, width=800, height=800, scrolling=True)