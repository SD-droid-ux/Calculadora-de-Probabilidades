import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter

st.set_page_config(page_title="Analisador de Dados", layout="wide")
st.title("🔍 Analisador de Lista Numérica")

# Entrada dos dados
entrada = st.text_area("Digite a lista de números separados por vírgula:", "1, -1, 2, 2, -2, -2, -2, 3")

# Função para processar a entrada
def processar_lista(entrada):
    try:
        numeros = [float(n.strip()) for n in entrada.split(",") if n.strip() != ""]
        return numeros
    except:
        st.error("Erro ao processar os números. Certifique-se de usar o formato correto: 1, 2, -3, 4")
        return []

numeros = processar_lista(entrada)

if numeros:
    aba = st.selectbox("Escolha a operação:", [
        "1 - Coluna Acumulada",
        "2 - Frequência dos Valores",
        "3 - Distribuição em Porcentagem",
        "4 - Gráfico de Linha",
        "5 - Gráfico de Barras"
    ])

    # Aba 1 - Coluna Acumulada
    if aba.startswith("1"):
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

        st.subheader("📋 Resultado da Coluna Acumulada:")
        st.write(resultados)

    # Aba 2 - Frequência dos Valores
    elif aba.startswith("2"):
        contagem = Counter(numeros)
        st.subheader("📊 Frequência dos Valores:")
        for valor in sorted(contagem.keys(), reverse=True):
            st.write(f"{valor:.3f} = {contagem[valor]}")

    # Aba 3 - Distribuição em Porcentagem
    elif aba.startswith("3"):
        contagem = Counter(numeros)
        total = sum(contagem.values())
        st.subheader("📈 Distribuição em Porcentagem:")
        for valor in sorted(contagem.keys()):
            porcentagem = (contagem[valor] / total) * 100
            st.write(f"{valor:.3f} = {porcentagem:.2f}%")

    # Aba 4 - Gráfico de Linha
    elif aba.startswith("4"):
        contagem = Counter(numeros)
        total = sum(contagem.values())
        valores = sorted(contagem.keys())
        porcentagens = [(contagem[v] / total) * 100 for v in valores]

        st.subheader("📉 Gráfico de Linha - Distribuição de Probabilidade")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(valores, porcentagens, marker='o', linestyle='-', color='blue')
        ax.set_title('Distribuição de Probabilidade (%)')
        ax.set_xlabel('Valor')
        ax.set_ylabel('Probabilidade (%)')
        ax.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig)

    # Aba 5 - Gráfico de Barras
    elif aba.startswith("5"):
        contagem = Counter(numeros)
        total = sum(contagem.values())
        valores = sorted(contagem.keys())
        porcentagens = [(contagem[v] / total) * 100 for v in valores]

        st.subheader("📊 Gráfico de Barras - Distribuição de Probabilidade")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar([str(v) for v in valores], porcentagens, color='skyblue')
        ax.set_title('Distribuição de Probabilidade (%)')
        ax.set_xlabel('Valor')
        ax.set_ylabel('Probabilidade (%)')
        ax.grid(axis='y', linestyle='--', alpha=0.6)
        st.pyplot(fig)