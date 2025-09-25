import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configurações Iniciais da Página ---
st.set_page_config(
    page_title="Análise de Clubes do Brasileirão 2014",
    page_icon="⚽",
    layout="wide"
)

# --- Função de Carregamento de Dados ---
@st.cache_data
def carregar_dados(caminho_arquivo):
    """
    Função para carregar e preparar os dados do CSV.
    A anotação @st.cache_data garante que os dados sejam carregados apenas uma vez.
    """
    df = pd.read_csv(caminho_arquivo)
    
    # Renomeia a coluna 'Pos.' para 'Posicao' para evitar conflitos com a nova coluna
    if 'Pos.' in df.columns:
        df = df.rename(columns={'Pos.': 'Posicao_Original'})
        
    # Adiciona a coluna de Posição baseada na ordem inicial do arquivo
    df['Posição'] = df['Posicao_Original']
    
    # Converte colunas de valor para o tipo numérico correto
    colunas_valor = ['Valor_total_formatted', 'Media_Valor_formatted']
    for col in colunas_valor:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace('.', '', regex=False).astype(int)
            
    return df

# --- Carregamento dos Dados ---
# O caminho foi ajustado para funcionar no Streamlit Cloud, que executa
# o script a partir da pasta raiz do repositório.
try:
    df_clubes = carregar_dados('CienciadeDados/Tabela_Clubes_2014.csv')
except FileNotFoundError:
    st.error("Arquivo 'CienciadeDados/Tabela_Clubes_2014.csv' não encontrado. Verifique se a estrutura de pastas no seu repositório GitHub está correta.")
    st.stop()


# --- Barra Lateral com Filtros ---
st.sidebar.header('Filtros')
clubes_lista = df_clubes['Clubes'].unique().tolist()
clubes_lista.insert(0, 'Todos') # Adiciona a opção "Todos" no início da lista

clube_selecionado = st.sidebar.selectbox(
    'Selecione um clube:',
    options=clubes_lista
)

# --- Início da Aplicação Streamlit ---
st.title('Análise de Clubes - Brasileirão 2014 ⚽')

st.markdown("""
Esta aplicação interativa realiza uma análise visual dos dados dos clubes de futebol
que participaram do campeonato brasileiro de 2014. Use o filtro na barra lateral para
analisar um time específico em comparação com os outros.
""")

# --- Seção de Classificação ---
st.header('Tabela de Classificação Final')
# Define o DataFrame a ser exibido, ordenando pela posição de forma crescente
tabela_para_exibir = df_clubes.sort_values(by='Posição', ascending=True).set_index('Posição')
st.dataframe(tabela_para_exibir[['Clubes', 'Vitorias', 'Derrotas', 'Empates', 'Saldo', 'Gols', 'GolsSofridos']])


# --- Seção de Análises Gráficas ---
st.header('Análises Gráficas Comparativas')

# Exibe as métricas apenas quando um clube específico é selecionado
if clube_selecionado != 'Todos':
    st.subheader(f'Métricas Principais de {clube_selecionado}')
    
    # Filtra os dados para o clube selecionado para buscar as métricas
    df_filtrado = df_clubes[df_clubes['Clubes'] == clube_selecionado]
    
    col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
    
    vitorias = df_filtrado.iloc[0]['Vitorias']
    saldo_gols = df_filtrado.iloc[0]['Saldo']
    gols_pro = df_filtrado.iloc[0]['Gols']
    valor_milhoes = df_filtrado.iloc[0]['Valor_total_formatted'] / 1_000_000

    col_metric1.metric("Vitórias", vitorias)
    col_metric2.metric("Saldo de Gols", saldo_gols)
    col_metric3.metric("Gols Marcados", gols_pro)
    col_metric4.metric("Valor do Elenco (Milhões €)", f"{valor_milhoes:.2f} M")

    st.divider()

