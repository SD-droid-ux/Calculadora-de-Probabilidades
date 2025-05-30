import streamlit as st
from collections import Counter
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análises Numéricas", layout="wide")
st.title("📊 Ferramentas de Análise Numérica")

# Abas superiores
abas = st.tabs([
    "1️⃣ Soma Condicional", 
    "2️⃣ Contagem de Frequência", 
    "3️⃣ Frequência (%)", 
    "4️⃣ Gráfico de Linhas", 
    "5️⃣ Gráfico de Barras",  
    "🧮 Calculadora Média Fechamentos Acima da Média (9)",
    "🧮 Calculadora Média Fechamentos Abaixo da Média (9)"
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
    st.subheader("📘 Média Móvel de 9 Períodos")

    entrada_texto = st.text_area("Cole sua lista de números (separados por vírgula ou quebra de linha):", "")

    if st.button("Calcular Médias"):
        try:
            # Normaliza entrada e converte para float
            numeros = [float(x.strip()) for x in entrada_texto.replace("\n", ",").split(",") if x.strip()]

            if len(numeros) < 9:
                st.warning("Você precisa inserir ao menos 9 números para calcular médias móveis.")
            else:
                # Calcula médias móveis de 9 períodos
                medias = [sum(numeros[i:i+9]) / 9 for i in range(len(numeros) - 8)]

                st.write("📋 **Médias Móveis (9 períodos):**")
                st.code("\n".join([f"{media:.3f}" for media in medias]))

                # Gráfico
                plt.figure(figsize=(10, 4))
                plt.plot(medias, marker='o', linestyle='-', color='purple')
                plt.title("Evolução das Médias Móveis (9 Períodos)")
                plt.xlabel("Período")
                plt.ylabel("Média")
                plt.grid(True, linestyle="--", alpha=0.6)
                st.pyplot(plt)

        except Exception as e:
            st.error("Erro ao processar os dados. Verifique se os números estão corretos e separados por vírgula ou nova linha.")

# --- Aba 7: Calculadora Simples (Independente) ---
with abas[6]:
    st.subheader("📘 Média Móvel de 9 Períodos")

    entrada_texto = st.text_area("Cole sua lista de números (separados por vírgula ou quebra de linha):", "")

    if st.button("Calcular Médias"):
        try:
            # Normaliza entrada e converte para float
            numeros = [float(x.strip()) for x in entrada_texto.replace("\n", ",").split(",") if x.strip()]

            if len(numeros) < 9:
                st.warning("Você precisa inserir ao menos 9 números para calcular médias móveis.")
            else:
                # Calcula médias móveis de 9 períodos
                medias = [sum(numeros[i:i+9]) / 9 for i in range(len(numeros) - 8)]

                st.write("📋 **Médias Móveis (9 períodos):**")
                st.code("\n".join([f"{media:.3f}" for media in medias]))

                # Gráfico
                plt.figure(figsize=(10, 4))
                plt.plot(medias, marker='o', linestyle='-', color='purple')
                plt.title("Evolução das Médias Móveis (9 Períodos)")
                plt.xlabel("Período")
                plt.ylabel("Média")
                plt.grid(True, linestyle="--", alpha=0.6)
                st.pyplot(plt)

        except Exception as e:
            st.error("Erro ao processar os dados. Verifique se os números estão corretos e separados por vírgula ou nova linha.")
