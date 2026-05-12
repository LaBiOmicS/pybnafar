import streamlit as st
import pandas as pd
import plotly.express as px
from pybnafar import Bnafar
import os
import sys

# Support for workspace via CLI arg (for Docker)
default_workspace = "bnafar_system"
if "--workspace" in sys.argv:
    idx = sys.argv.index("--workspace")
    if idx + 1 < len(sys.argv):
        default_workspace = sys.argv[idx + 1]

st.set_page_config(page_title="pybnafar - Painel de Gestão SUS", layout="wide")

st.title("🇧🇷 Painel de Inteligência Farmacêutica (BNAFAR)")
st.markdown("""
Este painel automatiza a análise de dados do OpenDATASUS para apoio à tomada de decisão na Assistência Farmacêutica.
""")

# Sidebar para configurações
st.sidebar.header("Configurações")
workspace = st.sidebar.text_input("Workspace", value=default_workspace)
bn = Bnafar(workspace=workspace)

if st.sidebar.button("🔄 Sincronizar Dados do Governo"):
    with st.spinner("Buscando snapshots oficiais..."):
        bn.sync()
        st.success("Sincronização concluída!")

# Carregamento de dados
@st.cache_data
def load_data(ufs=None):
    return bn.load_optimized(ufs=ufs)

df = load_data()

if df.empty:
    st.warning("O Data Lake está vazio. Clique em 'Sincronizar Dados' na barra lateral.")
else:
    # Filtros
    ufs = st.multiselect("Filtrar por Estados (UF)", options=sorted(df['sg_uf'].unique()))
    if ufs:
        df = df[df['sg_uf'].isin(ufs)]

    # Métricas Principais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Registros", f"{len(df):,}")
    
    with col2:
        conf_df = bn.analytics.calculate_confidence_score(df)
        avg_score = conf_df['confidence_score'].mean()
        st.metric("Score Médio de Confiança", f"{avg_score:.2f}")
    
    with col3:
        rupturas = bn.analytics.detect_real_ruptures(df)
        total_rupturas = len(rupturas['confirmed_ruptures'])
        st.metric("Rupturas Confirmadas", total_rupturas)

    # Gráficos
    st.divider()
    g1, g2 = st.columns(2)

    with g1:
        st.subheader("Distribuição do Score de Confiança")
        fig_score = px.histogram(conf_df, x="confidence_score", color="confidence_category",
                                 title="Municípios por Nível de Confiança",
                                 labels={'confidence_score': 'Score', 'count': 'Número de Municípios'})
        st.plotly_chart(fig_score, use_container_width=True)

    with g2:
        st.subheader("Risco de Desperdício (Vencimento Próximo)")
        waste_df = bn.analytics.calculate_priority_waste(df, days=90)
        if not waste_df.empty:
            fig_waste = px.bar(waste_df.head(10), x="severity_index", y="ds_produto", orientation='h',
                               title="Top 10 Medicamentos com Maior Risco Financeiro",
                               labels={'severity_index': 'Índice de Gravidade', 'ds_produto': 'Medicamento'})
            st.plotly_chart(fig_waste, use_container_width=True)
        else:
            st.info("Nenhum registro de vencimento próximo detectado nos filtros atuais.")

    # Tabela de Detalhes
    st.subheader("Dados Detalhados")
    st.dataframe(df.head(100), use_container_width=True)

    # Exportação FHIR
    if st.button("📦 Exportar para HL7 FHIR (RNDS)"):
        fhir_json = bn.interop.to_fhir_inventory(df.head(10)) # Exemplo com 10
        st.download_button("Baixar JSON FHIR", fhir_json, file_name="bnafar_fhir.json", mime="application/json")

st.sidebar.info(f"Dados armazenados em: {workspace}")
