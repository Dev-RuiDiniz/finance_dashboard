# 📈 Dashboard Financeiro Interativo

Um sistema de dashboard financeiro moderno e interativo construído com **Streamlit**, **Plotly** para visualização e um modelo de **Previsão** (integrado via `FinanceiroPredictor`) para análise preditiva de lucros.

O design do dashboard foi otimizado com um tema **claro, limpo e moderno** para garantir a melhor experiência e legibilidade, aplicando um estilo clean à página inteira.

---

## 🌟 Funcionalidades Principais

* **CRUD de Dados Simplificado:** Interface amigável para **adicionar, editar e excluir** registros financeiros mensais (Faturamento, Despesas, Custos e Impostos).
* **KPIs em Destaque:** Visualização imediata dos principais indicadores do ano selecionado, como **Faturamento Total, Lucro Total e Margem Média**, exibidos em cards modernos.
* **Visualização Mensal e Acumulada:** Gráfico interativo do Plotly mostrando a **Evolução Mensal** dos componentes (Faturamento vs. Custos) e o **Lucro Acumulado** em destaque.
* **Previsão Preditiva:** Utiliza o módulo `FinanceiroPredictor` para gerar **previsões de Lucro** para os próximos meses, permitindo uma análise prospectiva.
* **Design Moderno:** Estilo visual *clean*, com fundo branco, títulos em azul moderno, inputs arredondados e ótima legibilidade.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.8+**
* **Streamlit:** Para a construção rápida e interativa da interface de usuário (UI).
* **Plotly/Plotly Express:** Para gráficos dinâmicos e de alta qualidade.
* **Pandas:** Para manipulação e análise de dados eficiente.
* **OpenAI API:** Para previsões preditivas e geração de insights (opcional).
* **SQLite:** Banco de dados local para armazenamento de dados financeiros.
* **Estrutura em Pacote Python:** Módulos organizados dentro de `finance_dashboard/` para melhor manutenibilidade.

---

## 📁 Estrutura do Projeto

Após a refatoração, o projeto está organizado em uma estrutura de pacote Python limpa e modular:

```
finance_dashboard/
├── __init__.py              # Inicializa o pacote
├── __main__.py              # Ponto de entrada para python -m finance_dashboard
├── models.py                # Definição da classe Financeiro (dataclass)
├── repository.py            # Camada de acesso aos dados (SQLite)
├── service.py               # Lógica de negócio e cálculo de KPIs
├── predictor.py             # Integração com OpenAI para previsões
└── ui.py                    # Interface Streamlit (DashboardUI)

main.py                      # Wrapper que chama finance_dashboard.__main__
requirements.txt             # Dependências do projeto
README.md                    # Este arquivo
tools/
└── import_check.py          # Script para validar sintaxe dos módulos
```

### Camadas Arquiteturais

- **Models:** Classes de dados (`Financeiro`) com schema bem definido.
- **Repository:** Acesso e manipulação de dados no banco SQLite.
- **Service:** Lógica de negócio, cálculo de KPIs e transformação de dados.
- **Predictor:** Integração com IA (OpenAI) para gerar previsões e insights.
- **UI:** Interface interativa com Streamlit, renderização de gráficos e formulários.

Siga os passos abaixo para preparar o ambiente e iniciar o dashboard (atualizado para a estrutura em pacote).

### 1. Pré-requisitos

Certifique-se de ter o **Python** (versão 3.8+) instalado em sua máquina.

### 2. Configuração do Ambiente

```powershell
# 1. Clone o repositório (se necessário)
git clone <URL_DO_SEU_REPOSITORIO>
cd finance_dashboard

# 2. Crie e ative o ambiente virtual (PowerShell)
python -m venv .venv
. .venv\Scripts\Activate.ps1

# 3. Instale as dependências listadas
pip install -r requirements.txt
```

### 3. Variáveis de ambiente (OpenAI)

Se usar integração com OpenAI, defina a variável `OPENAI_API_KEY`. No PowerShell temporariamente:

```powershell
$env:OPENAI_API_KEY = 'sua_chave_aqui'
```

