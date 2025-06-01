import streamlit as st
from collections import Counter
import plotly.graph_objects as go

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

if "resultados" not in st.session_state:
    st.session_state.resultados = []

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

# Aba 1
with abas[0]:
    st.subheader("🔢 Soma Condicional com Regra de Sinais")
    entrada = st.text_area("Cole sua lista de números separados por vírgulas (ex: 1, -1, 1, 2, -2)", "")

    if st.button("Calcular Soma Condicional"):
        try:
            numeros = [float(x.strip()) for x in entrada.split(",") if x.strip()]
            resultados = calcular_soma_condicional(numeros)
            st.session_state.resultados = resultados

            st.write("📋 **Resultado da Coluna Acumulada:**")
            st.code("\n".join([str(r) for r in resultados]))
        except Exception:
            st.error("Erro ao processar a lista. Verifique se os números estão separados por vírgulas.")

# Aba 2
with abas[1]:
    st.subheader("📊 Contagem de Frequência dos Resultados")
    if st.session_state.resultados:
        contagem = Counter(st.session_state.resultados)
        for valor in sorted(contagem.keys(), reverse=True):
            st.write(f"{valor:.3f} = {contagem[valor]}")
    else:
        st.info("ℹ️ Calcule a soma condicional primeiro (aba 1).")

# Aba 3
with abas[2]:
    st.subheader("📈 Frequência em Porcentagem")
    if st.session_state.resultados:
        contagem = Counter(st.session_state.resultados)
        total = sum(contagem.values())
        valores = sorted(contagem.keys())
        porcentagens = [(contagem[v] / total) * 100 for v in valores]

        for v, p in zip(valores, porcentagens):
            st.write(f"{v:.3f} = {p:.2f}%")

        st.session_state.valores = valores
        st.session_state.porcentagens = porcentagens
    else:
        st.info("ℹ️ Calcule a soma condicional primeiro (aba 1).")

# Aba 4
with abas[3]:
    st.subheader("📉 Gráfico de Distribuição (Linhas)")
    if "valores" in st.session_state and "porcentagens" in st.session_state:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=st.session_state.valores, y=st.session_state.porcentagens,
                                 mode='lines+markers', name='Distribuição', line=dict(color='blue')))
        fig.update_layout(title="Distribuição de Probabilidade (%)",
                          xaxis_title="Valor", yaxis_title="Probabilidade (%)",
                          template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ Gere a frequência em porcentagem primeiro (aba 3).")

# Aba 5
with abas[4]:
    st.subheader("📊 Gráfico de Distribuição (Barras)")
    if "valores" in st.session_state and "porcentagens" in st.session_state:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=st.session_state.valores, y=st.session_state.porcentagens,
                             name='Distribuição', marker_color='green'))
        fig.update_layout(title="Distribuição de Probabilidades (%)",
                          xaxis_title="Valor", yaxis_title="Probabilidade (%)",
                          template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ Gere a frequência em porcentagem primeiro (aba 3).")

# Aba 6
with abas[5]:
    st.subheader("🖊️ Gráfico Interativo (Desenho e Pan)")
    if st.session_state.resultados:
        valores = st.session_state.resultados
        x = list(range(len(valores)))

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x, y=valores,
            mode='lines+markers', name='Resultados',
            line=dict(color='blue'), marker=dict(size=6)
        ))

        fig.update_layout(
            title='Gráfico com Ferramentas de Desenho e Navegação',
            xaxis_title='Índice', yaxis_title='Valor',
            hovermode='x unified', template='plotly_white',
            dragmode='pan', newshape_line_color='red',
            modebar_add=[
                'drawline', 'drawopenpath', 'drawrect',
                'drawcircle', 'eraseshape', 'pan'
            ]
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ Calcule os resultados na aba 1 (Soma Condicional) para exibir o gráfico.")
