import os
import openai
import pandas as pd
import json
import re
from typing import Optional

# Carrega chave de ambiente (deixe como variável de ambiente)
openai.api_key = os.getenv("OPENAI_API_KEY")

class FinanceiroPredictor:
    def __init__(self, modelo="gpt-4", temperatura=0.0):
        self.modelo = modelo
        self.temperatura = temperatura

    def _safe_parse_json(self, text: str) -> Optional[list]:
        """
        Tenta extrair o primeiro bloco JSON do texto. Retorna lista/dict parseado ou None.
        """
        # Busca o primeiro colchete/objeto JSON no texto
        m = re.search(r'(\[.*\])', text, re.S)
        if not m:
            # tenta extrair um objeto
            m = re.search(r'(\{.*\})', text, re.S)
        if not m:
            return None
        snippet = m.group(1)
        try:
            return json.loads(snippet)
        except Exception:
            # tentativa de limpar vírgulas triplas ou tamanhos
            try:
                # remove trailing commas
                cleaned = re.sub(r',\s*}', '}', snippet)
                cleaned = re.sub(r',\s*\]', ']', cleaned)
                return json.loads(cleaned)
            except Exception:
                return None

    def prever_lucro(self, df: pd.DataFrame, meses_futuros: int = 3) -> pd.DataFrame:
        """
        Recebe DataFrame com colunas ['ano','mes','lucro'] (histórico) e retorna DataFrame com previsões:
        columns: ['ano','mes','lucro_previsto'].
        """
        # Checagens simples
        if df is None or df.empty:
            return pd.DataFrame(columns=["ano","mes","lucro_previsto"])

        hist = df[['ano','mes','lucro']].sort_values(['ano','mes']).to_dict(orient='records')

        prompt = (
            f"Você é um assistente que prevê lucros mensais com base no histórico. "
            f"Receba o histórico (lista de objetos com ano, mes, lucro) e gere previsões "
            f"para os próximos {meses_futuros} meses. Retorne apenas JSON no formato:\n\n"
            f"[{{'ano': 2025, 'mes': 'Mai', 'lucro_previsto': 12345.67}}, ...]\n\n"
            f"Histórico: {hist}\n\n"
            "Forneça previsões coerentes com a tendência observada e explique nada (somente JSON)."
        )

        try:
            resp = openai.ChatCompletion.create(
                model=self.modelo,
                messages=[{"role":"user","content":prompt}],
                temperature=self.temperatura,
                max_tokens=800
            )
            content = resp.choices[0].message.content
            parsed = self._safe_parse_json(content)
            if not parsed:
                return pd.DataFrame(columns=["ano","mes","lucro_previsto"])
            df_prev = pd.DataFrame(parsed)
            # padroniza nomes
            df_prev = df_prev.rename(columns={c: c.strip() for c in df_prev.columns})
            # garantias de tipos
            df_prev['lucro_previsto'] = pd.to_numeric(df_prev['lucro_previsto'], errors='coerce').fillna(0.0)
            return df_prev
        except Exception as e:
            # falha silenciosa: retorna DF vazio e loga o erro
            print(f"[Predictor] Erro na chamada OpenAI: {e}")
            return pd.DataFrame(columns=["ano","mes","lucro_previsto"])

    def gerar_insights(self, df: pd.DataFrame, periodo: str = "últimos 12 meses") -> str:
        """
        Gera um resumo/insights em linguagem natural sobre o histórico.
        Retorna texto com recomendações.
        """
        if df is None or df.empty:
            return "Sem dados suficientes para gerar insights."

        hist = df[['ano','mes','faturamento','despesas','custo','impostos','lucro']].sort_values(['ano','mes']).tail(24).to_dict(orient='records')
        prompt = (
            f"Forneça um resumo analítico e recomendações com base no seguinte histórico financeiro "
            f"({periodo}). Seja objetivo (máx. 6 frases). Histórico: {hist}\n\n"
            "Retorne apenas o texto com bullets ou frases curtas."
        )
        try:
            resp = openai.ChatCompletion.create(
                model=self.modelo,
                messages=[{"role":"user","content":prompt}],
                temperature=0.3,
                max_tokens=300
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            print(f"[Predictor] Erro ao gerar insights: {e}")
            return "Não foi possível gerar insights no momento."
