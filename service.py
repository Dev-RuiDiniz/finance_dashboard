import pandas as pd

class FinanceiroService:
    MESES_ORDENADOS = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

    def __init__(self, repository):
        self.repo = repository

    def _calcular_kpis(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        df['lucro'] = df['faturamento'] - (df['despesas'] + df['custo'] + df['impostos'])
        df['margem'] = ((df['lucro'] / df['faturamento']) * 100).fillna(0)
        df['mes'] = pd.Categorical(df['mes'], categories=self.MESES_ORDENADOS, ordered=True)
        df = df.sort_values(['ano', 'mes'])
        return df

    def get_dados(self) -> pd.DataFrame:
        df = self.repo.listar()
        return self._calcular_kpis(df)

    def dados_por_ano(self, ano: int) -> pd.DataFrame:
        df = self.get_dados()
        df_ano = df[df['ano'] == ano].copy()
        df_ano['lucro_acumulado'] = df_ano['lucro'].cumsum()
        return df_ano
