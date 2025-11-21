from dataclasses import dataclass

@dataclass
class Financeiro:
    ano: int
    mes: str
    faturamento: float
    despesas: float
    custo: float
    impostos: float
    id: int = None  # ID opcional, gerado pelo DB
