import streamlit as st
from ui import render
from db import init_db

# Configuração inicial - deve ser o primeiro comando!
st.set_page_config(
    layout="wide",
    page_title="Dashboard Financeiro",
    page_icon="💰"
)

def main():
    init_db()  # cria tabela se não existir
    render()

if __name__ == "__main__":
    main()
