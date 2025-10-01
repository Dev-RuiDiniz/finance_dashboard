import streamlit as st
from repository import FinanceiroRepository
from service import FinanceiroService
from ui import DashboardUI

# ⚡ O set_page_config deve ser a PRIMEIRA chamada do Streamlit
st.set_page_config(layout="wide", page_title="Dashboard Financeiro Moderno")

def main():
    repo = FinanceiroRepository()
    service = FinanceiroService(repo)
    ui = DashboardUI(service, repo)
    ui.render()

if __name__ == "__main__":
    main()
