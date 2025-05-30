import streamlit as st
from collections import Counter
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análises Numéricas", layout="wide")
st.title("📊 Ferramentas de Análise Numérica")

# Abas superiores (corrigido com a vírgula entre as últimas duas abas)
abas = st.tabs([
    "1️⃣ Soma Condicional", 
    "2️⃣ Contagem de Frequência", 
    "3️⃣ Frequência (%)", 
    "4️⃣ Gráfico de Linhas", 
    "5️⃣ Gráfico de Barras",  # vírgula corrigida aqui ✅
    "🧮 Calculadora Simples"
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

# --- Aba 6: Calculadora Simples (Independente) ---
with abas[5]:
    st.subheader("📘 Calculadora de Média Aritmética (9 Períodos)")

    col1, col2, col3 = st.columns(3)

    with col1:
        p1 = st.number_input("Período 1", value=0.0)
        p4 = st.number_input("Período 4", value=0.0)
        p7 = st.number_input("Período 7", value=0.0)

    with col2:
        p2 = st.number_input("Período 2", value=0.0)
        p5 = st.number_input("Período 5", value=0.0)
        p8 = st.number_input("Período 8", value=0.0)

    with col3:
        p3 = st.number_input("Período 3", value=0.0)
        p6 = st.number_input("Período 6", value=0.0)
        p9 = st.number_input("Período 9", value=0.0)

    if st.button("Calcular Média"):
        valores = [p1, p2, p3, p4, p5, p6, p7, p8, p9]
        media = sum(valores) / 9
        st.success(f"Média Aritmética dos 9 períodos: {media:.2f}")


