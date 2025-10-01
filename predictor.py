import openai
import pandas as pd
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

class FinanceiroPredictor:
    def __init__(self, modelo="gpt-4"):
        self.modelo = modelo

    def prever_lucro(self, df: pd.DataFrame, meses_futuros: int = 3) -> pd.DataFrame:
        if df.empty:
            return pd.DataFrame()

        historico = df[["ano", "mes", "lucro"]].sort_values(["ano", "mes"]).to_dict(orient="records")
        prompt = f"""
        Baseado neste histórico financeiro mensal, forneça previsões de lucro para os próximos {meses_futuros} meses.
        Retorne apenas JSON no formato:
        [{{"ano": 2025, "mes": "Mai", "lucro_previsto": 10000.0}}, ...]
        Histórico: {historico}
        """
        try:
            resposta = openai.ChatCompletion.create(
                model=self.modelo,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            conteudo = resposta.choices[0].message.content
            previsoes = pd.read_json(conteudo)
            return previsoes
        except Exception as e:
            print(f"Erro na previsão: {e}")
            return pd.DataFrame()