Para definir de forma persistente no Windows (opcional):

```powershell
setx OPENAI_API_KEY "sua_chave_aqui"
```

### 4. Execução do Dashboard

O projeto agora está organizado como um pacote Python `finance_dashboard` executável.

**Opção 1: Recomendada (via Streamlit)**

```powershell
streamlit run main.py
```

**Opção 2: Via módulo Python**

```powershell
python -m finance_dashboard
```

O Streamlit abrirá o dashboard em `http://localhost:8501`.

---

## 🔧 Desenvolvimento

### Validar Sintaxe dos Módulos

Para verificar se todos os módulos do pacote compilam corretamente:

```powershell
python tools/import_check.py
```

### Estrutura de Imports

Após a refatoração, os imports dentro do pacote usam caminhos relativos:

```python
# Correto (dentro de finance_dashboard/)
from .models import Financeiro
from .repository import FinanceiroRepository

# Externo (fora do pacote)
from finance_dashboard.service import FinanceiroService
```

### Adicionando Novos Módulos

Se precisar adicionar um novo módulo:
1. Crie o arquivo dentro de `finance_dashboard/` (ex.: `analytics.py`).
2. Atualize `finance_dashboard/__init__.py` se quiser exportar publicamente.
3. Importe usando caminho relativo internamente (ex.: `from .analytics import ...`).

---
### Observações Importantes

- **Pacote Único:** Os módulos estão **exclusivamente** dentro de `finance_dashboard/`. Não há mais shims no nível raiz.
- **Imports:** Use sempre caminhos relativos para imports internos (ex.: `from .models import Financeiro`).
- **Variáveis de Ambiente:** A chave `OPENAI_API_KEY` é necessária apenas se usar a funcionalidade de previsão com OpenAI.
- **Banco de Dados:** O SQLite (`financeiro.db`) é criado automaticamente no diretório raiz na primeira execução.

---

---

## 🎨 Detalhes do Design

O design foi cuidadosamente atualizado para um visual moderno e premium:

| Elemento | Estilo |
|----------|--------|
| Fundo | Branco puro (#FFFFFF) |
| Títulos | Azul moderno (#007BFF), em negrito |
| KPI Cards | Fundo branco com sombra suave (box-shadow) |
| Inputs/Selects | Cantos arredondados (8px) e borda suave |
| Gráficos | Fundo Plotly em branco para integrar-se ao tema |
| Sidebar | Cinza muito claro (#F8F9FA) com sombra sutil |

---

## 📋 Funcionalidades do CRUD

1. **Adicionar Dados:** Preencha ano, mês, faturamento, despesas, custos e impostos. Os dados são salvos automaticamente no SQLite.
2. **Visualizar:** Todos os registros são listados em uma tabela interativa.
3. **Editar:** Selecione um registro pelo ID e atualize os valores.
4. **Deletar:** Remova registros que não são mais necessários.

---

## 📊 KPIs e Visualizações

- **Faturamento Total:** Soma de todos os faturamentos do período.
- **Lucro Total:** Faturamento menos (Despesas + Custos + Impostos).
- **Margem Média:** Margem de lucro média em percentual.
- **Evolução Mensal:** Gráfico de barras agrupadas mostrando faturamento vs. despesas vs. custos vs. impostos.
- **Lucro Acumulado:** Linha contínua mostrando lucro acumulado ao longo dos meses.

---

## 🤖 Previsões com OpenAI

Se configurar a chave `OPENAI_API_KEY`, você pode:
- Gerar **previsões de lucro** para os próximos 3 meses usando IA.
- Receber **insights automáticos** sobre a saúde financeira do negócio.

> **Nota:** OpenAI é opcional. O dashboard funciona perfeitamente sem ela.

---

## 🤝 Contribuições

Sua contribuição é muito bem-vinda! Sinta-se à vontade para:
- Abrir **Issues** para reportar bugs ou sugerir melhorias.
- Enviar **Pull Requests** com novos recursos ou correções.
- Melhorar a documentação ou o design.
