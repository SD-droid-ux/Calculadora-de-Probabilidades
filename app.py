import streamlit as st
from collections import Counter
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análises Numéricas", layout="wide")
st.title("📊 Ferramentas de Análise Numérica")

abas = st.tabs([
    "1️⃣ Soma Condicional", 
    "2️⃣ Contagem de Frequência", 
    "3️⃣ Frequência (%)", 
    "4️⃣ Gráfico de Linhas", 
    "5️⃣ Gráfico de Barras",  
    "🖊️ Gráfico Interativo"
])
  
   
])

# Variáveis compartilhadas
if "resultados" not in st.session_state:
    st.session_state.resultados = []

# Função para processar a soma condicional
def calcular_soma_condicional(numeros):
    resultados = []
    soma = 0
    anterior = None
    for n in numeros:
        if anterior is None or (n > 0 and anterior <= 0) or (n < 0 and anterior >= 0) or n != anterior:
            soma = n
        else:
            soma += n
        resultados.append(soma)
        anterior = n
    return resultados

# --- Aba 1: Soma Condicional ---
with abas[0]:
    st.subheader("🔢 Soma Condicional com Regra de Sinais")
    entrada = st.text_area("Cole sua lista de números separados por vírgulas (ex: 1, -1, 1, 2, -2)", "")
    
    if st.button("Calcular Soma Condicional"):
        try:
            numeros = [float(x.strip()) for x in entrada.split(",") if x.strip()]
            resultados = calcular_soma_condicional(numeros)
            st.session_state.resultados = resultados  # Armazena para uso posterior

            st.write("📋 **Resultado da Coluna Acumulada:**")
            st.code("\n".join([str(r) for r in resultados]))
        except Exception:
            st.error("Erro ao processar a lista. Verifique se os números estão separados por vírgulas.")

# --- Aba 2: Contagem de Frequência ---
with abas[1]:
    st.subheader("📊 Contagem de Frequência dos Resultados")
    if st.session_state.resultados:
        contagem = Counter(st.session_state.resultados)
        for valor in sorted(contagem.keys(), reverse=True):
            st.write(f"{valor:.3f} = {contagem[valor]}")
    else:
        st.info("ℹ️ Calcule a soma condicional primeiro (aba 1).")

# --- Aba 3: Frequência em Porcentagem ---
with abas[2]:
    st.subheader("📈 Frequência em Porcentagem")
    if st.session_state.resultados:
        contagem = Counter(st.session_state.resultados)
        total = sum(contagem.values())
        for valor in sorted(contagem.keys()):
            porcentagem = (contagem[valor] / total) * 100
            st.write(f"{valor:.3f} = {porcentagem:.2f}%")
        # Armazena para os gráficos
        st.session_state.valores = list(sorted(contagem.keys()))
        st.session_state.porcentagens = [(contagem[v] / total) * 100 for v in st.session_state.valores]
    else:
        st.info("ℹ️ Calcule a soma condicional primeiro (aba 1).")

# --- Aba 4: Gráfico de Linhas ---
with abas[3]:
    st.subheader("📉 Gráfico de Distribuição (Linhas)")
    if "valores" in st.session_state and "porcentagens" in st.session_state:
        plt.figure(figsize=(10, 4))
        plt.plot(st.session_state.valores, st.session_state.porcentagens, marker='o', linestyle='-', color='blue')
        plt.title("Distribuição de Probabilidade (%)")
        plt.xlabel("Valor")
        plt.ylabel("Probabilidade (%)")
        plt.grid(True, linestyle="--", alpha=0.6)
        st.pyplot(plt)
    else:
        st.info("ℹ️ Gere a frequência em porcentagem primeiro (aba 3).")

# --- Aba 5: Gráfico de Barras ---
with abas[4]:
    st.subheader("📊 Gráfico de Distribuição (Barras)")
    if "valores" in st.session_state and "porcentagens" in st.session_state:
        plt.figure(figsize=(10, 4))
        plt.bar(st.session_state.valores, st.session_state.porcentagens, color='green', alpha=0.7)
        plt.title("Distribuição de Probabilidades (%)")
        plt.xlabel("Valor")
        plt.ylabel("Probabilidade (%)")
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        st.pyplot(plt)
    else:
        st.info("ℹ️ Gere a frequência em porcentagem primeiro (aba 3).")

import plotly.graph_objects as go

# --- Aba 6: Gráfico Interativo com Ferramentas de Desenho ---
with abas[5]:
    st.subheader("🖊️ Gráfico Interativo (Desenho e Pan)")

    if st.session_state.resultados:
        valores = st.session_state.resultados
        x = list(range(len(valores)))

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=x,
            y=valores,
            mode='lines+markers',
            name='Resultados',
            line=dict(color='blue'),
            marker=dict(size=6)
        ))

        fig.update_layout(
            title='Gráfico com Ferramentas de Desenho e Navegação',
            xaxis_title='Índice',
            yaxis_title='Valor',
            hovermode='x unified',
            template='plotly_white',
            dragmode='pan',
            newshape_line_color='red',
            modebar_add=[
                'drawline',
                'drawopenpath',
                'drawrect',
                'drawcircle',
                'eraseshape',
                'pan'
            ]
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ Calcule os resultados na aba 1 (Soma Condicional) para exibir o gráfico.")


