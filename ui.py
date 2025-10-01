import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from models import Financeiro
from predictor import FinanceiroPredictor

# CSS simples para aparência mais moderna
STYLE = """
<style>
/* Remove Streamlit header and footer (opcional) */
.header, .stApp > header, footer {visibility: hidden;}
/* Card-like container */
.card {
  background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(245,245,245,0.98));
  padding: 12px;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(0,0,0,0.06);
  margin-bottom: 12px;
}
.kpi {
  font-size: 20px;
  color: #111827;
}
.small {
  color: #6b7280;
  font-size: 12px;
}
</style>
"""

class DashboardUI:
    def __init__(self, service, repository):
        self.service = service
        self.repo = repository
        self.predictor = FinanceiroPredictor()

    def render(self):
        st.markdown(STYLE, unsafe_allow_html=True)
        st.set_page_config(layout="wide", page_title="Dashboard Financeiro Moderno")
        st.title("💼 Dashboard Financeiro — Moderno")

        MESES = self.service.MESES_ORDENADOS

        # LAYOUT: barra lateral com controles e área principal com visualizações
        with st.sidebar:
            st.header("Controles")
            ano_default = int(st.number_input("Ano padrão (para adicionar)", 2000, 2100, value=st.session_state.get("ano_default", 2025)))
            st.session_state["ano_default"] = ano_default
            meses_futuros = st.number_input("Meses para previsão (OpenAI)", min_value=1, max_value=12, value=3)
            model_select = st.selectbox("Modelo OpenAI", options=["gpt-4","gpt-4o","gpt-4o-mini","gpt-3.5-turbo"], index=0)
            st.markdown("---")
            st.write("⚠️ Configure `OPENAI_API_KEY` no ambiente antes de usar previsões.")
            st.button("Atualizar previsão", key="btn_refresh_pred")

        # ADD / EDIT / DELETE cards
        with st.container():
            with st.expander("➕ Adicionar Dados Mensais", expanded=False):
                with st.form("form_add"):
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        ano = st.number_input("Ano", 2000, 2100, value=ano_default, key="add_ano")
                    with c2:
                        mes = st.selectbox("Mês", MESES, key="add_mes")
                    with c3:
                        faturamento = st.number_input("Faturamento (R$)", 0.0, 1e9, 0.0, step=100.0, key="add_fat")
                    with c4:
                        despesas = st.number_input("Despesas (R$)", 0.0, 1e9, 0.0, step=100.0, key="add_desp")
                    c5, c6 = st.columns(2)
                    with c5:
                        custo = st.number_input("Custo (R$)", 0.0, 1e9, 0.0, step=100.0, key="add_custo")
                    with c6:
                        impostos = st.number_input("Impostos (R$)", 0.0, 1e9, 0.0, step=100.0, key="add_imp")
                    if st.form_submit_button("Salvar", type="primary"):
                        if faturamento <= 0:
                            st.error("Faturamento precisa ser maior que zero.")
                        else:
                            financeiro = Financeiro(int(ano), mes, float(faturamento), float(despesas), float(custo), float(impostos))
                            if self.repo.inserir(financeiro):
                                st.success(f"✅ {mes}/{ano} salvo.")
                                st.experimental_rerun()

            with st.expander("✏️ Editar / ❌ Excluir", expanded=False):
                df_all = self.repo.listar()
                if df_all.empty:
                    st.info("Nenhum registro encontrado.")
                else:
                    st.dataframe(df_all.drop(columns=["id"]), use_container_width=True)
                    ids = df_all["id"].tolist()
                    id_sel = st.selectbox("Selecione ID", ids, key="sel_edit")
                    registro = df_all[df_all["id"] == id_sel].iloc[0]
                    with st.form("form_edit"):
                        e1, e2, e3, e4 = st.columns(4)
                        with e1:
                            ano_e = st.number_input("Ano", value=int(registro["ano"]), key="e_ano")
                        with e2:
                            mes_e = st.selectbox("Mês", MESES, index=MESES.index(registro["mes"]) if registro["mes"] in MESES else 0, key="e_mes")
                        with e3:
                            fatur_e = st.number_input("Faturamento", value=float(registro["faturamento"]), key="e_fat")
                        with e4:
                            desp_e = st.number_input("Despesas", value=float(registro["despesas"]), key="e_desp")
                        e5, e6 = st.columns(2)
                        with e5:
                            custo_e = st.number_input("Custo", value=float(registro["custo"]), key="e_custo")
                        with e6:
                            imp_e = st.number_input("Impostos", value=float(registro["impostos"]), key="e_imp")
                        col_update, col_del = st.columns(2)
                        if col_update.form_submit_button("Atualizar"):
                            financeiro = Financeiro(int(ano_e), mes_e, float(fatur_e), float(desp_e), float(custo_e), float(imp_e))
                            if self.repo.atualizar(id_sel, financeiro):
                                st.success("Registro atualizado.")
                                st.experimental_rerun()
                        if col_del.form_submit_button("Excluir"):
                            if self.repo.deletar(id_sel):
                                st.warning("Registro excluído.")
                                st.experimental_rerun()

        # DASHBOARD PRINCIPAL (visuais)
        df = self.service.get_dados()
        if df.empty:
            st.warning("Sem dados. Adicione registros para visualizar o dashboard.")
            return

        anos = sorted(df["ano"].unique(), reverse=True)
        ano_sel = st.selectbox("Ano para análise", anos, index=0, key="sel_ano_analise")
        df_ano = self.service.dados_por_ano(ano_sel)

        # KPIs em cards estilizados
        fatur = df_ano['faturamento'].sum()
        desp = df_ano['despesas'].sum()
        custo = df_ano['custo'].sum()
        imp = df_ano['impostos'].sum()
        lucro = df_ano['lucro'].sum()
        margem = df_ano['margem'].mean()

        k1, k2, k3, k4, k5 = st.columns([1.6,1.6,1.6,1.6,1.6])
        k1.markdown(f'<div class="card"><div class="kpi"><b>Faturamento</b><div class="small">Total ano</div><h3>R$ {fatur:,.2f}</h3></div></div>', unsafe_allow_html=True)
        k2.markdown(f'<div class="card"><div class="kpi"><b>Lucro</b><div class="small">Total ano</div><h3>R$ {lucro:,.2f}</h3></div></div>', unsafe_allow_html=True)
        k3.markdown(f'<div class="card"><div class="kpi"><b>Despesas</b><div class="small">Total ano</div><h3>R$ {desp:,.2f}</h3></div></div>', unsafe_allow_html=True)
        k4.markdown(f'<div class="card"><div class="kpi"><b>Custos</b><div class="small">Total ano</div><h3>R$ {custo:,.2f}</h3></div></div>', unsafe_allow_html=True)
        k5.markdown(f'<div class="card"><div class="kpi"><b>Margem Média</b><div class="small">Ano</div><h3>{margem:.2f}%</h3></div></div>', unsafe_allow_html=True)

        st.markdown("---")

        # Gráfico combinado (barras) + linha acumulada
        st.subheader("Evolução Mensal e Lucro Acumulado")
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Faturamento", x=df_ano["mes"], y=df_ano["faturamento"], marker_color="#4CAF50"))
        fig.add_trace(go.Bar(name="Despesas", x=df_ano["mes"], y=df_ano["despesas"], marker_color="#F44336"))
        fig.add_trace(go.Bar(name="Custos", x=df_ano["mes"], y=df_ano["custo"], marker_color="#FF9800"))
        fig.add_trace(go.Bar(name="Impostos", x=df_ano["mes"], y=df_ano["impostos"], marker_color="#2196F3"))

        # Lucro acumulado com eixo Y secundário
        fig.add_trace(go.Scatter(name="Lucro Acumulado", x=df_ano["mes"], y=df_ano["lucro_acumulado"],
                                 mode="lines+markers", line=dict(color="#7E22CE", width=3), yaxis="y2"))

        # layout para eixo secundário
        fig.update_layout(
            barmode="group",
            xaxis_title="Mês",
            yaxis=dict(title="R$ (Mensal)"),
            yaxis2=dict(title="R$ (Acumulado)", overlaying="y", side="right"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True, height=500)

        st.markdown("---")

        # Previsões com OpenAI
        st.subheader("🔮 Previsão de Lucro (OpenAI) & Insights")
        # troca de modelo selecionado na sidebar (opcional)
        predictor_model = st.sidebar.selectbox("Modelo para previsão (sob demanda):", options=["gpt-4","gpt-4o","gpt-3.5-turbo"], index=0)
        # atualiza o predictor dinamicamente
        self.predictor.modelo = predictor_model

        # botão para solicitar previsão
        if st.button("Gerar previsão e insights"):
            with st.spinner("Gerando previsões com OpenAI..."):
                df_prev = self.predictor.prever_lucro(df_ano, meses_futuros=st.sidebar.number_input("Meses futuros (sidebar)", 1, 12, value=meses_futuros))
                insights = self.predictor.gerar_insights(df)
                if not df_prev.empty:
                    st.markdown("**Previsões (próximos meses)**")
                    st.dataframe(df_prev)
                    # plot histórico + previsões
                    fig_prev = go.Figure()
                    # histórico lucro
                    fig_prev.add_trace(go.Scatter(x=df_ano["mes"], y=df_ano["lucro"], mode="lines+markers", name="Lucro Hist.", line=dict(color="#0ea5a4")))
                    # previsões (meses futuros)
                    fig_prev.add_trace(go.Scatter(x=df_prev["mes"], y=df_prev["lucro_previsto"], mode="lines+markers", name="Lucro Previsto", line=dict(color="#7E22CE", dash="dot")))
                    fig_prev.update_layout(title="Lucro Histórico vs Previsto", yaxis_title="R$")
                    st.plotly_chart(fig_prev, use_container_width=True)
                else:
                    st.info("Não foi possível gerar previsões (verifique OPENAI_API_KEY e limites).")

                st.markdown("**Insights gerados:**")
                st.info(insights)
