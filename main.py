import streamlit as st
from repository import FinanceiroRepository
from service import FinanceiroService
from ui import DashboardUI

# Configuração da página deve ser o primeiro comando
st.set_page_config(layout="wide", page_title="Dashboard Financeiro Moderno")

def main():
    repo = FinanceiroRepository()
    service = FinanceiroService(repo)
    ui = DashboardUI(service, repo)
    ui.render()

if __name__ == "__main__":
    main()
