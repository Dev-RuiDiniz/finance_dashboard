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

* **Python 3.x**
* **Streamlit:** Para a construção rápida e interativa da interface de usuário (UI).
* **Plotly/Plotly Express:** Para gráficos dinâmicos e de alta qualidade.
* **Pandas:** Para manipulação e análise de dados eficiente.
* **Módulos Internos:** `models`, `repository`, `service` e `predictor` para a arquitetura do projeto.

---

## 🚀 Como Executar o Projeto

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

O projeto agora está organizado como um pacote Python `finance_dashboard` com um entrypoint para execução via módulo.

Recomendo iniciar com o Streamlit apontando para o `main.py` no nível do repositório:

```powershell
streamlit run main.py
```

Alternativamente (nem sempre necessário) você pode executar o pacote diretamente (para testes rápidos de import):

```powershell
python -m finance_dashboard
```

O Streamlit abrirá o dashboard em `http://localhost:8501`.

---
### Observações

- Arquitetura: os módulos foram movidos para o pacote `finance_dashboard/` (ex.: `finance_dashboard/ui.py`, `finance_dashboard/service.py`).
- Arquivos no nível superior (`ui.py`, `service.py`, etc.) agora reexportam (shims) para compatibilidade.
- Se houver problemas ao rodar, verifique versões das dependências e se a `OPENAI_API_KEY` está definida.

---

## 🎨 **Detalhes do Design**
O design foi cuidadosamente atualizado para um visual mais premium:

- Elemento	Estilo
- Fundo	Branco puro (#FFFFFF)
- Títulos	Azul moderno (#007BFF), em negrito
- KPI Cards	Fundo branco com sombra suave (box-shadow)
- Inputs/Selects	Cantos arredondados (8px) e borda suave
- Gráficos	Fundo Plotly em branco para integrar-se ao tema
---

## 🤝 **Contribuições**
Sua contribuição é muito bem-vinda! Sinta-se à vontade para abrir Issues para bugs ou sugestões, ou enviar Pull Requests com melhorias no código ou no design.
