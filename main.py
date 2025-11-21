"""
Ponto de entrada principal do projeto finance_dashboard.

Este arquivo é um wrapper que chama o pacote finance_dashboard.__main__.
Você pode executar com:
  streamlit run main.py
ou
  python -m finance_dashboard
"""
from finance_dashboard.__main__ import main

if __name__ == "__main__":
    main()
