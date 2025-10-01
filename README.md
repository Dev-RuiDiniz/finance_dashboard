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

Siga os passos abaixo para preparar o ambiente e iniciar o dashboard.

### 1. Pré-requisitos

Certifique-se de ter o **Python** (versão 3.8+) instalado em sua máquina.

### 2. Configuração do Ambiente

```bash
# 1. Clone o repositório
git clone <URL_DO_SEU_REPOSITORIO>
cd dashboard-financeiro

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # No Linux/macOS
# ou
.\venv\Scripts\activate    # No Windows

# 3. Instale as dependências
pip install streamlit pandas plotly

⚠️ Atenção: Este projeto depende dos arquivos locais (models.py, predictor.py, etc.). Certifique-se de que todos os módulos necessários para a classe DashboardUI estão presentes.

3. Execução do Dashboard
Com o ambiente virtual ativado, inicie a aplicação:

Bash

streamlit run seu_arquivo_principal.py 
O dashboard será aberto no seu navegador em http://localhost:8501.

🎨 Detalhes do Design
O design foi cuidadosamente atualizado para um visual mais premium:

Elemento	Estilo
Fundo	Branco puro (#FFFFFF)
Títulos	Azul moderno (#007BFF), em negrito
KPI Cards	Fundo branco com sombra suave (box-shadow)
Inputs/Selects	Cantos arredondados (8px) e borda suave
Gráficos	Fundo Plotly em branco para integrar-se ao tema

Exportar para as Planilhas
🤝 Contribuições
Sua contribuição é muito bem-vinda! Sinta-se à vontade para abrir Issues para bugs ou sugestões, ou enviar Pull Requests com melhorias no código ou no design.
