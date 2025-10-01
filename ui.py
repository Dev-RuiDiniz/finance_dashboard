import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from models import Financeiro
from predictor import FinanceiroPredictor

class DashboardUI:
    def __init__(self, service, repository):
        self.service = service
        self.repo = repository
        self.predictor = FinanceiroPredictor()

    def set_style(self):
        st.markdown("""
            <style>
            /* Tema Moderno e Claro */

            /* Fundo principal: Branco 'puro' para clareza máxima */
            body {
                background-color: #FFFFFF; /* Branco */
                color: #333333; /* Texto principal mais escuro */
            }
            /* Sidebar: Um cinza muito, muito claro */
            section[data-testid="stSidebar"] {
                background-color: #F8F9FA; /* Cinza muito claro */
                box-shadow: 2px 0 5px rgba(0,0,0,0.05); /* Sombra sutil */
            }
            /* Títulos: Azul moderno, vibrante e claro */
            h1, h2, h3 {
                color: #007BFF; /* Azul principal moderno */
                font-weight: 700;
            }
            /* KPIs como cards: Fundo branco com sombra suave */
            div[data-testid="stMetric"] {
                background: #FFFFFF;
                border-radius: 12px;
                padding: 16px; 
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Sombra suave */
                border: 1px solid #EAEAEA; /* Borda sutil */
            }
            /* Texto secundário (para info/legendas) */
            p, label, span {
                color: #495057; 
            }
            /* Cor do delta de KPI (para contraste) */
            div[data-testid="stMetricDelta"] span {
                color: #28a745 !important; /* Verde moderno para positivo */
            }
            </style>
        """, unsafe_allow_html=True)

    def render(self):
        # --- aplicar estilo ---
        self.set_style()

        st.title("💼 Dashboard Financeiro")
        MESES = self.service.MESES_ORDENADOS

        # --- Adicionar (continua o mesmo) ---
        with st.expander("➕ Adicionar Dados Mensais", expanded=True):
            with st.form("form_financeiro"):
                col1, col2, col3, col4 = st.columns(4)
                with col1: ano = st.number_input("Ano", 2000, 2100, 2025)
                with col2: mes = st.selectbox("Mês", MESES)
                with col3: faturamento = st.number_input("Faturamento (R$)", 0.0, 1e9, 0.0, step=100.0)
                with col4: despesas = st.number_input("Despesas (R$)", 0.0, 1e9, 0.0, step=100.0)
                col5, col6 = st.columns(2)
                with col5: custo = st.number_input("Custo (R$)", 0.0, 1e9, 0.0, step=100.0)
                with col6: impostos = st.number_input("Impostos (R$)", 0.0, 1e9, 0.0, step=100.0)
                if st.form_submit_button("Salvar"):
                    financeiro = Financeiro(ano, mes, faturamento, despesas, custo, impostos)
                    if self.repo.inserir(financeiro):
                        st.success(f"✅ Dados de {mes}/{ano} adicionados!")
                        st.rerun()

        # --- Editar / Deletar (continua o mesmo) ---
        with st.expander("✏️ Editar / ❌ Excluir"):
            df_all = self.repo.listar()
            if not df_all.empty:
                st.dataframe(df_all.drop(columns=['id']), use_container_width=True)
                id_sel = st.selectbox("Selecione ID:", df_all["id"].tolist())
                registro = df_all[df_all["id"] == id_sel].iloc[0]
                with st.form("form_editar"):
                    ano_e = st.number_input("Ano", value=int(registro["ano"]))
                    mes_e = st.selectbox("Mês", MESES, index=MESES.index(registro["mes"]))
                    faturamento_e = st.number_input("Faturamento", value=float(registro["faturamento"]))
                    despesas_e = st.number_input("Despesas", value=float(registro["despesas"]))
                    custo_e = st.number_input("Custo", value=float(registro["custo"]))
                    impostos_e = st.number_input("Impostos", value=float(registro["impostos"]))
                    col1, col2 = st.columns(2)
                    if col1.form_submit_button("Atualizar"):
                        financeiro = Financeiro(ano_e, mes_e, faturamento_e, despesas_e, custo_e, impostos_e)
                        if self.repo.atualizar(id_sel, financeiro):
                            st.success("✅ Registro atualizado")
                            st.rerun()
                    if col2.form_submit_button("Excluir"):
                        if self.repo.deletar(id_sel):
                            st.warning("❌ Registro excluído")
                            st.rerun()

        # --- Dashboard ---
        df = self.service.get_dados()
        if df.empty:
            st.warning("Nenhum dado para exibir")
            return

        anos = sorted(df["ano"].unique(), reverse=True)
        ano_sel = st.selectbox("Ano para análise detalhada", anos)
        df_ano = self.service.dados_por_ano(ano_sel)

        # KPIs (Mantive o delta de Lucro com o novo estilo)
        st.subheader("📊 KPIs do Ano Selecionado")
        col1, col2, col3, col4, col5 = st.columns(5)
        fatur = df_ano['faturamento'].sum()
        desp = df_ano['despesas'].sum()
        custo = df_ano['custo'].sum()
        impostos = df_ano['impostos'].sum()
        lucro = df_ano['lucro'].sum()
        margem = df_ano['margem'].mean()
        col1.metric("Faturamento Total", f"R$ {fatur:,.2f}")
        col2.metric("Lucro Total", f"R$ {lucro:,.2f}", delta="↑" if lucro > 0 else "↓", delta_color="normal") # Usando delta_color="normal" para Streamlit respeitar o CSS
        col3.metric("Despesas Totais", f"R$ {desp:,.2f}")
        col4.metric("Custos Totais", f"R$ {custo:,.2f}")
        col5.metric("Margem Média", f"{margem:.2f}%")

        # Gráfico mensal + acumulado (CORES ATUALIZADAS)
        st.subheader("📈 Evolução Mensal + Lucro Acumulado")
        
        # Paleta de cores moderna:
        # Azul Principal: #007BFF
        # Despesas/Custos/Impostos (Tons de Cinza/Azul Suave):
        AZUL_PRINCIPAL = "#007BFF" 
        FUNDO_CLARO_A = "#3498db" # Azul um pouco mais claro
        FUNDO_CLARO_B = "#9BBFE0" # Azul acinzentado suave
        FUNDO_CLARO_C = "#BDD4E7" # Azul muito suave
        LINHA_LUCRO = "#28a745" # Verde para lucro (positivo)

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Faturamento", x=df_ano["mes"], y=df_ano["faturamento"], marker_color=AZUL_PRINCIPAL))
        fig.add_trace(go.Bar(name="Despesas", x=df_ano["mes"], y=df_ano["despesas"], marker_color=FUNDO_CLARO_A))
        fig.add_trace(go.Bar(name="Custos", x=df_ano["mes"], y=df_ano["custo"], marker_color=FUNDO_CLARO_B))
        fig.add_trace(go.Bar(name="Impostos", x=df_ano["mes"], y=df_ano["impostos"], marker_color=FUNDO_CLARO_C))
        
        # Lucro Acumulado em destaque (verde moderno)
        fig.add_trace(go.Scatter(name="Lucro Acumulado", x=df_ano["mes"], y=df_ano["lucro_acumulado"], mode="lines+markers", line=dict(color=LINHA_LUCRO, width=4)))
        
        # Atualização do layout para ser mais clean
        fig.update_layout(
            barmode="group", 
            yaxis_title="R$", 
            title=f"Evolução Mensal e Acumulado - {ano_sel}",
            plot_bgcolor='white', # Fundo do gráfico branco
            paper_bgcolor='white', # Fundo da área do gráfico branco
            font=dict(color='#333333'),
            hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial")
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- Previsão com OpenAI (CORES ATUALIZADAS) ---
        with st.expander("🔮 Previsão de Lucro com OpenAI"):
            previsoes = self.predictor.prever_lucro(df_ano, meses_futuros=3)
            if not previsoes.empty:
                st.dataframe(previsoes, use_container_width=True)
                fig_pred = px.line(
                    previsoes, x="mes", y="lucro_previsto", 
                    title="Previsão de Lucro", 
                    markers=True, line_shape="spline",
                    color_discrete_sequence=[AZUL_PRINCIPAL] # Usando o azul principal para a linha
                )
                
                # Ajustando o layout da Previsão também
                fig_pred.update_layout(
                    plot_bgcolor='white', 
                    paper_bgcolor='white', 
                    font=dict(color='#333333')
                )
                
                st.plotly_chart(fig_pred, use_container_width=True)
            else:
                st.info("Sem previsões disponíveis")