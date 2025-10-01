import sqlite3
import pandas as pd
import streamlit as st
from models import Financeiro

class FinanceiroRepository:
    def __init__(self, db_name="financeiro.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS financeiro (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ano INTEGER NOT NULL,
                mes TEXT NOT NULL,
                faturamento REAL NOT NULL,
                despesas REAL NOT NULL,
                custo REAL NOT NULL,
                impostos REAL NOT NULL,
                UNIQUE(ano, mes)
            )
        """)
        self.conn.commit()

    def _execute_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            st.error(f"Erro de Integridade: {e}")
            return False
        except Exception as e:
            st.error(f"Erro no Banco de Dados: {e}")
            return False

    def inserir(self, financeiro: Financeiro):
        query = """
            INSERT INTO financeiro (ano, mes, faturamento, despesas, custo, impostos)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (financeiro.ano, financeiro.mes, financeiro.faturamento,
                  financeiro.despesas, financeiro.custo, financeiro.impostos)
        return self._execute_query(query, params)

    def atualizar(self, id: int, financeiro: Financeiro):
        query = """
            UPDATE financeiro
            SET ano=?, mes=?, faturamento=?, despesas=?, custo=?, impostos=?
            WHERE id=?
        """
        params = (financeiro.ano, financeiro.mes, financeiro.faturamento,
                  financeiro.despesas, financeiro.custo, financeiro.impostos, id)
        return self._execute_query(query, params)

    def deletar(self, id: int):
        query = "DELETE FROM financeiro WHERE id=?"
        return self._execute_query(query, (id,))

    def listar(self) -> pd.DataFrame:
        self.cursor.execute("SELECT * FROM financeiro ORDER BY ano DESC, mes ASC")
        data = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        return pd.DataFrame(data, columns=columns)