# --- Os gráficos são exibidos em qualquer seleção (Todos ou clube específico) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader('Ranking de Vitórias por Clube')
    
    # Ordena os dados para o gráfico
    vitorias_por_clube = df_clubes.sort_values('Vitorias', ascending=False)
    
    # Lógica de cores dinâmicas
    if clube_selecionado == 'Todos':
        palette = sns.color_palette('viridis', n_colors=len(vitorias_por_clube))
    else:
        palette = ['#ff7f0e' if clube == clube_selecionado else '#d3d3d3' for clube in vitorias_por_clube['Clubes']]

    fig1, ax1 = plt.subplots(figsize=(10, 8))
    sns.barplot(data=vitorias_por_clube, x='Vitorias', y='Clubes', ax=ax1, palette=palette)
    ax1.set_title('Número de Vitórias por Clube em 2014')
    ax1.set_xlabel('Número de Vitórias')
    ax1.set_ylabel('Clube')
    plt.tight_layout()
    st.pyplot(fig1)

with col2:
    st.subheader('Desempenho Ofensivo vs. Defensivo')

    fig2, ax2 = plt.subplots(figsize=(10, 8))

    # Calcula as médias para as linhas dos quadrantes
    avg_gols_marcados = df_clubes['Gols'].mean()
    avg_gols_sofridos = df_clubes['GolsSofridos'].mean()

    # Desenha as linhas de média
    ax2.axvline(avg_gols_marcados, color='grey', linestyle='--', lw=1)
    ax2.axhline(avg_gols_sofridos, color='grey', linestyle='--', lw=1)

    # Cria o gráfico de dispersão principal para todos os clubes
    sns.scatterplot(
        data=df_clubes, x='Gols', y='GolsSofridos',
        s=150, alpha=0.7, ax=ax2, legend=False,
        color='#1f77b4'  # Uma cor única para todos os pontos
    )

    # Adiciona os rótulos de texto para cada clube
    for i, row in df_clubes.iterrows():
        ax2.text(row['Gols'] + 0.5, row['GolsSofridos'], row['Clubes'], fontsize=8)

    # Se um clube for selecionado, destaca-o
    if clube_selecionado != 'Todos':
        df_selecionado = df_clubes[df_clubes['Clubes'] == clube_selecionado]
        sns.scatterplot(
            data=df_selecionado, x='Gols', y='GolsSofridos',
            s=350, ax=ax2, legend=False,
            color='#ff7f0e', edgecolor='black', linewidth=1.5
        )
        # Torna o rótulo do clube selecionado maior e a negrito
        ax2.text(df_selecionado['Gols'].iloc[0] + 0.5, df_selecionado['GolsSofridos'].iloc[0],
                 df_selecionado['Clubes'].iloc[0], fontsize=10, fontweight='bold', color='black')

    # Adiciona a linha diagonal (saldo de golos zero)
    limite_max = max(df_clubes['Gols'].max(), df_clubes['GolsSofridos'].max())
    ax2.plot([0, limite_max + 5], [0, limite_max + 5], 'r--', lw=1)
    
    # Títulos e rótulos dos eixos
    ax2.set_title('Desempenho Ofensivo vs. Defensivo dos Clubes')
    ax2.set_xlabel('Golos Marcados (Melhor →)')
    ax2.set_ylabel('Golos Sofridos (Melhor ↓)')

    plt.tight_layout()
    st.pyplot(fig2)
    
    st.markdown("""
    **Como interpretar o gráfico:**
    * **Eixo X (Horizontal):** Quanto mais à direita, melhor o ataque (mais golos marcados).
    * **Eixo Y (Vertical):** Quanto mais abaixo, melhor a defesa (menos golos sofridos).
    * **Linhas Tracejadas cinzentas:** Representam a média do campeonato. Elas dividem o gráfico em quatro quadrantes.
    * **Quadrante Ideal:** O quadrante inferior direito representa um ataque acima da média e uma defesa também acima da média.
    """)

st.subheader('Valor de Mercado Total dos Clubes (em milhões de €)')

# Ordena os dados para o gráfico de valor de mercado
valor_mercado = df_clubes.sort_values('Valor_total_formatted', ascending=False)

# Lógica de cores dinâmicas
if clube_selecionado == 'Todos':
    palette_valor = sns.color_palette('mako', n_colors=len(valor_mercado))
else:
    palette_valor = ['#1f77b4' if clube == clube_selecionado else '#d3d3d3' for clube in valor_mercado['Clubes']]

