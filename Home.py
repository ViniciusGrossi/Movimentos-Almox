import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config('Consulta Estoque', layout='wide')

# Carregar os dados diretamente do arquivo local
arquivo = 'C:/Users/User/Documents/Data Analysis/Projeto_Estoque/Movimentos/Movimentos.xlsx'
df = pd.read_excel(arquivo, parse_dates=['Data'])  

# Configurações da página
st.title("Visualização de Estoque")
st.sidebar.header("Configurações do Filtro")

# Adicionar colunas de Ano e Mês
df['Ano'] = df['Data'].dt.year
df['Mes'] = df['Data'].dt.month

# Campo de busca
descricoes = df['Descricao'].unique().tolist()
codigos = df['Codigo'].unique().tolist()
opcoes_busca = descricoes + codigos

# Filtro por Descrição ou Código (Campo de Busca)
descricao_selecionada = st.selectbox(
    'Pesquisar por Descrição ou Código',
    options=[''] + opcoes_busca,
    index=0
)

# Filtros por Ano e Mês
anos_selecionados = st.sidebar.multiselect(
    "Selecione os Anos",
    options=sorted(df['Ano'].unique()),
    default=sorted(df['Ano'].unique())
)

meses_selecionados = st.sidebar.multiselect(
    "Selecione os Meses",
    options=sorted(df['Mes'].unique()),
    default=sorted(df['Mes'].unique())
)

# Aplicação dos Filtros
df_filtered = df.copy()

# Filtro por Descrição ou Código
if descricao_selecionada:
    if descricao_selecionada in descricoes:
        df_filtered = df_filtered[df_filtered['Descricao'] == descricao_selecionada]
    elif descricao_selecionada in codigos:
        df_filtered = df_filtered[df_filtered['Codigo'] == descricao_selecionada]

# Filtros por Ano e Mês
if anos_selecionados:
    df_filtered = df_filtered[df_filtered['Ano'].isin(anos_selecionados)]

if meses_selecionados:
    df_filtered = df_filtered[df_filtered['Mes'].isin(meses_selecionados)]

# Exibir seleções no painel principal
if descricao_selecionada:
    st.write(f"**Filtro Aplicado:** {descricao_selecionada}")
else:
    st.write("**Nenhum filtro por descrição ou código foi aplicado.**")

# Exibir gráfico e dataframe
if not df_filtered.empty:
    # Calcular soma e média das quantidades
    total_quantidade = df_filtered['Quantidade'].sum()
    media_quantidade = df_filtered['Quantidade'].mean()

    # Exibir as métricas
    st.subheader("Métricas Resumo")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Soma da Quantidade", value=int(total_quantidade))
    with col2:
        st.metric(label="Média da Quantidade", value=f"{media_quantidade:.2f}")

    # Exibir o dataframe filtrado
    st.subheader("Dados Filtrados")
    st.dataframe(df_filtered)

    # Gráfico de linha por data
    df_aux = df_filtered.groupby(['Data'])['Quantidade'].sum().reset_index()
    fig = px.line(df_aux, x='Data', y='Quantidade', title="Quantidade por Data (com filtros aplicados)")
    st.plotly_chart(fig)

    # Gráfico de barras por ano e mês
    df_aux = df_filtered.groupby(['Ano', 'Mes'])['Quantidade'].sum().reset_index()
    fig = px.bar(
        df_aux,
        x='Ano',
        y='Quantidade',
        color='Mes',
        title="Quantidade por Ano e Mês (com filtros aplicados)",
        labels={'Quantidade': 'Quantidade Total', 'Ano': 'Ano'}
    )
    st.plotly_chart(fig)
else:
    st.warning("Nenhum dado encontrado para os filtros aplicados.")
