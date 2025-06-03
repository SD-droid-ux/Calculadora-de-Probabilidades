import streamlit as st
import pandas as pd
from collections import Counter, defaultdict
import plotly.graph_objects as go

st.set_page_config(page_title="Análises Numéricas", layout="wide")
st.title("📊 Ferramentas de Análise Numérica")

abas = st.tabs([
    "1️⃣ Upload e Soma Condicional", 
    "2️⃣ Contagem de Frequência", 
    "3️⃣ Frequência (%)", 
    "4️⃣ Gráfico de Linhas", 
    "5️⃣ Gráfico de Barras",  
    "6️⃣ Gráfico Interativo",
    "7️⃣ Transições de Sinais"
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

# --- Aba 1: Upload e Soma Condicional ---
with abas[0]:
    st.subheader("📁 Upload de Arquivo com Números")

    arquivo = st.file_uploader("Envie um arquivo .txt ou .xlsx com uma lista de números", type=["txt", "xlsx"])

    if arquivo is not None:
        try:
            if arquivo.name.endswith(".txt"):
                conteudo = arquivo.read().decode("utf-8").splitlines()
                numeros = [float(linha.strip().replace(",", "")) for linha in conteudo if linha.strip()]
            elif arquivo.name.endswith(".xlsx"):
                df = pd.read_excel(arquivo)
                primeira_coluna = df.columns[0]
                numeros = [float(x) for x in df[primeira_coluna] if pd.notnull(x)]

            resultados = calcular_soma_condicional(numeros)
            st.session_state.resultados = resultados

            st.write("📋 **Resultado da Coluna Acumulada:**")
            st.code("\n".join([str(r) for r in resultados]))

        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {str(e)}")
    else:
        st.info("ℹ️ Envie um arquivo .txt ou .xlsx para processar a soma condicional.")

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
        st.session_state.valores = list(sorted(contagem.keys()))
        st.session_state.porcentagens = [(contagem[v] / total) * 100 for v in st.session_state.valores]
    else:
        st.info("ℹ️ Calcule a soma condicional primeiro (aba 1).")

# --- Aba 4: Gráfico de Linhas ---
with abas[3]:
    st.subheader("📉 Gráfico de Distribuição (Linhas)")
    if "valores" in st.session_state and "porcentagens" in st.session_state:
        fig = go.Figure(data=go.Scatter(
            x=st.session_state.valores,
            y=st.session_state.porcentagens,
            mode='lines+markers',
            line=dict(color='blue')
        ))
        fig.update_layout(title='Distribuição de Probabilidade (%)',
                          xaxis_title='Valor',
                          yaxis_title='Probabilidade (%)',
                          template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ Gere a frequência em porcentagem primeiro (aba 3).")

# --- Aba 5: Gráfico de Barras ---
with abas[4]:
    st.subheader("📊 Gráfico de Distribuição (Barras)")
    if "valores" in st.session_state and "porcentagens" in st.session_state:
        fig = go.Figure(data=go.Bar(
            x=st.session_state.valores,
            y=st.session_state.porcentagens,
            marker_color='green'
        ))
        fig.update_layout(title='Distribuição de Probabilidades (%)',
                          xaxis_title='Valor',
                          yaxis_title='Probabilidade (%)',
                          template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ Gere a frequência em porcentagem primeiro (aba 3).")

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

# --- Aba 7: Transições de Sinais ---
def transformar_em_sinais(dados):
    return [1 if x > 0 else -1 if x < 0 else 0 for x in dados]

def calcular_probabilidades_transicoes(sinais, max_seq=10):
    transicoes = defaultdict(lambda: {"+1": 0, "-1": 0})
    n = len(sinais)

    for seq_len in range(1, max_seq + 1):
        for i in range(n - seq_len):
            sequencia = tuple(sinais[i:i + seq_len])
            proximo = sinais[i + seq_len]
            if proximo == 0:
                continue
            chave = str(sequencia)
            if proximo == 1:
                transicoes[chave]["+1"] += 1
            elif proximo == -1:
                transicoes[chave]["-1"] += 1

    resultados = []
    for seq, valores in transicoes.items():
        total = valores["+1"] + valores["-1"]
        prob_mais1 = valores["+1"] / total if total > 0 else 0
        prob_menos1 = valores["-1"] / total if total > 0 else 0
        resultados.append({
            "Sequência": seq,
            "Transições para +1": valores["+1"],
            "Transições para -1": valores["-1"],
            "Total de Transições": total,
            "Probabilidade +1 (%)": round(prob_mais1 * 100, 2),
            "Probabilidade -1 (%)": round(prob_menos1 * 100, 2),
        })

    return pd.DataFrame(resultados).sort_values(by="Total de Transições", ascending=False)

with abas[6]:
    st.subheader("🔄 Análise de Transições de Sinais")

    arquivo_trans = st.file_uploader("Envie um arquivo .txt ou .xlsx com dados para análise de transições", type=["txt", "xlsx"], key="transicoes")

    if arquivo_trans is not None:
        try:
            if arquivo_trans.name.endswith(".txt"):
                conteudo = arquivo_trans.read().decode("utf-8").splitlines()
                dados = [float(l.strip().replace(",", "."))
                         for l in conteudo if l.strip()]
            elif arquivo_trans.name.endswith(".xlsx"):
                df = pd.read_excel(arquivo_trans)
                primeira_coluna = df.columns[0]
                dados = [float(x) for x in df[primeira_coluna] if pd.notnull(x)]

            sinais = transformar_em_sinais(dados)
            df_resultados = calcular_probabilidades_transicoes(sinais, max_seq=10)

            st.dataframe(df_resultados.head(50), use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {str(e)}")
    else:
        st.info("ℹ️ Envie um arquivo .txt ou .xlsx para analisar as transições.")

