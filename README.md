# ⚽ Análise de Clubes do Brasileirão 2014  

Este projeto é uma aplicação interativa desenvolvida em **Python** utilizando **Streamlit**, que realiza uma análise visual e estatística dos clubes participantes do **Campeonato Brasileiro de Futebol de 2014**.  

A aplicação exibe tabelas, métricas e gráficos comparativos para auxiliar na compreensão do desempenho esportivo e do valor de mercado dos clubes.  

---

## 🚀 Funcionalidades  

- Exibição da **tabela de classificação final** com vitórias, derrotas, empates, saldo e gols.  
- **Filtros interativos** para selecionar um clube específico ou visualizar todos.  
- **Métricas principais por clube**: vitórias, saldo de gols, gols marcados e valor do elenco.  
- **Gráficos comparativos**:  
  - Ranking de vitórias por clube.  
  - Desempenho ofensivo x defensivo (gols marcados vs. gols sofridos).  
  - Valor de mercado total dos clubes.  
  - Idade média do elenco por clube.  
  - Valor médio de mercado por jogador.  

---

## 📊 Visualizações  

- **Barras** → ranking de vitórias, valor de mercado e idade média do elenco.  
- **Dispersão** → desempenho ofensivo x defensivo.  
- **Métricas destacadas** → comparações individuais por clube.  

---

## 🛠️ Tecnologias Utilizadas  

- [Python 3.x](https://www.python.org/)  
- [Streamlit](https://streamlit.io/)  
- [Pandas](https://pandas.pydata.org/)  
- [Matplotlib](https://matplotlib.org/)  
- [Seaborn](https://seaborn.pydata.org/)  

---

## 📂 Estrutura do Projeto  

```text
├── CienciadeDados/
│   └── Tabela_Clubes_2014.csv  # Dataset com informações dos clubes
├── app.py                      # Código principal da aplicação Streamlit
├── requirements.txt            # Dependências do projeto
└── README.md                   # Documentação do projeto
```

---

## ⚙️ Instalação e Execução  

1. Clone este repositório:  

git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt

streamlit run app.py

http://localhost:8501

## 📑 Dataset

O dataset Tabela_Clubes_2014.csv contém:

Posição final dos clubes

Clubes participantes

Vitórias, Derrotas, Empates

Gols marcados e sofridos

Saldo de gols

Idade média dos jogadores

Valor de mercado total e valor médio por jogador
