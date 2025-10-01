from repository import FinanceiroRepository
from service import FinanceiroService
from ui import DashboardUI
import streamlit as st

def inicializar_e_semear(repo: FinanceiroRepository):
    """Gera dados de exemplo se o banco estiver vazio."""
    df = repo.listar()
    if df.empty:
        exemplo = [
            # 2024 exemplo
            (2024, "Jan", 15000.0, 3000.0, 4000.0, 2500.0),
            (2024, "Fev", 18000.0, 3500.0, 4500.0, 3000.0),
            (2024, "Mar", 22000.0, 4000.0, 5000.0, 3800.0),
            (2024, "Abr", 16000.0, 3200.0, 4200.0, 2700.0),
            (2024, "Mai", 25000.0, 4500.0, 5500.0, 4200.0),
            (2023, "Jan", 12000.0, 2500.0, 3500.0, 2000.0),
            (2023, "Fev", 14000.0, 2800.0, 3800.0, 2300.0),
            (2023, "Mar", 17000.0, 3100.0, 4100.0, 2700.0),
        ]
        for a,m,f,d,c,i in exemplo:
            from models import Financeiro
            repo.inserir(Financeiro(a,m,f,d,c,i))
        # não mostrar toasts aqui para simplificar

def main():
    repo = FinanceiroRepository(db_name="financeiro.db")
    service = FinanceiroService(repo)
    inicializar_e_semear(repo)
    ui = DashboardUI(service, repo)
    ui.render()

if __name__ == "__main__":
    main()