fig3, ax3 = plt.subplots(figsize=(12, 8))
sns.barplot(data=valor_mercado, x='Valor_total_formatted', y='Clubes', palette=palette_valor, ax=ax3)
ax3.set_title('Valor de Mercado por Clube')
ax3.set_xlabel('Valor Total (em €)')
ax3.set_ylabel('Clube')
# Formata o eixo x para exibir em milhões
ax3.xaxis.set_major_formatter(lambda x, pos: f'€{x/1_000_000:.0f}M')
plt.tight_layout()
st.pyplot(fig3)

# --- NOVA SEÇÃO DE GRÁFICOS (MODIFICADA) ---
st.header('Outras Análises Estatísticas dos Elencos')

col3, col4 = st.columns(2)

with col3:
    st.subheader('Idade Média do Elenco por Clube')
    
    # Ordena os dados para melhor visualização no gráfico
    dados_idade_ordenados = df_clubes.sort_values('Idade_Media', ascending=False)
    
    # Lógica de cores para destacar o clube selecionado
    if clube_selecionado == 'Todos':
        # Paleta de cores padrão quando nenhum clube está selecionado
        palette_idade = sns.color_palette("coolwarm_r", n_colors=len(dados_idade_ordenados))
    else:
        # Destaca o clube selecionado e deixa os outros cinzas
        palette_idade = ['#c51b7d' if clube == clube_selecionado else '#d3d3d3' for clube in dados_idade_ordenados['Clubes']]

    fig4, ax4 = plt.subplots(figsize=(10, 8))
    
    # Cria o gráfico de barras horizontal
    barplot_idade = sns.barplot(data=dados_idade_ordenados, x='Idade_Media', y='Clubes', palette=palette_idade, ax=ax4)
    
    # Adiciona os valores de idade diretamente nas barras
    ax4.bar_label(barplot_idade.containers[0], fmt='%.1f anos', padding=3, fontsize=10)
    
    ax4.set_title('Idade Média dos Jogadores por Clube em 2014')
    ax4.set_xlabel('Idade Média (anos)')
    ax4.set_ylabel('Clube')
    ax4.set_xlim(right=ax4.get_xlim()[1] * 1.1) # Aumenta o espaço para os rótulos
    
    plt.tight_layout()
    st.pyplot(fig4)

with col4:
    st.subheader('Valor Médio de Mercado por Jogador')
    
    # Ordena os dados para o gráfico de valor de mercado
    dados_media_valor = df_clubes.sort_values('Media_Valor_formatted', ascending=False)

    # Lógica de cores dinâmicas
    if clube_selecionado == 'Todos':
        palette_media_valor = sns.color_palette('summer', n_colors=len(dados_media_valor))
    else:
        palette_media_valor = ['#2ca02c' if clube == clube_selecionado else '#d3d3d3' for clube in dados_media_valor['Clubes']]

    fig5, ax5 = plt.subplots(figsize=(10, 8))
    barplot_media = sns.barplot(data=dados_media_valor, x='Media_Valor_formatted', y='Clubes', palette=palette_media_valor, ax=ax5)
    
    # Loop para adicionar os rótulos manualmente em cada barra
    for bar in barplot_media.patches:
        # Pega a largura da barra (o valor no eixo x)
        width = bar.get_width()
        # Formata o texto
        label_text = f'€{width/1_000_000:.2f}M'
        # Define a posição y do texto (no meio da barra)
        y_pos = bar.get_y() + bar.get_height() / 2
        # Adiciona o texto ao gráfico
        ax5.text(width + 0.3, y_pos, label_text, va='center') # Adicionado um pequeno deslocamento horizontal

    ax5.set_title('Valor Médio de Mercado por Jogador em 2014')
    ax5.set_xlabel('Valor Médio por Jogador (em €)')
    ax5.set_ylabel('Clube')
    
    # Formata o eixo X para milhões
    ax5.xaxis.set_major_formatter(lambda x, pos: f'€{x/1_000_000:.1f}M')
    ax5.set_xlim(right=ax5.get_xlim()[1] * 1.2) # Aumenta o espaço para os rótulos
    
    plt.tight_layout()
    st.pyplot(fig5)

st.info(
    "**Nota sobre as visualizações:** "
    "O gráfico de barras de idade média permite uma comparação direta entre os clubes. "
    "O gráfico de valor médio por jogador ajuda a analisar a 'qualidade' média do elenco, complementando a visão do valor total."
)
